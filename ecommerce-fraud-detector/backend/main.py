from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. GENERATE SYNTHETIC TRAINING DATA & TRAIN MODELS ---
np.random.seed(42)

# Normal user behavior
n_normal = 300
normal_data = {
    "order_amount": np.random.normal(50, 20, n_normal).clip(5, 300),
    "session_duration_sec": np.random.normal(180, 60, n_normal).clip(10, 600),
    "click_count": np.random.normal(25, 8, n_normal).clip(2, 80),
    "is_fraud": [0] * n_normal
}

# Bot/Fraud behavior (high amount or ultra-fast sessions with low clicks)
n_fraud = 30
fraud_data = {
    "order_amount": np.random.normal(800, 200, n_fraud).clip(300, 2000),
    "session_duration_sec": np.random.normal(2, 1, n_fraud).clip(0.1, 5),
    "click_count": np.random.normal(2, 1, n_fraud).clip(1, 5),
    "is_fraud": [1] * n_fraud
}

df_normal = pd.DataFrame(normal_data)
df_fraud = pd.DataFrame(fraud_data)
df = pd.concat([df_normal, df_fraud], ignore_index=True)

X = df[["order_amount", "session_duration_sec", "click_count"]]
y = df["is_fraud"]

# Scale features for DBSCAN
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit DBSCAN (eps and min_samples tuned for anomaly separation)
dbscan = DBSCAN(eps=0.8, min_samples=5)
dbscan.fit(X_scaled)

# Fit Random Forest Classifier for probability score
rf_model = RandomForestClassifier(n_estimators=50, random_state=42)
rf_model.fit(X, y)


# --- 2. SCHEMAS & API ENDPOINTS ---
class Transaction(BaseModel):
    order_amount: float
    session_duration_sec: float
    click_count: float

@app.get("/")
def read_root():
    return {"message": "E-Commerce Fraud Detection API is running!"}

@app.post("/predict")
def predict_fraud(txn: Transaction):
    input_data = np.array([[
        txn.order_amount, 
        txn.session_duration_sec, 
        txn.click_count
    ]])
    
    # Scale input for DBSCAN
    input_scaled = scaler.transform(input_data)
    
    # DBSCAN Outlier Check
    combined = np.vstack([X_scaled, input_scaled])
    clusters = dbscan.fit_predict(combined)
    is_anomaly = bool(clusters[-1] == -1)

    # Random Forest Probability
    fraud_prob = float(rf_model.predict_proba(input_data)[0][1])

    # --- ENSEMBLE DECISION LOGIC ---
    if fraud_prob > 0.6:
        # High probability of actual fraud -> Hard Flag
        status = "FLAGGED (High Fraud/Bot Risk)"
    elif is_anomaly or fraud_prob > 0.3:
        # Unusual behavior OR moderate fraud probability -> Manual Review
        status = "NEEDS REVIEW"
    else:
        # Normal behavior -> Approved
        status = "APPROVED"

    return {
        "status": status,
        "is_anomaly": is_anomaly,
        "fraud_probability": round(fraud_prob * 100, 2),
        "details": {
            "order_amount": txn.order_amount,
            "session_duration_sec": txn.session_duration_sec,
            "click_count": txn.click_count
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
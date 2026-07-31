import joblib
import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
import config

def generate_mock_data():
    np.random.seed(42)
    n_samples = 1000
    
    neighborhoods = ["Downtown", "Suburbs", "Uptown", "Financial District", "Old Town"]
    
    sq_ft = np.random.randint(500, 3500, n_samples)
    beds = np.random.randint(1, 5, n_samples)
    baths = np.random.randint(1, 4, n_samples)
    loc = np.random.choice(neighborhoods, n_samples)
    
    # Base price calculation with noise
    price = (sq_ft * 150) + (beds * 10000) + (baths * 15000) + np.random.normal(0, 10000, n_samples)
    
    # Neighborhood premiums
    loc_premiums = {"Downtown": 50000, "Suburbs": -20000, "Uptown": 30000, "Financial District": 70000, "Old Town": 10000}
    for i, l in enumerate(loc):
        price[i] += loc_premiums[l]
        
    df = pd.DataFrame({
        "square_footage": sq_ft,
        "bedrooms": beds,
        "bathrooms": baths,
        "neighborhood": loc,
        "price": price
    })
    return df, neighborhoods

def train_and_save_model():
    df, neighborhoods = generate_mock_data()
    
    X = df[config.NUMERIC_FEATURES + config.CATEGORICAL_FEATURES]
    y = df[config.TARGET_COLUMN]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), config.CATEGORICAL_FEATURES)
        ],
        remainder='passthrough'
    )
    
    # Regression Pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    
    import joblib
    joblib.dump(pipeline, config.MODEL_PATH)
    
    metadata = {"neighborhoods": sorted(neighborhoods)}
    with open(config.METADATA_PATH, "w") as f:
        json.dump(metadata, f)
        
    print("Model and metadata successfully saved!")

def predict_price(input_data: dict):
    import joblib
    if not os.path.exists(config.MODEL_PATH):
        raise FileNotFoundError("Model weights missing. Run training script first.")
        
    pipeline = joblib.load(config.MODEL_PATH)
    df_input = pd.DataFrame([input_data])
    prediction = pipeline.predict(df_input)[0]
    return max(0.0, prediction) # Ensure no negative outputs

if __name__ == "__main__":
    train_and_save_model()
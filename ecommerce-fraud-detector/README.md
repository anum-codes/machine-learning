# 🛡️ E-Commerce Fraud & Bot Detector

A real-time machine learning engine designed to detect fraudulent order checkouts and automated bot activity. The application combines **supervised** and **unsupervised** ML models to analyze behavioral patterns and output actionable risk scores through an interactive React dashboard.

---

## 📸 Overview & Demo

The application simulates real-time e-commerce checkouts by scoring transactions across three core metrics:
* **Order Amount ($)**
* **Session Duration (seconds)**
* **Clicks Before Checkout**

It uses a dual-model ensemble strategy to categorize orders into three distinct operational states:
1. ✅ **APPROVED:** Low risk score and standard human shopping behavior.
2. ⚠️ **NEEDS REVIEW:** Anomaly/outlier detected (e.g., hyper-active clicks), requiring manual audit rather than an immediate block.
3. 🚨 **FLAGGED:** High probability of fraud/bot activity (e.g., high-dollar rapid checkouts).

---

## 🛠️ Tech Stack

### **Backend**
* **Python 3.10+**
* **FastAPI** – High-performance asynchronous REST API framework
* **scikit-learn** – Machine learning engine implementing:
  * **Random Forest Classifier** (Supervised Learning for Fraud Risk Probability)
  * **DBSCAN** (Unsupervised Learning for Density-Based Outlier Detection)
* **StandardScaler** – Feature normalization pipeline

### **Frontend**
* **React (Vite)** – Modern UI component engine
* **Chart.js / react-chartjs-2** – Real-time dynamic cluster scatter plotting
* **Tailwind CSS / Custom CSS** – Responsive dark-mode interface design

---

## 🚀 Key Features

* **Hybrid ML Ensemble Logic:** Combines probabilistic classification with density clustering to drastically reduce false positives.
* **Real-Time Visualizations:** Interactive Chart.js scatter plot mapping transaction clusters dynamically on every submit.
* **Live Audit Logging:** Real-time log displaying risk scores, outlier flags, and behavioral breakdowns.
* **Preset Simulations:** Includes one-click test presets (`Preset: Bot Attack`, `Preset: Normal Human`) for rapid demonstration.
* **Export Capability:** Export active audit logs to CSV format for secondary inspection.

---

## ⚙️ Local Setup & Installation

### **Prerequisites**
* Python 3.9+
* Node.js 18+ and `npm`

---

### **1. Backend Setup**

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn scikit-learn numpy pydantic

# Start the FastAPI server
uvicorn main:app --reload --port 8000
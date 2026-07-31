import streamlit as st
import os
import json
import model_service
import config

st.set_page_config(page_title="Real Estate Price Estimator", layout="centered")

st.title("🏡 Real Estate Price Estimator")
st.write("Input the structural attributes below to estimate a fair market property valuation.")

# Making sure model exists
if not os.path.exists(config.MODEL_PATH) or not os.path.exists(config.METADATA_PATH):
    st.info("Initializing baseline machine learning model components...")
    model_service.train_and_save_model()

# Load metadata for categories
with open(config.METADATA_PATH, "r") as f:
    metadata = json.load(f)

# Form Elements
with st.form("valuation_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        square_footage = st.slider("Square Footage (sq ft)", min_value=500, max_value=4000, value=1500, step=50)
        neighborhood = st.selectbox("Neighborhood Location", options=metadata["neighborhoods"])
        
    with col2:
        bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=6, value=3, step=1)
        bathrooms = st.number_input("Number of Bathrooms", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
        
    submit_button = st.form_submit_button("Calculate Estimated Value")

if submit_button:
    user_inputs = {
        "square_footage": square_footage,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "neighborhood": neighborhood
    }
    
    with st.spinner("Calculating fair asset valuation..."):
        estimated_price = model_service.predict_price(user_inputs)
        
    st.success(f"### Estimated Market Price: ${estimated_price:,.2f}")
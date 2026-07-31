import os

# Paths
MODEL_PATH = "real_estate_model.pkl"
METADATA_PATH = "features.json"

# Feature definitions
TARGET_COLUMN = "price"
NUMERIC_FEATURES = ["square_footage", "bedrooms", "bathrooms"]
CATEGORICAL_FEATURES = ["neighborhood"]
"""Application configuration settings."""

import os

# Model Settings
MODEL_NAME = "resnet18"
IMAGE_SIZE = 224
IMAGE_RESIZE = 256

# Confidence threshold for a definitive diagnosis
CONFIDENCE_THRESHOLD = 70.0

# Server Settings
SERVER_NAME = "0.0.0.0"
SERVER_PORT = int(os.getenv("PORT", 7860))
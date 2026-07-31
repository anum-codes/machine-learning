"""Inference service engine utilizing locally saved Hugging Face model weights."""

import torch
from transformers import AutoConfig, AutoModelForImageClassification
from torchvision import transforms
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlantDiagnosticEngine:
    def __init__(self):
        logger.info("Loading local custom trained model weights...")
        try:
            # Read the class mapping file downloaded from Colab
            with open("classes.txt", "r") as f:
                self.categories = [line.strip() for line in f.readlines() if line.strip()]
            
            # Build a local configuration matching the exact HF repository setup
            # config matching the exact layout of the keys found inside plant_model.pth
            config = AutoConfig.from_pretrained(
                "mesabo/agri-plant-disease-resnet50", 
                num_labels=len(self.categories)
            )
            
            #Instantiate an empty model using that config framework
            self.model = AutoModelForImageClassification.from_config(config)
            
            # load plant_model.pth weights
            self.model.load_state_dict(torch.load("plant_model.pth", map_location=torch.device('cpu')))
            self.model.eval()
            
            self._setup_transforms()
            logger.info(f"Custom local model loaded successfully with {len(self.categories)} classes.")
        except Exception as e:
            logger.critical(f"Failed to load custom local model artifacts: {str(e)}")
            raise e

    def _setup_transforms(self):
        """Standardized preprocessing matching the ImageNet backbone expectation."""
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, raw_image_array) -> dict:
        if raw_image_array is None:
            return {"status": "error", "message": "No image input received."}

        try:
            pil_img = Image.fromarray(raw_image_array.astype('uint8'), 'RGB')
            tensor_img = self.transform(pil_img).unsqueeze(0)
            
            with torch.no_grad():
                outputs = self.model(tensor_img)
                logits = outputs.logits
                probabilities = torch.nn.functional.softmax(logits[0], dim=0)
            
            top_prob, top_catid = torch.topk(probabilities, 1)
            confidence = top_prob[0].item() * 100
            predicted_label = self.categories[top_catid[0].item()]
            
            # Formatting class names
            clean_label = predicted_label.replace("_", " ").replace("-", " ").title()
            
            return {
                "status": "success",
                "label": clean_label,
                "confidence": confidence
            }
        except Exception as e:
            logger.error(f"Inference error: {str(e)}")
            return {"status": "error", "message": "Internal processing failure."}
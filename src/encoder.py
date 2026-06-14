import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

class ImageEncoder:
    def __init__(self):
        # Charger ResNet50 pré-entraîné
        self.model = models.resnet50(pretrained=True)
        
        # Supprimer la dernière couche (classification)
        # On veut juste les embeddings, pas les prédictions
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])
        
        self.model.eval()
        
        # Transformations standard ImageNet
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def encode(self, image_path):
        """Retourne un vecteur de 2048 dimensions pour une image"""
        img = Image.open(image_path).convert("RGB")
        tensor = self.transform(img).unsqueeze(0)  # [1, 3, 224, 224]
        
        with torch.no_grad():
            embedding = self.model(tensor)
        
        # Aplatir → vecteur 1D de 2048 valeurs
        return embedding.squeeze().numpy()
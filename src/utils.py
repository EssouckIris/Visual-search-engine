import os
import base64
from PIL import Image

def image_to_base64(image_path):
    """Convertit une image en base64 pour l'envoyer au frontend"""
    # Corriger le chemin pour HuggingFace
    if not os.path.exists(image_path):
        # Essayer chemin relatif
        filename = os.path.basename(image_path)
        alt_path = os.path.join(
            os.path.dirname(__file__), '..', 
            'data', 'raw', 'clothing-dataset', 'images', filename
        )
        if os.path.exists(alt_path):
            image_path = alt_path
        else:
            return None

    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    
    ext = os.path.splitext(image_path)[1].lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp"
    }
    mime = mime_types.get(ext, "image/jpeg")
    
    return f"data:{mime};base64,{encoded}"
    mime = mime_types.get(ext, "image/jpeg")
    
    return f"data:{mime};base64,{encoded}"


def validate_image(file):
    """Vérifie que le fichier uploadé est bien une image valide"""
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    ext = os.path.splitext(file.filename)[1].lower()
    
    if ext not in allowed_extensions:
        return False, "Format non supporté. Utilise JPG, PNG ou WEBP."
    
    return True, "OK"

def resize_image(image_path, max_size=(800, 800)):
    """Redimensionne une image si elle est trop grande"""
    img = Image.open(image_path)
    img.thumbnail(max_size, Image.LANCZOS)
    img.save(image_path)
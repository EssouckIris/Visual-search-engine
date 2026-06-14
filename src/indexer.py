import os
import numpy as np
from tqdm import tqdm
from encoder import ImageEncoder

def index_dataset(images_dir, output_dir):
    """
    Parcourt toutes les images du dataset,
    génère leurs embeddings et les sauvegarde
    """
    encoder = ImageEncoder()
    
    # Récupérer tous les chemins d'images
    image_paths = []
    for root, _, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_paths.append(os.path.join(root, file))
    
    print(f"{len(image_paths)} images trouvées")
    
    embeddings = []
    valid_paths = []
    
    for path in tqdm(image_paths, desc="Encodage en cours"):
        try:
            emb = encoder.encode(path)
            embeddings.append(emb)
            valid_paths.append(path)
        except Exception as e:
            print(f"Erreur sur {path} : {e}")
            continue
    
    # Sauvegarder
    os.makedirs(output_dir, exist_ok=True)
    
    np.save(os.path.join(output_dir, "embeddings.npy"), np.array(embeddings))
    np.save(os.path.join(output_dir, "image_paths.npy"), np.array(valid_paths))
    
    print(f"✅ {len(embeddings)} embeddings sauvegardés dans {output_dir}")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_dataset(
        images_dir=os.path.join(BASE_DIR, "data", "raw", "clothing-dataset", "images"),
        output_dir=os.path.join(BASE_DIR, "data", "embeddings")
    )
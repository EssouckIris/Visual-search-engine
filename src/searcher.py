import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from encoder import ImageEncoder

class ImageSearcher:
    def __init__(self, embeddings_dir):
        """Charge les embeddings sauvegardés"""
        self.embeddings = np.load(
            f"{embeddings_dir}/embeddings.npy"
        )
        
        self.image_paths = np.load(
            f"{embeddings_dir}/image_paths.npy",
            allow_pickle=True
        )
    

        self.image_paths = np.array([
            str(p).replace('\\', '/').split('/')[-1] 
            for p in self.image_paths
        ])
        self.encoder = ImageEncoder()
        print(f"✅ {len(self.embeddings)} embeddings chargés")

    def search(self, query_image_path, top_k=10):
        """
        Prend une image en entrée,
        retourne les top_k images les plus similaires
        """
        # Encoder l'image requête
        query_embedding = self.encoder.encode(query_image_path)
        query_embedding = query_embedding.reshape(1, -1)

        # Calculer la similarité cosinus avec tous les embeddings
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]

        # Trier par similarité décroissante
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "path": self.image_paths[idx],
                "score": float(similarities[idx])
            })

        return results
import os
import sys
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

def fix_path(windows_path):
    """Convertit un chemin Windows en chemin HuggingFace"""
    filename = os.path.basename(str(windows_path))
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'clothing-dataset', 'images')
    return os.path.join(base_dir, filename)
# Ajouter src au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from searcher import ImageSearcher
from utils import validate_image, image_to_base64

app = Flask(__name__)
CORS(app)

# Charger le searcher une seule fois au démarrage
EMBEDDINGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'embeddings')
searcher = ImageSearcher(EMBEDDINGS_DIR)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "API opérationnelle"})


@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return jsonify({"error": "Aucune image reçue"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "Fichier vide"}), 400

    is_valid, message = validate_image(file)
    if not is_valid:
        return jsonify({"error": message}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        top_k = int(request.form.get('top_k', 10))
        results = searcher.search(tmp_path, top_k=top_k)

        response = []
        for r in results:
            fixed_path = fix_path(r["path"])
            response.append({
                "score": round(r["score"], 4),
                "image": image_to_base64(fixed_path),
                "path": fixed_path
            })

        return jsonify({"results": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        os.unlink(tmp_path)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(debug=False, host='0.0.0.0', port=port)
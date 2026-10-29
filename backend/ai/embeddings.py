import requests
from backend.app.config import settings

def embed(text: str):
    response = requests.post(
        f"{settings.OLLAMA_URL}/api/embeddings",
        json={"model": settings.EMBEDDING_MODEL, "prompt": text}
    )
    return response.json()["embedding"]

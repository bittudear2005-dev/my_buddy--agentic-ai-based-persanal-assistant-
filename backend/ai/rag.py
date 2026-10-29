import chromadb
from chromadb.config import Settings
from ai.embeddings import embed
from backend.app.config import settings

client = chromadb.PersistentClient(path=settings.CHROMA_PATH)

collection = client.get_or_create_collection(
    name=settings.CHROMA_COLLECTION,
    metadata={"hnsw:space": "cosine"}
)

def add_document(doc_id: str, text: str, metadata: dict):
    """
    Add text chunks into ChromaDB.
    """
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embed(text)],
        metadatas=[metadata]
    )

def search(query: str):
    """
    Semantic retrieval for RAG answers.
    """
    results = collection.query(
        query_embeddings=[embed(query)],
        n_results=settings.RAG_TOP_K
    )
    return results

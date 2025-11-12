import chromadb
from chromadb.config import Settings
from typing import List, Dict
from .config import CHROMA_PERSIST_DIR

_client = None
_collection = None
_COLLECTION_NAME = "shl_catalog"


def get_client():
    global _client
    if _client is None:
        # Disable telemetry to suppress harmless error messages
        settings = Settings(
            allow_reset=False,
            anonymized_telemetry=False
        )
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR, settings=settings)
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_client()
        # Important: Don't specify embedding_function to avoid default Gemini API calls
        # We handle embeddings manually in our code using local models
        _collection = client.get_or_create_collection(
            _COLLECTION_NAME, 
            metadata={"hnsw:space": "cosine"},
            embedding_function=None  # Explicitly disable to avoid API calls
        )
    return _collection


def add_items(ids: List[str], embeddings: List[List[float]], metadatas: List[Dict], documents: List[str]):
    col = get_collection()
    col.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)


def query(embedding: List[float], top_k: int = 20):
    col = get_collection()
    return col.query(query_embeddings=[embedding], n_results=top_k)

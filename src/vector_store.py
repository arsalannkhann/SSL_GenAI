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
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR, settings=Settings(allow_reset=False))
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(_COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
    return _collection


def add_items(ids: List[str], embeddings: List[List[float]], metadatas: List[Dict], documents: List[str]):
    col = get_collection()
    col.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)


def query(embedding: List[float], top_k: int = 20):
    col = get_collection()
    return col.query(query_embeddings=[embedding], n_results=top_k)

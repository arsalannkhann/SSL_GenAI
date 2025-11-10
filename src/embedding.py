from typing import List
from .gemini_client import get_embeddings, get_embedding, get_query_embedding


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts using Gemini."""
    return get_embeddings(texts)


def embed_text(text: str) -> List[float]:
    """Generate embedding for a single text using Gemini."""
    return get_embedding(text)


def embed_query(text: str) -> List[float]:
    """Generate embedding for a query using Gemini (optimized for retrieval)."""
    return get_query_embedding(text)

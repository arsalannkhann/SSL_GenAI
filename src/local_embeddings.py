"""
Local embedding generation using sentence-transformers.
No API calls, no quota limits - perfect for Vercel deployment.
"""
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

# Using a lightweight, high-quality model
# all-MiniLM-L6-v2: 384 dimensions, fast, good quality
_model = None
MODEL_NAME = "all-MiniLM-L6-v2"


def get_model():
    """Lazy load the model to save memory."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_embedding(text: str) -> List[float]:
    """Generate embedding for a single text using local model."""
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
    return embedding.tolist()


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts using local model."""
    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False, batch_size=32)
    return embeddings.tolist()


def get_query_embedding(text: str) -> List[float]:
    """Generate embedding for a query using local model."""
    return get_embedding(text)

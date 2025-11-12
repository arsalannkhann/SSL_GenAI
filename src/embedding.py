"""
Unified embedding module that supports multiple backends:
- Gemini: Google's text-embedding-004 (768 dimensions, high quality)
- Local: sentence-transformers (384 dimensions, no API calls)
- OpenAI: text-embedding-3-large (3072 dimensions, high quality)

The backend is configured via EMBEDDING_PROVIDER in config.py
"""
from typing import List
from .config import EMBEDDING_PROVIDER


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts using the configured provider.
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List of embedding vectors
    """
    if EMBEDDING_PROVIDER == "gemini":
        from .gemini_client import get_embeddings
        return get_embeddings(texts)
    elif EMBEDDING_PROVIDER == "openai":
        from .openai_client import get_embeddings
        return get_embeddings(texts)
    else:  # default to local
        from .local_embeddings import get_embeddings
        return get_embeddings(texts)


def embed_text(text: str) -> List[float]:
    """
    Generate embedding for a single text using the configured provider.
    
    Args:
        text: Text string to embed
        
    Returns:
        Embedding vector
    """
    if EMBEDDING_PROVIDER == "gemini":
        from .gemini_client import get_embedding
        return get_embedding(text)
    elif EMBEDDING_PROVIDER == "openai":
        from .openai_client import get_embedding
        return get_embedding(text)
    else:  # default to local
        from .local_embeddings import get_embedding
        return get_embedding(text)


def embed_query(text: str) -> List[float]:
    """
    Generate embedding for a query using the configured provider.
    Some providers (like Gemini) optimize embeddings for queries vs documents.
    
    Args:
        text: Query text to embed
        
    Returns:
        Query embedding vector
    """
    if EMBEDDING_PROVIDER == "gemini":
        from .gemini_client import get_query_embedding
        return get_query_embedding(text)
    elif EMBEDDING_PROVIDER == "openai":
        from .openai_client import get_query_embedding
        return get_query_embedding(text)
    else:  # default to local
        from .local_embeddings import get_query_embedding
        return get_query_embedding(text)


def get_embedding_dimensions() -> int:
    """
    Get the dimensionality of embeddings from the configured provider.
    
    Returns:
        Number of dimensions in the embedding vector
    """
    if EMBEDDING_PROVIDER == "gemini":
        return 768  # Gemini text-embedding-004
    elif EMBEDDING_PROVIDER == "openai":
        return 3072  # OpenAI text-embedding-3-large
    else:  # local
        return 384  # sentence-transformers all-MiniLM-L6-v2


def get_provider_info() -> dict:
    """
    Get information about the current embedding provider.
    
    Returns:
        Dictionary with provider details
    """
    return {
        "provider": EMBEDDING_PROVIDER,
        "dimensions": get_embedding_dimensions(),
        "description": {
            "gemini": "Google Gemini text-embedding-004 (768D, API-based)",
            "openai": "OpenAI text-embedding-3-large (3072D, API-based)",
            "local": "SentenceTransformers all-MiniLM-L6-v2 (384D, local)"
        }.get(EMBEDDING_PROVIDER, "Unknown provider")
    }

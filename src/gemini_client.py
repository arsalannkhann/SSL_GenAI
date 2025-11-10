import os
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# Use Gemini embedding model
EMBEDDING_MODEL = "models/embedding-001"

# Use Gemini for LLM tasks
LLM_MODEL = "gemini-pro"


def get_embedding(text: str) -> List[float]:
    """Generate embedding for a single text using Gemini."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document"
    )
    return result['embedding']


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts using Gemini."""
    embeddings = []
    for text in texts:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        embeddings.append(result['embedding'])
    return embeddings


def get_query_embedding(text: str) -> List[float]:
    """Generate embedding for a query using Gemini."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_query"
    )
    return result['embedding']


def generate_text(prompt: str, temperature: float = 0.7) -> str:
    """Generate text using Gemini LLM."""
    model = genai.GenerativeModel(LLM_MODEL)
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature,
        )
    )
    return response.text

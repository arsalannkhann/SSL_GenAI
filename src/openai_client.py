import os
from typing import List

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

_client = OpenAI(api_key=OPENAI_API_KEY)

# Model selections
EMBEDDING_MODEL = "text-embedding-3-large"
CHAT_MODEL = "gpt-4o-mini"


def get_embedding(text: str) -> List[float]:
    """Generate embedding for a single text using OpenAI."""
    response = _client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL,
    )
    return response.data[0].embedding


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts using OpenAI."""
    response = _client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL,
    )
    return [item.embedding for item in response.data]


def get_query_embedding(text: str) -> List[float]:
    """Generate embedding for a query using OpenAI."""
    response = _client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL,
    )
    return response.data[0].embedding


def generate_text(prompt: str, temperature: float = 0.7) -> str:
    """Generate text using OpenAI chat completion."""
    response = _client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured data."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

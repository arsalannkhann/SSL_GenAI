"""
Google Gemini API client for both LLM operations and embeddings.
Provides unified interface for text generation and embedding generation.
Uses REST API for better compatibility and reliability.
"""
import os
import requests
from typing import List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Model selections - using available models
# For REST API, use: gemini-pro, gemini-1.5-pro-latest, gemini-1.5-flash-latest
CHAT_MODEL = "gemini-pro"  # Stable and efficient for chat
EMBEDDING_MODEL = "models/text-embedding-004"  # Latest embedding model

# REST API endpoints
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"


def generate_text(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    system_message: Optional[str] = None,
    use_pro_model: bool = False
) -> str:
    """
    Generate text using Gemini REST API.
    
    Args:
        prompt: The user prompt/question
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate
        system_message: Optional system message to set context
        use_pro_model: Not used in this implementation (same model)
        
    Returns:
        Generated text response
    """
    try:
        # Combine system message with prompt if provided
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        
        # Make REST API call
        url = f"{GEMINI_API_BASE}/models/{CHAT_MODEL}:generateContent?key={GOOGLE_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract text from response
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                parts = candidate["content"]["parts"]
                if len(parts) > 0 and "text" in parts[0]:
                    return parts[0]["text"].strip()
        
        raise RuntimeError("No valid response from Gemini API")
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Gemini API request error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")


def generate_chat_response(
    messages: List[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024,
    use_pro_model: bool = False
) -> str:
    """
    Generate a chat response using Gemini with conversation history.
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate
        use_pro_model: Not used in this implementation
        
    Returns:
        Generated text response
    """
    # Build conversation history into a single prompt
    conversation = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        if role == "system":
            conversation += f"Instructions: {content}\n\n"
        elif role == "user":
            conversation += f"User: {content}\n\n"
        elif role == "assistant" or role == "model":
            conversation += f"Assistant: {content}\n\n"
    
    return generate_text(conversation, temperature, max_tokens)


def extract_structured_data(
    prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 512,
    use_pro_model: bool = False
) -> str:
    """
    Extract structured data using Gemini with lower temperature for consistency.
    
    Args:
        prompt: The extraction prompt
        temperature: Lower temperature for more deterministic output
        max_tokens: Maximum tokens to generate
        use_pro_model: Not used in this implementation
        
    Returns:
        Extracted structured data as text
    """
    return generate_text(
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        system_message="You are a precise data extraction assistant. Extract only the requested information in the specified format.",
        use_pro_model=use_pro_model
    )


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text using Gemini.
    
    Args:
        text: The text to embed
        
    Returns:
        List of float values representing the embedding vector
    """
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        raise RuntimeError(f"Gemini embedding error: {str(e)}")


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts using Gemini.
    Uses batch processing for efficiency.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    try:
        embeddings = []
        # Process in batches of 100 (Gemini API limit)
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            # Embed each text in the batch
            batch_embeddings = []
            for text in batch:
                result = genai.embed_content(
                    model=EMBEDDING_MODEL,
                    content=text,
                    task_type="retrieval_document"
                )
                batch_embeddings.append(result['embedding'])
            
            embeddings.extend(batch_embeddings)
        
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Gemini embeddings error: {str(e)}")


def get_query_embedding(text: str) -> List[float]:
    """
    Generate embedding for a query using Gemini.
    Uses the retrieval_query task type for better query understanding.
    
    Args:
        text: The query text to embed
        
    Returns:
        List of float values representing the embedding vector
    """
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']
    except Exception as e:
        raise RuntimeError(f"Gemini query embedding error: {str(e)}")


def get_dimensions() -> int:
    """
    Get the dimensionality of Gemini embeddings.
    text-embedding-004 produces 768-dimensional embeddings.
    
    Returns:
        Embedding dimension size
    """
    return 768

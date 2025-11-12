"""Groq API client for LLM operations."""
import os
from typing import List, Optional
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

_client = Groq(api_key=GROQ_API_KEY)

# Model selection - using the latest and most capable model
CHAT_MODEL = "llama-3.3-70b-versatile"
FAST_MODEL = "llama-3.1-8b-instant"  # For faster responses when needed


def generate_text(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    system_message: Optional[str] = None,
    use_fast_model: bool = False
) -> str:
    """
    Generate text using Groq chat completion.
    
    Args:
        prompt: The user prompt/question
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate
        system_message: Optional system message to set context
        use_fast_model: Use faster but smaller model for quick responses
        
    Returns:
        Generated text response
    """
    messages = []
    
    if system_message:
        messages.append({"role": "system", "content": system_message})
    else:
        messages.append({
            "role": "system",
            "content": "You are a helpful assistant that extracts structured data and provides accurate information."
        })
    
    messages.append({"role": "user", "content": prompt})
    
    model = FAST_MODEL if use_fast_model else CHAT_MODEL
    
    try:
        response = _client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq API error: {str(e)}")


def generate_chat_response(
    messages: List[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024,
    use_fast_model: bool = False
) -> str:
    """
    Generate a chat response using Groq with a conversation history.
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate
        use_fast_model: Use faster but smaller model for quick responses
        
    Returns:
        Generated text response
    """
    model = FAST_MODEL if use_fast_model else CHAT_MODEL
    
    try:
        response = _client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq API error: {str(e)}")


def extract_structured_data(
    prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 512
) -> str:
    """
    Extract structured data using Groq with lower temperature for consistency.
    
    Args:
        prompt: The extraction prompt
        temperature: Lower temperature for more deterministic output
        max_tokens: Maximum tokens to generate
        
    Returns:
        Extracted structured data as text
    """
    return generate_text(
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        system_message="You are a precise data extraction assistant. Extract only the requested information in the specified format.",
        use_fast_model=False  # Use the more capable model for structured extraction
    )


def get_client() -> Groq:
    """Get the Groq client instance."""
    return _client

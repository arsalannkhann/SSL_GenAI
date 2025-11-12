"""
LLM-based query parsing with support for multiple providers:
- Gemini: Google's Gemini models (default)
- Groq: Fast Llama models
- OpenAI: GPT models

The provider is configured via LLM_PROVIDER in config.py
"""
import json
from typing import Dict
from .config import LLM_PROVIDER

EXTRACTION_PROMPT = """Analyze this job query/description and extract structured information.

Query: {query}

Extract and return ONLY a valid JSON object with these fields:
{{
  "job_role": "primary role or position mentioned",
  "technical_skills": ["list", "of", "technical", "skills"],
  "soft_skills": ["list", "of", "behavioral", "traits"],
  "experience_level": "entry/mid/senior/executive or null",
  "duration_minutes": null or number,
  "test_type_preference": "technical/behavioral/both/none",
  "key_competencies": ["main", "competencies", "needed"]
}}

Return ONLY the JSON, no other text."""


def _extract_with_provider(prompt: str) -> str:
    """Extract structured data using the configured LLM provider."""
    if LLM_PROVIDER == "gemini":
        from .gemini_client import extract_structured_data
        return extract_structured_data(prompt, temperature=0.3, use_pro_model=False)
    elif LLM_PROVIDER == "groq":
        from .groq_client import extract_structured_data
        return extract_structured_data(prompt, temperature=0.3)
    elif LLM_PROVIDER == "openai":
        from .openai_client import generate_text
        return generate_text(prompt, temperature=0.3)
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")


def parse_query_with_llm(query: str) -> Dict:
    """
    Use configured LLM provider to extract structured information from query.
    
    Args:
        query: The user's job query/description
        
    Returns:
        Dictionary with extracted structured information
    """
    try:
        prompt = EXTRACTION_PROMPT.format(query=query)
        response = _extract_with_provider(prompt)
        
        # Clean response - extract JSON if wrapped in markdown
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        parsed = json.loads(response)
        
        # Add computed flags
        parsed["raw"] = query
        parsed["needs_balance"] = parsed.get("test_type_preference") == "both"
        parsed["prefers_tech"] = parsed.get("test_type_preference") == "technical"
        parsed["prefers_behavioral"] = parsed.get("test_type_preference") == "behavioral"
        parsed["llm_provider"] = LLM_PROVIDER
        
        return parsed
    except Exception as e:
        print(f"LLM parsing failed ({LLM_PROVIDER}): {e}, falling back to heuristic")
        # Fallback to heuristic parser
        from .query_parser import parse_query
        return parse_query(query)

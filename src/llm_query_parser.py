import json
from typing import Dict
from .gemini_client import generate_text

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


def parse_query_with_llm(query: str) -> Dict:
    """Use Gemini LLM to extract structured information from query."""
    try:
        prompt = EXTRACTION_PROMPT.format(query=query)
        response = generate_text(prompt, temperature=0.3)
        
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
        
        return parsed
    except Exception as e:
        print(f"LLM parsing failed: {e}, falling back to heuristic")
        # Fallback to heuristic parser
        from .query_parser import parse_query
        return parse_query(query)

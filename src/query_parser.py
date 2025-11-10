import re
from typing import Dict

# Very lightweight heuristic parser; LLM-based extraction can be added later
TECH_KEYWORDS = [
    "java", "python", "sql", "cloud", "aws", "azure", "gcp", "javascript",
    "data", "ml", "machine learning", "devops", "react", "node", "c++", "c#",
]
BEHAVIORAL_KEYWORDS = [
    "leadership", "communication", "teamwork", "collaboration", "dependability",
    "adaptability", "initiative", "integrity", "attention to detail"
]


def parse_query(query: str) -> Dict:
    q = query.lower()
    duration_match = re.search(r"(\d{1,3})\s*(min|mins|minutes|hour|hours)", q)
    minutes = None
    if duration_match:
        val = int(duration_match.group(1))
        unit = duration_match.group(2)
        minutes = val if "min" in unit else val * 60

    wants_tech = any(k in q for k in TECH_KEYWORDS)
    wants_behav = any(k in q for k in BEHAVIORAL_KEYWORDS) or ("behavior" in q or "personality" in q)

    return {
        "raw": query,
        "duration_minutes": minutes,
        "needs_balance": wants_tech and wants_behav,
        "prefers_tech": wants_tech and not wants_behav,
        "prefers_behavioral": wants_behav and not wants_tech,
    }

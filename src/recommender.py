from typing import List, Dict
from .embedding import embed_query, embed_texts
from . import vector_store
try:
    from .llm_query_parser import parse_query_with_llm as parse_query
except ImportError:
    from .query_parser import parse_query


def balance_recommendations(candidates: List[Dict], analysis: Dict, k: int) -> List[Dict]:
    if not analysis.get("needs_balance"):
        return candidates[:k]
    tech = [c for c in candidates if c.get("type") == "K"]
    beh = [c for c in candidates if c.get("type") == "P"]
    tech_n = int(round(k * 0.6))
    beh_n = k - tech_n
    out = tech[:tech_n] + beh[:beh_n]
    if len(out) < k:
        rest = [c for c in candidates if c not in out]
        out += rest[: k - len(out)]
    return out[:k]


def recommend_assessments(query: str, top_k: int = 10) -> List[Dict]:
    analysis = parse_query(query)
    q_emb = embed_query(query)
    res = vector_store.query(q_emb, top_k=50)

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    items = []
    for doc, meta, dist in zip(docs, metas, dists):
        score = 1.0 - dist if dist is not None else 0.0
        url = (meta or {}).get("url") or ""
        raw_name = (meta or {}).get("name") or ""

        if not raw_name and url:
            slug = url.rstrip("/").split("/")[-1]
            raw_name = slug.replace("-", " ").replace("_", " ").title()

        skills_meta = (meta or {}).get("skills")
        if isinstance(skills_meta, str):
            # Stored as string in metadata for Chroma compatibility
            try:
                import ast

                skills = ast.literal_eval(skills_meta)
                if not isinstance(skills, list):
                    skills = []
            except Exception:
                skills = []
        else:
            skills = skills_meta

        items.append({
            "name": raw_name,
            "url": url,
            "type": (meta or {}).get("type") or "",
            "duration": (meta or {}).get("duration") or "",
            "skills": skills,
            "score": score,
            "_doc": doc,
        })

    # Basic duration filter if present
    minutes = analysis.get("duration_minutes")
    if minutes:
        def parse_minutes(s):
            if not s:
                return None
            s = s.lower()
            if "hour" in s:
                m = [int(x) for x in s.split() if x.isdigit()]
                return (m[0] if m else 1) * 60
            m = [int(x) for x in s.split() if x.isdigit()]
            return m[0] if m else None
        items = [it for it in items if (parse_minutes(it.get("duration")) or 9999) <= minutes]

    # Sort by score desc
    items.sort(key=lambda x: x["score"], reverse=True)

    # Balance K vs P if needed
    items = balance_recommendations(items, analysis, top_k)
    return items

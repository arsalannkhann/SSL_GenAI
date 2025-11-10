import argparse
import json
from typing import List
from src.embedding import embed_texts
from src import vector_store


def build_index(path: str):
    with open(path, "r") as f:
        items = json.load(f)
    ids = []
    docs = []
    metas = []
    for i, it in enumerate(items):
        body = f"{it.get('name','')}\n{it.get('description','')}\nSkills: {', '.join(it.get('skills', []))}"
        ids.append(str(i))
        docs.append(body)
        # ChromaDB doesn't accept None values, convert to empty strings
        metas.append({
            "name": it.get("name") or "",
            "url": it.get("url") or "",
            "type": it.get("type") or "",
            "duration": it.get("duration") or "",
            "skills": str(it.get("skills") or []),
        })
    embs = embed_texts(docs)
    vector_store.add_items(ids, embs, metas, docs)
    print(f"Indexed {len(ids)} items")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Path to scraped JSON")
    ap.add_argument("--persist", dest="persist", default=None, help="Chroma persist dir (optional)")
    args = ap.parse_args()
    if args.persist:
        import os
        os.environ["CHROMA_PERSIST_DIR"] = args.persist
    build_index(args.inp)

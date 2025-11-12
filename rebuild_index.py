"""
Script to rebuild the vector database index with local embeddings.
Run this after switching embedding models.
"""
import json
import os
import shutil
from src.embedding import embed_texts
from src import vector_store

def rebuild_index():
    """Rebuild the vector database with local embeddings."""
    print("🔄 Rebuilding vector database with local embeddings...")
    
    # Remove old ChromaDB database
    chroma_dir = vector_store.CHROMA_PERSIST_DIR
    if os.path.exists(chroma_dir):
        print(f"📁 Removing old database at {chroma_dir}")
        shutil.rmtree(chroma_dir)
    
    # Load catalog data
    catalog_path = "data/catalog.json"
    print(f"📖 Loading catalog from {catalog_path}")
    with open(catalog_path, "r") as f:
        items = json.load(f)
    
    print(f"📊 Found {len(items)} items")
    
    # Prepare data
    ids = []
    docs = []
    metas = []
    
    for i, it in enumerate(items):
        body = f"{it.get('name','')}\n{it.get('description','')}\nSkills: {', '.join(it.get('skills', []))}"
        ids.append(str(i))
        docs.append(body)
        metas.append({
            "name": it.get("name") or "",
            "url": it.get("url") or "",
            "type": it.get("type") or "",
            "duration": it.get("duration") or "",
            "skills": str(it.get("skills") or []),
        })
    
    # Generate embeddings
    print("🧠 Generating embeddings using local model (this may take a minute)...")
    embs = embed_texts(docs)
    
    # Add to vector store
    print("💾 Storing embeddings in ChromaDB...")
    vector_store.add_items(ids, embs, metas, docs)
    
    print(f"✅ Successfully indexed {len(ids)} items!")
    print("🚀 Your system is now ready to use without API quota limits!")

if __name__ == "__main__":
    rebuild_index()

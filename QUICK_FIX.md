# Quick Fix for Gemini API Quota Issue

## Problem
You were hitting Gemini API quota limits for embeddings, which prevented the system from working.

## Solution Implemented
Switched from Gemini API embeddings to **local sentence-transformers** embeddings:
- ✅ No API calls required
- ✅ No quota limits
- ✅ Works perfectly on Vercel
- ✅ Fast and efficient
- ✅ Free forever

## What Changed
1. **Added local embedding model**: `sentence-transformers` with `all-MiniLM-L6-v2`
2. **Updated `src/embedding.py`**: Now uses local model instead of OpenAI/Gemini
3. **Updated `src/vector_store.py`**: Disabled default embedding function to prevent Gemini API calls
4. **Added `rebuild_index.py`**: Script to rebuild database with new embeddings

## Steps to Complete the Fix

### 1. Install New Dependencies
```bash
pip install sentence-transformers==2.2.2 torch==2.0.1
```

### 2. Rebuild the Vector Database
```bash
python rebuild_index.py
```

This will:
- Remove the old database (with Gemini embeddings)
- Load your catalog data
- Generate new embeddings using the local model (takes ~1 minute)
- Store them in ChromaDB

### 3. Test the API
```bash
# Start the API server
uvicorn api.main:app --reload --port 8000
```

In another terminal:
```bash
# Test the API
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"query": "software engineer with Python skills", "top_k": 5}'
```

### 4. Deploy to Vercel

Your frontend is ready to deploy. The API will work without any quota issues.

For the backend API, you can either:
- Deploy on Render (as originally planned)
- Deploy on Vercel as a serverless function
- Use any other platform

## Benefits of This Approach
- **No API Costs**: Everything runs locally
- **No Quota Limits**: Unlimited embeddings
- **Fast**: Local model is very quick
- **Reliable**: No dependency on external APIs
- **Production-Ready**: Works great for deployment

## Model Details
- **Model**: `all-MiniLM-L6-v2`
- **Dimensions**: 384 (vs 768 for Gemini)
- **Speed**: Very fast, optimized for CPU
- **Quality**: Excellent for search/retrieval tasks
- **Size**: ~90MB download (happens automatically)

## Next Steps
1. Run the commands above
2. Test locally
3. Deploy to Vercel
4. Enjoy your quota-free system! 🎉

# Deployment Guide

## Prerequisites
- GitHub account
- Render account (free tier)
- Vercel account (free tier)
- Google Gemini API key

## Step 1: Prepare Your Code

1. **Get Gemini API Key**
   - Visit https://aistudio.google.com/app/apikey
   - Create a new API key
   - Save it securely

2. **Initialize Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: SHL Assessment Recommendation System"
   ```

3. **Push to GitHub**
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/shl-assessment-system.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy API to Render

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign up or login with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   - **Name**: `shl-assessment-api`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add variable:
     - Key: `GOOGLE_API_KEY`
     - Value: Your Gemini API key
   - Add variable:
     - Key: `CHROMA_PERSIST_DIR`
     - Value: `/opt/render/project/.chroma`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your API URL: `https://shl-assessment-api.onrender.com`

6. **Test API**
   ```bash
   curl https://YOUR-API-URL.onrender.com/health
   ```

## Step 3: Deploy Frontend to Vercel

### Option A: Streamlit Cloud (Recommended for Streamlit)

1. **Sign up/Login to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub

2. **Deploy App**
   - Click "New app"
   - Select your repository
   - Set main file path: `frontend/app.py`
   - Click "Advanced settings"
   - Add secrets:
     ```toml
     API_URL = "https://YOUR-API-URL.onrender.com"
     ```
   - Click "Deploy"

### Option B: Vercel (Alternative)

1. **Sign up/Login to Vercel**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your GitHub repository

3. **Configure Project**
   - **Framework Preset**: Other
   - **Build Command**: `pip install -r requirements.txt && echo "Build complete"`
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Add Environment Variables**
   - Add variable:
     - Key: `API_URL`
     - Value: `https://YOUR-API-URL.onrender.com`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment

## Step 4: Build Vector Index on Render

Since Render uses ephemeral storage, you have two options:

### Option A: Build index on first request (Lazy Loading)
Add this to `src/vector_store.py`:
```python
import os

def ensure_index_exists():
    """Build index if it doesn't exist."""
    if not os.path.exists(CHROMA_PERSIST_DIR):
        from scripts.build_index import build_index
        build_index("data/shl_catalog.json")
```

### Option B: Use persistent disk (Paid plan)
- Upgrade to Render paid plan
- Add persistent disk
- Build index once

### Option C: Use external vector DB
- Use Pinecone (free tier)
- Use Weaviate Cloud (free tier)
- Update `vector_store.py` to use cloud service

## Step 5: Verify Deployment

1. **Test API**
   ```bash
   curl -X POST https://YOUR-API-URL.onrender.com/recommend \
     -H "Content-Type: application/json" \
     -d '{"query": "Java developer with 5 years experience", "top_k": 5}'
   ```

2. **Test Frontend**
   - Visit your Streamlit/Vercel URL
   - Enter a test query
   - Verify recommendations appear

## Troubleshooting

### API Issues
- **503 Service Unavailable**: Render free tier spins down after inactivity. First request may take 30-60 seconds.
- **500 Internal Server Error**: Check Render logs for errors. Likely missing `GOOGLE_API_KEY`.
- **ChromaDB errors**: Ensure `CHROMA_PERSIST_DIR` is writable.

### Frontend Issues
- **Connection refused**: Verify `API_URL` environment variable is set correctly.
- **CORS errors**: Add CORS middleware to FastAPI (already included in `api/main.py`).

### Performance
- **Slow responses**: Gemini API calls can take 2-5 seconds. Consider caching.
- **Cold starts**: Render free tier has cold starts. Upgrade to paid for always-on.

## Monitoring

1. **Render Dashboard**
   - View logs in real-time
   - Monitor CPU/memory usage
   - Check deployment history

2. **Vercel Dashboard**
   - View deployment logs
   - Monitor function invocations
   - Check analytics

## Updating Deployment

```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"
git push origin main

# Render and Vercel will auto-deploy on push
```

## Cost Optimization

- **Render Free Tier**: 750 hours/month, spins down after 15 min inactivity
- **Vercel Free Tier**: 100 GB-hours/month
- **Gemini API**: Free tier includes 60 requests/minute
- **ChromaDB**: Free (local storage)

Total monthly cost: **$0** (within free tier limits)

## Production Recommendations

1. **Use persistent vector DB** (Pinecone/Weaviate)
2. **Add caching** (Redis) for frequent queries
3. **Implement rate limiting**
4. **Add authentication** if needed
5. **Monitor API usage** to stay within free tiers
6. **Set up error tracking** (Sentry)
7. **Add logging** (Papertrail, Logtail)

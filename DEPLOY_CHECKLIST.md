# 🚀 Deployment Checklist

## Pre-Deployment

- [x] Local testing completed
- [x] API working on localhost:8000
- [x] Frontend working on localhost:8501
- [x] predictions.csv generated (90 rows: 9 queries × 10 assessments)
- [x] .env.example has API key template
- [x] .gitignore properly configured

## Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: SHL Assessment Recommendation System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shl-assessment-system.git
git push -u origin main
```

**IMPORTANT:** Before pushing, ensure `.env` is NOT committed (it's in .gitignore)

## Step 2: Deploy API to Render

1. Go to https://render.com
2. Sign in with GitHub
3. Click **New +** → **Web Service**
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml`
6. Add environment variable:
   - Key: `GOOGLE_API_KEY`
   - Value: Your Gemini API key
7. Click **Create Web Service**
8. Wait 5-10 minutes for deployment
9. **Copy your API URL**: `https://your-app-name.onrender.com`

## Step 3: Deploy Frontend to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select your repository
5. Set:
   - **Main file path**: `frontend/app.py`
   - **Python version**: 3.9
6. Click **Advanced settings** → **Secrets**
7. Add:
   ```toml
   API_URL = "https://your-app-name.onrender.com"
   ```
   (Replace with your actual Render URL from Step 2)
8. Click **Deploy**
9. **Copy your Streamlit URL**: `https://your-app.streamlit.app`

## Step 4: Update README

Update README.md with your deployment URLs:
```markdown
## 🚀 Live Demo
- **API:** https://your-actual-api.onrender.com
- **Frontend:** https://your-actual-app.streamlit.app
```

## Step 5: Final Verification

Test your deployed app:

1. **API Health Check:**
   ```bash
   curl https://your-api.onrender.com/health
   ```

2. **API Recommendation:**
   ```bash
   curl -X POST https://your-api.onrender.com/recommend \
     -H "Content-Type: application/json" \
     -d '{"query": "Java developer", "top_k": 5}'
   ```

3. **Frontend:** Visit your Streamlit URL and test a query

## Submission Files

Ensure you have:
- [ ] GitHub repository URL
- [ ] API URL (deployed)
- [ ] Frontend URL (deployed)
- [ ] `predictions.csv` (in repo)
- [ ] `APPROACH.md` (technical document)
- [ ] `DEPLOYMENT.md` (deployment guide)
- [ ] Mean Recall@10 calculated and documented

## Notes

- Render free tier: Cold starts after 15 min inactivity (first request may take 30-60s)
- Streamlit Cloud: Always on, no cold starts
- Vector index builds automatically during Render deployment
- Both services auto-deploy on git push

## Troubleshooting

**API returns 500:**
- Check Render logs
- Verify GOOGLE_API_KEY is set correctly

**Frontend can't connect:**
- Verify API_URL in Streamlit secrets matches Render URL
- Check CORS is enabled (already done in code)

**Build fails:**
- Check render.yaml syntax
- Ensure data/catalog.json exists in repo

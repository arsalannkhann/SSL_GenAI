#!/bin/bash
# SHL Assessment Recommendation System - Deployment Commands

echo "🚀 SHL Assessment Recommendation System - GitHub Push"
echo "======================================================"
echo ""

# Check if in correct directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Run this from the project root directory"
    exit 1
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
else
    echo "✓ Git already initialized"
fi

# Add all files
echo ""
echo "📦 Adding files to Git..."
git add .

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git status --short

# Commit
echo ""
echo "💾 Creating commit..."
git commit -m "Complete SHL Assessment Recommendation System with RAG implementation

- RAG-based recommendation engine with Gemini embeddings
- LLM query parsing with heuristic fallback
- ChromaDB vector database for semantic search
- FastAPI backend with /health and /recommend endpoints
- Streamlit frontend for interactive queries
- Balanced K/P test recommendations
- predictions.csv generated (90 rows: 9 queries × 10 assessments)
- Complete documentation (README, APPROACH, DEPLOYMENT)
- Deployment configs for Render and Streamlit Cloud
"

# Set main branch
echo ""
echo "🌿 Setting main branch..."
git branch -M main

echo ""
echo "======================================================"
echo "✅ Git repository ready!"
echo "======================================================"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Create GitHub repository:"
echo "   - Go to: https://github.com/new"
echo "   - Name: shl-assessment-recommendation"
echo "   - Keep it Public"
echo "   - DON'T initialize with README"
echo "   - Click 'Create repository'"
echo ""
echo "2. Push to GitHub (replace YOUR_USERNAME):"
echo "   git remote add origin https://github.com/YOUR_USERNAME/shl-assessment-recommendation.git"
echo "   git push -u origin main"
echo ""
echo "3. Deploy API to Render:"
echo "   - Go to: https://render.com"
echo "   - New Web Service → Select your repo"
echo "   - Add env var: GOOGLE_API_KEY=AIzaSyB2Hqji0BB1EU95IxKKDSmnNyj3_Z_H6-Q"
echo "   - Deploy!"
echo ""
echo "4. Deploy Frontend to Streamlit Cloud:"
echo "   - Go to: https://share.streamlit.io"
echo "   - New app → Select your repo"
echo "   - Main file: frontend/app.py"
echo "   - Add secret: API_URL = https://your-render-url.onrender.com"
echo "   - Deploy!"
echo ""
echo "======================================================"

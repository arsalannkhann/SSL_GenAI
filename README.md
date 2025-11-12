# SHL Assessment Recommendation System

An intelligent RAG-based assessment recommendation system with multi-provider support for embeddings and LLM operations.

## 🎯 Key Highlights
- **Multi-Provider Architecture**: Switch between Gemini, Groq, OpenAI, or local models
- **Hybrid AI**: Combines semantic search with LLM-powered query understanding
- **Production-Ready**: FastAPI backend + Modern React frontend
- **Cost-Optimized**: Default configuration uses free tiers (Groq + Gemini)
- **Flexible Deployment**: Render, Vercel, or local

## 🚀 Live Demo
- **API:** `https://your-api-name.onrender.com` (Replace after deployment)
- **Frontend:** `https://your-app.vercel.app` (Replace after deployment)
- **Documentation:** See `ARCHITECTURE.md`, `APPROACH.md`, and `DEPLOYMENT.md`

## ✨ Features
- **Multi-Provider Embeddings**: Gemini (768D), OpenAI (3072D), or Local (384D)
- **Multi-Provider LLM**: Groq (Llama 3.3), Gemini, or OpenAI (GPT-4)
- **LLM-based query parsing** to extract structured job requirements
- **Semantic search** with ChromaDB vector store
- **Intelligent ranking** with similarity scores
- **Balanced recommendations** across technical and behavioral assessments
- **FastAPI backend** with CORS support and health monitoring
- **Modern React frontend** with TailwindCSS and responsive design
- **Evaluation metrics** with Mean Recall@10

## ⚡ Quickstart

### 1. Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up environment
Create a `.env` file with your API keys:
```bash
# Required for default configuration
GROQ_API_KEY=your_groq_key_here           # Get from: https://console.groq.com
GOOGLE_API_KEY=your_google_key_here       # Get from: https://makersuite.google.com

# Provider Selection (defaults shown)
LLM_PROVIDER=groq                         # Options: groq, gemini, openai
EMBEDDING_PROVIDER=gemini                 # Options: gemini, local, openai

# Optional (only if using OpenAI)
OPENAI_API_KEY=your_openai_key_here       # Get from: https://platform.openai.com

# Storage
CHROMA_PERSIST_DIR=.chroma
```

### 3. Process dataset
```bash
python scripts/process_dataset.py --input "Gen_AI Dataset.xlsx" --output data
```

### 4. Build vector index
```bash
PYTHONPATH=. python scripts/build_index.py --in data/catalog.json --persist .chroma
```

### 5. Run API locally
```bash
PYTHONPATH=. uvicorn api.main:app --reload --port 8000
```

### 6. Run React frontend (in another terminal)
```bash
cd frontend
npm install
npm run dev
```
Visit http://localhost:3000 to use the app!

## Deployment

### API (Render)
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repo
4. Render will auto-detect `render.yaml`
5. Add `OPENAI_API_KEY` environment variable
6. Deploy!

### Frontend (Vercel/Netlify)
1. Push code to GitHub
2. Import project on Vercel or Netlify
3. Set root directory: `frontend`
4. Build command: `npm run build`
5. Output directory: `dist`
6. Add environment variable: `VITE_API_URL=https://your-api.onrender.com`
7. Deploy!

## Project Structure
```
├── src/
│   ├── gemini_client.py      # Gemini API wrapper
│   ├── embedding.py           # Embedding functions
│   ├── vector_store.py        # ChromaDB interface
│   ├── query_parser.py        # Heuristic parser (fallback)
│   ├── llm_query_parser.py    # LLM-based parser
│   ├── recommender.py         # Core recommendation engine
│   └── scrape_shl.py          # Web scraper
├── api/
│   └── main.py                # FastAPI application
├── frontend/
│   ├── src/                   # React source files
│   ├── package.json           # Node dependencies
│   └── README.md              # Frontend documentation
├── scripts/
│   ├── build_index.py         # Index builder
│   ├── evaluate.py            # Evaluation metrics
│   ├── generate_predictions.py
│   └── process_dataset.py     # Dataset processor
├── data/                      # Data files (gitignored)
├── requirements.txt
├── render.yaml                # Render deployment config
└── vercel.json                # Vercel deployment config
```

## Evaluation
```bash
# Generate predictions on test set
python scripts/generate_predictions.py --in data/test.csv --out predictions.csv --top_k 10

# Evaluate against ground truth
python scripts/evaluate.py --pred predictions.csv --truth data/train.csv --k 10
```

## 🛠️ Tech Stack

### Backend
- **LLM Providers**: 
  - Groq (Llama 3.3 70B, Llama 3.1 8B) - Default, fast & free
  - Google Gemini (gemini-pro)
  - OpenAI (GPT-4, GPT-3.5)
- **Embedding Providers**:
  - Google Gemini (text-embedding-004, 768D) - Default, high quality
  - Local (sentence-transformers, 384D) - No API needed
  - OpenAI (text-embedding-3-large, 3072D) - Premium
- **Vector DB**: ChromaDB with cosine similarity
- **API**: FastAPI + Uvicorn + Pydantic
- **Data Processing**: Pandas, NumPy, BeautifulSoup4

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS + shadcn/ui components
- **Build**: Fast HMR with Vite
- **Responsive**: Mobile-first design

### Deployment
- **API**: Render / AWS / Google Cloud
- **Frontend**: Vercel / Netlify
- **Storage**: Persistent ChromaDB

## 📚 Documentation
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Complete system architecture and design
- **[APPROACH.md](./APPROACH.md)** - Technical approach and methodology
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Detailed deployment guide
- **[FRONTEND_SETUP.md](./FRONTEND_SETUP.md)** - Frontend configuration
- **[DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md)** - Pre-deployment checklist

## 🧪 Testing

### Test Individual Components
```bash
# Test Gemini integration
python test_gemini.py

# Test Groq integration
python test_groq.py

# Test API endpoints
python test_api.py

# Test full integration
python test_integration.py
```

## 🔧 Configuration

### Provider Options

**Recommended (Production)**:
```bash
LLM_PROVIDER=groq           # Fast, reliable, free
EMBEDDING_PROVIDER=gemini   # High quality, generous free tier
```

**Development (No API)**:
```bash
LLM_PROVIDER=groq          # Fast & free
EMBEDDING_PROVIDER=local   # No API calls, runs locally
```

**Premium (Highest Quality)**:
```bash
LLM_PROVIDER=openai        # GPT-4
EMBEDDING_PROVIDER=openai  # 3072D embeddings
```

See `ARCHITECTURE.md` for detailed comparison of providers.

## 📊 Performance

| Component | Latency | Cost | Quality |
|-----------|---------|------|---------|
| Groq LLM | ~1-2s | Free | High |
| Gemini Embeddings | ~500ms | Free* | High |
| Local Embeddings | ~100ms | $0 | Good |
| ChromaDB Query | ~50ms | $0 | N/A |

*Free tier: 1,500 queries/day

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Test with multiple providers
4. Submit a pull request

## 📝 License
MIT License

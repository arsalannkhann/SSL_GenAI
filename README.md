# SHL Assessment Recommendation System

An intelligent RAG-based assessment recommendation system using Google Gemini for embeddings and LLM-powered query understanding.

## 🚀 Live Demo
- **API:** `https://your-api-name.onrender.com` (Replace after deployment)
- **Frontend:** `https://your-app.streamlit.app` (Replace after deployment)
- **Documentation:** See `APPROACH.md` and `DEPLOYMENT.md`

## Features
- **Gemini-powered embeddings** for semantic search
- **LLM-based query parsing** to extract job requirements
- **Hybrid retrieval** with semantic search and reranking
- **Balanced recommendations** across test types (K vs P)
- **FastAPI backend** with health and recommendation endpoints
- **Streamlit frontend** for interactive queries
- **Mean Recall@10 evaluation** on training data

## Quickstart

### 1. Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up environment
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY from https://aistudio.google.com/app/apikey
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

### 6. Run Streamlit UI (in another terminal)
```bash
PYTHONPATH=.
streamlit run frontend/app.py
```

## Deployment

### API (Render)
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repo
4. Render will auto-detect `render.yaml`
5. Add `GOOGLE_API_KEY` environment variable
6. Deploy!

### Frontend (Vercel)
1. Push code to GitHub
2. Import project on Vercel
3. Set build command: `pip install -r requirements.txt && echo "Build complete"`
4. Set install command: `pip install -r requirements.txt`
5. Add environment variable: `API_URL=https://your-api.onrender.com`
6. Deploy!

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
│   └── app.py                 # Streamlit UI
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

## Tech Stack
- **Embeddings**: Google Gemini `embedding-001`
- **LLM**: Google Gemini `gemini-1.5-flash`
- **Vector DB**: ChromaDB (local/persistent)
- **API**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **Deployment**: Render (API) + Vercel (Frontend)

# SHL Assessment Recommendation System - Architecture

## 🏗️ System Architecture

This system provides intelligent assessment recommendations using a hybrid AI architecture that combines vector search with LLM-powered query understanding.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                               │
│              "Senior Python developer assessment"               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   API Gateway   │
                    │  (FastAPI)      │
                    └────────┬────────┘
                             │
            ┌────────────────┴────────────────┐
            │                                 │
    ┌───────▼────────┐              ┌────────▼──────────┐
    │  LLM Parser    │              │  Embedding Module │
    │  (Groq/Gemini) │              │  (Gemini/Local)   │
    └───────┬────────┘              └────────┬──────────┘
            │                                 │
            │ Structured Analysis             │ Query Vector
            │ (skills, role, duration)        │ (768D or 384D)
            │                                 │
            └────────────────┬────────────────┘
                             │
                    ┌────────▼────────────┐
                    │  Vector Store       │
                    │  (ChromaDB)         │
                    │  + Assessment Data  │
                    └────────┬────────────┘
                             │
                    ┌────────▼────────────┐
                    │  Recommender        │
                    │  (Ranking + Filter) │
                    └────────┬────────────┘
                             │
                    ┌────────▼────────────┐
                    │  Top-K Results      │
                    │  (Assessments)      │
                    └─────────────────────┘
```

## 🧠 Core Components

### 1. API Layer (`api/main.py`)
- **Technology**: FastAPI
- **Endpoints**:
  - `GET /health` - Health check
  - `POST /recommend` - Get assessment recommendations
- **CORS**: Enabled for frontend access

### 2. LLM Query Parser (`src/llm_query_parser.py`)
- **Purpose**: Extract structured information from natural language queries
- **Providers**: Configurable (Groq/Gemini/OpenAI)
- **Extraction**:
  - Job role
  - Technical skills
  - Soft skills
  - Experience level
  - Duration requirements
  - Test type preference (technical/behavioral/both)
  - Key competencies

### 3. Embedding System (`src/embedding.py`)
- **Multi-Provider Support**:
  - **Gemini** (default): 768 dimensions, high quality
  - **Local**: 384 dimensions, no API calls (sentence-transformers)
  - **OpenAI**: 3072 dimensions, highest quality
- **Functions**:
  - `embed_text()` - Single text embedding
  - `embed_texts()` - Batch embeddings
  - `embed_query()` - Optimized query embeddings

### 4. Vector Store (`src/vector_store.py`)
- **Technology**: ChromaDB with persistent storage
- **Distance Metric**: Cosine similarity
- **Storage**: `.chroma/` directory
- **Operations**:
  - Add assessments with embeddings
  - Query for similar assessments
  - Retrieve with metadata

### 5. Recommender (`src/recommender.py`)
- **Ranking**: Cosine similarity scores (0-1)
- **Filtering**: Duration, skills, experience level
- **Balancing**: Technical vs behavioral assessments
- **Output**: Top-K recommendations with scores

## 🔧 Provider Clients

### Groq Client (`src/groq_client.py`)
- **Models**:
  - `llama-3.3-70b-versatile` - Primary (high capability)
  - `llama-3.1-8b-instant` - Fast model
- **Features**:
  - Text generation
  - Structured data extraction
  - Chat with history
- **Advantages**: Fast, reliable, free tier

### Gemini Client (`src/gemini_client.py`)
- **Embedding Model**: `text-embedding-004` (768D)
- **Features**:
  - Document embeddings
  - Query embeddings (optimized)
  - Batch processing
- **Advantages**: High quality embeddings, generous free tier

### OpenAI Client (`src/openai_client.py`)
- **Models**:
  - `text-embedding-3-large` (3072D)
  - `gpt-4o-mini` for chat
- **Features**: Highest quality, most expensive

### Local Embeddings (`src/local_embeddings.py`)
- **Model**: `all-MiniLM-L6-v2` (384D)
- **Advantages**: No API calls, no costs, good for development
- **Trade-off**: Lower quality than cloud models

## 📊 Data Flow

### Indexing Flow
```
SHL Catalog (CSV) → Process → Generate Embeddings → Store in ChromaDB
```

### Query Flow
```
User Query → LLM Parse → Extract Vector → Search Vector Store → 
Rank & Filter → Return Top-K
```

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# API Keys
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional

# Provider Selection
LLM_PROVIDER=groq           # Options: groq, gemini, openai
EMBEDDING_PROVIDER=gemini   # Options: gemini, local, openai

# Paths
CHROMA_PERSIST_DIR=.chroma
SCRAPE_OUTPUT_PATH=data/shl_catalog.json
```

### Provider Configuration (`src/config.py`)

The system supports multiple providers for both LLM and embeddings:

**LLM Providers**:
- `groq` (default): Fast Llama models, excellent for structured extraction
- `gemini`: Google's models (requires API access)
- `openai`: GPT models, highest cost

**Embedding Providers**:
- `gemini` (default): 768D high-quality embeddings
- `local`: 384D sentence-transformers (no API needed)
- `openai`: 3072D highest quality (expensive)

## 🚀 Recommended Configuration

### Production (Cost-Optimized)
```bash
LLM_PROVIDER=groq           # Fast & free
EMBEDDING_PROVIDER=gemini   # High quality & generous free tier
```

### Development (Free, No API)
```bash
LLM_PROVIDER=groq          # Fast & free
EMBEDDING_PROVIDER=local   # No API calls needed
```

### Premium (Highest Quality)
```bash
LLM_PROVIDER=openai        # GPT-4
EMBEDDING_PROVIDER=openai  # 3072D embeddings
```

## 📦 Dependencies

### Core
- `fastapi` - API framework
- `chromadb` - Vector database
- `pandas` - Data processing
- `numpy` - Numerical operations

### LLM Providers
- `groq` - Groq API client
- `google-generativeai` - Gemini API client
- `openai` - OpenAI API client

### Embeddings
- `sentence-transformers` - Local embedding model
- `torch` - PyTorch for transformers

## 🔄 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Build vector index
python scripts/build_index.py

# Start API server
uvicorn api.main:app --reload --port 8000
```

### Production (Render/Vercel)
1. Set environment variables in platform dashboard
2. Deploy API backend (Render)
3. Deploy frontend (Vercel)
4. Configure CORS and API URL

## 📈 Performance Characteristics

| Component | Latency | Cost | Quality |
|-----------|---------|------|---------|
| Groq LLM | ~1-2s | Free | High |
| Gemini Embeddings | ~500ms | Free* | High |
| Local Embeddings | ~100ms | $0 | Good |
| ChromaDB Query | ~50ms | $0 | N/A |
| OpenAI (premium) | ~2-3s | $$$ | Highest |

*Free tier: 1,500 queries/day

## 🎯 Key Features

1. **Multi-Provider Flexibility**: Switch between providers without code changes
2. **Hybrid Intelligence**: Combines semantic search with LLM understanding
3. **Balanced Recommendations**: Considers technical AND behavioral fit
4. **Scalable**: ChromaDB handles millions of vectors
5. **Cost-Optimized**: Default configuration uses free tiers
6. **Type-Safe**: Full Python type hints
7. **Production-Ready**: CORS, error handling, health checks

## 🔐 Security Considerations

- API keys stored in `.env` (never committed)
- CORS configured for specific origins in production
- Input validation via Pydantic models
- Rate limiting recommended for production
- API key rotation supported

## 📚 Additional Documentation

- `DEPLOY_CHECKLIST.md` - Deployment steps
- `DEPLOYMENT.md` - Detailed deployment guide
- `FRONTEND_SETUP.md` - Frontend configuration
- `README.md` - Quick start guide
- `APPROACH.md` - Technical approach

## 🧪 Testing

```bash
# Test Gemini integration
python test_gemini.py

# Test Groq integration
python test_groq.py

# Test full API
python test_api.py

# Test integration
python test_integration.py
```

## 🛠️ Maintenance

### Updating the Index
```bash
python scripts/build_index.py
```

### Switching Providers
Edit `.env`:
```bash
EMBEDDING_PROVIDER=local  # Switch to local embeddings
LLM_PROVIDER=openai       # Switch to OpenAI LLM
```

### Monitoring
- Check API health: `GET /health`
- Monitor token usage in provider dashboards
- Track query latency and accuracy

## 🤝 Contributing

1. Use type hints
2. Follow existing code structure
3. Test with multiple providers
4. Update documentation
5. Handle errors gracefully

## 📝 License

[Your License Here]

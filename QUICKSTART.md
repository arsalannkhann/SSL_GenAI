# 🚀 Quick Start Guide - SHL Assessment Recommender

## ⚡ 5-Minute Setup

### 1. Clone & Install (2 minutes)
```bash
cd /path/to/SHL
pip install -r requirements.txt
```

### 2. Configure API Keys (1 minute)
Edit `.env`:
```bash
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here

LLM_PROVIDER=groq
EMBEDDING_PROVIDER=gemini
```

**Get API Keys** (Free):
- Groq: https://console.groq.com/
- Google: https://makersuite.google.com/app/apikey

### 3. Build Index (1 minute)
```bash
source .venv/bin/activate
python rebuild_index.py
```

### 4. Start Services (1 minute)
```bash
# Terminal 1: Backend
source .venv/bin/activate
uvicorn api.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm install  # First time only
npm run dev
```

### 5. Access (Now!)
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## ✅ Verify Installation

```bash
# Run system tests
python test_full_system.py

# Expected: All tests pass ✅
```

## 🎯 Usage Examples

### Via Frontend
1. Open http://localhost:5173
2. Enter query: "Python developer with ML experience"
3. Click Search
4. View ranked recommendations

### Via API (cURL)
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Senior software engineer with leadership skills",
    "top_k": 5
  }'
```

### Via Python
```python
from src.recommender import recommend_assessments

results = recommend_assessments(
    "Data scientist with SQL and Python", 
    top_k=10
)

for r in results:
    print(f"{r['name']} - Score: {r['score']:.3f}")
```

## 🔧 Configuration Options

### Switch to Local Embeddings (No API)
```bash
# .env
EMBEDDING_PROVIDER=local
```

### Use OpenAI (Premium)
```bash
# .env
OPENAI_API_KEY=your_openai_key
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| No results | Run `python rebuild_index.py` |
| API errors | Check `.env` has valid API keys |
| Slow queries | Switch to `EMBEDDING_PROVIDER=local` |
| Frontend can't connect | Check backend is running on port 8000 |
| Import errors | `pip install -r requirements.txt` |

## 📊 Provider Quick Comparison

| Use Case | Configuration |
|----------|---------------|
| **Best Free** | `LLM_PROVIDER=groq` + `EMBEDDING_PROVIDER=gemini` |
| **No API Needed** | `LLM_PROVIDER=groq` + `EMBEDDING_PROVIDER=local` |
| **Highest Quality** | `LLM_PROVIDER=openai` + `EMBEDDING_PROVIDER=openai` |
| **Fastest** | `LLM_PROVIDER=groq` + `EMBEDDING_PROVIDER=local` |

## 🎓 Key Commands

```bash
# Rebuild vector index
python rebuild_index.py

# Run all tests
python test_full_system.py

# Test Gemini only
python test_gemini.py

# Test Groq only
python test_groq.py

# Start backend
uvicorn api.main:app --reload --port 8000

# Start frontend
cd frontend && npm run dev
```

## 📚 Documentation

- `README.md` - Overview and features
- `ARCHITECTURE.md` - Complete technical architecture
- `INTEGRATION_COMPLETE.md` - Integration summary
- `DEPLOY_CHECKLIST.md` - Deployment steps
- `DEPLOYMENT.md` - Production deployment guide

## 💡 Tips

1. **Free Tier**: Default config (Groq + Gemini) is completely free
2. **Development**: Use `local` embeddings for faster iteration
3. **Production**: Stick with Gemini embeddings for quality
4. **Testing**: Run `test_full_system.py` after any changes
5. **Debugging**: Check API health at `GET /health`

## 🎯 What You Can Query

- Job titles: "Python developer", "Data scientist"
- Skills: "Machine learning and SQL"
- Experience: "Senior engineer with 5 years"
- Soft skills: "Leadership and communication"
- Mixed: "Senior Python developer with leadership skills, 30 min test"
- Behavioral: "Team collaboration assessment"

## ✨ Features

✅ Natural language queries  
✅ Semantic matching  
✅ Skill-based filtering  
✅ Duration preferences  
✅ Technical/behavioral balance  
✅ Real-time recommendations  

## 🚀 Next Actions

1. ✅ System is ready - start using it!
2. ✅ Test with your queries
3. ✅ Explore API documentation at `/docs`
4. ✅ Customize providers in `.env`
5. ✅ Deploy to production (see `DEPLOYMENT.md`)

---

**Ready?** Run `python test_full_system.py` and start recommending! 🎉

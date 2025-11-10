# SHL Assessment Recommendation System - Technical Approach

## 1. System Architecture

### Overview
The system uses a hybrid retrieval approach combining semantic search with LLM-based query understanding and reranking to recommend relevant SHL assessments based on natural language job descriptions or queries.

### Components
1. **Data Collection**: Web scraping + dataset processing
2. **Embedding Generation**: Google Gemini embedding-001 model
3. **Vector Database**: ChromaDB for semantic search
4. **Query Understanding**: Gemini LLM for structured extraction
5. **Recommendation Engine**: Hybrid retrieval with balancing
6. **API Layer**: FastAPI with REST endpoints
7. **Frontend**: Streamlit interactive UI

## 2. Data Pipeline

### 2.1 Data Collection
- **Source**: SHL product catalog (https://www.shl.com/solutions/products/product-catalog/)
- **Method**: BeautifulSoup-based web scraping
- **Extracted Fields**:
  - Assessment name
  - URL (unique identifier)
  - Description
  - Test type (K=Knowledge/Skills, P=Personality/Behavior)
  - Duration
  - Skills/competencies covered
  - Target job roles/levels

### 2.2 Data Processing
- Clean and normalize text fields
- Extract structured metadata
- Handle missing values with defaults
- Deduplicate based on URL

### 2.3 Embedding Generation
- **Model**: Google Gemini `embedding-001`
- **Task Type**: `retrieval_document` for assessments, `retrieval_query` for queries
- **Input**: Concatenated assessment name + description + skills
- **Output**: 768-dimensional dense vectors
- **Normalization**: Cosine similarity for retrieval

## 3. Query Understanding

### 3.1 LLM-Based Extraction
Use Gemini `gemini-1.5-flash` to extract structured information from natural language queries:

**Extracted Fields**:
- Job role/position
- Technical skills required
- Soft skills/behavioral traits
- Experience level (entry/mid/senior/executive)
- Duration constraints
- Test type preferences (technical/behavioral/both)
- Key competencies

**Prompt Engineering**:
- Zero-shot extraction with structured JSON output
- Temperature: 0.3 (deterministic)
- Fallback to heuristic parser on failure

### 3.2 Heuristic Fallback
Regex-based extraction for:
- Duration parsing (minutes/hours)
- Keyword matching for technical vs behavioral
- Simple skill extraction

## 4. Recommendation Engine

### 4.1 Semantic Search
1. Generate query embedding using Gemini
2. Retrieve top-50 candidates from ChromaDB using cosine similarity
3. Score: `1 - cosine_distance`

### 4.2 Filtering
Apply hard constraints:
- Duration: Filter assessments exceeding specified time
- Test type: Prioritize based on query analysis

### 4.3 Balancing Algorithm
If query requires both technical and behavioral assessments:
- Target ratio: 60% technical (K), 40% behavioral (P)
- Maintain relevance while ensuring diversity
- Fallback to top-k by score if insufficient diversity

### 4.4 Ranking
Final ranking by relevance score (cosine similarity)

## 5. Optimization Strategies

### 5.1 Prompt Engineering
- Iterative refinement of extraction prompts
- Add examples for few-shot learning
- Structured output format (JSON)

### 5.2 Hybrid Search (Future)
- Combine semantic search with BM25 keyword search
- Weighted fusion: α * semantic + (1-α) * lexical
- Optimal α determined via grid search on training set

### 5.3 LLM Reranking (Future)
- Use Gemini to rerank top-20 candidates
- Holistic assessment of query-assessment fit
- Consider multiple factors: skills, experience, test type

### 5.4 Query Expansion (Future)
- Generate similar queries using LLM
- Retrieve for each variant
- Aggregate results with score fusion

## 6. Evaluation Methodology

### 6.1 Metric: Mean Recall@10
```
Recall@K = |Predicted ∩ Ground Truth| / |Ground Truth|
Mean Recall@K = Average(Recall@K) across all queries
```

### 6.2 Evaluation Process
1. Generate predictions for training set
2. Calculate Mean Recall@10
3. Analyze failures to identify patterns
4. Iterate on prompts/algorithms
5. Re-evaluate until target recall achieved

### 6.3 Target Performance
- **Baseline**: 0.4-0.5 (semantic search only)
- **Target**: 0.6-0.7 (with LLM parsing and balancing)
- **Stretch**: 0.75+ (with reranking and hybrid search)

## 7. Technical Stack

### 7.1 Core Technologies
- **Language**: Python 3.11
- **Embeddings**: Google Gemini embedding-001
- **LLM**: Google Gemini gemini-1.5-flash
- **Vector DB**: ChromaDB (local/persistent)
- **API**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **Data**: Pandas, NumPy

### 7.2 Deployment
- **API**: Render (free tier)
  - Auto-deploy on git push
  - Environment variables for secrets
  - Persistent disk for vector DB
- **Frontend**: Streamlit Cloud or Vercel
  - Connect to API via environment variable
  - Auto-deploy on git push

### 7.3 Cost
- **Total**: $0/month (within free tier limits)
- Gemini API: 60 requests/minute free
- Render: 750 hours/month free
- Vercel: 100 GB-hours/month free

## 8. Key Design Decisions

### 8.1 Why Gemini?
- Free tier with generous limits
- High-quality embeddings (768-dim)
- Fast LLM inference (<2s)
- Single API for embeddings + LLM

### 8.2 Why ChromaDB?
- Simple local deployment
- Persistent storage
- Good performance for <10k items
- Easy migration to cloud (Pinecone/Weaviate)

### 8.3 Why Balancing?
- Job descriptions often require both technical and behavioral assessments
- Pure semantic search may over-index on one type
- Balanced recommendations provide better coverage

### 8.4 Why LLM Query Parsing?
- Natural language queries are ambiguous
- Structured extraction improves filtering and balancing
- Enables more sophisticated ranking logic

## 9. Challenges & Solutions

### Challenge 1: Cold Start on Render
- **Problem**: Free tier spins down after 15 min inactivity
- **Solution**: Accept 30-60s first request latency, or upgrade to paid tier

### Challenge 2: Gemini Rate Limits
- **Problem**: 60 requests/minute on free tier
- **Solution**: Batch embedding generation, implement caching

### Challenge 3: Vector DB Persistence
- **Problem**: Render ephemeral storage
- **Solution**: Use persistent disk (paid) or cloud vector DB (Pinecone)

### Challenge 4: Low Initial Recall
- **Problem**: Baseline semantic search may have low recall
- **Solution**: Iterative prompt engineering, hybrid search, reranking

## 10. Future Enhancements

1. **Advanced Reranking**: Cross-encoder models for better ranking
2. **User Feedback Loop**: Collect clicks/ratings to improve recommendations
3. **Caching Layer**: Redis for frequent queries
4. **A/B Testing**: Compare different retrieval strategies
5. **Monitoring**: LangSmith for tracing and debugging
6. **Authentication**: API keys for production use
7. **Analytics**: Track query patterns and recommendation quality

## 11. Deliverables

1. ✅ **GitHub Repository**: Complete codebase with documentation
2. ✅ **API Deployment**: Render with /health and /recommend endpoints
3. ✅ **Frontend Deployment**: Streamlit Cloud or Vercel
4. ✅ **predictions.csv**: Test set predictions in required format
5. ✅ **Mean Recall@10**: Calculated and documented
6. ✅ **Approach Document**: This document (2 pages)
7. ✅ **README**: Setup and usage instructions

## 12. Conclusion

This system demonstrates a production-ready approach to semantic search and recommendation using modern LLM and embedding technologies. The hybrid retrieval strategy with LLM-based query understanding provides a strong foundation for high-quality recommendations while maintaining simplicity and cost-effectiveness.

The modular architecture allows for easy experimentation and iteration, with clear paths for future enhancements based on evaluation results and user feedback.

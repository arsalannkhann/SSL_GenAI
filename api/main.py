from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from src.recommender import recommend_assessments

app = FastAPI(title="SHL Assessment Recommendation API")

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 10

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/recommend")
async def recommend(request: RecommendationRequest):
    recs = recommend_assessments(request.query, top_k=request.top_k)
    return {
        "query": request.query,
        "recommendations": [
            {
                "assessment_name": r["name"],
                "assessment_url": r["url"],
                "relevance_score": r["score"],
                "test_type": r["type"],
                "duration": r.get("duration"),
            }
            for r in recs
        ],
        "total_results": len(recs),
    }

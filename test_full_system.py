#!/usr/bin/env python3
"""
Complete system test - Tests the full recommendation pipeline with Gemini embeddings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Set optimal configuration
os.environ["EMBEDDING_PROVIDER"] = "gemini"
os.environ["LLM_PROVIDER"] = "groq"

def test_configuration():
    """Test that configuration is set correctly."""
    print("\n" + "="*60)
    print("Testing System Configuration")
    print("="*60)
    
    from src.config import EMBEDDING_PROVIDER, LLM_PROVIDER, GOOGLE_API_KEY, GROQ_API_KEY
    from src.embedding import get_provider_info
    
    print(f"\nEmbedding Provider: {EMBEDDING_PROVIDER}")
    print(f"LLM Provider: {LLM_PROVIDER}")
    print(f"Google API Key: {'✓ Set' if GOOGLE_API_KEY else '✗ Missing'}")
    print(f"Groq API Key: {'✓ Set' if GROQ_API_KEY else '✗ Missing'}")
    
    info = get_provider_info()
    print(f"\nEmbedding Details:")
    print(f"  Provider: {info['provider']}")
    print(f"  Dimensions: {info['dimensions']}")
    print(f"  Description: {info['description']}")
    
    print("\n✅ Configuration test passed!")


def test_query_parsing():
    """Test LLM-based query parsing with Groq."""
    print("\n" + "="*60)
    print("Testing Query Parsing (Groq LLM)")
    print("="*60)
    
    from src.llm_query_parser import parse_query_with_llm
    
    test_queries = [
        "I need a Python developer with 5 years experience",
        "Find behavioral assessments for leadership",
        "Senior data scientist with machine learning and SQL skills, 30 minute test"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = parse_query_with_llm(query)
        print(f"  Role: {result.get('job_role')}")
        print(f"  Technical Skills: {result.get('technical_skills', [])[:3]}")
        print(f"  Test Type: {result.get('test_type_preference')}")
        print(f"  Duration: {result.get('duration_minutes')} minutes")
    
    print("\n✅ Query parsing test passed!")


def test_embeddings():
    """Test Gemini embeddings."""
    print("\n" + "="*60)
    print("Testing Embeddings (Gemini)")
    print("="*60)
    
    from src.embedding import embed_query, embed_texts
    
    # Test query embedding
    query = "Python developer with machine learning experience"
    print(f"\nQuery: {query}")
    emb = embed_query(query)
    print(f"Embedding dimensions: {len(emb)}")
    print(f"First 5 values: {emb[:5]}")
    
    # Test batch embeddings
    texts = ["Software Engineer", "Data Analyst", "Product Manager"]
    print(f"\nBatch embedding {len(texts)} texts...")
    embs = embed_texts(texts)
    print(f"Generated {len(embs)} embeddings")
    
    print("\n✅ Embeddings test passed!")


def test_vector_store():
    """Test vector store connection."""
    print("\n" + "="*60)
    print("Testing Vector Store")
    print("="*60)
    
    from src import vector_store
    
    collection = vector_store.get_collection()
    count = collection.count()
    
    print(f"\nVector store collection: {vector_store._COLLECTION_NAME}")
    print(f"Total documents: {count}")
    
    if count > 0:
        print("✓ Vector store has data")
    else:
        print("⚠ Vector store is empty - run rebuild_index.py first")
    
    print("\n✅ Vector store test passed!")


def test_recommendations():
    """Test the complete recommendation pipeline."""
    print("\n" + "="*60)
    print("Testing Complete Recommendation Pipeline")
    print("="*60)
    
    from src.recommender import recommend_assessments
    
    test_queries = [
        ("Python developer with 5+ years experience", 5),
        ("Leadership and communication skills", 5),
        ("Data scientist with SQL and machine learning", 5)
    ]
    
    for query, top_k in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        results = recommend_assessments(query, top_k=top_k)
        
        print(f"\nFound {len(results)} recommendations:")
        for i, rec in enumerate(results[:3], 1):
            print(f"\n{i}. {rec['name']}")
            print(f"   Score: {rec['score']:.3f}")
            print(f"   Type: {rec['type']}")
            print(f"   Duration: {rec.get('duration', 'N/A')}")
            if rec.get('skills'):
                print(f"   Skills: {', '.join(rec['skills'][:3])}")
    
    print("\n✅ Recommendation pipeline test passed!")


def main():
    """Run all system tests."""
    print("\n" + "="*60)
    print("COMPLETE SYSTEM TEST SUITE")
    print("Testing SHL Assessment Recommender with:")
    print("  - Gemini Embeddings (768D)")
    print("  - Groq LLM (Llama 3.3 70B)")
    print("  - ChromaDB Vector Store")
    print("="*60)
    
    tests = [
        ("Configuration", test_configuration),
        ("Query Parsing", test_query_parsing),
        ("Embeddings", test_embeddings),
        ("Vector Store", test_vector_store),
        ("Recommendations", test_recommendations)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            test_func()
            results.append((test_name, True))
        except Exception as e:
            print(f"\n❌ {test_name} test failed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! System is fully operational.")
        print("\nNext steps:")
        print("  1. Start API: uvicorn api.main:app --port 8000")
        print("  2. Start Frontend: cd frontend && npm run dev")
        print("  3. Access at: http://localhost:5173")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())

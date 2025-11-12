#!/usr/bin/env python3
"""
Test script for Gemini integration.
Tests both embedding generation and LLM capabilities.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_gemini_embeddings():
    """Test Gemini embedding generation."""
    print("\n" + "="*60)
    print("Testing Gemini Embeddings")
    print("="*60)
    
    try:
        from src.gemini_client import get_embedding, get_embeddings, get_query_embedding, get_dimensions
        
        # Test single embedding
        print("\n1. Testing single text embedding...")
        text = "Software engineer with Python and machine learning experience"
        embedding = get_embedding(text)
        print(f"   Text: {text}")
        print(f"   Embedding dimensions: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")
        print("   ✓ Single embedding successful")
        
        # Test batch embeddings
        print("\n2. Testing batch embeddings...")
        texts = [
            "Python developer needed for backend development",
            "Data scientist with SQL and Python skills",
            "Project manager for agile teams"
        ]
        embeddings = get_embeddings(texts)
        print(f"   Number of texts: {len(texts)}")
        print(f"   Number of embeddings: {len(embeddings)}")
        print(f"   Each embedding dimensions: {len(embeddings[0])}")
        print("   ✓ Batch embeddings successful")
        
        # Test query embedding
        print("\n3. Testing query embedding...")
        query = "Find me assessment for senior developers"
        query_emb = get_query_embedding(query)
        print(f"   Query: {query}")
        print(f"   Embedding dimensions: {len(query_emb)}")
        print("   ✓ Query embedding successful")
        
        # Test dimensions function
        print("\n4. Testing dimensions function...")
        dims = get_dimensions()
        print(f"   Reported dimensions: {dims}")
        print(f"   Actual dimensions: {len(embedding)}")
        assert dims == len(embedding), "Dimension mismatch!"
        print("   ✓ Dimensions correct")
        
        print("\n✅ All embedding tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Embedding test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gemini_chat():
    """Test Gemini chat completion."""
    print("\n" + "="*60)
    print("Testing Gemini Chat Completion")
    print("="*60)
    
    try:
        from src.gemini_client import generate_text, extract_structured_data
        
        # Test simple text generation
        print("\n1. Testing simple text generation...")
        prompt = "What are the key skills for a data scientist?"
        response = generate_text(prompt, temperature=0.7, max_tokens=200)
        print(f"   Prompt: {prompt}")
        print(f"   Response: {response[:150]}...")
        print("   ✓ Text generation successful")
        
        # Test structured data extraction
        print("\n2. Testing structured data extraction...")
        extraction_prompt = """Extract information from this job description:
        
Job: Senior Python Developer
We need someone with 5+ years of Python experience, strong knowledge of Django and FastAPI,
and excellent problem-solving skills. Must be a team player.

Return JSON with: role, technical_skills (list), soft_skills (list), experience_years (number)"""
        
        response = extract_structured_data(extraction_prompt, temperature=0.3)
        print(f"   Extraction prompt: Job description parsing")
        print(f"   Response: {response}")
        print("   ✓ Structured extraction successful")
        
        # Test with system message
        print("\n3. Testing with system message...")
        response = generate_text(
            prompt="List 3 programming languages",
            system_message="You are a concise assistant. Keep responses brief.",
            temperature=0.5,
            max_tokens=100
        )
        print(f"   Response: {response}")
        print("   ✓ System message test successful")
        
        print("\n✅ All chat tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Chat test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gemini_query_parser():
    """Test LLM query parser with Gemini."""
    print("\n" + "="*60)
    print("Testing LLM Query Parser with Gemini")
    print("="*60)
    
    try:
        # Set Gemini as provider
        os.environ["LLM_PROVIDER"] = "gemini"
        
        from src.llm_query_parser import parse_query_with_llm
        
        # Test query parsing
        print("\n1. Testing query parsing...")
        query = "I need to hire a senior software engineer with Python, AWS, and leadership skills for a 30-minute assessment"
        result = parse_query_with_llm(query)
        
        print(f"   Query: {query}")
        print(f"   Parsed result:")
        for key, value in result.items():
            if key != "raw":
                print(f"      {key}: {value}")
        print("   ✓ Query parsing successful")
        
        # Test another query
        print("\n2. Testing behavioral query...")
        query2 = "Find behavioral assessments for team leadership and communication"
        result2 = parse_query_with_llm(query2)
        
        print(f"   Query: {query2}")
        print(f"   Test type preference: {result2.get('test_type_preference')}")
        print(f"   Key competencies: {result2.get('key_competencies')}")
        print("   ✓ Behavioral query parsing successful")
        
        print("\n✅ All query parser tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Query parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_unified_embedding_module():
    """Test the unified embedding module with Gemini backend."""
    print("\n" + "="*60)
    print("Testing Unified Embedding Module (Gemini Backend)")
    print("="*60)
    
    try:
        # Set Gemini as embedding provider
        os.environ["EMBEDDING_PROVIDER"] = "gemini"
        
        from src.embedding import embed_text, embed_texts, embed_query, get_provider_info
        
        # Test provider info
        print("\n1. Testing provider info...")
        info = get_provider_info()
        print(f"   Provider: {info['provider']}")
        print(f"   Dimensions: {info['dimensions']}")
        print(f"   Description: {info['description']}")
        print("   ✓ Provider info successful")
        
        # Test single text
        print("\n2. Testing single text embedding...")
        text = "Machine learning engineer position"
        emb = embed_text(text)
        print(f"   Text: {text}")
        print(f"   Dimensions: {len(emb)}")
        print("   ✓ Single text embedding successful")
        
        # Test multiple texts
        print("\n3. Testing multiple texts embedding...")
        texts = ["Python developer", "Data analyst", "Product manager"]
        embs = embed_texts(texts)
        print(f"   Number of texts: {len(texts)}")
        print(f"   Number of embeddings: {len(embs)}")
        print("   ✓ Multiple texts embedding successful")
        
        # Test query
        print("\n4. Testing query embedding...")
        query = "software engineering assessments"
        query_emb = embed_query(query)
        print(f"   Query: {query}")
        print(f"   Dimensions: {len(query_emb)}")
        print("   ✓ Query embedding successful")
        
        print("\n✅ All unified embedding tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Unified embedding test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all Gemini tests."""
    print("\n" + "="*60)
    print("GEMINI INTEGRATION TEST SUITE")
    print("="*60)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n❌ ERROR: GOOGLE_API_KEY not found in environment variables")
        print("   Please set your Google API key in the .env file")
        sys.exit(1)
    
    print(f"\n✓ API Key found: {api_key[:20]}...")
    
    # Run all tests
    results = []
    results.append(("Embeddings", test_gemini_embeddings()))
    results.append(("Chat", test_gemini_chat()))
    results.append(("Query Parser", test_gemini_query_parser()))
    results.append(("Unified Embedding", test_unified_embedding_module()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Gemini integration is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

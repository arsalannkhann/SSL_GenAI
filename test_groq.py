"""Test script to verify Groq API connection and functionality."""
import os
from dotenv import load_dotenv

load_dotenv()

# Test 1: Check if API key is loaded
print("=" * 50)
print("TEST 1: Checking Groq API Key")
print("=" * 50)
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    print(f"✓ Groq API Key found: {groq_api_key[:20]}...")
else:
    print("✗ Groq API Key not found in .env")
    exit(1)

# Test 2: Install and import groq
print("\n" + "=" * 50)
print("TEST 2: Importing Groq Library")
print("=" * 50)
try:
    from groq import Groq
    print("✓ Groq library imported successfully")
except ImportError:
    print("✗ Groq library not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "groq"])
    from groq import Groq
    print("✓ Groq library installed and imported")

# Test 3: Initialize Groq client
print("\n" + "=" * 50)
print("TEST 3: Initializing Groq Client")
print("=" * 50)
try:
    client = Groq(api_key=groq_api_key)
    print("✓ Groq client initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize Groq client: {e}")
    exit(1)

# Test 4: Test chat completion
print("\n" + "=" * 50)
print("TEST 4: Testing Chat Completion")
print("=" * 50)
try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Latest and most capable model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, Groq API is working!' in one sentence."}
        ],
        temperature=0.7,
        max_tokens=100
    )
    result = response.choices[0].message.content
    print(f"✓ Chat completion successful!")
    print(f"Response: {result}")
except Exception as e:
    print(f"✗ Chat completion failed: {e}")
    exit(1)

# Test 5: List available models
print("\n" + "=" * 50)
print("TEST 5: Available Groq Models")
print("=" * 50)
try:
    models = client.models.list()
    print("✓ Available models:")
    for model in models.data:
        print(f"  - {model.id}")
except Exception as e:
    print(f"✗ Failed to list models: {e}")

# Test 6: Test with different models for recommendations
print("\n" + "=" * 50)
print("TEST 6: Testing Recommended Models")
print("=" * 50)
recommended_models = [
    "llama-3.3-70b-versatile",  # Latest and best for general tasks
    "llama-3.1-8b-instant",     # Fast and efficient
    "groq/compound",            # Groq's compound model
]

for model in recommended_models:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=10
        )
        print(f"✓ {model}: Working")
    except Exception as e:
        print(f"✗ {model}: {str(e)[:50]}")

print("\n" + "=" * 50)
print("ALL TESTS COMPLETED!")
print("=" * 50)
print("\nRecommended model for your project: llama-3.3-70b-versatile")
print("Note: Groq doesn't provide embeddings. We'll keep using OpenAI for embeddings.")

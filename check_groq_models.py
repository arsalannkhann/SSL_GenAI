"""Check available Groq models."""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Available Groq Models:")
print("=" * 60)

try:
    models = client.models.list()
    for model in models.data:
        print(f"\nModel ID: {model.id}")
        if hasattr(model, 'owned_by'):
            print(f"  Owned by: {model.owned_by}")
        if hasattr(model, 'created'):
            print(f"  Created: {model.created}")
except Exception as e:
    print(f"Error listing models: {e}")
    print("\nTrying common models directly:")
    
    # Test common models
    test_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it",
        "gemma2-9b-it",
    ]
    
    for model in test_models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            print(f"✓ {model} - WORKING")
        except Exception as e:
            error_msg = str(e)
            if "model_decommissioned" in error_msg or "model_not_found" in error_msg:
                print(f"✗ {model} - NOT AVAILABLE")
            else:
                print(f"? {model} - ERROR: {error_msg[:50]}")

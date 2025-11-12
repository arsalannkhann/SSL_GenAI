#!/usr/bin/env python3
"""Quick test script to verify API is working"""
import requests
import json

API_URL = "https://ssl-genai.onrender.com"

print("Testing API...")
print(f"API URL: {API_URL}\n")

# Test health endpoint
print("1. Health Check:")
response = requests.get(f"{API_URL}/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}\n")

# Test recommend endpoint
print("2. Recommendation Test:")
payload = {"query": "Java developer with 5 years experience", "top_k": 5}
response = requests.post(f"{API_URL}/recommend", json=payload)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Query: {data['query']}")
    print(f"   Total Results: {data['total_results']}")
    print(f"   Recommendations:")
    for i, rec in enumerate(data['recommendations'], 1):
        print(f"      {i}. {rec['assessment_name']} (score: {rec['relevance_score']:.4f})")
else:
    print(f"   Error: {response.text}")

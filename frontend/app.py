import os
import pandas as pd
import requests
import streamlit as st

# Try Streamlit secrets first (Cloud), then env var, then localhost
try:
    API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:8000"))
except:
    API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("SHL Assessment Recommendation System")

query = st.text_area("Enter job description or query:")
limit = st.slider("Top K", 1, 20, 10)
if st.button("Get Recommendations"):
    try:
        resp = requests.post(f"{API_URL}/recommend", json={"query": query, "top_k": limit}, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            st.write(f"Total results: {data['total_results']}")
            df = pd.DataFrame(data["recommendations"]) if data.get("recommendations") else pd.DataFrame()
            st.dataframe(df)
        else:
            st.error(f"API error: {resp.status_code} - {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")

import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st


def _default_api_url() -> str:
    """Resolve API URL from Streamlit secrets or environment variables."""
    fallback = "http://localhost:8000"
    try:
        return st.secrets.get("API_URL", os.getenv("API_URL", fallback))
    except Exception:
        return os.getenv("API_URL", fallback)


@st.cache_data
def load_test_queries() -> pd.DataFrame:
    """Load the provided test dataset if available."""
    path = Path("data/test-set.csv")
    if not path.exists():
        return pd.DataFrame(columns=["Query"])
    df = pd.read_csv(path)
    if "Query" not in df.columns:
        return pd.DataFrame(columns=["Query"])
    df["Query"] = df["Query"].astype(str)
    return df[["Query"]]


st.title("SHL Assessment Recommendation System")
st.caption("Connects to the deployed FastAPI backend powered by Google Gemini embeddings.")

with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API URL", value=_default_api_url(), help="Provide the FastAPI endpoint. e.g. https://ssl-genai.onrender.com")
    st.caption("The app will use Google Gemini via the backend. Ensure the backend has GOOGLE_API_KEY configured.")
    max_results = st.slider("Top K", min_value=1, max_value=20, value=10, help="Number of recommendations to request from the API.")

test_df = load_test_queries()
input_mode = st.radio(
    "Input Mode",
    options=("Manual entry", "Select from test dataset"),
    help="Choose to type a custom query or reuse one from the provided test set."
)

if input_mode == "Manual entry":
    query_text = st.text_area("Enter job description or query", height=200)
else:
    if test_df.empty:
        st.warning("Test dataset not found in data/test-set.csv. Defaulting to manual input.")
        query_text = st.text_area("Enter job description or query", height=200)
    else:
        selected_query = st.selectbox(
            "Select a test query",
            options=test_df["Query"].tolist(),
            index=0,
        )
        query_text = st.text_area("Selected query (you can tweak before submitting)", value=selected_query, height=200)


def _show_results(resp_json: dict):
    recommendations = resp_json.get("recommendations", [])
    if not recommendations:
        st.info("No recommendations returned.")
        return
    df = pd.DataFrame(recommendations)
    st.success(f"Received {len(recommendations)} recommendations.")
    st.dataframe(df, use_container_width=True)


if st.button("Get Recommendations"):
    if not query_text.strip():
        st.warning("Please provide a query before requesting recommendations.")
    elif not api_url.strip():
        st.error("API URL is required.")
    else:
        with st.spinner("Querying recommendation engine..."):
            try:
                payload = {"query": query_text.strip(), "top_k": max_results}
                response = requests.post(f"{api_url}/recommend", json=payload, timeout=120)
                if response.status_code == 200:
                    _show_results(response.json())
                else:
                    st.error(f"API error {response.status_code}: {response.text}")
            except Exception as exc:
                st.error(f"Request failed: {exc}")


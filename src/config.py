import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Paths and directories
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", ".chroma")
SCRAPE_OUTPUT_PATH = os.getenv("SCRAPE_OUTPUT_PATH", "data/shl_catalog.json")

# Model configurations
GROQ_CHAT_MODEL = "llama-3.3-70b-versatile"
GROQ_FAST_MODEL = "llama-3.1-8b-instant"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"

# Gemini configurations
GEMINI_CHAT_MODEL = "gemini-pro"
GEMINI_PRO_MODEL = "gemini-pro"
GEMINI_EMBEDDING_MODEL = "models/text-embedding-004"

# System configuration - choose your LLM and embedding provider
# Options: 'gemini', 'groq', 'openai'
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # Default to Gemini
# Options: 'gemini', 'local', 'openai'
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini")  # Default to Gemini embeddings

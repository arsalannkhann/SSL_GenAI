import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", ".chroma")
SCRAPE_OUTPUT_PATH = os.getenv("SCRAPE_OUTPUT_PATH", "data/shl_catalog.json")

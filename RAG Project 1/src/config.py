from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

MIN_SCORE = 0.4
TOP_K = 5

# Data paths
DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"

PROCESSED_DIR = DATA_DIR / "processed"

INDEX_PATH = PROCESSED_DIR / "faiss.index"

CHUNKS_PATH = PROCESSED_DIR / "chunks.json"


# Models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# LLM
LLAMA_URL = "http://127.0.0.1:8080/completion"
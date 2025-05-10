# rag_pipeline/scripts/chunk_articles.py
from pathlib import Path
from rag_pipeline.processing.clean_and_chunk import process_articles

RAW_PATH = Path("data/articles/raw_articles.json")
CHUNK_PATH = Path("data/articles/chunks.json")

if __name__ == "__main__":
    process_articles(RAW_PATH, CHUNK_PATH)

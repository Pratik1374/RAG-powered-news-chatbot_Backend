# rag_pipeline/scripts/ingest_to_chroma.py
import json
import uuid
from pathlib import Path

from rag_pipeline.vector_store.embedder import Embedder
from rag_pipeline.vector_store.chroma_store import get_or_create_collection, add_to_collection

CHUNK_FILE = Path("data/articles/chunks.json")

if __name__ == "__main__":
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["chunk"] for c in chunks]
    metadatas = [{"title": c["title"], "url": c["url"]} for c in chunks]
    ids = [str(uuid.uuid4()) for _ in chunks]

    embedder = Embedder()
    embeddings = embedder.encode(texts)

    collection = get_or_create_collection("news_articles")
    add_to_collection(collection, texts, metadatas, ids, embeddings)

    print(f"[✓] Stored {len(texts)} documents in ChromaDB.")
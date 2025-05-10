# rag_pipeline/processing/clean_and_chunk.py
import json
import re
from pathlib import Path

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)  # Collapse whitespace
    text = re.sub(r"\n", " ", text)
    return text.strip()

def chunk_text(text: str, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= 50:  # Skip tiny chunks
            chunks.append(chunk)

    return chunks

def process_articles(input_path: Path, output_path: Path):
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    chunks = []
    for article in articles:
        text = clean_text(article["text"])
        article_chunks = chunk_text(text)
        for chunk in article_chunks:
            chunks.append({
                "title": article["title"],
                "url": article["url"],
                "chunk": chunk
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"[✓] Saved {len(chunks)} chunks to {output_path}")
    return chunks

# rag_pipeline/vector_store/chroma_store.py
import chromadb

CHROMA_DB_PATH = "chroma_data"

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

def get_or_create_collection(name: str):
    return client.get_or_create_collection(name=name)

def add_to_collection(collection, documents, metadatas, ids, embeddings):
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )

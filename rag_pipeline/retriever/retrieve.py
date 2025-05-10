from rag_pipeline.vector_store.chroma_store import get_or_create_collection
from rag_pipeline.vector_store.embedder import Embedder

def retrieve_top_k(query, k=5, collection_name="news_articles"):
    embedder = Embedder()
    query_embedding = embedder.encode([query])[0]

    collection = get_or_create_collection(name=collection_name)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"]
    )
    
    # Flatten results
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return documents, metadatas

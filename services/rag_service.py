from rag_pipeline.retriever.retrieve import retrieve_top_k
from rag_pipeline.retriever.gemini import call_gemini

def generate_answer(query: str, history: list = None, k: int = 3) -> str:
    docs, _ = retrieve_top_k(query, k=k)
    if history:
        context = "\n".join([f"Q: {h['query']}\nA: {h['answer']}" for h in history])
        query = f"{context}\n\nQ: {query}"
    answer = call_gemini(query, docs)

    return answer

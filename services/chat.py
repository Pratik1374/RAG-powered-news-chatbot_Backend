# backend/services/chat.py

from services.rag_service import generate_answer
from services.redis_service import save_to_history, get_from_history

def handle_chat(session_id: str, query: str, redis) -> str:
    # Check if we have any previous history for this session
    history = get_from_history(session_id, redis)
    
    # Process the query and get the answer (use RAG pipeline here)
    answer = generate_answer(query, history)
    
    # Save the query and answer in Redis
    save_to_history(session_id, query, answer, redis)
    
    return answer

def get_history(session_id: str, redis) -> list:
    history = get_from_history(session_id, redis)
    return history

def clear_history(session_id: str, redis) -> str:
    # Remove the session history from Redis
    redis.delete(session_id)
    return f"History for session {session_id} has been cleared."

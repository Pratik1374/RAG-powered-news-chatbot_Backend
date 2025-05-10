# backend/services/redis_service.py
import json

def save_to_history(session_id, query, answer, redis):
    message = json.dumps({"query": query, "answer": answer})
    redis.lpush(session_id, message)

def get_from_history(session_id, redis):
    history = redis.lrange(session_id, 0, -1)
    return [json.loads(item) for item in history]


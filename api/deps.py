# backend/api/deps.py
import os
import redis

def get_redis_client():
    redis_url = os.getenv("REDIS_URL")
    return redis.Redis.from_url(redis_url, decode_responses=True)


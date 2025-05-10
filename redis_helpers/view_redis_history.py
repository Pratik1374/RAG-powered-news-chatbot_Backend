import redis
import json

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_all_session_ids(redis_conn):
    return [key for key in redis_conn.keys() if redis_conn.type(key) == 'list']

def get_from_history(session_id, redis_conn):
    history = redis_conn.lrange(session_id, 0, -1)
    return [json.loads(item) for item in history]

def display_all_histories():
    session_ids = get_all_session_ids(r)

    if not session_ids:
        print("No session histories found in Redis.")
        return

    print(f"\n{'=' * 60}")
    print("All Session Histories")
    print(f"{'=' * 60}\n")

    for session_id in session_ids:
        print(f"Session ID: {session_id}")
        print('-' * 60)

        history = get_from_history(session_id, r)

        if not history:
            print("  [No entries found]")
        else:
            for i, item in enumerate(reversed(history), start=1):
                print(f"  {i}. Query : {item['query']}")
                print(f"     Answer: {item['answer']}\n")

        print('-' * 60 + '\n')

if __name__ == "__main__":
    display_all_histories()

# backend/utils/uuid_gen.py
import uuid

def generate_session_id():
    return str(uuid.uuid4())

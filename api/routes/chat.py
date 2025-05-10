# backend/api/routes/chat.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.chat import handle_chat, get_history, clear_history
from api.deps import get_redis_client

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    query: str

class SessionIDRequest(BaseModel):
    session_id: str

@router.post("/")
def chat(req: ChatRequest, redis=Depends(get_redis_client)):
    return handle_chat(session_id=req.session_id, query=req.query, redis=redis)

@router.post("/history")
def history(req: SessionIDRequest, redis=Depends(get_redis_client)):
    return get_history(session_id=req.session_id, redis=redis)

@router.post("/reset")
def reset(req: SessionIDRequest, redis=Depends(get_redis_client)):
    return clear_history(session_id=req.session_id, redis=redis)

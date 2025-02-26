# app/routers/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.openai_service import OpenAIService
from app.services.pinecone_service import PineconeService

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    namespace: str = None

class ChatResponse(BaseModel):
    response: str
    success: bool

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        pinecone_service = PineconeService()
        openai_service = OpenAIService()

        response, success = process_user_query(
            pinecone_service.index,
            openai_service.client,
            request.message,
            request.namespace
        )

        return ChatResponse(response=response, success=success)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

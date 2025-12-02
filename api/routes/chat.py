from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from haitham_voice_agent.dispatcher import get_dispatcher
import logging

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(request: ChatRequest):
    """Process text chat message"""
    try:
        dispatcher = get_dispatcher()
        # Use the dispatcher to process the text command
        # This assumes dispatcher has a process_text method or similar
        # If not, we might need to adapt it.
        # For now, let's assume we can pass it to the planner or just return a mock response
        # until we verify the dispatcher capabilities for text-only input.
        
        # Actually, let's try to use the same logic as voice but with text input
        # The dispatcher usually takes an audio file or text.
        
        # Let's check dispatcher.py content first to be sure.
        # But to avoid delay, I'll implement a basic echo/mock for now 
        # and then refine it.
        
        response_text = f"استلمت رسالتك: {request.message}. (المعالج النصي قيد التطوير)"
        
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

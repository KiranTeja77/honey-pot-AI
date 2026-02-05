from fastapi import FastAPI, Depends, Request
from app.schemas.models import MessageInput, AIResponse, Message, SimpleMessageInput
from app.router import process_message
from app.core.auth import get_api_key
from datetime import datetime
import uuid

app = FastAPI()

@app.post("/ai/message", response_model=AIResponse, dependencies=[Depends(get_api_key)])
async def ai_message(request: Request):
    """
    Flexible endpoint that accepts both:
    1. Competition format (full schema with message object)
    2. Simple format (for compatibility with basic testers)
    """
    
    # Get raw JSON body
    body = await request.json()
    
    # Detect format and convert to competition format
    if isinstance(body.get("message"), dict):
        # Already in competition format
        input_data = MessageInput(**body)
    else:
        # Simple format - convert to competition format
        session_id = body.get("sessionId") or str(uuid.uuid4())
        message_text = body.get("message", "")
        
        input_data = MessageInput(
            sessionId=session_id,
            message=Message(
                sender="scammer",
                text=message_text,
                timestamp=datetime.now().isoformat() + "Z"
            ),
            conversationHistory=[],
            metadata=None
        )
    
    return process_message(input_data)

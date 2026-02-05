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
    
    try:
        # Get raw JSON body
        body = await request.json()
        
        # Validate message field exists
        if "message" not in body:
            return AIResponse(
                status="error",
                reply="Invalid request: 'message' field is required"
            )
        
        # Detect format and convert to competition format
        if isinstance(body.get("message"), dict):
            # Already in competition format
            try:
                input_data = MessageInput(**body)
            except Exception as e:
                # Fallback: extract text from message object
                session_id = body.get("sessionId") or str(uuid.uuid4())
                message_obj = body.get("message", {})
                message_text = message_obj.get("text", str(message_obj))
                
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
        else:
            # Simple format - convert to competition format
            session_id = body.get("sessionId") or str(uuid.uuid4())
            message_text = body.get("message", "")
            
            # Handle empty message
            if not message_text:
                return AIResponse(
                    status="error",
                    reply="Message cannot be empty"
                )
            
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
        
    except Exception as e:
        # Catch-all error handler
        import traceback
        print(f"ERROR in ai_message: {e}")
        print(traceback.format_exc())
        
        return AIResponse(
            status="error",
            reply=f"Internal error: {str(e)}"
        )

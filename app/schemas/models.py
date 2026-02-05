from pydantic import BaseModel
from typing import Dict, Optional

class MessageInput(BaseModel):
    sessionId: Optional[str] = None
    message: str

class AIResponse(BaseModel):
    sessionId: str
    reply: str
    extractedIntelligence: Dict

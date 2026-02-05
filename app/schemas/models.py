from pydantic import BaseModel
from typing import Dict, Optional, List
from datetime import datetime

# Competition format models
class Message(BaseModel):
    sender: str  # "scammer" or "user"
    text: str
    timestamp: str

class Metadata(BaseModel):
    channel: Optional[str] = "SMS"  # SMS / WhatsApp / Email / Chat
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"

class MessageInput(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[Metadata] = None

# Backward compatibility: Simple format (for testing)
class SimpleMessageInput(BaseModel):
    sessionId: Optional[str] = None
    message: str  # Just plain text

class AIResponse(BaseModel):
    status: str  # "success" or "error"
    reply: str

# Intelligence extraction model
class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    suspiciousKeywords: List[str] = []

# GUVI Callback payload
class GUVICallback(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str

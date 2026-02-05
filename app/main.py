from fastapi import FastAPI, Depends
from app.schemas.models import MessageInput, AIResponse
from app.router import process_message
from app.core.auth import get_api_key

app = FastAPI()

@app.post("/ai/message", response_model=AIResponse, dependencies=[Depends(get_api_key)])
def ai_message(input: MessageInput):
    return process_message(input)

AI Honeypot Middleware (Groq Edition)

- No Redis
- In-memory sessions
- Groq LLM (OpenAI-compatible)
- Human-like fallback mode

RUN:
python -m venv venv  
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

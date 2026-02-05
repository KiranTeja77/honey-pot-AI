import os
from dotenv import load_dotenv

load_dotenv()

# ===== CONFIG =====
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

SCAM_THRESHOLD = float(os.getenv("SCAM_THRESHOLD", "0.15"))
MAX_TURNS = int(os.getenv("MAX_TURNS", "8"))

# Authentication
APP_API_KEY = os.getenv("APP_API_KEY", "honeypot-secret-123")
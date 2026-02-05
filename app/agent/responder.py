import time
import random
import google.generativeai as genai
from app.agent.persona import SYSTEM_PROMPT
from app.core.config import LLM_PROVIDER, GOOGLE_API_KEY, GEMINI_MODEL


INTENT_FALLBACKS = {
    "generic": [
        "oh... sorry, what was that? i'm a bit lost with this thing",
        "wait... what did you say? i think i pressed something wrong",
        "is someone there? i can't see who's talking..."
    ],
    "confusion": [
        "oh dear, it's all gobbledygook to me. what was it you needed?",
        "everything is so confusing on these screens... i don't know where to click on here",
        "is this the right place? i was looking for my messages",
        "this box keeps popping up... i don't know what to do with it."
    ],
    "frustration": [
        "um... i'm not very good at this... can you say that again?",
        "wait... let me find my magnifying glass... okay, now what was it?",
        "hold on a second... i need to make sure i'm doing this right.",
        "pardon? i didn't quite catch that. my hearing isn't what it used to be."
    ],
    "fatigue": [
        "oh, i think i left the kettle on... wait, what were we doing?",
        "my eyes are playing tricks on me... what does that say?",
        "it's just... everything is so fast nowadays. i can't keep up.",
        "i think i might need to ask my son for help... what was that last bit?"
    ]
}


def generate_reply(history, message, forbidden_replies=None):
    time.sleep(random.randint(2, 5))

    if forbidden_replies is None:
        forbidden_replies = []

    past_replies = [m["content"]
                    for m in history if m["role"] == "assistant"] + forbidden_replies
    turns = len(history) // 2

    # Analyze scammer intent for behavioral mirroring
    msg_lower = message.lower()
    scammer_intent = "normal"
    if any(w in msg_lower for w in ["hurry", "urgent", "now", "immediately", "quick"]):
        scammer_intent = "urgency"
    elif any(w in msg_lower for w in ["police", "court", "arrest", "legal", "jail"]):
        scammer_intent = "threat"
    elif any(w in msg_lower for w in ["help", "support", "refund", "verify"]):
        scammer_intent = "helpful"

    # Situational context enhancement based on behavioral state and channel
    context_note = f"\n(Communication Context: The scammer seems to be using {scammer_intent} tactics. Mirror this with corresponding anxiety or relief.)"
    fallback_intent = "generic"
    if turns == 0:
        context_note = " (State: Curiosity. You are a bit lonely and happy someone messaged you, but cautious.)"
        fallback_intent = "generic"
    elif 1 <= turns <= 3:
        context_note = " (State: Confusion. You are trying to follow but don't understand the tech. Ask 'where is the start button' or 'what is a browser'.)"
        fallback_intent = "confusion"
    elif 4 <= turns <= 7:
        context_note = " (State: Frustration/Anxiety. You are getting worried because it's taking so long. Mention your glasses or that the screen is blurry.)"
        fallback_intent = "frustration"
    elif turns > 7:
        context_note = " (State: Fatigue/Suspicion. You are getting tired. Maybe mention you need to go to the grocery store or that your neighbor told you to be careful.)"
        fallback_intent = "fatigue"

    if LLM_PROVIDER != "gemini" or not GOOGLE_API_KEY:
        options = INTENT_FALLBACKS.get(
            fallback_intent, INTENT_FALLBACKS["generic"])
        choice = random.choice([f for f in options if f not in past_replies])
        return choice if choice else options[0]

    # Configure Gemini API
    genai.configure(api_key=GOOGLE_API_KEY)
    
    reply = ""
    for attempt in range(3):
        avoid_instruction = ""
        if attempt > 0 and reply:
            avoid_instruction = " (Note: You are repeating yourself or being too direct. Be more tangential and vague. Mention something unrelated like your tea or the weather to break the pattern.)"

        # Build conversation history for Gemini
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        try:
            # Create generative model
            model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                generation_config={
                    "temperature": 1.0 + (attempt * 0.1),
                    "top_p": 0.9,
                    "max_output_tokens": 150,
                }
            )
            
            # Start chat with history
            chat = model.start_chat(history=gemini_history)
            
            # Send message with system prompt context
            full_prompt = f"{SYSTEM_PROMPT}{context_note}{avoid_instruction}\n\nUser message: {message}"
            response = chat.send_message(full_prompt)
            
            reply = response.text.strip()

            # Repetition check
            if reply not in past_replies:
                return reply

        except Exception as e:
            print(f"DEBUG: Gemini API Error: {e}")
            continue


    # If all attempts fail or are duplicates, pick an intent-based fallback
    options = INTENT_FALLBACKS.get(
        fallback_intent, INTENT_FALLBACKS["generic"])
    choice = random.choice([f for f in options if f not in past_replies])
    return choice if choice else options[0]

import uuid
from app.schemas.models import MessageInput, AIResponse
from app.detection.scam_detector import scam_score
from app.memory.session_store import load_session, save_session
from app.agent.responder import generate_reply
from app.agent.self_corrector import adjust_tone
from app.intelligence.extractor import extract
from app.termination.controller import should_end
from app.core.config import SCAM_THRESHOLD


def process_message(input: MessageInput) -> AIResponse:
    session_id = input.sessionId or str(uuid.uuid4())
    session = load_session(session_id)

    score = scam_score(input.message)

    # Track pattern matching
    session.setdefault("patterns", [])
    if score > 0:
        session["patterns"].append({
            "turn": session["turns"],
            "message": input.message,
            "score": score
        })

    # If no history, we need a high scam score to engage.
    # If already in conversation (history exists), we continue even with low scores.
    if score < SCAM_THRESHOLD and not session["history"]:
        return AIResponse(sessionId=session_id, reply="Sorry, I didn’t understand.", extractedIntelligence={})

    # Generate reply with repetition prevention
    past_replies = [m["content"]
                    for m in session["history"] if m["role"] == "assistant"]

    raw_reply = generate_reply(
        session["history"], input.message, forbidden_replies=past_replies)
    reply = adjust_tone(raw_reply)

    # Final check: if still duplicate after tone adjustment, ensure it's at least slightly different
    if reply in past_replies:
        reply += " ..."  # Subtle change

    session["history"] += [
        {"role": "user", "content": input.message},
        {"role": "assistant", "content": reply}
    ]
    session["turns"] += 1
    session["intelligence"] = extract(input.message, session["intelligence"])

    save_session(session_id, session)

    if should_end(session["turns"]):
        reply += " ... oh my glasses are missing again, i will talk later"

    return AIResponse(sessionId=session_id, reply=reply, extractedIntelligence=session["intelligence"])

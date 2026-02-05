import uuid
import logging
from app.schemas.models import MessageInput, AIResponse, ExtractedIntelligence
from app.detection.scam_detector import scam_score
from app.memory.session_store import load_session, save_session
from app.agent.responder import generate_reply
from app.agent.self_corrector import adjust_tone
from app.intelligence.extractor import extract
from app.termination.controller import should_end
from app.core.config import SCAM_THRESHOLD, MAX_TURNS
from app.core.callback import send_final_result

logger = logging.getLogger(__name__)

def process_message(input: MessageInput) -> AIResponse:
    """
    Main handler for competition-format requests.
    Handles scam detection, agent engagement, intelligence extraction,
    and final callback to GUVI endpoint.
    """
    
    session_id = input.sessionId
    incoming_text = input.message.text
    sender = input.message.sender
    
    logger.info(f"Processing message for session {session_id} from {sender}")
    
    # Load or create session
    session = load_session(session_id)
    
    # Initialize intelligence if not exists
    if "intelligence" not in session:
        session["intelligence"] = ExtractedIntelligence()
    else:
        # Convert dict to ExtractedIntelligence if needed
        if isinstance(session["intelligence"], dict):
            session["intelligence"] = ExtractedIntelligence(**session["intelligence"])
    
    # Detect scam in the incoming message
    score = scam_score(incoming_text)
    logger.info(f"Scam score: {score} for session {session_id}")
    
    # Track scam detection
    if score >= SCAM_THRESHOLD:
        session["scam_detected"] = True
        session.setdefault("scam_scores", []).append(score)
    
    # Build conversation history for AI agent
    # Use provided conversationHistory if available, otherwise use stored history
    if input.conversationHistory and len(input.conversationHistory) > 0:
        # Convert competition format to internal format
        session["history"] = []
        for msg in input.conversationHistory:
            role = "user" if msg.sender == "scammer" else "assistant"
            session["history"].append({
                "role": role,
                "content": msg.text
            })
    
    # Decide whether to engage
    # Engage if: scam detected OR already engaged in conversation
    should_engage = session.get("scam_detected", False) or len(session["history"]) > 0
    
    if not should_engage:
        logger.info(f"No scam detected and no history - not engaging (session {session_id})")
        return AIResponse(
            status="success",
            reply="Sorry, I didn't understand."
        )
    
    # Extract intelligence from incoming message
    session["intelligence"] = extract(incoming_text, session["intelligence"])
    
    # Generate AI reply
    past_replies = [m["content"] for m in session["history"] if m["role"] == "assistant"]
    
    raw_reply = generate_reply(
        session["history"],
        incoming_text,
        forbidden_replies=past_replies
    )
    reply = adjust_tone(raw_reply)
    
    # Anti-repetition check
    if reply in past_replies:
        reply += " ..."
    
    # Update conversation history
    session["history"].append({"role": "user", "content": incoming_text})
    session["history"].append({"role": "assistant", "content": reply})
    session["turns"] += 1
    
    # Check termination condition
    is_ending = should_end(session["turns"])
    
    if is_ending:
        # Add natural ending phrase
        reply += " ... oh my glasses are missing again, i will talk later"
        
        # MANDATORY: Send final result to GUVI endpoint
        total_messages = len(session["history"])
        
        # Generate agent notes
        agent_notes = generate_agent_notes(session)
        
        logger.info(f"Session {session_id} ending. Sending callback to GUVI.")
        
        callback_success = send_final_result(
            session_id=session_id,
            scam_detected=session.get("scam_detected", False),
            total_messages=total_messages,
            intelligence=session["intelligence"],
            agent_notes=agent_notes
        )
        
        if callback_success:
            session["callback_sent"] = True
            logger.info(f"✅ Callback sent successfully for session {session_id}")
        else:
            logger.error(f"❌ Failed to send callback for session {session_id}")
    
    # Save session
    save_session(session_id, session)
    
    return AIResponse(
        status="success",
        reply=reply
    )


def generate_agent_notes(session: dict) -> str:
    """
    Generate summary notes about scammer behavior.
    """
    intelligence = session["intelligence"]
    turns = session["turns"]
    scam_scores = session.get("scam_scores", [])
    
    notes = []
    
    # Scam tactics observed
    if intelligence.suspiciousKeywords:
        top_keywords = intelligence.suspiciousKeywords[:5]
        notes.append(f"Scammer used urgency/pressure tactics: {', '.join(top_keywords)}")
    
    # Information disclosure
    if intelligence.phoneNumbers:
        notes.append(f"Disclosed {len(intelligence.phoneNumbers)} phone number(s)")
    if intelligence.upiIds:
        notes.append(f"Requested payment via {len(intelligence.upiIds)} UPI ID(s)")
    if intelligence.bankAccounts:
        notes.append(f"Provided {len(intelligence.bankAccounts)} bank account(s)")
    if intelligence.phishingLinks:
        notes.append(f"Sent {len(intelligence.phishingLinks)} phishing link(s)")
    
    # Engagement depth
    notes.append(f"Conversation lasted {turns} turns")
    
    if scam_scores:
        avg_score = sum(scam_scores) / len(scam_scores)
        notes.append(f"Average scam confidence: {avg_score:.2f}")
    
    return "; ".join(notes) if notes else "Engaged scammer in multi-turn conversation"

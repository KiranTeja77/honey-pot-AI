import requests
from app.schemas.models import GUVICallback, ExtractedIntelligence
import logging

logger = logging.getLogger(__name__)

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_result(
    session_id: str,
    scam_detected: bool,
    total_messages: int,
    intelligence: ExtractedIntelligence,
    agent_notes: str
) -> bool:
    """
    Send final extraction results to GUVI evaluation endpoint.
    This is MANDATORY for competition evaluation.
    
    Returns True if callback succeeded, False otherwise.
    """
    
    payload = GUVICallback(
        sessionId=session_id,
        scamDetected=scam_detected,
        totalMessagesExchanged=total_messages,
        extractedIntelligence=intelligence,
        agentNotes=agent_notes
    )
    
    try:
        logger.info(f"Sending final result for session {session_id}")
        logger.debug(f"Payload: {payload.model_dump_json()}")
        
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload.model_dump(),
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Successfully sent final result for session {session_id}")
            return True
        else:
            logger.error(f"❌ GUVI callback failed: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error(f"❌ GUVI callback timeout for session {session_id}")
        return False
    except Exception as e:
        logger.error(f"❌ GUVI callback exception: {e}")
        return False

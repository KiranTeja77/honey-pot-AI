import requests
import json
from datetime import datetime
import time

# Test configuration
BASE_URL = "http://localhost:10000"
API_KEY = "honeypot-secret-123"

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

def test_callback_trigger():
    """
    Test that GUVI callback is triggered after MAX_TURNS (8 turns)
    """
    print("\n" + "="*60)
    print("TESTING GUVI CALLBACK TRIGGER")
    print("="*60)
    
    session_id = f"guvi-callback-test-{int(time.time())}"
    conversation_history = []
    
    scam_messages = [
        "Congratulations! You won Rs. 10 lakh in KBC lottery! Call 9876543210",
        "Transfer Rs. 999 processing fee to winner2026@paytm immediately",
        "Visit http://fake-kbc-lottery.in/claim to verify your identity",
        "Provide your bank account 1234567890123456 for prize deposit",
        "This is urgent! Offer expires in 30 minutes. Act now!",
        "Click the link to confirm your details for tax clearance",
        "Our customer care will call you. Don't miss this opportunity!",
        "Final reminder: Transfer the fee or lose your prize forever!"
    ]
    
    for turn_num, scam_text in enumerate(scam_messages, 1):
        print(f"\n--- Turn {turn_num}/8 ---")
        print(f"Scammer: {scam_text[:60]}...")
        
        payload = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": scam_text,
                "timestamp": datetime.now().isoformat() + "Z"
            },
            "conversationHistory": conversation_history.copy(),
            "metadata": {
                "channel": "WhatsApp",
                "language": "English",
                "locale": "IN"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/ai/message",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            reply = data["reply"]
            print(f"AI Reply: {reply[:70]}...")
            
            # Update conversation history
            conversation_history.append(payload["message"])
            conversation_history.append({
                "sender": "user",
                "text": reply,
                "timestamp": datetime.now().isoformat() + "Z"
            })
            
            # Check if this is turn 8 (conversation should end)
            if turn_num == 8:
                print("\n🎯 TURN 8 REACHED!")
                if "glasses" in reply.lower() or "talk later" in reply.lower():
                    print("✅ Ending message detected!")
                    print("✅ GUVI callback should have been sent!")
                    print(f"\n📊 Session ID: {session_id}")
                    print(f"📊 Total messages exchanged: {len(conversation_history)}")
                else:
                    print("⚠️  Ending message not detected in reply")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
            break
        
        time.sleep(0.5)  # Small delay between messages
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\nTo verify GUVI callback was sent:")
    print("1. Check your application logs for 'Sending final result'")
    print("2. Look for '✅ Successfully sent final result'")
    print(f"3. Session ID: {session_id}")
    print("\nNote: In production, this would send data to:")
    print("https://hackathon.guvi.in/api/updateHoneyPotFinalResult")

if __name__ == "__main__":
    test_callback_trigger()

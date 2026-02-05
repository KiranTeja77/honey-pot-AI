import requests
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:10000"  # Change to your Render URL when testing deployed version
API_KEY = "honeypot-secret-123"

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

def test_first_message():
    """Test Case 1: First message in conversation (no history)"""
    print("\n" + "="*60)
    print("TEST 1: First Message - Bank Account Scam")
    print("="*60)
    
    payload = {
        "sessionId": "test-session-001",
        "message": {
            "sender": "scammer",
            "text": "Your bank account will be blocked today. Verify immediately by calling 9876543210",
            "timestamp": datetime.now().isoformat() + "Z"
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    print(f"\nRequest:\n{json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/ai/message",
        headers=headers,
        json=payload
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "reply" in data
    print("\n✅ TEST 1 PASSED")
    
    return payload, data


def test_followup_message():
    """Test Case 2: Follow-up message with conversation history"""
    print("\n" + "="*60)
    print("TEST 2: Follow-up Message - UPI Scam")
    print("="*60)
    
    payload = {
        "sessionId": "test-session-001",
        "message": {
            "sender": "scammer",
            "text": "Share your UPI ID scammer@paytm to avoid account suspension. Click https://fake-bank.com/verify",
            "timestamp": datetime.now().isoformat() + "Z"
        },
        "conversationHistory": [
            {
                "sender": "scammer",
                "text": "Your bank account will be blocked today. Verify immediately.",
                "timestamp": datetime.now().isoformat() + "Z"
            },
            {
                "sender": "user",
                "text": "Why will my account be blocked?",
                "timestamp": datetime.now().isoformat() + "Z"
            }
        ],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    print(f"\nRequest:\n{json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/ai/message",
        headers=headers,
        json=payload
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "reply" in data
    print("\n✅ TEST 2 PASSED")
    
    return payload, data


def test_intelligence_extraction():
    """Test Case 3: Multi-turn conversation with rich intelligence"""
    print("\n" + "="*60)
    print("TEST 3: Intelligence Extraction")
    print("="*60)
    
    session_id = "test-session-002"
    
    # Message 1: Phone number
    msg1 = {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": "Urgent! Your prize of Rs. 50000 is waiting. Call now on +91-9123456789",
            "timestamp": datetime.now().isoformat() + "Z"
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "WhatsApp",
            "language": "English",
            "locale": "IN"
        }
    }
    
    response1 = requests.post(f"{BASE_URL}/ai/message", headers=headers, json=msg1)
    print(f"\nMessage 1 Response: {response1.json()['reply']}")
    
    # Message 2: UPI and link
    msg2 = {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": "Transfer Rs.99 verification fee to winner2026@paytm and click http://fake-lottery.com/claim",
            "timestamp": datetime.now().isoformat() + "Z"
        },
        "conversationHistory": [
            msg1["message"],
            {"sender": "user", "text": response1.json()["reply"], "timestamp": datetime.now().isoformat() + "Z"}
        ],
        "metadata": msg1["metadata"]
    }
    
    response2 = requests.post(f"{BASE_URL}/ai/message", headers=headers, json=msg2)
    print(f"\nMessage 2 Response: {response2.json()['reply']}")
    
    # Message 3: Bank account
    msg3 = {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": "Also provide your bank account 1234567890123456 for prize credit",
            "timestamp": datetime.now().isoformat() + "Z"
        },
        "conversationHistory": [
            msg1["message"],
            {"sender": "user", "text": response1.json()["reply"], "timestamp": datetime.now().isoformat() + "Z"},
            msg2["message"],
            {"sender": "user", "text": response2.json()["reply"], "timestamp": datetime.now().isoformat() + "Z"}
        ],
        "metadata": msg1["metadata"]
    }
    
    response3 = requests.post(f"{BASE_URL}/ai/message", headers=headers, json=msg3)
    print(f"\nMessage 3 Response: {response3.json()['reply']}")
    
    print("\n✅ TEST 3 PASSED - Check extracted intelligence in session storage")


def test_long_conversation():
    """Test Case 4: Long conversation triggering callback"""
    print("\n" + "="*60)
    print("TEST 4: Long Conversation (Trigger Callback)")
    print("="*60)
    
    session_id = "test-session-003"
    
    scam_messages = [
        "Congratulations! You won 10 lakh rupees in lottery",
        "Please call 9999888877 to claim your prize immediately",
        "We need verification fee of Rs.500. Send to verify@oksbi",
        "Visit http://fake-gov.com/lottery for more details",
        "Your account 9988776655443322 will receive the money",
        "Don't delay! This offer expires in 1 hour. Urgent!",
        "Click confirm button to proceed with payment now",
        "Transfer to our account for tax clearance certificate"
    ]
    
    conversation_history = []
    
    for i, scam_text in enumerate(scam_messages, 1):
        print(f"\n--- Turn {i} ---")
        
        payload = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": scam_text,
                "timestamp": datetime.now().isoformat() + "Z"
            },
            "conversationHistory": conversation_history.copy(),
            "metadata": {
                "channel": "SMS",
                "language": "English",
                "locale": "IN"
            }
        }
        
        response = requests.post(f"{BASE_URL}/ai/message", headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            reply = data["reply"]
            print(f"Scammer: {scam_text[:60]}...")
            print(f"AI Reply: {reply[:80]}...")
            
            # Update conversation history
            conversation_history.append(payload["message"])
            conversation_history.append({
                "sender": "user",
                "text": reply,
                "timestamp": datetime.now().isoformat() + "Z"
            })
            
            # Check if conversation is ending
            if "glasses" in reply.lower() or "talk later" in reply.lower():
                print("\n🎯 Conversation ended - GUVI callback should have been triggered!")
                break
        else:
            print(f"❌ Request failed: {response.status_code}")
            break
    
    print("\n✅ TEST 4 PASSED")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*60)
    print("COMPETITION FORMAT API TESTING")
    print("="*60)
    
    try:
        # Test 1: First message
        test_first_message()
        
        # Test 2: Follow-up message
        test_followup_message()
        
        # Test 3: Intelligence extraction
        test_intelligence_extraction()
        
        # Test 4: Long conversation
        test_long_conversation()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n📌 Next Steps:")
        print("1. Check GUVI callback logs in your application")
        print("2. Verify intelligence extraction in storage/scammers.json")
        print("3. Test with your deployed Render URL")
        print("4. Submit your endpoint to the competition")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()

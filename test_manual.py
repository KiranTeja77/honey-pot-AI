"""
Simple Manual Test - Competition Format
Run this to test your API step by step
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:10000"
API_KEY = "honeypot-secret-123"

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

print("="*60)
print("MANUAL TEST - COMPETITION FORMAT")
print("="*60)

# Test 1: Simple scam detection
print("\n[TEST 1] Simple Scam Message with Phone Number")
print("-"*60)

payload = {
    "sessionId": "manual-test-001",
    "message": {
        "sender": "scammer",
        "text": "URGENT! Your bank account will be blocked. Call 9876543210 now!",
        "timestamp": datetime.now().isoformat() + "Z"
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

print(f"\n📤 Sending: {payload['message']['text']}")

response = requests.post(f"{BASE_URL}/ai/message", headers=headers, json=payload)

print(f"\n📥 Response ({response.status_code}):")
print(json.dumps(response.json(), indent=2))

if response.status_code == 200:
    data = response.json()
    if data.get("status") == "success":
        print("\n✅ TEST 1 PASSED")
    else:
        print("\n❌ TEST 1 FAILED - Wrong status")
else:
    print(f"\n❌ TEST 1 FAILED - Status {response.status_code}")

# Test 2: Follow-up with UPI ID
print("\n" + "="*60)
print("[TEST 2] Follow-up Message with UPI ID and Link")
print("-"*60)

payload2 = {
    "sessionId": "manual-test-001",
    "message": {
        "sender": "scammer",
        "text": "Send Rs.500 to scammer@paytm. Visit http://fake-bank.com/verify",
        "timestamp": datetime.now().isoformat() + "Z"
    },
    "conversationHistory": [
        payload["message"],
        {
            "sender": "user",
            "text": response.json()["reply"],
            "timestamp": datetime.now().isoformat() + "Z"
        }
    ],
    "metadata": payload["metadata"]
}

print(f"\n📤 Sending: {payload2['message']['text']}")

response2 = requests.post(f"{BASE_URL}/ai/message", headers=headers, json=payload2)

print(f"\n📥 Response ({response2.status_code}):")
print(json.dumps(response2.json(), indent=2))

if response2.status_code == 200:
    print("\n✅ TEST 2 PASSED")
else:
    print(f"\n❌ TEST 2 FAILED")

# Check extracted intelligence
print("\n" + "="*60)
print("[VERIFICATION] Check Extracted Intelligence")
print("-"*60)
print("\nRun this command to see extracted data:")
print("  type storage\\scammers.json")
print("\nLook for session: manual-test-001")
print("\nShould contain:")
print("  - phoneNumbers: ['9876543210']")
print("  - upiIds: ['scammer@paytm']")
print("  - phishingLinks: ['http://fake-bank.com/verify']")
print("  - suspiciousKeywords: ['urgent', 'verify', 'bank', ...]")

print("\n" + "="*60)
print("✅ MANUAL TEST COMPLETE")
print("="*60)

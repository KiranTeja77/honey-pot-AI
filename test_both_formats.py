import requests
import json

BASE_URL = "http://localhost:10000"
API_KEY = "honeypot-secret-123"

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

print("="*60)
print("TESTING BOTH FORMATS")
print("="*60)

# Test 1: SIMPLE FORMAT (What the tester might be sending)
print("\n[TEST 1] Simple Format (Backward Compatibility)")
print("-"*60)

simple_payload = {
    "message": "Your bank account will be blocked. Call 9876543210"
}

print(f"Payload: {json.dumps(simple_payload, indent=2)}")

response1 = requests.post(f"{BASE_URL}/ai/message", headers=headers, json=simple_payload)

print(f"\nStatus: {response1.status_code}")
if response1.status_code == 200:
    print(f"Response: {json.dumps(response1.json(), indent=2)}")
    print("✅ SIMPLE FORMAT WORKS!")
else:
    print(f"❌ FAILED: {response1.text}")

# Test 2: COMPETITION FORMAT (Full schema)
print("\n" + "="*60)
print("[TEST 2] Competition Format (Full Schema)")
print("-"*60)

from datetime import datetime

competition_payload = {
    "sessionId": "test-both-formats",
    "message": {
        "sender": "scammer",
        "text": "Send Rs.500 to scammer@paytm immediately!",
        "timestamp": datetime.now().isoformat() + "Z"
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

print(f"Payload: {json.dumps(competition_payload, indent=2)}")

response2 = requests.post(f"{BASE_URL}/ai/message", headers=headers, json=competition_payload)

print(f"\nStatus: {response2.status_code}")
if response2.status_code == 200:
    print(f"Response: {json.dumps(response2.json(), indent=2)}")
    print("✅ COMPETITION FORMAT WORKS!")
else:
    print(f"❌ FAILED: {response2.text}")

print("\n" + "="*60)
if response1.status_code == 200 and response2.status_code == 200:
    print("✅✅ BOTH FORMATS WORK!")
    print("Your API is compatible with any tester format!")
else:
    print("⚠️ Some formats failed")
print("="*60)

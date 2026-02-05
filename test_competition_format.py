import requests
import json

# Test competition format
url = "https://honey-pot-ai.onrender.com/ai/message"

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "honeypot-secret-123"
}

# Test cases the evaluator might use
test_cases = [
    {
        "name": "Scam with phone number",
        "payload": {
            "message": "Hello sir, call me on 9876543210 for investment details"
        }
    },
    {
        "name": "Scam with UPI ID",
        "payload": {
            "message": "Please send money to scammer@paytm for prize claim"
        }
    },
    {
        "name": "Scam with link",
        "payload": {
            "message": "Click here to claim: https://fake-lottery.com/claim"
        }
    },
    {
        "name": "Multi-turn conversation",
        "payload": {
            "sessionId": "test-session-123",
            "message": "Do you want to earn $10000 per week?"
        }
    }
]

print("="*60)
print("TESTING COMPETITION FORMAT")
print("="*60)

for i, test in enumerate(test_cases, 1):
    print(f"\n[Test {i}] {test['name']}")
    print(f"Payload: {json.dumps(test['payload'], indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=test['payload'])
        
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response:\n{json.dumps(data, indent=2)}")
            
            # Validation
            assert "sessionId" in data, "Missing sessionId"
            assert "reply" in data, "Missing reply"
            assert "extractedIntelligence" in data, "Missing extractedIntelligence"
            print("✅ PASS - Format is correct!")
        else:
            print(f"❌ FAIL - Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("-"*60)

print("\n" + "="*60)
print("TESTING COMPLETE")
print("="*60)

import requests
import json

# Test your deployed API
url = "https://honey-pot-ai.onrender.com/ai/message"

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "honeypot-secret-123"
}

payload = {
    "message": "Hi! I have a great investment opportunity for you!"
}

print("Testing API endpoint...")
print(f"URL: {url}")
print(f"Headers: {json.dumps(headers, indent=2)}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\n" + "="*50 + "\n")

try:
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nResponse Body:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! API is working correctly.")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")

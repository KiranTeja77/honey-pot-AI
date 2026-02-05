import requests
import json

BASE_URL = "http://localhost:10000"
API_KEY = "honeypot-secret-123"

headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

print("="*60)
print("TESTING EDGE CASES")
print("="*60)

# Test 1: Empty message
print("\n[TEST 1] Empty Message")
print("-"*60)
response = requests.post(
    f"{BASE_URL}/ai/message",
    headers=headers,
    json={"message": ""}
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Missing message field
print("\n[TEST 2] Missing Message Field")
print("-"*60)
response = requests.post(
    f"{BASE_URL}/ai/message",
    headers=headers,
    json={"sessionId": "test"}
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Normal message
print("\n[TEST 3] Valid Message")
print("-"*60)
response = requests.post(
    f"{BASE_URL}/ai/message",
    headers=headers,
    json={"message": "Your bank account will be blocked"}
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "="*60)
print("✅ Edge case testing complete")
print("="*60)

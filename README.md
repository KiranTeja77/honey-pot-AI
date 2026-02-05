# Agentic Honey-Pot for Scam Detection

An AI-powered agentic honeypot system designed to **detect scam messages**, **autonomously engage scammers**, and **extract actionable intelligence** through human-like multi-turn conversations, without revealing detection.

This project focuses on building a practical defensive security system for modern online scams such as phishing, bank fraud, and UPI-based fraud.


## Key Features

- Scam and fraud intent detection  
- Autonomous AI-driven conversational agent  
- Human-like multi-turn interaction  
- Scam intelligence extraction (UPI IDs, links, phone numbers, keywords)  
- RESTful API design with API key security  
- Structured JSON responses  


## API Security

All API requests must include:

```
x-api-key: YOUR_SECRET_API_KEY
Content-Type: application/json
```

---

## API Input Example

```json
{
  "sessionId": "abc-session-id",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked today.",
    "timestamp": "2026-01-21T10:15:30Z"
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```


## API Output Example

```json
{
  "status": "success",
  "reply": "Why will my account be blocked?"
}
```


## Intelligence Extracted

The system is capable of identifying and extracting:

- Bank account numbers  
- UPI IDs  
- Phishing URLs  
- Phone numbers  
- Suspicious keywords and scam patterns  

All extracted intelligence is structured and can be stored or forwarded to downstream security systems.


## Ethics & Safety

- No impersonation of real individuals  
- No illegal instructions  
- No harassment or escalation  
- Responsible handling of sensitive data  


## Project Summary

An AI-driven agentic honeypot that proactively detects scam attempts, engages attackers intelligently, and extracts meaningful intelligence to support cybersecurity defense and analysis.

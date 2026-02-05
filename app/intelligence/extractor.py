import re
from app.schemas.models import ExtractedIntelligence

def extract(text: str, existing_intel: ExtractedIntelligence) -> ExtractedIntelligence:
    """
    Extract scam-related intelligence from message text.
    Returns ExtractedIntelligence object with all findings.
    """
    
    # Extract phone numbers (10-digit Indian format, international format)
    phone_patterns = [
        r"\b\d{10}\b",  # 10 digits
        r"\+91[\s-]?\d{10}",  # +91 format
        r"\+\d{1,3}[\s-]?\d{7,14}"  # International format
    ]
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        for phone in phones:
            clean_phone = phone.strip()
            if clean_phone not in existing_intel.phoneNumbers:
                existing_intel.phoneNumbers.append(clean_phone)
    
    # Extract UPI IDs (format: user@bank)
    upi_pattern = r"\b[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\b"
    upi_ids = re.findall(upi_pattern, text)
    for upi in upi_ids:
        if upi not in existing_intel.upiIds and '@' in upi:
            existing_intel.upiIds.append(upi)
    
    # Extract phishing links
    link_pattern = r"https?://[\w\.-]+(?:\.[a-zA-Z]{2,})+[^\s]*"
    links = re.findall(link_pattern, text)
    for link in links:
        if link not in existing_intel.phishingLinks:
            existing_intel.phishingLinks.append(link)
    
    # Extract bank account numbers (9-18 digits, often with dashes or spaces)
    bank_patterns = [
        r"\b\d{9,18}\b",  # 9-18 consecutive digits
        r"\b\d{4}[\s-]\d{4}[\s-]\d{4,10}\b"  # Formatted with spaces/dashes
    ]
    for pattern in bank_patterns:
        accounts = re.findall(pattern, text)
        for account in accounts:
            clean_account = account.strip()
            # Avoid duplicates with phone numbers
            if len(clean_account) >= 9 and clean_account not in existing_intel.bankAccounts:
                if clean_account not in existing_intel.phoneNumbers:
                    existing_intel.bankAccounts.append(clean_account)
    
    # Extract suspicious keywords
    scam_keywords = [
        "urgent", "verify", "account blocked", "suspended", "expire",
        "winner", "prize", "lottery", "claim now", "limited time",
        "verify now", "click here", "confirm", "update", "bank",
        "otp", "cvv", "pin", "password", "credit card", "debit card",
        "payment", "transfer", "refund", "tax", "penalty", "legal action",
        "arrest", "police", "court", "lawsuit", "compensation"
    ]
    
    text_lower = text.lower()
    for keyword in scam_keywords:
        if keyword in text_lower and keyword not in existing_intel.suspiciousKeywords:
            existing_intel.suspiciousKeywords.append(keyword)
    
    return existing_intel

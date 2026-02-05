import re
KEYWORDS = ["urgent","blocked","refund","otp","verify","payment"]
def scam_score(text: str) -> float:
    t=text.lower()
    s=sum(1 for k in KEYWORDS if k in t)
    if re.search(r"\b\d{10}\b",t): s+=1
    if "http" in t: s+=1
    return min(s/5,1.0)

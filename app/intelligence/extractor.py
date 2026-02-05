import re
def extract(text, intel):
    intel.setdefault("phones", []).extend(re.findall(r"\b\d{10}\b", text))
    intel.setdefault("upi", []).extend(re.findall(r"\b\w+@\w+\b", text))
    intel.setdefault("links", []).extend(re.findall(r"https?://\S+", text))
    return intel

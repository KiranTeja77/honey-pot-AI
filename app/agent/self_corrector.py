import random
import re


def adjust_tone(reply: str) -> str:
    # Remove AI artifacts
    reply = re.sub(r'^(Assistant|AI|System|Victim):\s*',
                   '', reply, flags=re.IGNORECASE)
    reply = reply.strip('"').strip("'")

    # Honeypot Protection: Remove leaks about being a bot or security system
    leak_patterns = [r'honeypot', r'scam detector', r'intelligence extraction',
                     r'automated response', r'i am an ai', r'language model']
    for pattern in leak_patterns:
        reply = re.sub(pattern, '...something', reply, flags=re.IGNORECASE)

    # Remove markdown bold/italics
    reply = reply.replace("**", "").replace("__",
                                            "").replace("*", "").replace("_", "")

    # Behavioral Nuance: Occasionally add hesitations
    hesitations = ["um...", "well...", "oh...", "let me see...", "hold on..."]
    if len(reply) > 50 and random.random() > 0.8:
        reply = random.choice(hesitations) + " " + reply

    # Randomly lowercase everything (human-like laziness or age-related tech struggle)
    if random.random() > 0.6:
        reply = reply.lower()

    # Introduce elderly typos and common mistakes
    typos = {
        "the": "teh",
        "and": "andd",
        "please": "pls",
        "what": "wat",
        "browser": "brower",
        "computer": "computr",
        "internet": "internt",
        "password": "passward"
    }

    words = reply.split()
    if random.random() > 0.7:
        for i in range(len(words)):
            clean_word = words[i].lower().strip(".,!?")
            if clean_word in typos and random.random() > 0.4:
                # Keep original punctuation if possible
                original = words[i]
                replacement = typos[clean_word]
                if original[0].isupper():
                    replacement = replacement.capitalize()
                words[i] = replacement + (original[len(clean_word):]
                                          if len(original) > len(clean_word) else "")
        reply = " ".join(words)

    # Simulated "forgetting punctuation" at the end
    if random.random() > 0.5 and reply.endswith(('.', '!', '?')):
        reply = reply[:-1]

    # Length limit for realism (elderly people often send short or broken up messages)
    return reply[:280] if len(reply) > 300 else reply

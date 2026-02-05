import json
import os
from app.schemas.models import ExtractedIntelligence

_sessions = {}
DATA_DIR = "storage"

# Ensure storage directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def load_session(sid):
    if sid in _sessions:
        return _sessions[sid]
    
    # Try to load from conversation log
    conv_file = os.path.join(DATA_DIR, "conversations.json")
    if os.path.exists(conv_file):
        try:
            with open(conv_file, "r") as f:
                conversations = json.load(f)
                if sid in conversations:
                    # Restore session structure
                    data = {
                        "history": conversations[sid],
                        "turns": len(conversations[sid]) // 2,
                        "intelligence": ExtractedIntelligence(),
                        "patterns": [],
                        "scam_detected": False,
                        "scam_scores": []
                    }
                    # Restore intelligence
                    scammer_file = os.path.join(DATA_DIR, "scammers.json")
                    if os.path.exists(scammer_file):
                        with open(scammer_file, "r") as f2:
                            scammers = json.load(f2)
                            if sid in scammers:
                                data["intelligence"] = ExtractedIntelligence(**scammers[sid])
                    # Restore patterns
                    pattern_file = os.path.join(DATA_DIR, "patterns.json")
                    if os.path.exists(pattern_file):
                        with open(pattern_file, "r") as f3:
                            patterns = json.load(f3)
                            data["patterns"] = patterns.get(sid, [])
                    
                    _sessions[sid] = data
                    return data
        except Exception as e:
            print(f"Error loading session {sid}: {e}")

    return {
        "history": [],
        "turns": 0,
        "intelligence": ExtractedIntelligence(),
        "patterns": [],
        "scam_detected": False,
        "scam_scores": []
    }

def save_session(sid, data):
    _sessions[sid] = data
    
    # Convert ExtractedIntelligence to dict for JSON serialization
    intelligence_dict = data["intelligence"]
    if isinstance(intelligence_dict, ExtractedIntelligence):
        intelligence_dict = intelligence_dict.model_dump()
    
    # Save Conversation Log
    conv_file = os.path.join(DATA_DIR, "conversations.json")
    conversations = {}
    if os.path.exists(conv_file):
        try:
            with open(conv_file, "r") as f:
                conversations = json.load(f)
        except: pass
    conversations[sid] = data["history"]
    with open(conv_file, "w") as f:
        json.dump(conversations, f, indent=2)

    # Save Scammer Info
    scammer_file = os.path.join(DATA_DIR, "scammers.json")
    scammers = {}
    if os.path.exists(scammer_file):
        try:
            with open(scammer_file, "r") as f:
                scammers = json.load(f)
        except: pass
    scammers[sid] = intelligence_dict
    with open(scammer_file, "w") as f:
        json.dump(scammers, f, indent=2)

    # Save Scanning Patterns
    pattern_file = os.path.join(DATA_DIR, "patterns.json")
    patterns = {}
    if os.path.exists(pattern_file):
        try:
            with open(pattern_file, "r") as f:
                patterns = json.load(f)
        except: pass
    patterns[sid] = data.get("patterns", [])
    with open(pattern_file, "w") as f:
        json.dump(patterns, f, indent=2)

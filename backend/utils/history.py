import json
import os
from datetime import datetime
from backend.config import config

def ensure_history_dir():
    """Create history directory if it doesn't exist."""
    os.makedirs(config.HISTORY_DIR, exist_ok=True)

def save_to_history(mode, prompt, response):
    """Save chat interaction to history.json."""
    ensure_history_dir()
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "prompt": prompt,
        "response": response
    }
    
    try:
        # Load existing history
        if os.path.exists(config.HISTORY_FILE):
            with open(config.HISTORY_FILE, "r") as f:
                history = json.load(f)
        else:
            history = []
        
        # Append new entry
        history.append(history_entry)
        
        # Save updated history
        with open(config.HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

def load_history():
    """Load chat history from history.json."""
    ensure_history_dir()
    try:
        if os.path.exists(config.HISTORY_FILE):
            with open(config.HISTORY_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading history: {e}")
        return []

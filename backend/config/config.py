import os

def read_key(file_name):
    try:
        with open(f"backend/config/{file_name}", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise Exception(f"Key file {file_name} not found")

# Load API keys from files or environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or read_key("gemini_key.txt")
GROK_API_KEY = os.getenv("GROK_API_KEY") or read_key("grok_key.txt")
SERPAPI_KEY = os.getenv("SERPAPI_KEY") or read_key("serpapi_key.txt")

# History file path
USER_HOME = os.path.expanduser("~")
HISTORY_DIR = os.path.join(USER_HOME, ".HexAi", "history")
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")

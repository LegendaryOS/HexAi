import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Validate API keys
if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not found in .env")
if not GROK_API_KEY:
    raise Exception("GROK_API_KEY not found in .env")
if not SERPAPI_KEY:
    raise Exception("SERPAPI_KEY not found in .env")

# History file path
USER_HOME = os.path.expanduser("~")
HISTORY_DIR = os.path.join(USER_HOME, ".HexAi", "history")
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")

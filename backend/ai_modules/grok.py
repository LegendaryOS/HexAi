from fastapi import APIRouter
from pydantic import BaseModel
from backend.config import config
from backend.utils import history
import requests

router = APIRouter()

class Prompt(BaseModel):
    text: str

@router.post("/api/grok")
async def grok_chat(prompt: Prompt):
    api_key = config.GROK_API_KEY
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"prompt": prompt.text}
    try:
        response = requests.post(
            "https://api.x.ai/v1/grok",  # Hypothetical Grok API endpoint
            json=data,
            headers=headers,
            stream=True
        )
        response.raise_for_status()
        
        full_response = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                full_response += chunk.decode('utf-8')
        
        result = {"response": full_response}
        history.save_to_history("grok", prompt.text, full_response)
        return result
    except requests.RequestException as e:
        error = {"error": str(e)}
        history.save_to_history("grok", prompt.text, error)
        return error

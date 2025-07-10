from fastapi import APIRouter
from pydantic import BaseModel
from backend.config import config
from backend.utils import history
import requests

router = APIRouter()

class Prompt(BaseModel):
    text: str

@router.post("/api/gemini")
async def gemini_chat(prompt: Prompt):
    api_key = config.GEMINI_API_KEY
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt.text}]}]}
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
            params={"key": api_key},
            json=data,
            headers=headers,
            stream=True  # Enable streaming
        )
        response.raise_for_status()
        
        # Collect streamed response
        full_response = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                full_response += chunk.decode('utf-8')
        
        result = {"response": full_response}
        history.save_to_history("gemini", prompt.text, full_response)
        return result
    except requests.RequestException as e:
        error = {"error": str(e)}
        history.save_to_history("gemini", prompt.text, error)
        return error

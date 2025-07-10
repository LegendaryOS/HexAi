from fastapi import APIRouter
from pydantic import BaseModel
from backend.config import config
from backend.utils import history
import requests

router = APIRouter()

class ImagePrompt(BaseModel):
    text: str

@router.post("/api/generate-image")
async def generate_image(prompt: ImagePrompt):
    api_key = config.GEMINI_API_KEY
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt.text}
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1/models/gemini-vision:generateImage",
            params={"key": api_key},
            json=data,
            headers=headers
        )
        response.raise_for_status()
        result = response.json()
        history.save_to_history("image", prompt.text, result)
        return result
    except requests.RequestException as e:
        error = {"error": str(e)}
        history.save_to_history("image", prompt.text, error)
        return error

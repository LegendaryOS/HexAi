from fastapi import APIRouter
from pydantic import BaseModel
from backend.config import config
from backend.utils import history
import requests

router = APIRouter()

class SearchQuery(BaseModel):
    query: str

@router.post("/api/search")
async def search_web(query: SearchQuery):
    api_key = config.SERPAPI_KEY
    try:
        response = requests.get(
            "https://serpapi.com/search",
            params={"q": query.query, "api_key": api_key}
        )
        response.raise_for_status()
        result = response.json()
        history.save_to_history("search", query.query, result)
        return result
    except requests.RequestException as e:
        error = {"error": str(e)}
        history.save_to_history("search", query.query, error)
        return error

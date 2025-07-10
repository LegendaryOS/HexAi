from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_modules import gemini, grok, image_gen
from utils import search, history
import uvicorn

app = FastAPI()

# Enable CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(gemini.router)
app.include_router(grok.router)
app.include_router(image_gen.router)
app.include_router(search.router)

# History endpoint
@app.get("/api/history")
async def get_history():
    return history.load_history()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)

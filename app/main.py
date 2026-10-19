from fastapi import FastAPI
from app.routes.ai import router as ai_router

app = FastAPI(
    title="AI Text Intelligence Service",
    description="A modular FastAPI service powered by Google Gemini API for summarization, classification, and sentiment analysis.",
    version="1.0.0"
)

# Include the AI routes
app.include_router(ai_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Text Intelligence Service! Navigate to /docs for interactive API documentation."
    }
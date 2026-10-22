from fastapi import FastAPI
from app.routes import rag
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Semantic RAG Document Search API",
    description="API for retrieving context and generating grounded answers using Gemini LLM.",
    version="1.0.0"
)

# Include RAG routes
app.include_router(rag.router)

@app.get("/")
def root():
    return {"message": "Welcome to the RAG Document QA API. Visit /docs for Swagger UI."}
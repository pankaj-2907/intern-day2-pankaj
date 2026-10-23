from fastapi import FastAPI
from app.routes.assistant import router as assistant_router

app = FastAPI(
    title="AI Assistant with Executable Tools (Day 7 RAG)",
    version="1.0.0"
)

# Include assistant endpoints
app.include_router(assistant_router)

@app.get("/")
def root():
    return {"message": "Welcome to Day 7 RAG Tool Calling API. Visit /docs for Swagger UI."}
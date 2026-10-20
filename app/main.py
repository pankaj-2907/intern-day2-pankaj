from fastapi import FastAPI
from app.routes import search, document

app = FastAPI(
    title="Semantic Document Search API",
    description="API that performs meaning-based semantic document retrieval using Google embeddings and cosine similarity.",
    version="1.0.0"
)

# Include the search router
app.include_router(search.router)
app.include_router(document.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Semantic Document Search API"}
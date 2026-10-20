import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initializing  Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
EMBEDDING_MODEL = "text_embedding-004"

def generate_embedding(text: str) -> list[float]:
    """
    Generates a numerical embedding vector for a given text input
    using Google's text-embedding-004 model.
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty or whitespace.")
    
    try:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
        )
        # Extract the embedding values
        if response and response.embedding:
            return response.embedding.values
        raise ValueError("Failed to retrieve embedding values from response.")
    
    except Exception as e:
        raise RuntimeError(f"Embedding generation failed: {str(e)}")
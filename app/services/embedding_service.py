import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initializing  Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
EMBEDDING_MODEL = "gemini-embedding-001"

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
        # response.embeddings is a list of embedding objects.
        # Each object contains the vector values.
        if response and response.embeddings:
            # Access the first element of the list, then get its values
            first_embedding = response.embeddings[0]
            if hasattr(first_embedding, 'values'):
                return first_embedding.values
            return list(first_embedding)
        raise ValueError("Failed to retrieve embedding values from response.")
    
    except Exception as e:
        raise RuntimeError(f"Embedding generation failed: {str(e)}")
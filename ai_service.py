import os
from dotenv import load_dotenv
from google import genai

# load variable from .env file
load_dotenv()

# Read API key from environment variable. (Not hardcode)
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client 
client = genai.Client(api_key=API_KEY)

def generate_ai_summary(text: str) -> str:
    """
    This function take text and use Gemini AI to summarize it.
    """
    if not text or not text.strip():
        raise ValueError("Text input cannot be empty.")
    
    try:
        # Giving prompt to Gemini AI.
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=f"Provide a concise summary of the following text:\n\n{text}"
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API Error: {str(e)}")

def translate_text(text: str) -> str:
    """
    This function take text and use Gemini AI to translate it.
    """
    if not text or not text.strip():
        raise ValueError("Text input cannot be empty.")
    
    try:
        # Giving prompt to Gemini AI.
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=f"Provide translation in Hindi and sanskrit for the following text:\n\n{text}"
        )
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API Error: {str(e)}")
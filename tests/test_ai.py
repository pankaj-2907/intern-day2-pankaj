import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- 1. Successful Responses (Mocked) ---
@patch("app.services.llm_service.client.models.generate_content")
def test_summarize_success(mock_gen):
    mock_gen.return_value.text = "This is a concise summary."
    response = client.post("/ai/summarize", json={"text": "Python 3.12 introduces major performance updates."})
    assert response.status_code == 200
    assert "summary" in response.json()

@patch("app.services.llm_service.client.models.generate_content")
def test_classify_success(mock_gen):
    mock_gen.return_value.text = "Category: Technical\nConfidence: 0.98\nReasoning: Code optimization."
    response = client.post("/ai/classify", json={"text": "Writing cleaner code with pytest and git."})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Technical"

@patch("app.services.llm_service.client.models.generate_content")
def test_sentiment_success(mock_gen):
    mock_gen.return_value.text = "Sentiment: Positive\nScore: 0.9\nExplanation: Great experience."
    response = client.post("/ai/sentiment", json={"text": "I love developing with FastAPI!"})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "Positive"


# --- 2. Validation Failures (Empty text & Missing fields) ---
def test_empty_text_validation():
    response = client.post("/ai/summarize", json={"text": "   "})
    assert response.status_code == 422

def test_missing_field_validation():
    response = client.post("/ai/classify", json={})
    assert response.status_code == 422


# --- 3. Provider Error Handling (Mocked 429/502) ---
@patch("app.services.llm_service.client.models.generate_content")
def test_provider_rate_limit(mock_gen):
    from google.genai import errors
    
    # Bypass __init__ to avoid missing argument errors in SDK exception
    api_error = errors.APIError.__new__(errors.APIError)
    api_error.code = 429
    api_error.message = "Resource exhausted"
    
    mock_gen.side_effect = api_error
    response = client.post("/ai/summarize", json={"text": "Triggering rate limit check."})
    assert response.status_code == 500

# --- 4. Real Integration Test (Runs against live API if key is present) ---
def test_real_api_integration():
    """Real integration test using actual Gemini API credentials."""
    import os
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not set, skipping real integration test.")
    
    response = client.post("/ai/summarize", json={"text": "FastAPI is a modern, fast web framework for building APIs with Python."})
    assert response.status_code == 200
    assert len(response.json().get("summary", "")) > 0
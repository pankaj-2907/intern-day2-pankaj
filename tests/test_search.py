import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.search_service import search_service

client = TestClient(app)

def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]


def test_search_endpoint_valid_query():
    """Test /search endpoint with a valid technical query."""
    response = client.post("/search", json={"query": "How can I protect an API?", "top_k": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "How can I protect an API?"
    assert len(data["results"]) <= 2
    assert "id" in data["results"][0]
    assert "score" in data["results"][0]


def test_search_endpoint_empty_query():
    """Test /search endpoint with an empty query (should fail validation)."""
    response = client.post("/search", json={"query": "", "top_k": 3})
    assert response.status_code == 422 # Pydantic validation error for empty string


def test_search_service_invalid_top_k():
    """Test search service with invalid top_k value."""
    with pytest.raises(ValueError):
        search_service.search(query="API security", top_k=0)
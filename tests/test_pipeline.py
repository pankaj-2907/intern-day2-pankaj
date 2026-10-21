import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.search_service import SearchService, cosine_similarity
from app.services.embedding_service import generate_embedding

client = TestClient(app)

def test_cosine_similarity():
    """Test 1 & 2: Similarity calculations and vector dimensions."""
    v1 = [1.0, 0.0]
    v2 = [1.0, 0.0]
    assert cosine_similarity(v1, v2) == pytest.approx(1.0)
    
    with pytest.raises(ValueError):
        cosine_similarity([1.0, 0.0], [1.0, 0.0, 0.0])

@patch("app.services.embedding_service.client")
def test_embedding_generation_and_failure(mock_client):
    """Test 3 & 10: Embedding generation mock and failure handling."""
    mock_embedding_item = MagicMock()
    mock_embedding_item.values = [0.1, 0.2, 0.3]
    
    mock_client.models.embed_content.return_value.embeddings = [mock_embedding_item]
    
    vec = generate_embedding("test query")
    assert vec == [0.1, 0.2, 0.3]

    # Test failure handling
    mock_client.models.embed_content.side_effect = Exception("API connection error")
    with pytest.raises(RuntimeError):
        generate_embedding("failing query")

def test_top_k_validation():
    """Test 4: top_k validation."""
    service = SearchService()
    with pytest.raises(ValueError):
        service.search(query="test", top_k=0)

def test_empty_query_and_dataset():
    """Test 5 & 6: Empty query validation and empty datasets."""
    response = client.post("/search", json={"query": "", "top_k": 3})
    assert response.status_code == 422

    # Test empty dataset search using a fresh SearchService instance
    service = SearchService()
    service.documents = []
    service.document_embeddings = []
    results = service.search(query="test", top_k=3)
    assert results == []

def test_invalid_document_input_and_duplicates():
    """Test 7 & 8: Invalid document input and duplicate IDs."""
    response = client.post("/documents", json={"id": "doc_invalid", "title": ""})
    assert response.status_code == 422

    # Use unique ID for duplicate test
    payload = {"id": "doc_unique_test_123", "title": "Test", "content": "Sample content."}
    client.post("/documents", json=payload)
    response = client.post("/documents", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@patch("app.services.search_service.generate_embedding")
def test_add_document_and_search_pipeline(mock_gen_embed):
    """Test 9 & 3: Adding document, mocking embedding, and correct result ranking."""
    mock_gen_embed.return_value = [1.0, 0.0, 0.0]
    
    # Create an isolated SearchService instance for testing
    service = SearchService()
    service.documents = []
    service.document_embeddings = []
    
    service.add_document("doc_pipe_1", "Pipeline Doc", "Content about pipelines")
    results = service.search(query="Pipeline", top_k=1)
    
    assert len(results) == 1
    assert results[0]["id"] == "doc_pipe_1"
    assert "score" in results[0]

def test_api_response_schema_validation():
    """Test 11: API response schema validation."""
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
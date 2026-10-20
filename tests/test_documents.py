import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_documents():
    """Test GET /documents endpoint returns list of documents with id and title."""
    response = client.get("/documents")
    assert response.status_code == 200
    docs = response.json()
    assert isinstance(docs, list)
    if len(docs) > 0:
        assert "id" in docs[0]
        assert "title" in docs[0]
        # Ensure raw embeddings are NOT exposed
        assert "embedding" not in docs[0]


def test_add_document_success():
    """Test POST /documents successfully adds a new document."""
    payload = {
        "id": "doc_test_999",
        "title": "Automated Testing Guide",
        "content": "Automated testing executes predefined tests to verify software behavior and ensure quality."
    }
    response = client.post("/documents", json=payload)
    # Status can be 201 Created on success
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == payload["id"]
    assert data["title"] == payload["title"]


def test_add_document_duplicate_id():
    """Test POST /documents rejects duplicate document IDs with 400 Bad Request."""
    payload = {
        "id": "doc_test_999",  # Same ID added in the previous test
        "title": "Duplicate Test",
        "content": "Trying to insert duplicate ID."
    }
    response = client.post("/documents", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_add_document_invalid_payload():
    """Test POST /documents fails validation when required fields are missing."""
    payload = {
        "id": "doc_invalid",
        "title": ""  # Empty title should trigger Pydantic validation error
    }
    response = client.post("/documents", json=payload)
    assert response.status_code == 422
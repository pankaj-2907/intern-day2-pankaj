import pytest
from app.services.chunking_service import chunk_document

def test_chunk_document_basic():
    doc = {
        "id": "doc_001",
        "title": "API Security",
        "content": "API security includes authentication, authorization, input validation, and rate limiting."
    }
    chunks = chunk_document(doc, chunk_size=50, chunk_overlap=10)
    assert len(chunks) > 0
    assert chunks[0]["document_id"] == "doc_001"
    assert chunks[0]["title"] == "API Security"
    assert "chunk_id" in chunks[0]

def test_empty_document():
    doc = {"id": "doc_empty", "title": "Empty", "content": ""}
    chunks = chunk_document(doc)
    assert chunks == []
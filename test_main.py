from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_word_frequency():
    response = client.post("/text/word-frequency", json={"text": "AI is useful and AI is growing"})
    assert response.status_code == 200
    data = response.json()
    assert "word_frequency" in data
    assert data["word_frequency"]["ai"] == 2
    assert data["word_frequency"]["is"] == 2
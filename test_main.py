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

def test_reproduce_bug():
    # Yeh test check karega ki analyze endpoint empty ya specific text par fail ho raha hai ya nahi
    response = client.post("/text/analyze", json={"text": ""})
    # Kyunki min_length=1 hai, agar validation fail hoti hai toh 400 aana chahiye, 
    # par bug ki wajah se agar 500 (Server Error) aa raha hai, toh bug reproduce ho gaya!
    assert response.status_code == 422
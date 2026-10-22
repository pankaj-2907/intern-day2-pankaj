# Production-Grade RAG API (FastAPI & Google GenAI)

A robust, modular Retrieval-Augmented Generation (RAG) backend service built with Python, FastAPI, and the official Google GenAI SDK (`google-genai`). The system features decoupled retrieval and generation services, automated vector search using cosine similarity, security guardrails against prompt injection, comprehensive automated testing via `pytest`, and empirical evaluation metrics tracking.

---

## 1. Project Overview

This API allows users to query document knowledge bases securely and accurately. Key architectural highlights include:

*   **Decoupled Architecture:** 
    *   `RetrievalService`: Handles document loading, text chunking, embedding generation, and cosine similarity ranking.
    *   `RAGService`: Orchestrates prompt construction, strict grounding guardrails, and Gemini model generation.
*   **Security & Robustness:** Protects against malicious prompt injections, handles missing/unanswerable contexts gracefully with explicit fallback abstentions, and implements graceful error management for API quotas (`429`) and server unavailability (`503`).
*   **Evaluation Framework:** Automated evaluation scripts measuring Retrieval Recall@3, Answerability Accuracy, and Citation Correctness against a curated evaluation dataset.

---

## 2. Project Directory Structure

```text
├── app/
│   ├── main.py                 # FastAPI application and route entrypoints
│   ├── schemas/                # Pydantic request/response validation schemas
│   └── services/               # Core business logic (Retrieval, RAG, Chunking, Embedding)
├── data/
│   ├── documents.json          # Source document knowledge base
│   └── rag_evaluation.json     # Ground-truth evaluation dataset
├── experiments/
│   └── RAG_EVALUATION.md       # Empirical evaluation report and metrics
├── docs/
│   └── TEST_RESULTS.md         # Detailed test suite execution results
├── tests/
│   └── test_rag_system.py      # Comprehensive pytest automated test suite
├── scripts/
│   └── rag_evaluate.py         # Automated pipeline evaluation script
├── requirements.txt            # Project Python dependencies
└── README.md                   # Project documentation
```

---

## 3. Setup & Installation

### Prerequisites
*   Python 3.10 or higher
*   A valid Google Gemini API Key (`GEMINI_API_KEY`)

### Step 1: Clone and Navigate to Repository
```powershell
git clone <your-repository-url>
cd Task_day2
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv venv
# On Windows (PowerShell):
.\venv\Scripts\Activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

---

## 4. Execution (Running the API Server)

Start the FastAPI application using Uvicorn with auto-reload enabled:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Once running, you can access the interactive Swagger API documentation at:
*   **URL:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 5. Automated Testing

The project includes an extensive test suite covering document chunking, metadata preservation, retrieval ranking, empty index edge cases, error handling, prompt injection defense, and schema validation. Tests utilize mocking so they run without requiring paid API calls or live credentials.

Run the test suite using pytest:

```powershell
pytest -v
```

For detailed test verification records, refer to `docs/TEST_RESULTS.md`.

---

## 6. Running RAG Evaluation

To execute the empirical evaluation script against the test dataset and generate updated performance metrics (Recall@3, Answerability Accuracy, Citation Correctness), run:

```powershell
python scripts/rag_evaluate.py
```

The resulting per-question log and metrics will be automatically saved to `experiments/RAG_EVALUATION.md`.

---

## 7. Example API Requests

### Ask Endpoint (`POST /rag/ask`)
Sends a query to the RAG pipeline, retrieves top relevant chunks, and returns a grounded response with source citations.

*   **Endpoint:** `POST http://127.0.0.1:8000/rag/ask`

**Request Body:**

```json
{
  "question": "How can unauthorized API access be prevented?",
  "top_k": 3
}
```

**Example curl command:**

```bash
curl -X POST "http://127.0.0.1:8000/rag/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "How can unauthorized API access be prevented?", "top_k": 3}'
```

**Example JSON Response:**

```json
{
  "question": "How can unauthorized API access be prevented?",
  "answer": "Unauthorized API access can be prevented by implementing robust authentication mechanisms such as OAuth2 tokens, API keys, and proper role-based access control.",
  "sources": [
    {
      "document_id": "doc_001",
      "title": "API Security Best Practices",
      "chunk_id": "doc_001_chunk_001"
    }
  ],
  "retrieved_chunks": 3
}
```

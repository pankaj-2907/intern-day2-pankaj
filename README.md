# Semantic Document Search API

A high-performance, robust RESTful API built with **FastAPI** and **Google GenAI (`text-embedding-004`)** that enables semantic searching over document collections using vector embeddings and cosine similarity math.

## Project Overview

This project provides an end-to-end semantic document search service capable of:

* Generating high-dimensional text embeddings using Google's GenAI API.

* Storing document metadata and corresponding vector embeddings in memory.

* Executing real-time semantic search queries scored by cosine similarity.

* Providing comprehensive API validation, error handling, and guardrails.

* Evaluating search quality against standard IR metrics (Precision@k, Recall@k, MRR).

* Ensuring high stability and coverage through automated unit/integration tests with `pytest`.

## Tech Stack

* **Language:** Python 3.10+

* **Framework:** FastAPI

* **Validation & Schemas:** Pydantic

* **AI & Embeddings:** Google GenAI SDK (`google-genai`) — Model: `text-embedding-004`

* **Math & Scientific Computing:** NumPy

* **Testing:** Pytest, HTTPX / FastAPI TestClient

* **Server:** Uvicorn

## Repository Structure

```
├── app/
│   ├── main.py                  # FastAPI app entry point & route definitions
│   ├── models.py                # Pydantic schemas for requests & responses
│   └── services/
│       ├── embedding_service.py # Integration with Google GenAI API
│       └── search_service.py    # Vector math & document management core
├── docs/
│   ├── TESTING.md               # Overview of testing strategies
│   └── TEST_RESULTS.md          # Recorded automated test execution outputs
├── experiments/
│   └── SEARCH_EVALUATION.md     # Quality metrics evaluation report (P@3, R@3, MRR)
├── scripts/
│   ├── evaluate.py              # Search quality evaluation runner
│   └── test_queries.json        # Evaluation test benchmark query set
├── tests/
│   └── test_pipeline.py         # Complete Pytest automated test suite
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation

```

## Quick Start & Setup

### 1. Prerequisites

Ensure Python 3.10 or higher is installed along with your Google GenAI API key.

### 2. Clone the Repository & Setup Environment

```
# Clone repository
git clone https://github.com/pankaj-2907/intern-day2-pankaj.git
cd intern-day2-pankaj

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Environment Variables

Set your Google Gemini API key:

```
# On Windows (PowerShell):
$env:GEMINI_API_KEY="your-actual-api-key-here"

# On Linux/macOS:
export GEMINI_API_KEY="your-actual-api-key-here"

```

### 4. Running the API

Start the FastAPI server locally using Uvicorn:

```
uvicorn app.main:app --reload

```

The server will run at `http://127.0.0.1:8000`.
Interactive Swagger UI documentation is available at `http://127.0.0.1:8000/docs`.

## 📡 API Endpoints

### 1. Health Check

* **`GET /`**

  * **Description:** Health check and status ping.

  * **Response:** `200 OK`

  ```
  {
    "status": "online",
    "message": "Semantic Document Search API is operational."
  }
  
  ```

### 2. Add / Store Document

* **`POST /documents`**

  * **Description:** Index a new document, generate its vector embedding, and save it.

  * **Request Body:**

    ```
    {
      "id": "doc_101",
      "title": "FastAPI Guide",
      "content": "FastAPI is a modern, fast web framework for building APIs with Python."
    }
    
    ```

  * **Response:** `201 Created`

### 3. List Documents

* **`GET /documents`**

  * **Description:** Retrieve metadata of all currently stored documents.

  * **Response:** `200 OK`

### 4. Semantic Search

* **`POST /search`**

  * **Description:** Perform semantic vector search for a given natural language query.

  * **Request Body:**

    ```
    {
      "query": "python web frameworks",
      "top_k": 3
    }
    
    ```

  * **Response:** `200 OK`

  ```
  [
    {
      "id": "doc_101",
      "title": "FastAPI Guide",
      "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
      "score": 0.8245
    }
  ]
  
  ```

## Automated Testing

Automated tests are implemented using `pytest` and mock the Google GenAI client for 100% deterministic, offline execution.

To run the complete test suite:

```
pytest tests/test_pipeline.py -v

```

The test suite covers:

* Vector embedding generation & API failure handling

* Cosine similarity calculations & vector dimension verification

* Result ranking accuracy

* Search guardrails (`top_k` parameter validation, empty queries, empty index)

* Data validation & duplicate ID protection

* REST API schema compliance

Detailed execution reports are recorded in [`docs/TEST_RESULTS.md`](docs/TEST_RESULTS.md).

## Evaluation Metrics

Evaluation script (`scripts/evaluate.py`) benchmarks search accuracy across test queries (`scripts/test_queries.json`).

* **Precision@3:** Proportion of top-3 results that are relevant.

* **Recall@3:** Proportion of total relevant documents retrieved in top-3.

* **Mean Reciprocal Rank (MRR):** Reciprocal rank score of the first relevant result.

Refer to [`experiments/SEARCH_EVALUATION.md`](experiments/SEARCH_EVALUATION.md) for full benchmark results.
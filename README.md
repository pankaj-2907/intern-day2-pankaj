# Google Gemini Tool-Calling RAG Application

## Project Description
This project is a secure, production-grade tool-calling Retrieval-Augmented Generation (RAG) backend application built with **FastAPI**, **Google Gemini SDK (`google-genai`)**, and **Pydantic** data validation. It orchestrates intelligent conversational interactions while maintaining rigorous safety controls, decentralized tool registration, and deterministic error handling.

---

## Available Tools
All registered tools are strictly **read-only** with respect to external systems:

* **`calculate`**: Performs safe arithmetic operations (`add`, `subtract`, `multiply`, `divide`) using validated operands.
* **`get_current_datetime`**: Retrieves current timestamps based on specified valid timezones.
* **`search_knowledge_base`**: Performs semantic document retrieval from the local vector database index.

---

## Architecture Overview
* **Centralized Tool Registry (`tool_registry`)**: Maps explicit function schemas and prevents the execution of unregistered or arbitrary code.
* **Strict Argument Validation**: All parameters passed to tools are validated via Pydantic models.
* **LLM Orchestration**: Powered by Google Gemini with a built-in execution round limit (`max_rounds=5`) to prevent infinite tool-calling loops.
* **Sanitized Error Boundaries**: Contains internal exceptions, preventing stack traces, file paths, or credentials from leaking to clients.

---

## Environment Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create and activate a virtual environment:
   * **On Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * **On macOS/Linux:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables by creating a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   *(Note: Never commit your `.env` file or API keys to version control.)*

---

## How to Run the API
Start the FastAPI development server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
* The API will be accessible at `http://127.0.0.1:8000`.
* You can explore interactive API docs via Swagger UI at `http://127.0.0.1:8000/docs`.

---

## How to Run Tests
Run the comprehensive automated pytest suite with verbose output:
```bash
pytest -v
```

---

## Example Chat Requests

### 1. Arithmetic Calculation
* **Endpoint:** `POST /chat`
* **Payload:**
  ```json
  {
    "message": "What is 250 multiplied by 4?"
  }
  ```

### 2. Knowledge Base Search
* **Endpoint:** `POST /search`
* **Payload:**
  ```json
  {
    "query": "authentication security headers",
    "top_k": 3
  }
  ```

---

## Known Limitations
* **Read-Only Tools:** The application does not support side-effect actions such as sending emails, making purchases, or modifying production databases.
* **Local State Indexing:** Knowledge base search relies on pre-indexed local documents; dynamic runtime web scraping is out of scope.

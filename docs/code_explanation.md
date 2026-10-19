# 📖 Code Explanation & Architecture Overview

This document provides a clear, high-level walkthrough of how the AI Text Intelligence Service operates internally based on our FastAPI and `google-genai` implementation.

---

### 1. Request Lifecycle (What happens between request and response?)
1. **Client Request:** A client sends a POST request with JSON payload to an endpoint (e.g., `/ai/summarize`, `/ai/classify`, or `/ai/sentiment`).
2. **Input Validation:** FastAPI intercepts the request and uses Pydantic schemas (`SummarizeRequest`, `ClassifyRequest`, `SentimentRequest`) to validate data types and minimum length rules.
3. **Route Handling:** The route handler in `app/routes/ai.py` forwards the validated input string to the corresponding service function in `app/services/llm_service.py`.
4. **Prompt Construction & Inference:** The service builds a clear prompt template and calls the Gemini API (`client.models.generate_content`).
5. **Output Parsing & Validation:** The raw output string returned from the LLM is parsed line-by-line, and specific values (like classification categories) are checked against allowed sets (`PERMITTED_CATEGORIES`).
6. **HTTP Response:** The final structured data dictionary is serialized back to JSON using response schemas (`SummarizeResponse`, etc.) and returned to the client with an HTTP `200 OK` status.

---

### 2. Where is the prompt constructed?
The prompts are constructed inside **`app/services/llm_service.py`** within their respective service functions (`generate_summary`, `generate_classification`, and `generate_sentiment`). 
Each function builds an f-string prompt combining strict formatting instructions, constraints (e.g., allowed categories), and the user's input text.

---

### 3. Where does model inference happen?
Model inference happens **remotely on Google's cloud infrastructure** via the `google-genai` SDK. In `app/services/llm_service.py`, executing `client.models.generate_content(model=MODEL_NAME, contents=prompt)` triggers the network call where Google's `gemini-flash-latest` model processes the prompt and computes the completion.

---

### 4. What determines the structure of the model response?
Two main components enforce the response structure:
1. **Prompt Formatting Instructions:** The prompt explicitly instructs the model to return outputs in key-value lines (e.g., `Category: ...`, `Confidence: ...`, `Reasoning: ...`).
2. **Pydantic Response Schemas:** In `app/schemas/ai_schemas.py`, defined models (`ClassifyResponse`, `SentimentResponse`) strictly type-check and constrain the final JSON payload returned by the API.

---

### 5. How is the response validated?
Response validation happens in two steps:
* **Custom Parsing & Boundary Checks:** Inside `llm_service.py`, the string is checked for empty returns. For classification, the extracted category string is checked against `PERMITTED_CATEGORIES = {"Technical", "Business", "Education", "General"}`. If an unpermitted value is returned, a `502 Bad Gateway` error is raised instead of returning invalid data.
* **Schema Validation:** FastAPI validates the parsed dictionary against the Pydantic response schema before serialization.

---

### 6. What happens if the provider is unavailable?
If Google GenAI is down, rate-limited, or times out:
* The exception is caught in the service/route exception handling block.
* Upstream 429 quota errors trigger a `429 Too Many Requests` HTTP error.
* Upstream timeouts or connection errors raise `504 Gateway Timeout` or `502 Bad Gateway`.
* Internal API keys and raw stack traces are masked, ensuring security while logging diagnostic info internally.

---

### 7. What is the difference between an HTTP error and an LLM hallucination?
* **HTTP Error:** A deterministic system failure during network transport, authentication, or input validation (e.g., `422` for invalid JSON, `401` for invalid API key, `502` for API down). No LLM generation occurs.
* **LLM Hallucination:** A probabilistic output issue where the network call succeeds (`200 OK`), but the model generates factually incorrect, ungrounded, or unexpected text that does not follow reality or strict prompt instructions.

---

### 8. Which parts of the system are deterministic, and which are probabilistic?
* **Deterministic (100% predictable):**
  * Pydantic schema validation for request payloads and response bodies.
  * FastAPI routing and HTTP status code selection.
  * Python string parsing logic and category allowed-set checking (`PERMITTED_CATEGORIES`).
* **Probabilistic (Generative / Non-deterministic):**
  * The actual text/reasoning generation produced by Gemini model inference.

---

### 9. Which parts of the implementation used AI assistance?
AI assistance (Gemini / LLM tools) was used for:
* Accelerating boilerplate setup for FastAPI routers and Pydantic schemas.
* Designing mock tests using `unittest.mock` for `pytest` coverage.
* Structuring prompt templates and refining error handling documentation.

---

### 10. What would you change if this service had to handle 1,000 requests per minute?
To handle 1,000 RPM in production:
1. **Asynchronous Architecture:** Convert sync route handlers and service functions to `async` / `await` using `httpx` or Google's async SDK methods to avoid blocking worker threads.
2. **Caching:** Implement Redis caching for identical input text requests to eliminate redundant LLM API calls.
3. **Queueing & Rate Limiting:** Introduce Redis/Celery background task queues to buffer sudden traffic spikes and avoid exceeding Google's API rate limits.
4. **Horizontal Scaling:** Deploy the FastAPI service across multiple container instances (Docker/Kubernetes) behind an NGINX load balancer.
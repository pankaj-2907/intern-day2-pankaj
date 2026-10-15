# Code explanation


### 1. How does a request reach the FastAPI endpoint?

When a client (such as your browser via Swagger UI, a curl command, or a frontend app) sends an HTTP request over the network:
1. **Uvicorn Server:** The Uvicorn server listens on `http://127.0.0.1:8000` and receives incoming TCP/HTTP connections.
2. **FastAPI Routing:** FastAPI checks the URL path (e.g., `/text/summarize`) and the HTTP method (e.g., `POST`). It matches the request against the registered route decorators (like `@app.post("/text/summarize")`) defined in `main.py`.
3. **Execution:** Once matched, FastAPI routes the request payload into the corresponding Python handler function.

---

### 2. How is the request body validated?

Request validation is handled automatically by **Pydantic**, which FastAPI integrates seamlessly:
1. **Pydantic Models:** The request body must match the defined schema class (e.g., `TextSummarizeRequest` inheriting from `BaseModel`).
2. **Constraints and Rules:** Fields are declared with type hints (`text: str`) and constraints via `Field(...)` (such as `min_length=20` or `min_length=1`).
3. **Automatic Rejection:** If a client sends invalid JSON, missing keys, or text that fails length constraints, FastAPI automatically intercepts the request before your code runs and returns a **`422 Unprocessable Entity`** response with detailed error locations.

---

### 3. Where does the application call the AI API?

The application separates concerns by isolating all AI communication within the **`ai_service.py`** module:
1. Inside `ai_service.py`, the `generate_ai_summary(text: str)` function prepares the prompt.
2. It invokes the official Google GenAI SDK client via:
   ```python
   response = client.models.generate_content(
       model="gemini-flash-latest",
       contents=f"Provide a concise summary of the following text:\n\n{text}"
   )
   ```
3. This sends an outbound HTTPS request to Google's Gemini servers and returns the response object.

---

### 4. How does the API response reach the client?

Once the AI or text analysis logic completes:
1. **Data Packaging:** The function returns a standard Python dictionary (e.g., `{"summary": summary}` or `{"word_count": word_count, ...}`).
2. **JSON Serialization:** FastAPI automatically serializes this Python dictionary into a JSON formatted string.
3. **HTTP Transport:** FastAPI packages the JSON into an HTTP response with a status code (`200 OK`), sends it back through Uvicorn across the network socket, and delivers it to the waiting client.

---

### 5. What happens if the AI provider is unavailable?

If the AI provider encounters network drops, high demand (`503 Service Unavailable`), or authentication errors:
1. **Exception Raising:** The Google GenAI SDK or network layer throws an exception, which is caught inside the `try...except` block in `ai_service.py` and wrapped in a `RuntimeError`.
2. **FastAPI Error Handling:** The `main.py` endpoint catches this exception:
   ```python
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
   ```
3. **Graceful Failure:** Instead of crashing the entire backend server, FastAPI returns a clean, structured JSON error response with an HTTP 500 status code, protecting system stability.

---

### 6. Where are the environment variables loaded?

Environment variables (such as `GEMINI_API_KEY`) are loaded securely at the very top of **`ai_service.py`**:
```python
from dotenv import load_dotenv
import os

# Load variables from the local .env file into environment memory
load_dotenv()

# Read the secret key safely without hardcoding
API_KEY = os.getenv("GEMINI_API_KEY")
```
The `.env` file resides in the root directory of the project alongside `main.py` and is excluded from version control (via `.gitignore`) to protect credentials.

---

### 7. Which parts of your code were written or modified with AI assistance?

* **AI Service Integration (`ai_service.py`):** The initialization of the official Google GenAI SDK client (`genai.Client`) and the specific model parameter syntax (`gemini-flash-latest`) were structured and refined with AI assistance to ensure compatibility with current API standards.
* **Error Handling & Exception Wrapping:** The `try...except` exception wrapping blocks in both `ai_service.py` and `main.py` were optimized with AI guidance to map backend errors cleanly to HTTP status codes (`400`, `422`, `500`).
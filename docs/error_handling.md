# Output Validation & Error Handling Specification

---

## Test Cases & Observed Behavior

### 1. Empty Text
* **Scenario:** Request body contains `{"text": ""}` or `{"text": "   "}`.
* **HTTP Status:** `422 Unprocessable Entity`
* **Client Response:**
  ```json
  {
    "detail": [
      {
        "loc": ["body", "text"],
        "msg": "String should have at least 5 characters",
        "type": "string_type"
      }
    ]
  }
  ```
* **Logged Diagnostic:** `WARNING: Request validation failed: Text input must not be empty or below minimum character threshold.`

### 2. Missing Request Field
* **Scenario:** Request body is missing the required text field (e.g., `{}`).
* **HTTP Status:** `422 Unprocessable Entity`
* **Client Response:**
  ```json
  {
    "detail": [
      {
        "loc": ["body", "text"],
        "msg": "Field required",
        "type": "missing"
      }
    ]
  }
  ```
* **Logged Diagnostic:** `Pydantic schema validation error caught automatically by FastAPI middleware.`

### 3. Invalid Request Data Type
* **Scenario:** Passing an invalid type for text, e.g., `{"text": ["invalid", "array"]}`.
* **HTTP Status:** `422 Unprocessable Entity`
* **Client Response:**
  ```json
  {
    "detail": [
      {
        "loc": ["body", "text"],
        "msg": "Input should be a valid string",
        "type": "string_type"
      }
    ]
  }
  ```
* **Logged Diagnostic:** `Data type validation failed during body deserialization.`

### 4. LLM Provider Authentication Failure
* **Scenario:** Invalid or missing `GEMINI_API_KEY` in environment variables.
* **HTTP Status:** `502 Bad Gateway`
* **Client Response:**
  ```json
  {
    "detail": "AI service authentication error. Please contact system administrator."
  }
  ```
* **Logged Diagnostic:** `ERROR: Authentication failed with GenAI provider (API_KEY_INVALID). Secrets masked.`

### 5. Rate-Limit Response
* **Scenario:** Gemini API rate limit or quota exceeded (HTTP 429 from upstream).
* **HTTP Status:** `429 Too Many Requests`
* **Client Response:**
  ```json
  {
    "detail": "AI provider rate limit reached. Please try again later."
  }
  ```
* **Logged Diagnostic:** `WARNING: Upstream Gemini API returned rate limit error (RESOURCE_EXHAUSTED / HTTP 429).`

### 6. Provider Timeout
* **Scenario:** Network latency or provider failure resulting in request timeout.
* **HTTP Status:** `504 Gateway Timeout`
* **Client Response:**
  ```json
  {
    "detail": "AI service provider request timed out."
  }
  ```
* **Logged Diagnostic:** `ERROR: Call to Gemini API timed out after socket threshold.`

### 7. Provider Returns Malformed or Unexpected Output
* **Scenario:** Output string does not match required key-value extraction pattern.
* **HTTP Status:** `502 Bad Gateway`
* **Client Response:**
  ```json
  {
    "detail": "Failed to parse structured response from AI provider."
  }
  ```
* **Logged Diagnostic:** `WARNING: Failed to parse raw model response into expected fields.`

### 8. Model Returns Category Outside Permitted Values
* **Scenario:** Model classifies text into an unpermitted category (e.g., `"Sports"` when allowed set is `{"Technical", "Business", "Education", "General"}`).
* **HTTP Status:** `502 Bad Gateway`
* **Client Response:**
  ```json
  {
    "detail": "AI model produced invalid output category."
  }
  ```
* **Logged Diagnostic:** `WARNING: Model returned unpermitted category 'Sports'. Permitted: ['Business', 'Education', 'General', 'Technical'].`

### 9. Provider Returns an Empty Response
* **Scenario:** Model returns `""` or `None` due to safety/content filter blocks.
* **HTTP Status:** `502 Bad Gateway`
* **Client Response:**
  ```json
  {
    "detail": "AI provider returned empty generation response."
  }
  ```
* **Logged Diagnostic:** `ERROR: Gemini response text is empty or blocked by upstream content filters.`

### 10. Unexpected Backend Exception
* **Scenario:** Unhandled internal server runtime exception.
* **HTTP Status:** `500 Internal Server Error`
* **Client Response:**
  ```json
  {
    "detail": "An unexpected internal server error occurred."
  }
  ```
* **Logged Diagnostic:** `CRITICAL: Unhandled exception caught: [Stack trace logged internally in server logs].`

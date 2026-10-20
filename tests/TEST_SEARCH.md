# Search API Testing Documentation

This document describes the testing implementation for the Search API endpoints and validation logic.

## 1. Overview & Test Scope
The search test suite (`tests/test_search.py`) uses FastAPI's `TestClient` to validate HTTP endpoints, schema validation, and edge-case handling.

### Test Cases Covered:
1. **`test_read_root`**:
   - Verifies that the root endpoint (`/`) is active and returns the expected status code (`200 OK`) and welcome message.
2. **`test_search_endpoint_valid_query`**:
   - Tests the POST `/search` endpoint with a realistic technical query and `top_k=2`.
   - Validates that the HTTP status is `200 OK`, response contains the query string, result count respects `top_k`, and individual items contain required `id` and `score` fields.
3. **`test_search_endpoint_empty_query`**:
   - Verifies Pydantic schema validation. Sending an empty query string (`""`) correctly triggers an HTTP `422 Unprocessable Entity` validation error.
4. **`test_search_service_invalid_top_k`**:
   - Directly tests `SearchService` error handling when an invalid `top_k=0` is provided, confirming that a `ValueError` is raised.

## 2. Execution Command
To run this test suite using `pytest`:

```powershell
python -m pytest -v
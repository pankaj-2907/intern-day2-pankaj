# API Testing & Quality Assurance Documentation

## 1. Test Suites Overview

### A. Search Engine & Similarity Tests (`tests/test_search.py`)
- **`test_read_root`**: Verifies that the root endpoint (`/`) is active and returns the expected welcome message (`200 OK`).
- **`test_search_endpoint_valid_query`**: Tests the POST `/search` endpoint with a realistic technical query and `top_k=2`, validating the response structure and scores.
- **`test_search_endpoint_empty_query`**: Ensures Pydantic catches empty queries with an HTTP `422 Unprocessable Entity` error.
- **`test_search_service_invalid_top_k`**: Directly validates that `SearchService` raises a `ValueError` for invalid `top_k` bounds.

### B. Document Lifecycle Tests (`tests/test_documents.py`)
- **`test_list_documents`**: Verifies that GET `/documents` returns a list of available documents containing only `id` and `title`, strictly ensuring that raw embedding vectors are **not** exposed.
- **`test_add_document_success`**: Tests POST `/documents` with a valid payload, confirming successful creation (`201 Created`).
- **`test_add_document_duplicate_id`**: Tests duplicate protection, ensuring inserting an existing ID returns an HTTP `400 Bad Request` with an appropriate error detail.
- **`test_add_document_invalid_payload`**: Validates that missing or empty required fields trigger a Pydantic validation error (`422 Unprocessable Entity`).

## 2. Execution Command
To run the complete test suite using `pytest`:

```powershell
python -m pytest -v
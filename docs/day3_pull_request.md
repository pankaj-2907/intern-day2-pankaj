# Pull Request Report — Part 3

## PR Title: feat: add POST /text/word-frequency endpoint
**Target Branch:** `main`  
**Source Branch:** `feature/word-frequency`  

### 1. What Changed
* Added a new FastAPI POST endpoint at `/text/word-frequency`.
* Used `re` and `collections.Counter` to clean, tokenize, and count words case-insensitively.
* Added input validation using Pydantic.

### 2. Why It Changed
* To expand the text-processing capabilities as requested in the Day 3 engineering workshop requirements.

### 3. How It Was Tested
* Tested locally using `pytest` via FastAPI `TestClient`.
* All test cases passed successfully (`1 passed`).

### 4. Known Limitations
* Punctuation is stripped; hyphenated words are split into separate tokens.
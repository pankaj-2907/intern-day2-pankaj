## Project Structure
* `main.py` - FastAPI application routes and request validation.
* `ai_service.py` - Google Gemini AI integration and business logic.
* `API_TEST_RESULTS.md` - Manual test logs and verification results.
* `AI_NOTES_DAY2.md` - Core AI concepts and assignment notes.
* `CODE_EXPLANATION.md` - Architecture and implementation details.

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pankaj-2907/intern-day2-pankaj.git
   cd intern-day2-pankaj
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn python-dotenv google-genai pydantic
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

---

## Running the Application

Start the development server using Uvicorn:
```bash
uvicorn main:app --reload
```

* The server will run at: `http://127.0.0.1:8000`
* Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`
# 🔄 LLM Request Lifecycle & Architecture

---

## 📊 End-to-End Request Flow Diagram

```mermaid
graph TD
    Client[User / Client] -->|1. HTTP POST Request e.g., /ai/classify| Backend[FastAPI Backend]
    Backend -->|2. Validate Input Schema Pydantic| PromptService[Prompt Construction Service]
    PromptService -->|3. Inject Input into Structured Prompt Template| GeminiAPI[LLM Provider API Google Gemini]
    GeminiAPI -->|4. API Call over HTTPS with Auth Token| Inference[Model Inference Engine]
    Inference -->|5. Process Tokens & Generate Response| RespHandler[Response Handler]
    RespHandler -->|6. Receive Raw Text / JSON Response| Validation[Output Validation & Parsing]
    Validation -->|7. Validate JSON Schema & Allowed Values Enums| FinalResponse[Final Clean API Response]
    FinalResponse -->|8. Return Structured JSON HTTP 200| Client

    %% GitHub-friendly Minimalist Styling
    style Client fill:#f9f9f9,stroke:#333,stroke-width:1px
    style Backend fill:#e1f5fe,stroke:#03a9f4,stroke-width:1px
    style GeminiAPI fill:#ede7f6,stroke:#673ab7,stroke-width:1px
    style Inference fill:#fff3e0,stroke:#ff9800,stroke-width:1px
    style Validation fill:#e8f5e9,stroke:#4caf50,stroke-width:1px
```

---

## 🛠️ Component Roles & Explanations

### 1. User / Client
* **Role:** Triggers the system execution.
* **Description:** Initiates an asymmetric request payload via a secure `HTTP POST` request to a specific endpoint (e.g., `/ai/classify` or `/ai/extract`).

### 2. FastAPI Backend
* **Role:** Security, gateway enforcement, and protocol handling.
* **Description:** Acts as the primary interface layer. It manages routing, enforces application middleware (like CORS policies and rate limits), and uses **Pydantic** models to rigorously typecheck incoming request bodies. If a client payload fails validation here, it halts execution immediately with an explicit `HTTP 422 Unprocessable Entity` error.

### 3. Prompt Construction Service
* **Role:** Deterministic context assembly.
* **Description:** Isolates user inputs from the direct instruction layers. This service safely injects variables into rigid, version-controlled system prompt templates to prevent prompt injection attacks and provide structural guardrails for the underlying model.

### 4. LLM Provider API (Google Gemini)
* **Role:** Network serialization and token routing.
* **Description:** Translates internal application payloads into network requests targeting Google's Gemini infrastructure. It injects active `GEMINI_API_KEY` configurations, handles connection timeouts, and routes payloads cleanly using the official Google GenAI SDK architecture.

### 5. Model Inference Engine
* **Role:** Probabilistic machine learning compute.
* **Description:** Executed entirely on Google's cloud-hosted infrastructure. The core engine ingests the context, converts characters to vector tokens, routes calculations through the model weights, and iteratively predicts the mathematical sequence of response tokens.

### 6. Response Handler
* **Role:** Network streaming or block resolution.
* **Description:** Receives incoming network chunks or completed unary bodies returned by the Google API. It converts network stream protocols into a clean string or primitive JSON data type block while intercepting premature connection failures.

### 7. Output Validation & Parsing
* **Role:** Structural assertion and reliability enforcement.
* **Description:** Evaluates the unstructured text response. It attempts to parse raw strings into targeted **Pydantic schemas**, verifying that keys exist and that string tokens conform to programmatic application invariants like fixed **Python Enums**.

### 8. Final Clean API Response
* **Role:** Synchronous client handoff.
* **Description:** Standardizes output structure. It wraps the fully validated data objects into a finalized web frame, returning a structured `HTTP 200 OK` JSON response seamlessly back down the network connection to the client runtime.

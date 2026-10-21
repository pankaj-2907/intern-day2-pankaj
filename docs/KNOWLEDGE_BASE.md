# Knowledge Base Architecture & Design

This document details the structure, ingestion flow, and vector initialization of the document dataset used in the RAG pipeline.

---

## 1. Dataset Structure
The knowledge base resides in `data/documents.json` and consists of a JSON array of document objects. Each document object adheres strictly to the following schema:
* `id` (String): A unique identifier (e.g., `"doc_001"`).
* `title` (String): A concise descriptive title of the document topic.
* `content` (String): Non-empty textual body containing technical or business information.

---

## 2. Number of Documents
* **Total Documents:** 20 synthetic documents covering core technical domains including API security, FastAPI architecture, vector embeddings, RAG workflows, testing, and system architecture.

---

## 3. Supported Content Format
* **Format:** UTF-8 encoded JSON format.
* **Validation:** Validated at startup using schema checks to ensure no document contains empty titles or missing fields.

---

## 4. How Documents Are Loaded
1. The application reads `data/documents.json` during service startup or initialization.
2. Each record is parsed and checked for required keys (`id`, `title`, `content`).
3. Invalid or duplicate IDs are rejected to maintain index integrity.

---

## 5. How Document Embeddings Are Generated
1. Document text (or chunks) are passed to the `embedding_service`.
2. The Google GenAI SDK (`text-embedding-004`) processes the text string.
3. A dense vector embedding list of floating-point numbers is returned and associated with the respective document chunk.

---

## 6. How the Searchable Index Is Initialized
1. The `SearchService` (or `RetrievalService`) loads the raw documents from storage.
2. It loops through each document, calls the embedding generator, and stores tuples of `(metadata, vector)` in active memory.
3. Once initialized, the index is ready to receive incoming queries for cosine similarity ranking.
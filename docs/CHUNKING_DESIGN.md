# Document Chunking Design & Strategy

This document outlines the architectural decisions, parameters, and trade-offs made during the implementation of the document chunking service.

---

## 1. Chosen Strategy
We use a **Character-Based Sliding Window Chunking Strategy**. Rather than splitting strictly by sentences or paragraphs (which can vary wildly in length), a fixed character length with sliding overlap ensures predictable chunk sizing for vector embeddings.

---

## 2. Configuration Parameters
* **Chunk Size (`chunk_size = 300` characters):** Balances granularity and context. 300 characters roughly equates to 2-4 sentences, providing enough local context for semantic search without diluting the vector representation.
* **Chunk Overlap (`chunk_overlap = 50` characters):** Ensures that words or concepts bridging two boundaries aren't split off or lost between adjacent chunks.

---

## 3. Metadata Preservation
Every generated chunk retains explicit traceability back to its origin:
* `chunk_id`: Unique identifier (e.g., `doc_001_chunk_001`).
* `document_id`: Links the chunk to its parent document.
* `title`: Retains the parent document title for human readability and LLM grounding context.

---

## 4. Edge Case Handling
* **Empty Documents:** Returns an empty list (`[]`) without crashing.
* **Short Documents:** If a document's length is less than or equal to `chunk_size`, it produces a single chunk identical to the content.
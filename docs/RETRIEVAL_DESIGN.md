# Retrieval Pipeline Design & Architecture

This document describes how the retrieval system processes queries, matches chunks, and ranks results.

---

## 1. Retrieval Flow
1. **Query Ingestion:** User provides a natural language question via the API.
2. **Query Embedding:** The question is passed to `embedding_service` to generate its semantic vector representation.
3. **Similarity Computation:** The query vector is compared against all pre-computed document chunk embeddings using **Cosine Similarity**.
4. **Ranking & Top-K Selection:** Chunks are sorted in descending order of their similarity score, and the top-$K$ results are returned along with their source metadata and scores.

---

## 2. Guardrails & Error Handling
* **Empty Queries:** Validated and rejected with a `ValueError`.
* **Empty Index:** Gracefully returns an empty list (`[]`) if no chunks are loaded.
* **Invalid `top_k`:** Enforces `top_k > 0`.
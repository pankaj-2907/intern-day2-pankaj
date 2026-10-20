# In-Memory Vector Indexing & Lifecycle

This document outlines how the document dataset is initialized, loaded, and updated within the Semantic Document Search API.

## 1. Index Initialization (`_initialize_index`)
When the FastAPI application boots up, the `SearchService` class singleton (`search_service`) is instantiated. During its initialization:
1. **Dataset Loading:** The application reads the raw JSON file from disk (`data/documents.json`).
2. **Embedding Generation:** For every document object, the `content` field is sent to Google's embedding model via `embedding_service.generate_embedding()`.
3. **In-Memory Storage:** The raw document metadata (ID, title, content) and their corresponding multi-dimensional vectors are stored concurrently in parallel lists (`self.documents` and `self.document_embeddings`), acting as a lightweight in-memory vector index.

* **Design Choice:** Pre-computing embeddings at startup eliminates runtime latency during search requests, ensuring sub-second response times for incoming queries.

## 2. Index Updates & Evolution
Because this implementation utilizes an in-memory index optimized for lightweight demonstration and performance:
* **Static Refresh (Restart):** If `data/documents.json` is modified (e.g., adding, updating, or deleting documents), restarting the FastAPI server (`uvicorn app.main:app --reload`) automatically triggers `_initialize_index()`, re-reading the dataset and refreshing the index.
* **Dynamic Scaling (Production Considerations):** In a production environment scaling beyond thousands of documents, this in-memory index can be seamlessly swapped out for a persistent vector database (like ChromaDB, Pinecone, or pgvector) while maintaining the exact same `SearchService` interface contract.
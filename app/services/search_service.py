import json
import os
from pathlib import Path
from app.services.embedding_service import generate_embedding
from app.services.similarity_service import cosine_similarity

class SearchService:
    def __init__(self, data_path: str = "data/documents.json"):
        self.data_path = data_path
        self.documents = []
        self.document_embeddings = []
        self._initialize_index()

    def _initialize_index(self):
        """
        Loads the document dataset from disk and pre-computes embeddings for all documents.
        This serves as our in-memory vector index.
        """
        path = Path(self.data_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")

        with open(path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        if not self.documents:
            return

        # Pre-compute embeddings for each document in the dataset
        self.document_embeddings = []
        for doc in self.documents:
            content = doc.get("content", "")
            # Generate embedding for the document content
            embedding = generate_embedding(content)
            self.document_embeddings.append(embedding)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Accepts a natural language query, generates its embedding, computes similarity
        against all document embeddings, ranks them, and returns top-K results.
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be a positive integer greater than 0.")

        if not self.documents:
            return []

        # 1. Generate query embedding
        query_embedding = generate_embedding(query)

        # 2. Compute similarity scores for all documents
        scored_results = []
        for idx, doc in enumerate(self.documents):
            doc_embedding = self.document_embeddings[idx]
            score = cosine_similarity(query_embedding, doc_embedding)
            
            scored_results.append({
                "id": doc.get("id"),
                "title": doc.get("title"),
                "content": doc.get("content"),
                "score": round(float(score), 4)
            })

        # 3. Sort documents by similarity score in descending order (highest score first)
        scored_results.sort(key=lambda x: x["score"], reverse=True)

        # 4. Return top-K results, ensuring no duplicates
        seen_ids = set()
        unique_results = []
        for res in scored_results:
            if res["id"] not in seen_ids:
                seen_ids.add(res["id"])
                unique_results.append(res)
            if len(unique_results) >= top_k:
                break

        return unique_results

    def add_document(self, doc_id: str, title: str, content: str) -> None:
        """
        Validates duplicate ID, generates embedding, and adds the new document to the in-memory index.
        """
        # 1. Check for duplicate IDs
        if any(doc["id"] == doc_id for doc in self.documents):
            raise ValueError(f"Document with ID '{doc_id}' already exists.")
        
        # 2. Generate embedding for the new content
        try:
            embedding = generate_embedding(content)
        except Exception as e:
            raise RuntimeError(f"Embedding generation failed: {str(e)}")
        
        # 3. Add to in-memory index
        self.documents.append({
            "id": doc_id,
            "title": title,
            "content": content
        })
        self.document_embeddings.append(embedding)

    def get_all_documents(self) -> list[dict]:
        """
        Returns a list of all available documents with their IDs and titles (hiding raw embeddings).
        """
        return [{"id": doc["id"], "title": doc["title"]} for doc in self.documents]

# Singleton instance for dependency injection or direct usage
search_service = SearchService()
import json
import os
import numpy as np
from app.services.chunking_service import chunk_document
from app.services.embedding_service import generate_embedding

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Calculates cosine similarity between two vectors."""
    if len(v1) != len(v2):
        raise ValueError("Vectors must have the same dimension")
    
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
        
    return float(dot_product / (norm1 * norm2))

class RetrievalService:
    def __init__(self, documents_path: str = "data/documents.json"):
        self.chunks = []  # Stores chunk dicts: {chunk_id, document_id, title, content}
        self.chunk_embeddings = []  # Stores corresponding embedding vectors
        self.load_and_index_documents(documents_path)

    def load_and_index_documents(self, path: str):
        """Loads documents from JSON, chunks them, generates embeddings, and indexes them."""
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            raw_docs = json.load(f)

        for doc in raw_docs:
            # 1. Chunk each document using chunking_service
            doc_chunks = chunk_document(doc, chunk_size=300, chunk_overlap=50)
            
            for chunk in doc_chunks:
                # 2. Generate embedding for each chunk's content
                try:
                    embedding = generate_embedding(chunk["content"])
                    self.chunks.append(chunk)
                    self.chunk_embeddings.append(embedding)
                except Exception:
                    # Skip or handle embedding generation failure gracefully during indexing
                    continue

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Accepts a query, generates its embedding, compares with chunk embeddings,
        and returns the top-K relevant chunks with similarity scores.
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
            
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        if not self.chunks or not self.chunk_embeddings:
            return []

        # Generate embedding for the user query
        query_embedding = generate_embedding(query)

        scores = []
        for i, chunk_embed in enumerate(self.chunk_embeddings):
            score = cosine_similarity(query_embedding, chunk_embed)
            scores.append((score, i))

        # Sort by similarity score in descending order
        scores.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, idx in scores[:top_k]:
            chunk_data = self.chunks[idx].copy()
            chunk_data["score"] = round(score, 4)
            results.append(chunk_data)

        return results
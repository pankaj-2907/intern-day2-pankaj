import math

def dot_product(vec1: list[float], vec2: list[float]) -> float:
    """
    Computes the dot product of two numerical vectors of equal length.
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same length for dot product computation.")
    
    return sum(a * b for a, b in zip(vec1, vec2))


def vector_magnitude(vec: list[float]) -> float:
    """
    Computes the Euclidean norm (magnitude/length) of a vector.
    """
    return math.sqrt(sum(a * a for a in vec))


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Computes the cosine similarity between two vectors.
    Formula: cos(theta) = (A . B) / (||A|| * ||B||)
    Returns a score between -1.0 and 1.0 (typically 0.0 to 1.0 for normalized text embeddings).
    """
    if not vec1 or not vec2:
        raise ValueError("Vectors cannot be empty.")
        
    if len(vec1) != len(vec2):
        raise ValueError(f"Vector dimensions must match. Got {len(vec1)} and {len(vec2)}.")

    mag1 = vector_magnitude(vec1)
    mag2 = vector_magnitude(vec2)

    if mag1 == 0.0 or mag2 == 0.0:
        raise ValueError("Cannot compute cosine similarity for zero-magnitude vectors.")

    return dot_product(vec1, vec2) / (mag1 * mag2)
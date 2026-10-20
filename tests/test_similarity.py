import pytest
from app.services.similarity_service import cosine_similarity, dot_product, vector_magnitude

def test_identical_vectors():
    """Test similarity for identical vectors (should be close to 1.0)."""
    vec1 = [1.0, 2.0, 3.0]
    vec2 = [1.0, 2.0, 3.0]
    score = cosine_similarity(vec1, vec2)
    assert score == pytest.approx(1.0, abs=1e-6)


def test_orthogonal_vectors():
    """Test similarity for orthogonal/perpendicular vectors (should be close to 0.0)."""
    vec1 = [1.0, 0.0]
    vec2 = [0.0, 1.0]
    score = cosine_similarity(vec1, vec2)
    assert score == pytest.approx(0.0, abs=1e-6)


def test_opposite_vectors():
    """Test similarity for exact opposite vectors (should be close to -1.0)."""
    vec1 = [1.0, 2.0, 3.0]
    vec2 = [-1.0, -2.0, -3.0]
    score = cosine_similarity(vec1, vec2)
    assert score == pytest.approx(-1.0, abs=1e-6)


def test_different_dimensions():
    """Test that comparing vectors of different lengths raises a ValueError."""
    vec1 = [1.0, 2.0]
    vec2 = [1.0, 2.0, 3.0]
    with pytest.raises(ValueError):
        cosine_similarity(vec1, vec2)


def test_empty_vectors():
    """Test that passing empty vectors raises a ValueError."""
    with pytest.raises(ValueError):
        cosine_similarity([], [])


def test_zero_magnitude_vectors():
    """Test that zero-magnitude vectors raise a ValueError to prevent division by zero."""
    vec1 = [0.0, 0.0, 0.0]
    vec2 = [1.0, 2.0, 3.0]
    with pytest.raises(ValueError):
        cosine_similarity(vec1, vec2)


def test_numerical_range_and_tolerance():
    """Verify that valid non-zero normalized vectors stay within [-1.0, 1.0]."""
    vec1 = [0.5, 0.5, 0.5, 0.5]
    vec2 = [0.1, 0.8, 0.3, 0.4]
    score = cosine_similarity(vec1, vec2)
    assert -1.0 <= score <= 1.0
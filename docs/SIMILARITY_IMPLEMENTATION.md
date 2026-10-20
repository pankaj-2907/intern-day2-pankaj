# Similarity Implementation & Mathematical Foundations

This document details the implementation of vector similarity metrics used in the Semantic Document Search API.

## Mathematical Formulation
Cosine similarity measures the cosine of the angle between two multi-dimensional vectors, quantifying how directionally aligned their semantic meanings are.

$$\cos(\theta) = \frac{A \cdot B}{\vert{}\vert{}A\vert{}\vert{} \times \vert{}\vert{}B\vert{}\vert{}}$$

Where:
- $A \cdot B$ is the dot product of vectors $A$ and $B$.
- $\vert{}\vert{}A\vert{}\vert{}$ and $\vert{}\vert{}B\vert{}\vert{}$ represent the Euclidean norms (magnitudes) of the respective vectors.

## Edge Case Handling
The service layer (`app/services/similarity_service.py`) incorporates robust validation checks:
1. **Dimension Mismatch:** Validates that both vectors share identical lengths; raises `ValueError` otherwise.
2. **Empty Inputs:** Prevents computation on empty lists.
3. **Zero Magnitudes:** Catches zero-magnitude vectors to avoid division-by-zero runtime exceptions.

## Unit Test Coverage
All core scenarios are verified using `pytest` in `tests/test_similarity.py`:
- **Identical Vectors:** Verifies a score of $1.0$ within floating-point tolerance.
- **Orthogonal Vectors:** Verifies a score of $0.0$ for perpendicular vectors.
- **Opposite Vectors:** Verifies a score of $-1.0$ for inverse vectors.
- **Dimension & Shape Errors:** Confirms proper exception raising for mismatched sizes or empty inputs.
- **Range Boundaries:** Ensures all valid semantic scores stay strictly within $[-1.0, 1.0]$.
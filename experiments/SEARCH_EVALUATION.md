# Search Quality Evaluation Report

This document reports the actual evaluation metrics, qualitative analysis, and system limitations for the Semantic Document Search API based on real test script runs.

---

## 1. Evaluation Metrics Definitions

1. **Precision@3**: 
   - *Definition*: The proportion of top-3 retrieved documents that are actually relevant to the query.
   - *Formula*: $\text{Precision@3} = \frac{\vert{}\text{Relevant Docs in Top 3}\vert{}}{3}$

2. **Recall@3**:
   - *Definition*: The proportion of all known relevant documents that are retrieved within the top-3 results.
   - *Formula*: $\text{Recall@3} = \frac{\vert{}\text{Relevant Docs in Top 3}\vert{}}{\vert{}\text{Total Known Relevant Docs}\vert{}}$

3. **Mean Reciprocal Rank (MRR)**:
   - *Definition*: The average of the reciprocal ranks of the first relevant document retrieved across all test queries.
   - *Formula*: $\text{MRR} = \frac{1}{\vert{}Q\vert{}} \sum_{i=1}^{\vert{}Q\vert{}} \frac{1}{\text{rank}_i}$

---

## 2. Actual Evaluation Results

Running the evaluation script (`python -m scripts.evaluate`) across 10 test queries yielded the following metrics:

* **Average Precision@3**: **0.20**
* **Average Recall@3**: **0.70**
* **Mean Reciprocal Rank (MRR)**: **0.53**

---

## 3. Qualitative Case Analysis

### Case A: Query Uses Different Words (Semantic Paraphrasing)
* **Query**: *"Securing web services and endpoints"*
* **Relevant Doc**: `doc_001`
* **Observation**: Successfully retrieved `doc_001` at Rank 1, showing that semantic embedding (`text-embedding-004`) bridges vocabulary gaps effectively even with phrasing variations.

### Case B: Multiple Documents / Related Concepts
* **Query**: *"How can I prevent unauthorized API usage?"*
* **Relevant Doc**: `doc_001`
* **Observation**: Retrieved `['doc_001', 'doc_008', 'doc_010']`. The correct document was found at Rank 1 (yielding $RR = 1.00$), though other retrieved neighbor documents lowered the Precision@3 ratio.

### Case C: Dataset Has No Clearly Relevant Document
* **Query**: *"What is quantum computing and dark matter?"*
* **Relevant Docs**: `[]` (None)
* **Observation**: Retrieved `['doc_002', 'doc_008', 'doc_006']`. Because there is no similarity cutoff threshold, the system still returned the top-3 nearest neighborhood vectors, demonstrating the necessity for minimum score filtering.

---

## 4. Observed Failures & Limitations
1. **Low Precision@3 (0.20)**: Since `top_k=3` always returns 3 results even when only 1 document is relevant, Precision@3 is capped at $1/3 \approx 0.33$ per single-relevant query, bringing down the macro average.
2. **Domain Mismatch for Specific Topics**: Queries regarding software testing (`doc_021`) failed to rank in the top-3 because other general documents scored higher similarity distances in the current small vector space.
3. **Absence of Score Cutoff**: Out-of-domain queries (like quantum computing) still return arbitrary documents instead of safely returning empty results.
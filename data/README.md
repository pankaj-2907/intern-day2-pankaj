# Dataset Documentation

This directory contains the core document dataset and evaluation queries used by the Semantic Document Search API.

## Files
- `documents.json`: Contains 20 distinct synthetic technical and business documents spanning API development, cloud infrastructure, cybersecurity, machine learning, DevOps, and database management.
- `evaluation_queries.json`: Contains test queries with expected relevant document IDs used for evaluating search precision, recall, and MRR.

## Document Structure
Each document entry in `documents.json` strictly adheres to the following JSON schema:
```json
{
  "id": "doc_001",
  "title": "Document Title",
  "content": "Detailed descriptive text content used for generating vector embeddings."
}
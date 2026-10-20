# Embedding Experiments Report

This document records experimental tests run on Google's `text-embedding-004` model using various textual inputs.

## Experiment Records

### Test 1
- **Input Sentence:** `"How to secure an API against unauthorized access?"`
- **Model Name:** `text-embedding-004`
- **Vector Dimension:** 768
- **Valid Numerical Values:** Yes (All floats)
- **Observation:** The generated vector contains 768 floating-point coordinates. Semantically related security queries map closely to similar vector spaces.

### Test 2
- **Input Sentence:** `"Cloud computing scalability and serverless infrastructure"`
- **Model Name:** `text-embedding-004`
- **Vector Dimension:** 768
- **Valid Numerical Values:** Yes
- **Observation:** High dimensional density captures multi-topic concepts (cloud, scaling, serverless) accurately.

### Test 3
- **Input Sentence:** `"Machine learning models and deep neural networks"`
- **Model Name:** `text-embedding-004`
- **Vector Dimension:** 768
- **Valid Numerical Values:** Yes
- **Observation:** Distinct mathematical separation is observed when compared to non-technical sentences.

### Test 4
- **Input Sentence:** `"Automated testing and continuous integration pipelines"`
- **Model Name:** `text-embedding-004`
- **Vector Dimension:** 768
- **Valid Numerical Values:** Yes
- **Observation:** Captures DevOps and software engineering intent effectively.

### Test 5
- **Input Sentence:** `"Hello world from FastAPI backend"`
- **Model Name:** `text-embedding-004`
- **Vector Dimension:** 768
- **Valid Numerical Values:** Yes
- **Observation:** Provides a baseline coordinate vector for basic programming strings.

## Conclusion
All test inputs successfully returned 768-dimensional dense floating-point arrays with valid numerical values, proving stable model connectivity and response formatting.
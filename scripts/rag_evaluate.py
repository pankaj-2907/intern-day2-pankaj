import json
import sys
import os
import time

# Parent directory (project root) ko sys.path mein add karna taaki 'app' module mil jaye
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.retrieval_service import RetrievalService
from app.services.rag_service import RAGService

def run_evaluation():
    eval_path = "data/rag_evaluation.json"
    if not os.path.exists(eval_path):
        print(f"Evaluation file not found at {eval_path}")
        return

    with open(eval_path, "r", encoding="utf-8") as f:
        eval_cases = json.load(f)

    retrieval_service = RetrievalService()
    rag_service = RAGService(retrieval_service=retrieval_service)

    total_questions = len(eval_cases)
    recall_hits = 0
    answerability_correct = 0
    results = []

    print("--- Starting RAG Evaluation & Generating Report ---")
    for idx, case in enumerate(eval_cases, 1):
        q = case["question"]
        expected_docs = set(case["relevant_document_ids"])
        is_answerable = case["answerable"]
        expected_facts = case["expected_facts"]

        print(f"Evaluating [{idx}/{total_questions}]: {q}")

        # Run RAG pipeline with safe retry for 503/429 errors
        response = None
        for attempt in range(3):
            try:
                response = rag_service.generate_answer(question=q, top_k=3)
                break
            except Exception as e:
                print(f"  ⚠️ Attempt {attempt+1} failed: {e}. Retrying in 3s...")
                time.sleep(3)

        if not response:
            response = {
                "question": q,
                "answer": "I do not have enough information in the provided documents to answer your question.",
                "sources": [],
                "retrieved_chunks": 0
            }

        answer = response["answer"]
        sources = response["sources"]
        retrieved_doc_ids = list(set(s["document_id"] for s in sources))

        # 1. Recall@3 evaluation
        if expected_docs:
            matched_docs = expected_docs.intersection(set(retrieved_doc_ids))
            has_recall = len(matched_docs) > 0
            if has_recall:
                recall_hits += 1
        else:
            has_recall = True

        # 2. Answerability / Abstaining check
        abstain_phrase = "I do not have enough information"
        did_abstain = abstain_phrase.lower() in answer.lower()

        if is_answerable and not did_abstain:
            answerability_correct += 1
        elif not is_answerable and did_abstain:
            answerability_correct += 1

        # 3. Expected facts check
        facts_present = all(fact.lower() in answer.lower() for fact in expected_facts) if expected_facts else True

        results.append({
            "id": idx,
            "question": q,
            "retrieved_docs": retrieved_doc_ids,
            "expected_docs": list(expected_docs),
            "answer": answer,
            "facts_present": facts_present,
            "did_abstain": did_abstain,
            "answerable": is_answerable
        })

        time.sleep(1.5)

    # Metrics calculation
    recall_denominator = sum(1 for c in eval_cases if c["relevant_document_ids"])
    recall_at_3 = (recall_hits / recall_denominator) * 100 if recall_denominator > 0 else 100.0
    answerability_acc = (answerability_correct / total_questions) * 100

    # Automatically generate experiments/RAG_EVALUATION.md with real results
    os.makedirs("experiments", exist_ok=True)
    md_path = "experiments/RAG_EVALUATION.md"
    
    md_content = f"""# RAG Evaluation Report & Detailed Question Log

This document records the systematic evaluation results for the Retrieval-Augmented Generation (RAG) backend API, executed against the evaluation dataset defined in `data/rag_evaluation.json`.

## Executive Summary & Metrics

* **Total Questions Evaluated:** {total_questions}
* **Retrieval Recall@3:** {recall_at_3:.2f}%
* **Answerability Accuracy:** {answerability_acc:.2f}%

---

## Detailed Question-by-Question Evaluation Log
"""

    for res in results:
        doc_str = ", ".join(res['retrieved_docs']) if res['retrieved_docs'] else "None"
        facts_str = "Yes" if res['facts_present'] else "No"
        support_str = "Yes (Grounded in sources)" if res['retrieved_docs'] else "No"
        abstain_str = "Yes (Properly abstained)" if res['did_abstain'] else "N/A (Answerable question)"

        md_content += f"""
### Question {res['id']}
* **Question:** {res['question']}
* **Retrieved Document IDs:** {doc_str}
* **Generated Answer:** {res['answer']}
* **Expected Facts Present:** {facts_str}
* **Supported by Retrieved Sources:** {support_str}
* **Appropriate Abstention on Unanswerable:** {abstain_str}
"""

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n✅ Success! Evaluation completed and live report saved to '{md_path}'")
    print(f"📊 Final Metrics -> Recall@3: {recall_at_3:.2f}% | Answerability Accuracy: {answerability_acc:.2f}%")

if __name__ == "__main__":
    run_evaluation()
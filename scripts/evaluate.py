import json
from app.services.search_service import search_service

def evaluate():
    # 1. Load evaluation queries
    with open("data/evaluation_query.json", "r") as f:
        queries = json.load(f)

    total_queries = len(queries)
    if total_queries == 0:
        print("No evaluation queries found.")
        return

    precisions = []
    recalls = []
    reciprocal_ranks = []

    print("\n--- Running Evaluation ---")
    for item in queries:
        query = item["query"]
        relevant_ids = set(item["relevant_document_ids"])

        # Run search with top_k = 3
        results = search_service.search(query=query, top_k=3)
        retrieved_ids = [res["id"] for res in results]

        # Precision@3: Relevant docs in top 3 / 3
        retrieved_set = set(retrieved_ids)
        intersection = retrieved_set.intersection(relevant_ids)
        
        p_at_3 = len(intersection) / 3.0
        precisions.append(p_at_3)

        # Recall@3: Relevant docs in top 3 / Total relevant docs
        if len(relevant_ids) > 0:
            r_at_3 = len(intersection) / len(relevant_ids)
        else:
            r_at_3 = 1.0 if len(retrieved_set.intersection(relevant_ids)) == 0 else 0.0
        recalls.append(r_at_3)

        # Reciprocal Rank (MRR)
        rr = 0.0
        for rank, doc_id in enumerate(retrieved_ids, start=1):
            if doc_id in relevant_ids:
                rr = 1.0 / rank
                break
        reciprocal_ranks.append(rr)

        print(f"Query: {query}")
        print(f"  Retrieved: {retrieved_ids}")
        print(f"  Expected: {list(relevant_ids)}")
        print(f"  P@3: {p_at_3:.2f}, R@3: {r_at_3:.2f}, RR: {rr:.2f}\n")

    # Compute averages
    avg_precision = sum(precisions) / total_queries
    avg_recall = sum(recalls) / total_queries
    mrr = sum(reciprocal_ranks) / total_queries

    print("============================")
    print(f"Average Precision@3: {avg_precision:.2f}")
    print(f"Average Recall@3: {avg_recall:.2f}")
    print(f"Mean Reciprocal Rank (MRR): {mrr:.2f}")
    print("============================")

if __name__ == "__main__":
    evaluate()
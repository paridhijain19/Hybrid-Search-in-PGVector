import json
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
from search_dense import search_dense
from search_hybrid import search_hybrid

# Load test queries
with open("claude/test_queries.json", "r") as f:
    queries = json.load(f)

# Run search and log results
results = []
for entry in queries:
    query = entry["query"] if isinstance(entry, dict) else entry

    print(f"🔍 Query: {query}")

    # Dense
    start = time.time()
    dense_results = search_dense(query)
    dense_time = time.time() - start
    dense_score = dense_results[0]["score"] if dense_results else 0
    dense_doc = dense_results[0]["doc_name"] if dense_results else "None"

    # Hybrid
    start = time.time()
    hybrid_results = search_hybrid(query)
    hybrid_time = time.time() - start
    hybrid_score = hybrid_results[0]["hybrid"] if hybrid_results else 0
    hybrid_doc = hybrid_results[0]["doc_name"] if hybrid_results else "None"

    results.append({
        "query": query,
        "dense_top_doc": dense_doc,
        "hybrid_top_doc": hybrid_doc,
        "dense_score": round(dense_score, 4),
        "hybrid_score": round(hybrid_score, 4),
        "dense_time": round(dense_time, 4),
        "hybrid_time": round(hybrid_time, 4)
    })

# Save CSV
csv_file = "dense_vs_hybrid_comparison.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Results saved to {csv_file}")

# Optional: Plot scores
df = pd.DataFrame(results)
fig, ax = plt.subplots(figsize=(10, 6))

x = range(len(df))
ax.bar(x, df["dense_score"], width=0.4, label="Dense", align='center')
ax.bar([i + 0.4 for i in x], df["hybrid_score"], width=0.4, label="Hybrid", align='center')

ax.set_xticks([i + 0.2 for i in x])
ax.set_xticklabels([f"Q{i+1}" for i in x], rotation=45)
ax.set_ylabel("Top-1 Similarity Score")
ax.set_title("Dense vs Hybrid Search Comparison")
ax.legend()
plt.tight_layout()
plt.savefig("score_comparison_chart.png")
print("📊 Bar chart saved as score_comparison_chart.png")

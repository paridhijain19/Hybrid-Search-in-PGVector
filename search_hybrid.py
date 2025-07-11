import psycopg2
import numpy as np
import json
from transformers import AutoTokenizer, AutoModel
from rank_bm25 import BM25Okapi
import torch


def search_hybrid(query, top_k=5, alpha=0.85):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def get_dense_vector(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    dense_vector = get_dense_vector(query)

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="yourpassword",    # change pwd here
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute("SELECT doc_name, chunk, dense FROM documents")
    rows = cur.fetchall()

    results = []
    tokenized_corpus = []

    # --- Collect data ---
    for doc_name, chunk, dense_str in rows:
        try:
            d_vec = np.array(json.loads(dense_str), dtype=np.float32)
        except:
            continue 

        # Dense cosine similarity
        denom = np.linalg.norm(dense_vector) * np.linalg.norm(d_vec)
        d_score = np.dot(dense_vector, d_vec) / denom if denom > 0 else 0.0

        tokenized_chunk = chunk.split()  
        tokenized_corpus.append(tokenized_chunk)

        results.append({
            "doc_name": doc_name,
            "chunk": chunk,
            "dense_score": d_score,
        })

    # --- Compute BM25 sparse scores ---
    bm25 = BM25Okapi(tokenized_corpus)
    query_tokens = query.split()
    bm25_scores = bm25.get_scores(query_tokens)

    max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1.0  

    for r, bm25_score in zip(results, bm25_scores):
        s_score = bm25_score / max_bm25  
        hybrid = alpha * r["dense_score"] + (1 - alpha) * s_score
        r["hybrid"] = hybrid

    results.sort(key=lambda x: x["hybrid"], reverse=True)
    top_results = [
        {
            "doc_name": r["doc_name"],
            "chunk": r["chunk"],
            "hybrid": r["hybrid"]
        }
        for r in results[:top_k]
    ]
    return top_results

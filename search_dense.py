import psycopg2
import numpy as np
import json

def search_dense(query, top_k=5):
    from transformers import AutoTokenizer, AutoModel
    import torch

    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def get_dense_vector(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    dense_vector = get_dense_vector(query)

    conn = psycopg2.connect(
        dbname="postgres",             # ← use "postgres" unless you've created a different DB
        user="postgres",
        password="yourpassword",        # ← your actual password
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute("""
        SELECT doc_name, chunk, dense
        FROM documents
    """)
    rows = cur.fetchall()

    results = []
    for doc_name, chunk, dense_str in rows:
        d_vec = np.array(json.loads(dense_str), dtype=np.float32)
        score = np.dot(dense_vector, d_vec) / (np.linalg.norm(dense_vector) * np.linalg.norm(d_vec))
        results.append({"doc_name": doc_name, "chunk": chunk, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

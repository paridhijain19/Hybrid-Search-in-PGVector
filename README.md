
# Hybrid Search in PGVector

## PGVector Hybrid Search Application

### Objective

This project implements a hybrid semantic search engine for financial documents (e.g., annual reports, earnings calls) using PGVector. It compares **dense-only** vs **dense+sparse (hybrid)** search strategies and presents an interactive **Streamlit UI**.

---

## Project Structure

| File | Purpose |
|------|---------|
| `extract_text.py`         | Extracts raw text from PDFs in the `/data` folder |
| `chunk_documents.py`      | Splits extracted text into 500-word chunks |
| `create_pgvector_table.py`| Initializes PGVector table in PostgreSQL |
| `generate_embeddings.py`    | Generates dense and sparse embeddings for chunks |
| `insert_embeddings.py`    | Inserts dense and sparse vectors into the database |
| `search_dense.py`         | Dense-only semantic search |
| `search_hybrid.py`        | Hybrid (dense + sparse) search |
| `app.py`                  | Streamlit UI for querying |
| `evaluation.py`           | Compares dense vs hybrid search quantitatively |

---

## Setup Instructions

### 1. Set Up PostgreSQL with PGVector

Make sure Docker is installed and run the PGVector container:

```bash
docker run -p 5432:5432 \
  -e POSTGRES_PASSWORD=#Happyday22 \
  --name pgvector \
  -d ankane/pgvector
```

> **Note:**  
> Update the `password`, `dbname`, `user`, and `host` in your Python scripts (`connect_pg.py`, `create_pgvector_table.py`, `search_dense.py`, `search_hybrid.py`) to match these credentials.

---

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

---

## Pipeline (Run in Order)

```bash
# Step 1: Extract text from PDFs (place PDFs inside /data/)
python extract_text.py

# Step 2: Chunk the text into 500-word blocks
python chunk_documents.py

# Step 3: Create the PGVector table in PostgreSQL
python create_pgvector_table.py

# Step 4: Create dense and sparse embeddings
python generate_embeddings.py

# Step 5: Insert embeddings into the PostgreSQL table
python insert_embeddings.py

# Step 6: (Optional) Run evaluation to compare dense and hybrid search
python evaluation.py

# Step 7: Run the Streamlit app
streamlit run app.py
```

---

## Output Files

| File | Description |
|------|-------------|
| `dense_vs_hybrid_comparison.csv` | Comparison of top docs, scores, and response times |
| `score_comparison_chart.png`     | Bar chart comparing dense vs hybrid search performance |

---


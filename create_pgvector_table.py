#code 6
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="yourpassword"  #change pwd here
)
cur = conn.cursor()

# Enable pgvector
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

cur.execute("DROP TABLE IF EXISTS documents;")
cur.execute("""
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    doc_name TEXT,
    chunk TEXT,
    dense VECTOR(384),     -- from MiniLM
    sparse FLOAT[]         -- TF-IDF sparse vectors
);
""")

conn.commit()
cur.close()
conn.close()

print("PGVector table created!")

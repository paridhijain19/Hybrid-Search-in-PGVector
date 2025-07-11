#code 5 
import pandas as pd
import psycopg2
import ast

df = pd.read_pickle("embedded_chunks.pkl")

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="yourpassword" # change pwd here
)
cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO documents (doc_name, chunk, dense, sparse)
        VALUES (%s, %s, %s, %s)
    """, (
        row["doc_name"],
        row["chunk"],
        row["dense"],
        row["sparse"]  
    ))

conn.commit()
cur.close()
conn.close()

print(" All chunks inserted into PGVector!")

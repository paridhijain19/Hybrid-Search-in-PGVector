#code 3
import os
from pathlib import Path
import textwrap

CHUNK_SIZE = 500  # words
INPUT_DIR = "processed"
OUTPUT_FILE = "chunks.csv"

chunks = []

for file in os.listdir(INPUT_DIR):
    if file.endswith(".txt"):
        with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
            text = f.read()
            words = text.split()
            for i in range(0, len(words), CHUNK_SIZE):
                chunk = " ".join(words[i:i+CHUNK_SIZE])
                chunks.append({
                    "doc_name": file,
                    "chunk": chunk
                })

import pandas as pd
df = pd.DataFrame(chunks)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(df)} chunks to {OUTPUT_FILE}")

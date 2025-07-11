#code 4
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle

df = pd.read_csv("chunks.csv")
texts = df["chunk"].tolist()

model = SentenceTransformer('all-MiniLM-L6-v2')
dense_embeddings = model.encode(texts, show_progress_bar=True)
vectorizer = TfidfVectorizer(max_features=5000)
sparse_embeddings = vectorizer.fit_transform(texts).toarray()
df["dense"] = dense_embeddings.tolist()
df["sparse"] = sparse_embeddings.tolist()

df.to_pickle("embedded_chunks.pkl")
pickle.dump(vectorizer, open("tfidf_vectorizer.pkl", "wb"))

print("Saved dense + sparse embeddings")
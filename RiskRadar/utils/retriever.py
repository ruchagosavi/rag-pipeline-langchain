import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def query_faiss(index, question, texts, top_k=3):
    q_embedding = model.encode([question])
    _, indices = index.search(np.array(q_embedding), top_k)
    return [texts[i] for i in indices[0]]

import faiss
import numpy as np
import os

def build_faiss_index(embeddings, save_path="vectorstore/faiss.index"):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    faiss.write_index(index, save_path)
    return index

def load_faiss_index(path="vectorstore/faiss.index"):
    return faiss.read_index(path)

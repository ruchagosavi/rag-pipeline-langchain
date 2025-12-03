# Install dependencies first:
# pip install sentence-transformers faiss-cpu langchain

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Sample documents
documents = [
    "Python is a popular programming language for web and AI.",
    "Java is commonly used for backend and Android development.",
    "React is a JavaScript library for building user interfaces.",
    "LangChain is a framework to build AI applications with LLMs."
]

#  SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

#  Documents to embeddings
embeddings = model.encode(documents)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings, dtype=np.float32))


query = "Tell me about Web development languages"
query_embedding = model.encode([query])

# Search top 2 similar documents
k = 2
distances, indices = index.search(np.array(query_embedding, dtype=np.float32), k)

print("Query:", query)
for i, idx in enumerate(indices[0]):
    print(f"{i+1}. {documents[idx]}")

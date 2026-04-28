import sys
import os

# -----------------------------
# Add project root to path
# -----------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from utils.data_loader import load_business_data
from utils.embeddings import generate_embeddings
from utils.vector_store import build_faiss_index, load_faiss_index
from utils.retriever import query_faiss
from langchain_groq import ChatGroq

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = "data/business_data.json"
FAISS_PATH = "vector-store/faiss.index"

# -----------------------------
# Load data ONCE
# -----------------------------
data, texts = load_business_data(DATA_PATH)

# -----------------------------
# Load or Build FAISS ONCE
# -----------------------------
if not os.path.exists(FAISS_PATH):
    embeddings = generate_embeddings(texts)
    index = build_faiss_index(embeddings, FAISS_PATH)
else:
    index = load_faiss_index(FAISS_PATH)

# -----------------------------
# Initialize LLM ONCE
# -----------------------------
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# Prompt Builder
# -----------------------------
def build_prompt(context: str, question: str) -> str:
    return f"""
You are a banking risk analyst.
Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer in a clean, structured format:
- Each point on a new line
- Start each point with "-"
- Keep points concise

Answer:
"""

# -----------------------------
# RAG Pipeline (CORE FUNCTION)
# -----------------------------
def run_rag(question: str) -> str:
    retrieved_chunks = query_faiss(
        index=index,
        query=question,
        texts=texts,
        top_k=5
    )

    if not retrieved_chunks:
        return "No relevant information found in the knowledge base."

    context = "\n".join(retrieved_chunks)
    prompt = build_prompt(context, question)

    response = llm.invoke(prompt)
    return response

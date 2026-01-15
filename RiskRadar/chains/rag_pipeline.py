# # import sys
# # import os

# # # Add project root to Python path
# # ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# # sys.path.append(ROOT_DIR)

# # from utils.data_loader import load_business_data, generate_embeddings, build_faiss_index
# # from utils.retriever import load_faiss_index, query_faiss

# # if __name__ == "__main__":
# #     # -----------------------------
# #     # Step 1: Load dataset
# #     # -----------------------------
# #     chunks = load_business_data('../data/business_data.json')
# #     print(f"Loaded {len(chunks)} business entries.")

# #     # -----------------------------
# #     # Step 2: Generate embedding
# #     # -----------------------------
# #     embeddings = generate_embeddings(chunks)
# #     print(f"Generated embeddings with shape: {embeddings.shape}")

# #     # -----------------------------
# #     # Step 3: Build FAISS index
# #     # -----------------------------
# #     faiss_index = build_faiss_index(embeddings)
# #     print("FAISS index built successfully.")

# #     # -----------------------------
# #     # Step 4 & 5: Query FAISS
# #     # -----------------------------
# #     faiss_index = load_faiss_index()  # Simulate new session
# #     user_query = "Businesses with negative news and low rating"
# #     top_results = query_faiss(user_query, faiss_index, chunks, top_k=5)

# #     print("\nTop-k FAISS Results:")
# #     for r in top_results:
# #         print(r)

# import sys
# import os

# # Add project root to Python path
# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(ROOT_DIR)

# from utils.data_loader import load_business_data, generate_embeddings, build_faiss_index
# from utils.retriever import query_faiss
# from langchain_community.llms import LlamaCpp  # Llama3 ChatQA

# JSON_PATH = "../data/business_data.json"  # <-- JSON file
# MODEL_PATH = "../models/llama3-chatqa.gguf"


# def build_prompt(context_chunks, question):
#     """
#     Construct ChatQA prompt using retrieved FAISS context.
#     """
#     context_text = "\n\n".join(context_chunks)
#     prompt = f"""
# You are an expert business risk analyst.
# Use only the following context to answer the question.

# ----CONTEXT----
# {context_text}
# ----------------

# Question: {question}

# Provide a short, clear, factual response based only on the context.
# """
#     return prompt


# def run_rag_pipeline(question):
#     # Step 1: Load Data
#     texts = load_business_data(JSON_PATH)  # JSON returns list of strings

#     # Step 2: Generate Embeddings
#     embeddings = generate_embeddings(texts)

#     # Step 3: Build FAISS Index
#     index = build_faiss_index(embeddings)

#     # Step 4: Query FAISS
#     top_k_chunks = query_faiss(index, question, texts, k=5)

#     # Step 5: Build prompt
#     prompt = build_prompt(top_k_chunks, question)

#     # Step 6: Load Llama3
#     llm = LlamaCpp(
#         model_path=MODEL_PATH,
#         temperature=0.1,
#         max_tokens=512
#     )

#     # Step 7: Get final answer
#     answer = llm(prompt)
#     return answer


# if __name__ == "__main__":
#     user_q = input("Enter your question: ")
#     output = run_rag_pipeline(user_q)
#     print("\nFinal Answer:")
#     print(output)


import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from utils.data_loader import load_business_data
from utils.embeddings import generate_embeddings
from utils.vector_store import build_faiss_index, load_faiss_index
from utils.retriever import query_faiss
from langchain_ollama import OllamaLLM



DATA_PATH = "data/business_data.json"
FAISS_PATH = "vector-store/faiss.index"

def build_prompt(context, question):
    return f"""
You are a banking risk analyst.
Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

def run_rag(question):
    if not os.path.exists(FAISS_PATH):
        data, texts = load_business_data(DATA_PATH)
        embeddings = generate_embeddings(texts)
        index = build_faiss_index(embeddings, FAISS_PATH)
    else:
        _, texts = load_business_data(DATA_PATH)
        index = load_faiss_index(FAISS_PATH)

    retrieved = query_faiss(index, question, texts, top_k=5)
    context = "\n".join(retrieved)

    llm = OllamaLLM(
        model="llama3.2:3b",
        temperature=0.1
    )


    prompt = build_prompt(context, question)
    return llm.invoke(prompt)


if __name__ == "__main__":
    q = input("Enter question: ")
    print(run_rag(q))

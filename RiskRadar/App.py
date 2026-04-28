from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from chains.rag_pipeline import run_rag

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(
    title="RiskRadar RAG API",
    description="Retrieval-Augmented Generation API for financial risk analysis",
    version="1.0.0"
)

# -------------------------
# CORS CONFIGURATION
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React dev
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Schema
# -------------------------
class QueryRequest(BaseModel):
    question: str

# -------------------------
# Health Check (IMPORTANT)
# -------------------------
@app.get("/")
def health_check():
    return {"status": "RiskRadar API is running 🚀"}

# -------------------------
# RAG Query Endpoint
# -------------------------
@app.post("/query")
def query_rag(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer = run_rag(req.question)
        return {"answer": answer}
    except Exception as e:
        # Log error in real production
        raise HTTPException(status_code=500, detail=str(e))

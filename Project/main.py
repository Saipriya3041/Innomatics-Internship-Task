from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from graph_flow import process_query
from human_loop import human_response

app = FastAPI(title="Customer Support RAG")

# Load DB
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

retriever = db.as_retriever(search_kwargs={"k": 3})

class AskInput(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "RAG API Running"}

@app.post("/ask")
def ask_question(data: AskInput):
    docs = retriever.invoke(data.query)

    result = process_query(data.query, docs)

    if result["route"] == "human":
        result["answer"] = human_response(data.query)

    return result

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    path = f"data/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "PDF uploaded successfully", "file": file.filename}

@app.get("/health")
def health():
    return {"status": "ok"}
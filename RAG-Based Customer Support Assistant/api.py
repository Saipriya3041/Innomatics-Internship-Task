from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AskInput(BaseModel):
    query: str

@app.post("/ask")
def ask(data: AskInput):
    return {
        "query": data.query,
        "answer": "Sample support answer"
    }
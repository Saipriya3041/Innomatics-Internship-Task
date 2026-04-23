from typing import TypedDict

class GraphState(TypedDict):
    query: str
    answer: str
    confidence: float
    route: str

def process_query(query, docs):
    if docs:
        answer = docs[0].page_content
        confidence = 0.90
        route = "final"
    else:
        answer = "Escalated to human support."
        confidence = 0.20
        route = "human"

    return {
        "query": query,
        "answer": answer,
        "confidence": confidence,
        "route": route
    }
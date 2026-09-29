from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from memory import recall_incidents

app = FastAPI(title="PostmortemLink")


class CodeChange(BaseModel):
    change: str


def detect_topic(change):
    text = change.lower()

    if any(word in text for word in [
        "payment", "timeout", "retry", "backoff"
    ]):
        return "payment"

    if any(word in text for word in [
        "database", "connection pool", "connection", "cleanup"
    ]):
        return "database"

    if any(word in text for word in [
        "order", "idempotency", "duplicate order"
    ]):
        return "order"

    return None


@app.post("/analyze")
def analyze(change: CodeChange):

    topic = detect_topic(change.change)

    # If the change does not match any known incident area,
    # do not treat Hindsight's broad semantic results as relevant.
    if topic is None:
        return {
            "found": False,
            "risk": "low",
            "recommendation": "No relevant historical incident found."
        }

    result = recall_incidents(change.change)

    memories = result.results

    topic_keywords = {
        "payment": ["payment", "timeout", "retry", "backoff"],
        "database": ["database", "connection", "pool", "cleanup"],
        "order": ["order", "idempotency", "duplicate"]
    }

    keywords = topic_keywords[topic]

    relevant_memories = [
        memory.text
        for memory in memories
        if any(keyword in memory.text.lower() for keyword in keywords)
    ]

    if not relevant_memories:
        return {
            "found": False,
            "risk": "low",
            "recommendation": "No relevant historical incident found."
        }

    return {
        "found": True,
        "risk": "high",
        "memories": relevant_memories[:5],
        "recommendation": (
            "Review the historical incidents retrieved from "
            "Hindsight before merging this change."
        )
    }


app.mount("/", StaticFiles(directory="static", html=True), name="static")
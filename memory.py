import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "postmortem-link")

if not API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing from .env")

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=API_KEY
)


def retain_incident(incident):
    """Store a production incident in Hindsight."""

    content = f"""
Incident ID: {incident['id']}
Title: {incident['title']}
Service: {incident['service']}
Problem: {incident['problem']}
Root Cause: {incident['root_cause']}
Previous Fix: {incident['fix']}
Lesson: {incident['lesson']}
"""

    return client.retain(
        bank_id=BANK_ID,
        content=content,
        document_id=incident["id"]
    )


def recall_incidents(code_change):
    """Find historical incidents relevant to a code change."""

    result = client.recall(
        bank_id=BANK_ID,
        query=f"""
Find production incidents that are directly relevant to this code change.

Code change:
{code_change}

Only consider incidents that have a clear connection to:
- the same service
- the same type of failure
- the same technical problem
- or the same root cause

If the code change is unrelated to the stored production incidents,
do not treat unrelated incidents as relevant.
"""
    )

    return result
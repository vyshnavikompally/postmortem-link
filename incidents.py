INCIDENTS = [
    {
        "id": "INC-101",
        "title": "Payment API Timeout",
        "service": "Payment API",
        "problem": "Payment requests were timing out.",
        "root_cause": "Incorrect timeout handling.",
        "fix": "Added exponential backoff and retry handling.",
        "lesson": "Payment requests need controlled retry behavior."
    },
    {
        "id": "INC-102",
        "title": "Database Connection Failure",
        "service": "User API",
        "problem": "Users experienced database connection errors.",
        "root_cause": "Connection pool exhaustion.",
        "fix": "Added connection pool limits and proper cleanup.",
        "lesson": "Database connections must be released correctly."
    },
    {
        "id": "INC-103",
        "title": "Duplicate Order Creation",
        "service": "Order API",
        "problem": "Some orders were created twice.",
        "root_cause": "Missing idempotency handling.",
        "fix": "Added idempotency keys.",
        "lesson": "Order creation must be idempotent."
    }
]
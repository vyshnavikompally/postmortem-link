# PostmortemLink: Connecting Code Changes to Lessons from Past Incidents

Software teams regularly write postmortems after production incidents. The difficult part is not documenting what happened—it is remembering those lessons when a similar code change appears weeks or months later.

A developer working on payment retries may not know that the same area previously caused a timeout incident. Another developer changing database connection handling may not remember an earlier connection-pool failure.

**PostmortemLink** is a small developer tool designed to connect these two moments: the historical incident and the new code change.

The idea is simple:

> **Before a developer merges a change, check whether the team has already experienced a similar problem.**

PostmortemLink uses **Hindsight** as its memory layer. Historical incidents are stored using Hindsight's **RETAIN** operation, and proposed code changes are checked against that accumulated knowledge using **RECALL**.

---

## The Problem: Production Lessons Are Easy to Forget

Production incidents often contain valuable information:

- What failed?
- What caused the failure?
- How was it fixed?
- What should the team remember next time?

That information may live inside postmortems, incident reports, tickets, or documentation.

However, normal development workflows are focused on the code being written today. A developer usually does not search through old postmortems every time they modify a timeout, database connection, retry mechanism, or API.

This creates a gap between **organizational memory** and **daily development**.

PostmortemLink attempts to close that gap by putting historical incident knowledge closer to the code-change workflow.

---

## The Solution

PostmortemLink provides a simple interface where a developer enters a proposed code change.

For example:

```text
Improve payment timeout handling and retry logic

The application sends the change to Hindsight and uses RECALL to retrieve relevant historical memories.

If a related incident is found, the application displays the historical incident and recommends reviewing it before merging the change.

The basic flow is:

Historical Incidents
        |
        | RETAIN
        v
    Hindsight
        |
        | RECALL
        v
  Proposed Code Change
        |
        v
Relevant Historical Incident
        |
        v
Review Previous Fix / Lesson
Architecture

The architecture separates the system into two flows.

Background knowledge flow

Historical incidents are stored in Hindsight using RETAIN.

Real-time analysis flow

A new code change is sent through PostmortemLink, which calls Hindsight RECALL to retrieve potentially relevant historical incidents.

Using Hindsight RETAIN

The demo contains three sample production incidents:

Payment API Timeout
Incorrect timeout handling
Fixed with exponential backoff and retry handling
Database Connection Failure
Connection pool exhaustion
Fixed with connection pool limits and proper cleanup
Duplicate Order Creation
Missing idempotency handling
Fixed with idempotency keys

Each incident is converted into structured text before being stored.

The core RETAIN integration is:

return client.retain(
    bank_id=BANK_ID,
    content=content,
    document_id=incident["id"]
)

This allows the incident information to become part of the Hindsight memory bank.

The application keeps the Hindsight API key outside the source code using an environment variable:

HINDSIGHT_API_KEY=your_api_key
HINDSIGHT_BANK_ID=postmortem-link

The API key is intentionally excluded from the Git repository.

Using Hindsight RECALL

When a developer enters a code change, PostmortemLink sends it to Hindsight.

The relevant code is:

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

The returned memories are then checked by the application before being shown to the developer.

This creates a simple pattern:

RETAIN historical knowledge → RECALL that knowledge during development.

A Before-and-After Example

Without PostmortemLink, a developer might enter a change such as:

Improve payment timeout handling and retry logic

They could make the change without remembering that payment timeout handling had previously caused a production incident.

With PostmortemLink, the same change produces a warning.

The application retrieves the historical Payment API timeout incident and shows the previous problem, root cause, fix, and lesson.

The developer can then review the previous retry and backoff solution before merging the new change.

The result is not an automatic code rejection. Instead, it provides context at the moment when the developer can use it.

Payment Demo

Testing Relevance

One important problem appeared while building the prototype.

Semantic memory retrieval can sometimes return information that is broadly related to the query but not actually relevant to the specific code change.

For example, an unrelated UI change such as:

Update the user profile page styling and button colors

could potentially retrieve memories that contain common technical terms even though the historical incident has nothing to do with the UI change.

For this reason, the MVP adds a lightweight relevance guard.

The application first detects whether the change belongs to one of the incident areas represented in the demo:

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

If no known topic is detected, the application reports that no relevant historical incident was found rather than presenting an unrelated memory.

This is deliberately a simple MVP approach rather than pretending that semantic retrieval alone solves relevance perfectly.

Three Demo Scenarios

The prototype was tested with three different inputs.

1. Related Payment Change
Improve payment timeout handling and retry logic

The application retrieves the historical Payment API timeout incident.

The result highlights the previous retry/backoff solution and recommends reviewing the historical incident.

2. Related Database Change
Fix database connection pool exhaustion and ensure connections are cleaned up

The application retrieves the historical database connection failure.

The previous connection-pool problem and cleanup lesson are surfaced to the developer.

3. Unrelated UI Change
Update the user profile page styling and button colors

No relevant historical incident is presented.

This third test is important because a memory system should not simply display whatever information it can retrieve. The useful behavior is retrieving relevant history.

What the Developer Sees

The interface is intentionally simple.

The developer enters a code change and clicks Analyze Change.

PostmortemLink then displays one of two outcomes:

⚠ Similar Historical Incidents Found

or:

✓ No Similar Incident Found

When an incident is found, the interface displays the memories returned from Hindsight along with a recommendation to review the historical incidents before merging.

The prototype uses:

Python
FastAPI
Hindsight
HTML
CSS
JavaScript

The backend handles the Hindsight integration, while the frontend provides the developer-facing workflow.

Why This Approach Matters

The main idea behind PostmortemLink is not to replace developers or automatically decide whether a change is safe.

Instead, it makes historical engineering knowledge easier to access.

A useful development workflow can be summarized as:

Write Code
    ↓
Check Historical Memory
    ↓
Find Similar Incident?
    ↓
Review Previous Lesson
    ↓
Make an Informed Change

This turns postmortems from documents that are mostly consulted after failures into knowledge that can also be useful before a potential failure.

Limitations and What We Learned

PostmortemLink is currently a prototype, so there are important limitations.

First, the incident dataset used in the demo is intentionally small. It contains three sample incidents, so the system does not yet represent the full range of production incidents that a real engineering organization would have.

Second, semantic retrieval does not automatically guarantee perfect relevance. During development, unrelated changes could produce broadly related memories. The prototype therefore adds a deterministic topic/relevance guard.

Third, the current application analyzes manually entered code-change descriptions. A future version could integrate directly with GitHub pull requests, commits, changed files, or CI pipelines so developers would not have to enter the change manually.

Finally, the current recommendation is informational. PostmortemLink does not automatically block a deployment or claim that a change will cause an incident. It surfaces historical context so the developer can make the final decision.

What's Next

The next version could connect PostmortemLink directly to the development workflow.

For example:

GitHub Pull Request
        ↓
Changed Files / Commit
        ↓
PostmortemLink
        ↓
Hindsight RECALL
        ↓
Historical Incidents
        ↓
PR Warning / Context

The system could also continuously RETAIN new postmortems and incident reports, allowing the memory bank to grow as the engineering team learns.

Over time, this could create a feedback loop:

Incident
   ↓
Postmortem
   ↓
Hindsight RETAIN
   ↓
Organizational Memory
   ↓
Future Code Change
   ↓
Hindsight RECALL
   ↓
Previous Lesson

The goal is straightforward: make yesterday's production lessons available when today's code is being written.

That is the idea behind PostmortemLink.

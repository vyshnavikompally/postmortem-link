# PostmortemLink

PostmortemLink connects today's code changes with yesterday's production incidents.

## Problem

Important lessons from production incidents are often forgotten when new code changes are made.

A developer may unknowingly introduce a change similar to something that previously caused a production failure.

## Solution

PostmortemLink stores historical production incidents in Hindsight and recalls relevant memories when a developer enters a new code change.

The flow is:

Code Change
↓
PostmortemLink
↓
Hindsight RECALL
↓
Relevant Historical Incident
↓
Previous Fix / Lesson

## How It Works

1. Historical production incidents are stored in Hindsight using RETAIN.
2. A developer enters a proposed code change.
3. PostmortemLink sends the change to Hindsight using RECALL.
4. Relevant historical incidents are returned.
5. The developer can review the previous root cause and fix before merging.

## Example

Input:

Improve payment timeout handling and retry logic

PostmortemLink retrieves the previous Payment API timeout incident and its previous retry/backoff solution.

For an unrelated change such as:

Update the user profile page styling and button colors

PostmortemLink reports:

No Similar Historical Incident Found.

## Tech Stack

- Python
- FastAPI
- Hindsight
- HTML
- CSS
- JavaScript

## Project Structure

```text
postmortem-link/
├── app.py
├── incidents.py
├── memory.py
├── test_memory.py
├── requirements.txt
├── ├── .gitignoregit 
└── static/
    ├── index.html
    ├── app.js
    └── style.css
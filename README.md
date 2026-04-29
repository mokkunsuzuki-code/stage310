# Stage310 REMEDA Trust Score Visualization

Stage310 adds a human-readable Trust Score visualization layer to REMEDA.

## Core Concept

Before Stage310:

```text
verification result → JSON

After Stage310:

verification result → Trust Score → visual decision dashboard

This makes REMEDA easier to understand, demonstrate, sell, and explain.

What Stage310 Adds
Trust Score dashboard
accept / pending / reject visualization
Trust breakdown by category
Integrity trust
Execution trust
Identity trust
Time trust
Sigstore trust
Manifest hash evidence
Policy threshold display
Verification history
API endpoint
Why This Stage Matters

Stage310 maximizes product value because trust must be visible.

A verification engine is valuable, but a visible trust dashboard is easier for users, customers, reviewers, and partners to understand.

Trust Model
Trust Score =
average(
  integrity,
  execution,
  identity,
  time,
  sigstore
)
Decision Policy
trust_score >= 0.85  → accept
trust_score >= 0.45  → pending
trust_score < 0.45   → reject

Fail-closed is enabled.

Run Locally
pip install -r requirements.txt
python app.py

Open:

http://127.0.0.1:3100
API
curl -X POST http://127.0.0.1:3100/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "manifest": {
      "claims": {
        "execution": true,
        "identity": true,
        "integrity": true,
        "timestamp": true,
        "workflow": "github-actions",
        "sigstore": true,
        "policy_version": "v1"
      }
    }
  }'
License

MIT License

Copyright (c) 2025 Motohiro Suzuki

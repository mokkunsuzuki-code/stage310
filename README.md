# Stage310 REMEDA Trust Score Visualization

Stage310 introduces a Trust Score visualization layer for REMEDA.

This stage transforms verification results into a human-readable trust decision.

---

## Core Concept

Before:

verification result → JSON only

After:

verification result → Trust Score → Visual Decision Dashboard

---

## What This Stage Adds

- Trust Score visualization (0.0 - 1.0)
- accept / pending / reject decision UI
- Trust Breakdown:
  - Integrity
  - Execution
  - Identity
  - Time
  - Sigstore
- Evidence JSON display
- Verification history
- API endpoint (/api/verify)

---

## Trust Model

Trust Score = average(
  integrity,
  execution,
  identity,
  time,
  sigstore
)

---

## Decision Policy

trust_score >= 0.85 → accept  
trust_score >= 0.45 → pending  
trust_score < 0.45 → reject  

Fail-closed is enabled.

---

## Why This Matters

Trust must be visible.

Stage310 converts verification into something that:
- users can understand
- engineers can validate
- businesses can sell

---

## Run

pip install -r requirements.txt  
python app.py  

http://127.0.0.1:3100

---

## API Example

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

---

## License

MIT License

Copyright (c) 2025 Motohiro Suzuki

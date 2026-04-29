# Stage310 REMEDA Trust Score URL + External Verification API

Stage310 transforms verification results into a **visual and shareable Trust Score system**.

---

## Core Concept

Before Stage310:

verification result → JSON

After Stage310:

verification result → Trust Score → Public URL → API

---

## What Stage310 Adds

- Trust Score visualization (0.0 - 1.0)
- accept / pending / reject decision
- Public Trust URL (/trust/<id>)
- External API (/api/verify, /api/trust/<id>)
- Trust breakdown:
  - Integrity
  - Execution
  - Identity
  - Time
  - Sigstore (current: declared)
- Evidence JSON
- Fail-closed policy

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

Stage310 converts verification into something that:

- users can understand instantly
- engineers can validate
- systems can consume via API
- businesses can share via URL

---

## Run

pip install -r requirements.txt  
python app.py  

http://127.0.0.1:3110

---

## API Example

curl -X POST http://127.0.0.1:3110/api/verify \
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

## Next Stage

Stage311 will introduce **real Sigstore verification**.

---

## License

MIT License

Copyright (c) 2025 Motohiro Suzuki

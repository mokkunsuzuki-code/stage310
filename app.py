from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import hashlib
import json

app = Flask(__name__)

HISTORY = []

HTML = """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>Stage310 REMEDA Trust Score Visualization</title>
  <style>
    body { font-family: system-ui, sans-serif; background:#0f172a; color:#e5e7eb; margin:0; }
    header { padding:32px; background:#111827; border-bottom:1px solid #334155; }
    main { padding:32px; max-width:1100px; margin:auto; }
    .card { background:#111827; border:1px solid #334155; border-radius:16px; padding:24px; margin-bottom:24px; }
    input, textarea { width:100%; padding:12px; border-radius:10px; border:1px solid #475569; background:#020617; color:#e5e7eb; }
    button { padding:12px 20px; border:0; border-radius:10px; background:#38bdf8; color:#020617; font-weight:700; cursor:pointer; }
    .score { font-size:56px; font-weight:800; }
    .accept { color:#22c55e; }
    .pending { color:#facc15; }
    .reject { color:#ef4444; }
    .bar { background:#334155; border-radius:999px; height:18px; overflow:hidden; }
    .fill { height:100%; background:#38bdf8; }
    .grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }
    .mini { background:#020617; padding:16px; border-radius:14px; border:1px solid #334155; }
    pre { background:#020617; padding:16px; border-radius:12px; overflow:auto; }
    table { width:100%; border-collapse:collapse; }
    th, td { border-bottom:1px solid #334155; padding:10px; text-align:left; }
  </style>
</head>
<body>
<header>
  <h1>Stage310 REMEDA Trust Score Visualization</h1>
  <p>Verification result を Trust Score として可視化し、人間が理解できる判断画面にします。</p>
</header>

<main>
  <div class="card">
    <h2>検証入力</h2>
    <form method="post" action="/verify">
      <p>URL</p>
      <input name="url" value="https://example.com">

      <p>Manifest JSON</p>
      <textarea name="manifest" rows="10">{
  "claims": {
    "execution": true,
    "identity": true,
    "integrity": true,
    "timestamp": true,
    "workflow": "github-actions",
    "sigstore": true,
    "policy_version": "v1"
  }
}</textarea>
      <br><br>
      <button type="submit">Trust Score を可視化する</button>
    </form>
  </div>

  {% if result %}
  <div class="card">
    <h2>Decision</h2>
    <div class="score {{ result.decision }}">{{ result.decision.upper() }}</div>
    <p>Trust Score: {{ result.trust_score }}</p>
    <div class="bar"><div class="fill" style="width: {{ result.trust_score * 100 }}%"></div></div>
    <p>{{ result.reason }}</p>
  </div>

  <div class="card">
    <h2>Trust Breakdown</h2>
    <div class="grid">
      {% for key, value in result.breakdown.items() %}
      <div class="mini">
        <h3>{{ key }}</h3>
        <div class="score">{{ value }}</div>
        <div class="bar"><div class="fill" style="width: {{ value * 100 }}%"></div></div>
      </div>
      {% endfor %}
    </div>
  </div>

  <div class="card">
    <h2>Evidence JSON</h2>
    <pre>{{ result | tojson(indent=2) }}</pre>
  </div>
  {% endif %}

  <div class="card">
    <h2>Verification History</h2>
    <table>
      <tr>
        <th>Time</th>
        <th>Decision</th>
        <th>Score</th>
        <th>URL</th>
      </tr>
      {% for item in history %}
      <tr>
        <td>{{ item.created_at }}</td>
        <td class="{{ item.decision }}">{{ item.decision }}</td>
        <td>{{ item.trust_score }}</td>
        <td>{{ item.url }}</td>
      </tr>
      {% endfor %}
    </table>
  </div>
</main>
</body>
</html>
"""

def calculate_trust(url, manifest):
    claims = manifest.get("claims", {})

    integrity = 1.0 if claims.get("integrity") else 0.0
    execution = 1.0 if claims.get("execution") and claims.get("workflow") == "github-actions" else 0.0
    identity = 1.0 if claims.get("identity") else 0.0
    time = 1.0 if claims.get("timestamp") else 0.0
    sigstore = 1.0 if claims.get("sigstore") else 0.0

    breakdown = {
        "integrity": integrity,
        "execution": execution,
        "identity": identity,
        "time": time,
        "sigstore": sigstore
    }

    trust_score = round(sum(breakdown.values()) / len(breakdown), 2)

    if trust_score >= 0.85:
        decision = "accept"
        reason = "All major trust conditions are satisfied."
    elif trust_score >= 0.45:
        decision = "pending"
        reason = "Some trust conditions are missing or incomplete."
    else:
        decision = "reject"
        reason = "Trust score is too low. Fail-closed."

    manifest_sha256 = hashlib.sha256(
        json.dumps(manifest, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return {
        "stage": 310,
        "url": url,
        "decision": decision,
        "trust_score": trust_score,
        "breakdown": breakdown,
        "reason": reason,
        "policy": {
            "accept_threshold": 0.85,
            "pending_threshold": 0.45,
            "reject_below": 0.45,
            "fail_closed": True
        },
        "evidence": {
            "manifest_sha256": manifest_sha256,
            "policy_version": claims.get("policy_version", "unknown"),
            "sigstore_present": bool(claims.get("sigstore")),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
    }

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML, result=None, history=HISTORY)

@app.route("/verify", methods=["POST"])
def verify():
    url = request.form.get("url", "")
    manifest_text = request.form.get("manifest", "{}")

    try:
        manifest = json.loads(manifest_text)
        result = calculate_trust(url, manifest)
    except Exception as e:
        result = {
            "stage": 310,
            "url": url,
            "decision": "reject",
            "trust_score": 0.0,
            "breakdown": {
                "integrity": 0,
                "execution": 0,
                "identity": 0,
                "time": 0,
                "sigstore": 0
            },
            "reason": f"Invalid manifest JSON: {e}",
            "policy": {"fail_closed": True},
            "evidence": {"created_at": datetime.utcnow().isoformat() + "Z"}
        }

    HISTORY.insert(0, {
        "created_at": result["evidence"]["created_at"],
        "decision": result["decision"],
        "trust_score": result["trust_score"],
        "url": url
    })

    return render_template_string(HTML, result=result, history=HISTORY)

@app.route("/api/verify", methods=["POST"])
def api_verify():
    data = request.get_json(force=True)
    url = data.get("url", "")
    manifest = data.get("manifest", {})
    result = calculate_trust(url, manifest)
    return jsonify(result)

@app.route("/api/health")
def health():
    return jsonify({
        "ok": True,
        "stage": 310,
        "service": "remeda-trust-score-visualization"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3100, debug=True)

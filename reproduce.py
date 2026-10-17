"""Offline consistency check for the published n=100 evidence chain."""
from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "verify/out/n100-candidate-complete-225.json": "PASS",
    "verify/out/n100-tail-candidate-224.json": "PASS",
    "verify/out/n100-candidate-budget-222.json": "PASS",
}

def load(rel):
    p = ROOT / rel
    if not p.is_file():
        raise SystemExit(f"MISSING: {rel}")
    return p, json.loads(p.read_text(encoding="utf-8"))

def main():
    rows = []
    for rel, expected_status in EXPECTED.items():
        p, data = load(rel)
        status = data.get("status")
        if status != expected_status:
            raise SystemExit(f"BAD STATUS: {rel}: {status!r}")
        rows.append((rel, status, hashlib.sha256(p.read_bytes()).hexdigest()))
    cert = load("verify/out/n100-candidate-complete-225.json")[1]
    ledger = load("verify/out/n100-six-branch-ledger-226.json")[1]
    if cert.get("candidate_radius") != "22647/200000":
        raise SystemExit("candidate radius mismatch")
    if cert.get("accepted_global_lower_bound") != "22647/200000":
        raise SystemExit("accepted bound mismatch")
    if cert.get("all_six_closed") is not True:
        raise SystemExit("six-branch closure flag is not true")
    if ledger.get("all_six_closed") is not True or ledger.get("pending_branches") != []:
        raise SystemExit("ledger is not closed")
    if "0.11324" not in (ROOT / "README.md").read_text(encoding="utf-8"):
        raise SystemExit("README evidence boundary missing")
    print("n=100 publication consistency: PASS")
    print("accepted bound: r_D(100) > 0.113235")
    print("0.11324: not closed; B36 residual retained")
    for rel, status, digest in rows:
        print(f"{status:4} {rel} sha256={digest}")

if __name__ == "__main__":
    main()

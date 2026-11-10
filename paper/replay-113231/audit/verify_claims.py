from __future__ import annotations
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

PAPER_ROOT = Path(__file__).resolve().parents[1]
ROOT = PAPER_ROOT / "evidence-root"
TAG = "113231/1000000"
PACKAGE = ROOT / "runtime/lower-small-advance-direct-113231-fresh/package"
FOLDER = ROOT / "runtime/lower-small-advance-direct-113231-fresh"
OUT = ROOT / "verify/out"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def inverse_radius_transform(data: bytes, rel: str) -> bytes:
    if not rel.endswith((".py", ".json")):
        return data
    text = data.decode("utf-8")
    text = re.sub(r"F\(\s*113231\s*,\s*1000000\s*\)", "F(11323,100000)", text)
    return text.replace("113231/1000000", "11323/100000").encode("utf-8")

def main() -> dict:
    complete = load(OUT / "n100-direct-113231-complete.json")
    first = load(OUT / "n100-lower-small-advance-direct-113231-fresh.json")
    trace = load(OUT / "n100-radius-dependency-audit-direct-113231-fresh.json")
    controls = load(OUT / "n100-direct-113231-controls.json")
    manifest = load(FOLDER / "transformation.json")
    require(complete["status"] == "PASS_ALL_SIX_BRANCH_ARITHMETIC_AT_SAME_RADIUS", "combined certificate status")
    require(complete["radius"] == TAG and first["radius"] == TAG and trace["radius"] == TAG and controls["radius"] == TAG, "exact radius")
    require(complete["fresh_full_runs"] == 2 and complete["all_six_branch_arithmetic_closed"], "two complete runs")
    require(not complete["uses_0p113235_certificates"] and not complete["uses_saved_branch_PASS_reports_for_acceptance"], "no inherited PASS evidence")
    require(first["exit_code"] == 0 and first["all_six_branch_arithmetic_closed"], "first complete run")
    require(trace["exit_code"] == 0 and trace["all_branches_replayed"] and not trace["entries_with_other_global_R"], "traced complete run")
    require(trace["process_count"] == 20 and trace["loaded_source_count"] == 28, "trace counts")
    require(controls["status"] == "PASS_TRANSFORMATION_AND_NEGATIVE_CONTROLS", "negative-control status")
    require(controls["snapshot_files"] == 626 and controls["python_sources_parsed"] == 158 and controls["assertions_preserved"] == 1662, "source audit counts")
    require(controls["all_changes_reconstructed_from_exact_radius_rule"] and controls["source_and_copy_hashes_match"], "source transform audit")

    expected_cap = Fraction(1, 1) - Fraction(TAG) ** 2
    require(expected_cap == Fraction(987178740639, 10**12), "normalized squared-radius cap")
    manuscript = (PAPER_ROOT / "paper.tex").read_text(encoding="utf-8")
    require("987178740639" in manuscript and "10^{12}" in manuscript, "paper normalization constant")
    branches = ("B31", "B32", "B33", "B34", "B35", "B36plus")
    first_result = first["result"]
    second_result = load(FOLDER / "audit.stdout.json")
    expected_rows = {row["branch"]: row for row in complete["branch_margins"]}
    require(set(expected_rows) == set(branches), "branch set")
    for branch in branches:
        a = first_result[branch]["result"]
        b = second_result[branch]["result"]
        row = expected_rows[branch]
        key = next(k for k in ("minimum_area_margin", "minimum_reported_area_margin", "minimum_area_margin_at_B36") if k in a)
        require(a["status"] == b["status"] == "PASS", f"{branch} status")
        require(a["radius"] == b["radius"] == row["radius"] == TAG, f"{branch} radius")
        require(a[key] == b[key] == row["minimum_margin"], f"{branch} exact repeated margin")
        require(Fraction(a[key]) > 0, f"{branch} positive rational margin")

    bridge = complete["count_bridge"]
    require(bridge["n"] == 99 and bridge["radius"] == TAG and Fraction(bridge["minimum_area_margin"]) > 0, "99-site bridge")
    require(complete["complete_surviving_boundary_counts"] == list(range(31, 40)), "surviving boundary counts")
    require(complete["parameter_trace"]["other_global_R_entries"] == [], "combined trace radius entries")

    source = manifest["source_snapshot"]
    copied = manifest["copy_snapshot"]
    changes = {row["path"]: row for row in manifest["changes"]}
    require(manifest["radius"] == TAG and len(source) == len(copied) == 626 and len(changes) == 60, "manifest dimensions")
    for rel, src_hash in source.items():
        path = PACKAGE / Path(rel)
        require(path.is_file(), f"missing transformed source: {rel}")
        current = path.read_bytes()
        require(sha(path) == copied[rel], f"copy hash mismatch: {rel}")
        reconstructed = inverse_radius_transform(current, rel)
        require(hashlib.sha256(reconstructed).hexdigest() == src_hash, f"inverse source hash mismatch: {rel}")
        if rel in changes:
            require(sha(path) == changes[rel]["new_sha256"] and src_hash == changes[rel]["old_sha256"], f"change manifest mismatch: {rel}")
    require(set(changes).issubset(source), "changed paths are source-bound")

    for relative, digest in complete["bindings"].items():
        path = ROOT / Path(relative)
        require(path.is_file() and sha(path) == digest, f"evidence source binding mismatch: {relative}")

    report = {
        "status": "PASS",
        "radius": TAG,
        "complete_replays": 2,
        "branches": list(branches),
        "count_bridge_cases": bridge["cases"],
        "source_files": len(source),
        "transformed_files": len(changes),
        "python_files_parsed": controls["python_sources_parsed"],
        "assertions_preserved": controls["assertions_preserved"],
        "trace_processes": trace["process_count"],
        "loaded_sources": trace["loaded_source_count"],
        "no_other_global_radius_entries": True,
        "negative_controls_rejected": all(x["expected_rejection"] and x["exit_code"] == 1 for x in controls["controls"]),
        "higher_radius_pass_inherited": False,
        "geometric_premises_formalized": False,
    }
    print(json.dumps(report, indent=2))
    (PAPER_ROOT / "audit/replay-audit.json").write_text(json.dumps(report, indent=2) + "\\n", encoding="utf-8")
    return report

if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"AUDIT FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(f"AUDIT ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)

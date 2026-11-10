"""Audit the bundled .113231 replay evidence, without rerunning the full calculation."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    runpy.run_path(str(ROOT / "paper/replay-113231/audit/verify_claims.py"), run_name="__main__")
    print("Evidence/provenance audit only; no new complete mathematical replay was executed.")
    print("0.113235: replay not successful; not an accepted verified bound.")
    print("0.113231: two recorded same-radius arithmetic replays; geometric transfer premises remain analytic.")

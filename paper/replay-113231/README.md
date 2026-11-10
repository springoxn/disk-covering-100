# Radius 0.113231 replay paper

This folder preserves the exact-radius replay at `R = 113231/1000000` as a reproducible computational record. The repository also contains a later claim at `R = 0.113235`, but that radius did not complete a successful replay; it is not treated here as an established verified bound. The `0.113231` replay is separately supported by the evidence bundled below.

## Contents

- `paper.tex`, `references.bib`: manuscript source.
- `build/paper.pdf`: six-page compiled manuscript.
- `evidence-root/`: exact replay receipts, source scripts, 626-file transformed verifier copy, runtime outputs and process trace.
- `audit/verify_claims.py`: checks exact margins, radius parameters, negative controls, source transformation and SHA-256 bindings.
- `audit/verify_source.py`: checks source structure and the displayed normalization constant.
- `audit/verify_pdf.py`: independently checks the compiled PDF text, page count and fonts.
- `build.ps1`: Tectonic build entry point.

## Recheck

From this directory, with Python 3.10+ and Tectonic installed:

```powershell
python -B audit/verify_source.py
python -B audit/verify_claims.py
pwsh -File build.ps1 -Tectonic C:\path\to\tectonic.exe
python -B audit/verify_pdf.py
```

The evidence audit checks the included transformed source against its exact-radius substitution rule and manifest, and validates the two fresh replays. It does not rerun the several-minute geometric certificate; the stored stdout, stderr, parameter traces and machine-readable results are retained. No proof-assistant formalization of the geometric transfer premises is claimed.

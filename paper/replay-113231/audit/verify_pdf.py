from __future__ import annotations
import json
import re
import sys
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build/paper.pdf"
REQUIRED = [
    "A Source-Bound Arithmetic Replay",
    "Abstract",
    "Problem and scope",
    "The six arithmetic branches",
    "Replay protocol and provenance",
    "Geometric transfer obligations",
    "Limitations and interpretation",
    "Evidence ledger",
    "0.113231",
    "3,767,981",
    "1,879,204",
    "1,662",
    "not formalized",
    "exact optimum",
]

def main() -> None:
    if not PDF.is_file():
        raise AssertionError(f"Missing compiled PDF: {PDF}")
    doc = fitz.open(PDF)
    if len(doc) < 5:
        raise AssertionError(f"Expected a full-length article, got {len(doc)} pages")
    texts = [page.get_text("text") for page in doc]
    text = "\n".join(texts)
    normalized = re.sub(r"\s+", " ", text)
    missing = [s for s in REQUIRED if s.lower() not in normalized.lower()]
    if missing:
        raise AssertionError(f"PDF is missing required text: {missing}")
    if len(text) < 12000:
        raise AssertionError(f"PDF text unexpectedly short: {len(text)} characters")
    for page_number, page_text in enumerate(texts, 1):
        if len(page_text.strip()) < 100:
            raise AssertionError(f"Page {page_number} appears blank or nearly blank")
    fonts = set()
    for page in doc:
        for font in page.get_fonts(full=True):
            fonts.add(font[3])
    if not fonts:
        raise AssertionError("No fonts detected in PDF")
    result = {
        "status": "PASS",
        "pdf": str(PDF.relative_to(ROOT)),
        "pages": len(doc),
        "text_characters": len(text),
        "unique_fonts": sorted(fonts),
        "required_markers_checked": len(REQUIRED),
        "all_pages_have_text": True,
    }
    out = ROOT / "audit/pdf-audit.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"PDF AUDIT FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(f"PDF AUDIT ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)

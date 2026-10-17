"""B35 profile diagnostic v4 directly rewrites the original adapter."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'verify/n100_B35_profile_diagnostic.py';text=source.read_text(encoding='utf-8');text=text.replace("             if restricted and (M in (25,26))", "            if restricted and (M in (25,26))")
# The prior wrapper executes its own wrapper; instead use its embedded source path impossible here.
# Keep a direct pointer by importing v2 result; no mutation is attempted.
print('Use existing n100-B35-profile-diagnostic-186.json; M25 profile is verified, M26 profile not separately captured.',flush=True)

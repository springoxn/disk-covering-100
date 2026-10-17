"""B35 profile diagnostic with source-indent corrected."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'verify/n100_B35_profile_diagnostic.py';text=source.read_text(encoding='utf-8');text=text.replace("             if restricted and (M in (25,26))", "            if restricted and (M in (25,26))");exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

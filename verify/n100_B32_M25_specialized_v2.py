"""Correct source indentation for filtered original81-profile verifier."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'verify/n100_B32_M25_specialized.py';text=path.read_text(encoding='utf-8');old="\\n     '+needle";new="\\n    '+needle";assert text.count(old)==1;text=text.replace(old,new);exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

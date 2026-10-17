"""Retain the +a term in general DDD count; surviving slots all havea0."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'verify/n100_B34_high_topology.py';text=source.read_text(encoding='utf-8');rules=[('solution[x]-(58+C+h)','solution[x]-(58+C+h+a)'),('for p in (Path(__file__),cp,original)',"for p in (Path(__file__),ROOT/'verify/n100_B34_high_topology.py',cp,original)")]
for old,new in rules:assert text.count(old)==1;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

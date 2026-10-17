"""Separate72 core ring corners from124 including52 outerBRR corners."""
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions must remain enabled')
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'verify/n100_B34_complete_180.py';text=source.read_text(encoding='utf-8');rules=[("sum(m['DDR'])+drR+drH+3==124","sum(m['DDR'])+drR+drH+3==72"),('[Path(__file__),*paths]',"[Path(__file__),ROOT/'verify/n100_B34_complete_180.py',*paths]")]
for old,new in rules:assert text.count(old)==1;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

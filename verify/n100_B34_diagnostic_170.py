"""Expose both genuine B34 failing endpoints; keep every support premise."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'verify/n100_B34_diagnostic_169.py';text=source.read_text(encoding='utf-8');rules=[("if idx!=1:assert gap>0","if idx==0:assert gap>0"),('other2 area assertions retained','only M22 area assertion retained'),('n100-B34-diagnostic-169.json','n100-B34-diagnostic-170.json'),("for p in (Path(__file__),ROOT/'verify/n100_remaining_branches_new_radius.py')","for p in (Path(__file__),ROOT/'verify/n100_B34_diagnostic_169.py',ROOT/'verify/n100_remaining_branches_new_radius.py')")]
for old,new in rules:assert text.count(old)==1;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

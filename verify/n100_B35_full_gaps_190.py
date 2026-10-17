"""Fresh correctly attributed B35 complete vertex-gap diagnostics."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'verify/n100_B35_diagnostic_v4.py'
text=source.read_text(encoding='utf-8')
needle='    for src,dst in rules:assert text.count(src)==1,(src,text.count(src));text=text.replace(src,dst)'
old='        return report,margin,coefficient,gaps,shifted_ear,bad'
new="        report['full_vertex_gaps']=[[p,d,str(v)] for (p,d),v in sorted(gaps.items())]\n        return report,margin,coefficient,gaps,shifted_ear,bad"
assert text.count(needle)==1
text=text.replace(needle,'    rules.append('+repr((old,new))+')\n'+needle)
assert text.count('n100-B35-diagnostic-184.json')==1
text=text.replace('n100-B35-diagnostic-184.json','n100-B35-full-gaps-190.json')
needle2="(Path(__file__),SRC,ROOT/'verify/n100_remaining_branches_new_radius.py')"
assert text.count(needle2)==1
text=text.replace(needle2,"(Path(__file__),ROOT/'verify/n100_B35_diagnostic_v4.py',SRC,ROOT/'verify/n100_remaining_branches_new_radius.py')")
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

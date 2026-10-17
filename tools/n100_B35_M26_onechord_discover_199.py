"""Rebuild B35 M26 single-chord discovery with B35 boundary endpoint filter."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
wrapper=ROOT/'tools/n100_B35_M26_onechord_discover_194.py'
source=ROOT/'tools/n100_B34_onechord_labelled_discover.py'
import ast
wt=wrapper.read_text(encoding='utf-8');assignment=next(n for n in ast.parse(wt).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rules' for t in n.targets));rules=ast.literal_eval(assignment.value)
text=source.read_text(encoding='utf-8')
for old,new in rules:assert old in text,old;text=text.replace(old,new)
old=' if base.evaluate(p,True) is None:return None if full else 1e9'
new=''' if not (.00001<ar<.5 and .05<ah<.8 and .25<b<.97 and .05<tau<1.4 and .2<K<.56 and max(ls+[0])-min(ls+[0])+tau/2<.99 and max(ls+[LB])-min(ls+[LB])<.99):return None if full else 1e9
 mu=math.pi/35;s=math.sin(mu);co=math.cos(mu);hm=math.sqrt(R*R-s*s);bt=R*K*(hm*co+s*s);fm=s*hm+mu-s*co+bt*(math.asin(s/R)-mu);dm=co*(R*R-2*s*s)/hm+2*s*s+bt*(co/hm-1)
 if fm-dm*mu-K*R*R*math.sqrt(2*(1-R))<2e-6:return None if full else 1e9'''
assert text.count(old)==1;text=text.replace(old,new)
text=text.replace('B35-M26-onechord-discovery-194','B35-M26-onechord-discovery-199')
text=text.replace('B34-chordless-labelled-discovery-176','B35-M26-chordless-discovery-195')
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

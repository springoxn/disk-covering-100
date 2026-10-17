"""B35 M26 single-chord exact replay with independently reconstructed cycles."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];src=ROOT/'verify/n100_B34_onechord_complete.py';text=src.read_text(encoding='utf-8')
start="tree=ast.parse(source.read_text(encoding='utf-8'));node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='models');env={'itertools':itertools,'Counter':Counter,'PAIRS':PAIRS};exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),env);models=env['models']();"
replacement="""models=[];types=set()
 for positions in itertools.combinations(range(26),3):
  lab=[int(i in positions) for i in range(26)];ear=lab[0];paid=Counter(tuple(sorted((lab[i],lab[(i+1)%26]))) for i in range(1,25));unpaid=Counter([tuple(sorted((lab[25],lab[0]))),tuple(sorted((lab[0],lab[1])))]);diag=tuple(sorted((lab[25],lab[1])));drr=paid.copy();drr[diag]+=1;rrr=(ear,*sorted((lab[25],lab[1])));types.add((ear,tuple(drr[p] for p in PAIRS),tuple(paid[p] for p in PAIRS),tuple(unpaid[p] for p in PAIRS),rrr))
 for ear,drr,paid,unpaid,rrr in sorted(types):
  ph=9+ear;pr=35-ph;ddr=[46-pr+2*(1-ear)-rrr.count(0),9-ph+2*ear-rrr.count(1)]
  if min(ddr)<0:continue
  models.append({'high_ring_degrees':[7]*3,'ear_high':ear,'pH':ph,'pR':pr,'DDD':57,'DDR':ddr,'DRR':list(drr),'BRR':list(paid),'BRR0':list(unpaid),'RRR':list(rrr)})
 """
assert text.count(start)==1;text=text.replace(start,replacement)
rules=[('B34-onechord-labelled-discovery-178','B35-M26-onechord-discovery-194'),('n100-B34-high-topology-174.json','n100-B35-profile-reduction-191.json'),("'tools/n100_B34_onechord_labelled_discover.py'","'tools/n100_B35_M26_onechord_discover_194.py'"),('boundary.B=34','boundary.B=35'),('mu=PI/34','mu=PI/35'),('outer=34*','outer=35*'),("m['pR']+m['pH']==34","m['pR']+m['pH']==35"),("sum(d-6 for d in m['high_ring_degrees'])==2","sum(d-6 for d in m['high_ring_degrees'])==3"),('59+19+25+1==104 and 3*59+2*19+25==240','57+19+25+1==102 and 3*57+2*19+25==234'),('19+2*25+3==124','19+2*25+3==72'),('center=59*','center=57*'),("(m['pH']-2)","(m['pH']-3)"),('n100-B34-onechord-complete-179.json','n100-B35-M26-onechord-196.json'),('B34-onechord-exact/v1','B35-M26-onechord-exact/v1'),("'B':34","'B':35"),("'core_faces':104","'core_faces':102"),('full_B34_closed','full_B35_closed'),('B34 ONECHORD EXACT PASS','B35 M26 ONECHORD EXACT PASS'),('for p in (Path(__file__),pp,tp,source)',"for p in (Path(__file__),ROOT/'verify/n100_B34_onechord_complete.py',pp,tp,source,ROOT/'tools/n100_B34_onechord_labelled_discover.py')")]
for old,new in rules:assert old in text,old;text=text.replace(old,new)
if not __debug__:raise RuntimeError('Assertions must remain enabled')
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

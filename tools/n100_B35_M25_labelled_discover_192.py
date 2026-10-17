"""B35 M25 discovery: four ring7 points, marked total11 or12."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'tools/n100_B34_chordless_labelled_discover.py'
text=source.read_text(encoding='utf-8')
node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='models')
old=ast.get_source_segment(text,node)
new='''def models():
 out=[];signatures=set()
 for positions in itertools.combinations(range(25),4):
  labels=[int(i in positions) for i in range(25)]
  ct=Counter(tuple(sorted((labels[i],labels[(i+1)%25]))) for i in range(25))
  signatures.add(tuple(ct[p] for p in PAIRS))
 for ph in (11,12):
  for edges in sorted(signatures):
   out.append({'high_ring_degrees':[7]*4,'deep_excess':0,'pH':ph,'pR':35-ph,'DDD':59,'DDR':[7+ph,12-ph],'edges':list(edges)})
 return out'''
assert text.count(old)==1;text=text.replace(old,new)
rules=[('math.pi/34','math.pi/35'),('outer=34*','outer=35*'),('26*math.pi/3','25*math.pi/3'),("'B34-chordless-labelled/v1'","'B35-M25-labelled/v1'"),("'B':34","'B':35"),('B34-chordless-labelled-discovery-176','B35-M25-labelled-discovery-192'),('B34 CHORDLESS DISCOVERY','B35 M25 DISCOVERY')]
for old,new in rules:
 assert old in text,old;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

"""B35 M26 chordless discovery after exact three7 profile reduction."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'tools/n100_B34_chordless_labelled_discover.py';text=source.read_text(encoding='utf-8');node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='models');old=ast.get_source_segment(text,node)
new='''def models():
 signatures=set();out=[]
 for pos in itertools.combinations(range(26),3):
  lab=[int(i in pos) for i in range(26)];ct=Counter(tuple(sorted((lab[i],lab[(i+1)%26]))) for i in range(26));signatures.add(tuple(ct[p] for p in PAIRS))
 for edges in sorted(signatures):out.append({'high_ring_degrees':[7]*3,'deep_excess':0,'pH':9,'pR':26,'DDD':56,'DDR':[20,0],'edges':list(edges)})
 return out'''
assert text.count(old)==1;text=text.replace(old,new)
for old,new in [('math.pi/34','math.pi/35'),('outer=34*','outer=35*'),("'B':34","'B':35"),('B34-chordless-labelled/v1','B35-M26-chordless/v1'),('B34-chordless-labelled-discovery-176','B35-M26-chordless-discovery-195'),('B34 CHORDLESS DISCOVERY','B35 M26 CHORDLESS DISCOVERY')]:
 assert old in text,old;text=text.replace(old,new)
exec(compile(text,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})

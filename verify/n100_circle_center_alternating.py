"""Audit co-vertex redundancy and alternate circle/shared-vertex with center adjacency."""
from pathlib import Path
from itertools import combinations
import json, hashlib
from n100_axis_coupled_boxes import build,contract,radiussquared
from n100_boundary_circle_propagation import setup
from n100_boundary_circle_branch_tree import propagate
import n100_boundary_circle_branch_tree_independent_full as independent
from n100_axis_coupled_boxes_independent import clip
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x: raise ValueError(m)
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def coupled(initial,edges,quads,pairs,alt=False,limit=160):
 B=[b[:] for b in initial];trace=[];fn=independent.propagate if alt else propagate;dist=clip if alt else contract
 for sw in range(limit):
  before=[b[:] for b in B];r=fn(B,edges,quads,limit=1)
  if r['excluded']:return {'excluded':True,'sweep':sw+1,'phase':'circle_shared','result':r,'trace':trace}
  B=r['boxes'];changes=0
  for a,b in pairs:
   for x,y in ((a,b),(b,a)):
    new=dist(B[x],B[y],radiussquared(2))
    if new is None:return {'excluded':True,'sweep':sw+1,'phase':'center_pair','failure':[x,y],'boxes':B,'trace':trace}
    if new!=B[x]:changes+=1;B[x]=new
  trace.append(changes)
  if B==before:return {'excluded':False,'fixed':True,'sweeps':sw+1,'boxes':B,'pair_changes_by_sweep':trace}
 return {'excluded':False,'fixed':False,'sweeps':limit,'boxes':B,'pair_changes_by_sweep':trace}
def main():
 cp='verify/out/n100-cubic-core-roundtrip.json';bp='verify/out/n100-axis-coupled-boxes.json';core=load(cp)['core'];prior=load(bp);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j})
 # Independently obtain face pairs meeting at vertices from the 562 incidences.
 p=[30,6,14,22];root=next(r['boxes'] for r in prior['retained'] if r['placement']==p);B,E,q=setup(core,p,root);inc={}
 for f,v in E:inc.setdefault(v,set()).add(f)
 vertex_pairs={pair for faces in inc.values() for pair in combinations(sorted(faces),2)}
 need(vertex_pairs==set(pairs),'co-vertex/adjacency equality')
 # Independent edge-side adjacency reconstruction, avoiding build().
 F=independent.cyc(core['phi']);owner={d:i for i,row in enumerate(F) for d in row};outer=next(i for i,row in enumerate(F) if core['core_tags'][row[0]][0]=='outer');index={f:i for i,f in enumerate(f for f in range(len(F)) if f!=outer)}
 pairs2=sorted({tuple(sorted((index[owner[d]],index[owner[e]]))) for d,e in enumerate(core['alpha']) if owner[d]!=outer and owner[e]!=outer and owner[d]!=owner[e]})
 need(pairs==pairs2,'independent adjacency')
 rows=[]
 for p in ([30,6,14,22],[20,27,2,9]):
  root=next(r['boxes'] for r in prior['retained'] if r['placement']==p);B,E,q=setup(core,p,root);IB,IE,Iq=independent.setup(core,p,root);need((B,E,q)==(IB,IE,Iq),'setup equality');baseline=propagate(B,E,q,limit=160);need(not baseline['excluded'],'baseline retained');start=baseline['boxes'];a=coupled(start,E,q,pairs);b=coupled(start,IE,Iq,pairs2,True);need(a==b,'full alternating replay');need(not a['excluded'],'unexpected exclusion: inspect before accepting');reduction=sum(sum(start[i][j+1]-start[i][j]-a['boxes'][i][j+1]+a['boxes'][i][j] for j in (0,2)) for i in range(len(start)));rows.append({'placement':p,'baseline_sweeps':baseline['sweeps'],'additional_total_width_reduction':reduction,'result':a});print('PASS alternating',p,'extra width',reduction,'fixed',a['fixed'],'sweeps',a['sweeps'],flush=True)
 out=ROOT/'verify/out/n100-circle-center-alternating.json';need(not out.exists(),'overwrite');paths=[cp,bp,'verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-circle-center-alternating/v1','verified_integer_replay':True,'adjacent_pair_count':len(pairs),'co_vertex_pair_count':len(vertex_pairs),'co_vertex_equals_adjacency':True,'independent_adjacency_equal':True,'cases':rows,'machine_verified_geometry':False,'global_optimality':False,'scope':'two placements on one fixed core; necessary constraints only','bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()

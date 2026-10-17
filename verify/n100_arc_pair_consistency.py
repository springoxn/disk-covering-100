"""Finite-domain arc consistency for boundary tile pairs sharing a center."""
from pathlib import Path
from itertools import combinations
import json,hashlib
from n100_arc_center_projection import checked_contract
from n100_boundary_arc_tiles import ROOT,load,need,setup,intersect,support,radiussquared
from n100_boundary_arc_tiles_audit import independent_tile

def mask(labels):return sum(1<<j for j in labels)
def labels(bits):return [i for i in range(bits.bit_length()) if (bits>>i)&1]
def propagate(initial,relations):
 D=initial.copy();log=[]
 while True:
  changed=False
  for i,r in enumerate(relations):
   for v,w,table in ((r['v'],r['w'],r['forward']),(r['w'],r['v'],r['reverse'])):
    for j in labels(D[v]):
     if not table[j]&D[w]:
      log.append({'relation':i,'vertex':v,'label':j,'other_domain':D[w]});D[v]&=~(1<<j);changed=True
      if not D[v]:return D,log,True
  if not changed:return D,log,False

def replay_removals(initial,relations,log,final):
 D={v:set(labels(b)) for v,b in initial.items()}
 for row in log:
  r=relations[row['relation']];v=row['vertex'];w=r['w'] if v==r['v'] else r['v'];table=r['forward'] if v==r['v'] else r['reverse'];j=row['label'];need(j in D[v] and mask(D[w])==row['other_domain'],'replay domain');need(not (set(labels(table[j]))&D[w]),'removal lacks reason');D[v].remove(j)
 need({v:mask(s) for v,s in D.items()}==final,'final replay')

def main():
 # Toy compatibility controls: equality relation must propagate singleton; impossible edge rejects.
 rel=[{'v':0,'w':1,'forward':{0:1,1:2},'reverse':{0:1,1:2}}];d,l,e=propagate({0:3,1:1},rel);need(d=={0:1,1:1} and not e,'singleton propagation');replay_removals({0:3,1:1},rel,l,d);d,l,e=propagate({0:1,1:2},rel);need(e,'contradictory labels reject')
 source='verify/out/n100-arc-center-projection.json';z=load(source);leaf=max((c for c in z['cases'] if c['source_node'] is not None),key=lambda c:c['extra_width_reduction']);candidate=next(c for c in z['cases'] if c['source_node'] is None);core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};rows=[]
 for case in (leaf,candidate):
  p=case['placement'];r=case['result'];need(not r['excluded'] and r['fixed'],'fixed input');B=r['boxes'];_,E,q=setup(core,p,prior[tuple(p)]);initial={100+int(v):mask(m) for v,m in r['masks'].items()};face_vertices={};signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};pieces={}
  for v,sg in q.items():
   for j in labels(initial[100+v]):
    c=intersect(B[100+v],independent_tile(j,256,signs[sg]));need(c is not None,'retained tile');pieces[(100+v,j)]=c
  for f,v in E:
   if v in initial:face_vertices.setdefault(f,set()).add(v)
  projections={}
  for f,vs in face_vertices.items():
   for v in vs:
    for j in labels(initial[v]):projections[(f,v,j)]=checked_contract(B[f],pieces[(v,j)],radiussquared(1));need(projections[(f,v,j)] is not None,'retained projection')
  relations=[];tested=accepted=0
  for f,vs in sorted(face_vertices.items()):
   for v,w in combinations(sorted(vs),2):
    forward={j:0 for j in labels(initial[v])};reverse={k:0 for k in labels(initial[w])}
    for j in forward:
     for k in reverse:
      a=projections[(f,v,j)];b=projections[(f,w,k)];overlap=intersect(a,b) is not None;alt=all(max(a[2*t],b[2*t])<=min(a[2*t+1],b[2*t+1]) for t in (0,1));need(overlap==alt,'projection intersection audit');good=overlap and support(pieces[(v,j)],pieces[(w,k)],radiussquared(2));tested+=1
      if good:forward[j]|=1<<k;reverse[k]|=1<<j;accepted+=1
    relations.append({'face':f,'v':v,'w':w,'forward':forward,'reverse':reverse})
  D,log,excluded=propagate(initial,relations);replay_removals(initial,relations,log,D)
  if not excluded:
   for rel in relations:
    for v,w,table in ((rel['v'],rel['w'],rel['forward']),(rel['w'],rel['v'],rel['reverse'])):
     need(all(table[j]&D[w] for j in labels(D[v])),'fixed compatibility')
  if case is candidate:need(not excluded,'candidate lost: investigate')
  rows.append({'placement':p,'source_node':case['source_node'],'relation_count':len(relations),'pairs_tested':tested,'pairs_accepted':accepted,'initial_label_count':sum(b.bit_count() for b in initial.values()),'final_label_count':sum(b.bit_count() for b in D.values()),'excluded':excluded,'initial_domains':initial,'final_domains':D,'removals':log,'relations':relations});print('case',p,'node',case['source_node'],'relations',len(relations),'pairs',tested,'accepted',accepted,'removed',len(log),'excluded',excluded,flush=True)
 out=ROOT/'verify/out/n100-arc-pair-consistency.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_center_projection.py','verify/n100_boundary_arc_tiles.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py'];out.write_text(json.dumps({'schema':'n100-arc-pair-consistency/v1','verified_integer_relation_tests':True,'synthetic_propagation_and_rejection_controls':True,'all_removals_replayed_with_sets':True,'all_projection_contractors_equal':True,'candidate_retained':True,'cases':rows,'scope':'one narrowed leaf plus candidate; pair compatibility is necessary only, not sufficient for one common center point or global realization; shared relation builder','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS pair consistency',len(rows),'cases')
if __name__=='__main__':main()

"""Expand a geometric label nogood into ranges; count exact finite-model effect."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,state_dp
from n100_arc_learning_counts import count_dp
from n100_arc_nogood_reinjection import setup,build,intersect,independent_tile,coupled,independent

def range_marks(order,D,clauses):
 return [{j:sum(1<<i for i,c in enumerate(clauses) if any(v==w and not lo<=j<=hi for w,lo,hi in c)) for j in range(256) if (D[v]>>j)&1} for v in order]

def controls():
 D={i:7 for i in range(3)};tables=[{j:7 for j in range(3)} for _ in range(3)];cases=[[[[0,0,1],[1,1,2]]],[[[0,0,2]]],[[[0,1,1]],[[1,0,1],[2,1,2]]]]
 for clauses in cases:
  expected=[0]*3;ways=0
  for values in product(range(3),repeat=3):
   if not all(any(not lo<=values[v]<=hi for v,lo,hi in c) for c in clauses):continue
   ways+=1
   for i,j in enumerate(values):expected[i]|=1<<j
  marks=range_marks(list(D),D,clauses);got,w,st=state_dp([7]*3,tables,[False]*3,marks,len(clauses));count,a=count_dp([7]*3,tables,[False]*3,marks,len(clauses));need(got==expected and count==ways,'range clause brute control')
 return len(cases)

def main():
 ccount=controls();source='verify/out/n100-arc-bounded-learning.json';z=load(source);p=z['placement'];node=z['source_node'];base=next(c['result']['boxes'] for c in load('verify/out/n100-arc-center-projection.json')['cases'] if c['placement']==p and c['source_node']==node);core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};active=[[v,j,j] for v,j in z['clauses'][0]];need(len(active)==4,'four-restriction seed');log=[]
 def test(ranges):
  B=[b[:] for b in base]
  for v,lo,hi in ranges:
   a=independent_tile(lo,256,signs[q[v-100]]);b=independent_tile(hi,256,signs[q[v-100]]);arc=[min(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),max(a[3],b[3])];c=intersect(B[v],arc);need(c is not None,'expanded seed retains nonempty part');B[v]=c
  a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'expanded conflict alternate geometry');return a
 need(test(active)['excluded'],'seed proof')
 def trial(i,side,value):
  candidate=[r[:] for r in active];candidate[i][side]=value;r=test(candidate);log.append({'restriction':i,'side':side,'value':value,'excluded':r['excluded'],'result_sha256':hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()});return r['excluded']
 for i in range(len(active)):
  for side,target in ((1,0),(2,255)):
   accepted=active[i][side]
   if accepted==target:continue
   if trial(i,side,target):active[i][side]=target;continue
   rejected=target
   while abs(rejected-accepted)>1:
    middle=(rejected+accepted)//2
    if trial(i,side,middle):accepted=middle;active[i][side]=middle
    else:rejected=middle
  print('EXPANDED',active[i],flush=True)
 proof=test(active);need(proof['excluded'],'final expanded range proof');oldclauses=[[[v,j,j] for v,j in c] for c in z['clauses']];newclauses=[active]+oldclauses[1:];model=next(c for c in load('verify/out/n100-arc-ordered-cycle.json')['cases'] if c['placement']==p and c['source_node']==node);D={int(v):b for v,b in model['globally_supported_domains'].items()};order=z['boundary_order'];lookup={frozenset((r['v'],r['w'])):r for r in model['relations']};tables=[];same=[]
 for i,v in enumerate(order):
  w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];tables.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[w-100])
 marks=range_marks(order,D,newclauses);support,witnesses,stats=state_dp([D[v] for v in order],tables,same,marks,len(newclauses));after,anchors=count_dp([D[v] for v in order],tables,same,marks,len(newclauses));before=load('verify/out/n100-arc-learning-counts.json')['rows'][-1]['assignment_count'];oldD={int(v):b for v,b in z['final_supported_domains'].items()};need(after<=before and all(b&~oldD[v]==0 for v,b in zip(order,support)),'generalization strengthens old nogood')
 for witness in witnesses:
  values=dict(zip(order,(s[0] for s in witness)));need(all(any(not lo<=values[v]<=hi for v,lo,hi in c) for c in newclauses),'range clauses satisfied')
 ratio=Fraction(after,before);out=ROOT/'verify/out/n100-arc-range-nogood.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-learning-counts.json','verify/out/n100-arc-center-projection.json','verify/out/n100-arc-ordered-cycle.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_learning_counts.py','verify/n100_arc_nogood_reinjection.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-range-nogood/v1','verified_integer_range_generalization':True,'range_clause_brute_controls':ccount,'all_geometry_alternate_equal':True,'placement':p,'source_node':node,'original_singleton_clause':oldclauses[0],'generalized_range_clause':active,'generalized_clause_proof':proof,'expansion_trials':log,'clauses':newclauses,'supported_labels_before':z['final_supported_label_count'],'supported_labels_after':sum(b.bit_count() for b in support),'supported_domains':dict(zip(order,support)),'boundary_order':order,'anchor_witnesses':witnesses,'state_statistics':stats,'assignments_before':before,'assignments_after':after,'retained_fraction':[ratio.numerator,ratio.denominator],'anchor_counts':anchors,'root_excluded':not any(support),'scope':'one parent-specific interval nogood replaces a singleton nogood; accepted enlargements have exact proofs, no maximality claim; finite count is not coverage count','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS range nogood labels',z['final_supported_label_count'],sum(b.bit_count() for b in support),'counts',before,after,'ratio',ratio,'root',not any(support))
if __name__=='__main__':main()

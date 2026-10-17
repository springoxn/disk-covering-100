"""Reverse-order upper-parameter set DP independent of forward lower-state solver."""
from pathlib import Path
from itertools import product
import json,hashlib
from n100_circle_center_alternating import ROOT,load,need
from n100_boundary_circle_propagation import setup

def elements(b):return {j for j in range(b.bit_length()) if b&(1<<j)}
def reverse_support(order,D,relations,q,clauses):
 # Reverse traversal, rotated to start at a quadrant change. U is minimum of
 # visited upper label endpoints, so nonincreasing parameters can be realized.
 order=list(reversed(order));start=next(i for i,v in enumerate(order) if q[v]!=q[order[i-1]]);order=order[start:]+order[:start];edges={}
 for r in relations:
  edges[r['v'],r['w']]={(int(a),b) for a,bits in r['forward'].items() for b in elements(bits)};edges[r['w'],r['v']]={(b,a) for a,b in edges[r['v'],r['w']]}
 domains={v:elements(D[v]) for v in order};full=(1<<len(clauses))-1;marks={}
 for v in order:
  for j in domains[v]:marks[v,j]=sum(1<<c for c,row in enumerate(clauses) if any(v==w and (j<lo or j>hi) for w,lo,hi in row))
 total={v:set() for v in order};witnesses=[];peak=0
 for anchor in sorted(domains[order[0]]):
  initial=(anchor,anchor+1,marks[order[0],anchor]);layers=[{initial}];graph=[]
  for i in range(len(order)-1):
   v,w=order[i:i+2];same=q[v]==q[w];arcs={};nxt=set()
   for state in layers[-1]:
    j,U,sat=state;targets=set()
    for k in domains[w]:
     if (j,k) not in edges[v,w]:continue
     upper=min(U,k+1) if same else k+1
     if upper<k:continue
     target=(k,upper,sat|marks[w,k]);targets.add(target);nxt.add(target)
    arcs[state]=targets
   graph.append(arcs);layers.append(nxt)
  peak=max(peak,max(map(len,layers)));good={s for s in layers[-1] if s[2]==full and (s[0],anchor) in edges[order[-1],order[0]]};accepted=[set() for _ in order];accepted[-1]=good
  for i in range(len(order)-2,-1,-1):accepted[i]={s for s,targets in graph[i].items() if targets&accepted[i+1]}
  if initial not in accepted[0]:continue
  witness=[initial]
  for i in range(len(order)-1):witness.append(min(graph[i][witness[-1]]&accepted[i+1]))
  witnesses.append(witness)
  for v,S in zip(order,accepted):total[v].update(s[0] for s in S)
 return {v:sum(1<<j for j in S) for v,S in total.items()},order,witnesses,peak

def main():
 controls=0
 for trial in range(12):
  order=[0,1,2,3];D={v:7 for v in order};q={0:0,1:0,2:1,3:1};relations=[]
  for i,v in enumerate(order):
   w=order[(i+1)%4];forward={j:sum(1<<k for k in range(3) if (j+k+i+trial)%4) for j in range(3)};relations.append({'v':v,'w':w,'forward':forward})
  clauses=[[[c%4,c%3,min(2,c%3+1)],[(c+1)%4,0,0]] for c in range(trial%5)];expected={v:0 for v in order};edge={(r['v'],r['w']):{int(j):bits for j,bits in r['forward'].items()} for r in relations}
  for vals in product(range(3),repeat=4):
   if any(not edge[v,order[(i+1)%4]][vals[v]]&(1<<vals[order[(i+1)%4]]) for i,v in enumerate(order)):continue
   if not (vals[0]<=vals[1]+1 and vals[2]<=vals[3]+1):continue
   if not all(any(not lo<=vals[v]<=hi for v,lo,hi in c) for c in clauses):continue
   for v,j in enumerate(vals):expected[v]|=1<<j
  got,_,_,_=reverse_support(order,D,relations,q,clauses);need(got==expected,'reverse controls versus exhaustive 81 assignments');controls+=1
 source='verify/out/n100-spatial-leaf-joint.json';z=load(source);parent=load('verify/out/n100-arc-conflict-branch.json');child=next(r for r in parent['children'] if r['child']==1);median=load('verify/out/n100-arc-median-learning.json');model=load('verify/out/n100-arc-geometry-feedback.json');p=z['placement'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,rawq=setup(core,p,prior);q={100+v:sg for v,sg in rawq.items()};order=z['boundary_order'];clauses=z['clauses'];D={int(v):b for v,b in child['final_supported_domains'].items()};cases=[{'id':'child1_parent','input':D,'expected':D}];leaves=[r for r in z['leaves'] if not r['excluded'] and 'supported_domains' in r];small=min(leaves,key=lambda r:(r['labels_after_twelve_clauses'],r['tree_node']));large=max(leaves,key=lambda r:(r['labels_after_twelve_clauses'],r['tree_node']))
 for row in (small,large):
  domains={v:bits&sum(1<<j for j in row['arc_result']['masks'][str(v-100)]) for v,bits in D.items()};cases.append({'id':row['tree_node'],'input':domains,'expected':{int(v):b for v,b in row['supported_domains'].items()}})
 rows=[]
 for case in cases:
  got,reverse_order,w,peak=reverse_support(order,case['input'],model['final_relations'],q,clauses);need(got==case['expected'],'reverse upper DP equals saved forward lower DP');rows.append({'case':case['id'],'supported_domains':got,'reverse_order':reverse_order,'anchor_witnesses':w,'max_layer_states':peak,'all_vertex_bitsets_equal':True});print('REVERSE',case['id'],'labels',sum(b.bit_count() for b in got.values()),'peak',peak,'equal',True,flush=True)
 out=ROOT/'verify/out/n100-arc-reverse-support-audit.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-conflict-branch.json','verify/out/n100-arc-median-learning.json','verify/out/n100-arc-geometry-feedback.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json'];out.write_text(json.dumps({'schema':'n100-arc-reverse-support-audit/v1','verified_integer_reverse_upper_dp':True,'exhaustive_small_controls':controls,'all_three_cases_equal_saved_forward_support':True,'rows':rows,'scope':'independent reverse traversal upper-bound finite support algorithm; shares inherited relation tables, masks, clauses and topology setup; no independent continuous geometry or global proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent reverse support')
if __name__=='__main__':main()

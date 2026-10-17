"""Exact counts of finite ordered label assignments under learned clauses."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,make_marks,labels
from n100_boundary_circle_propagation import setup

def count_dp(domains,tables,same,marks,clause_count):
 need(not same[-1],'quadrant-reset anchor');allbits=(1<<clause_count)-1;total=0;anchors=[];moves=[]
 for i in range(len(domains)-1):
  row={}
  for j in labels(domains[i]):
   for M in (j,j+1):row[j,M]=[(k,max(M,k) if same[i] else k) for k in labels(tables[i][j]&domains[i+1]) if not same[i] or M<=k+1]
  moves.append(row)
 for anchor in labels(domains[0]):
  current={(anchor,anchor,marks[0][anchor]):1}
  for i,row in enumerate(moves):
   nxt={}
   for (j,M,sat),ways in current.items():
    for k,N in row[j,M]:
     s=(k,N,sat|marks[i+1][k]);nxt[s]=nxt.get(s,0)+ways
   current=nxt
  number=sum(ways for (j,M,sat),ways in current.items() if sat==allbits and tables[-1][j]&(1<<anchor));anchors.append([anchor,number]);total+=number
 return total,anchors

def main():
 source='verify/out/n100-arc-bounded-learning.json';z=load(source);controls=z['exhaustive_small_model_controls']
 for control in controls:
  seed=control['seed'];order=list(range(4));D={v:5 for v in order};same=[True,True,False,False];tables=[{j:(5 if (seed+edge)%3 else (1<<j)) for j in (0,2)} for edge in order];clauses=[[[((ci+k)%4),2*((seed+ci+k)%2)] for k in range(1+(ci%3))] for ci in range(seed%9)];n,anchors=count_dp([5]*4,tables,same,make_marks(order,D,clauses),len(clauses));need(n==control['accepted_assignments'],'exact brute count control')
 p=z['placement'];node=z['source_node'];model=next(c for c in load('verify/out/n100-arc-ordered-cycle.json')['cases'] if c['placement']==p and c['source_node']==node);D={int(v):b for v,b in model['globally_supported_domains'].items()};core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);order=z['boundary_order'];lookup={frozenset((r['v'],r['w'])):r for r in model['relations']};tables=[];same=[]
 for i,v in enumerate(order):
  w=order[(i+1)%len(order)];r=lookup[frozenset((v,w))];tables.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[w-100])
 rows=[];last=None
 for size in range(3,len(z['clauses'])+1):
  clauses=z['clauses'][:size];n,anchors=count_dp([D[v] for v in order],tables,same,make_marks(order,D,clauses),size);need(last is None or n<=last,'count monotonicity');rows.append({'clause_count':size,'assignment_count':n,'removed_since_previous':None if last is None else last-n,'anchor_counts':anchors});last=n;print('COUNT clauses',size,n,flush=True)
 before=rows[0]['assignment_count'];after=rows[-1]['assignment_count'];need(before>0,'nonempty baseline');retained=Fraction(after,before);out=ROOT/'verify/out/n100-arc-learning-counts.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-ordered-cycle.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_bounded_learning.py'];out.write_text(json.dumps({'schema':'n100-arc-learning-counts/v1','verified_integer_assignment_counts':True,'exhaustive_small_count_controls':len(controls),'placement':p,'source_node':node,'rows':rows,'retained_fraction':[retained.numerator,retained.denominator],'removed_assignment_count':before-after,'scope':'counts finite label assignments, not distinct circular point choices or continuous coverings; may count multiple tile labels at shared endpoints; no independent full-size counter','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS counts removed',before-after,'fraction',str(retained))
if __name__=='__main__':main()

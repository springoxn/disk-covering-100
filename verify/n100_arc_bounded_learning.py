"""Bounded conflict learning on one parent, with exhaustive small-model DP controls."""
from pathlib import Path
from itertools import product
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,state_dp,make_marks,mask
from n100_arc_nogood_reinjection import setup,build,intersect,independent_tile,coupled,independent

def controls():
 counts=[]
 for seed in range(18):
  order=list(range(4));D={v:5 for v in order};same=[True,True,False,False];tables=[]
  for edge in order:tables.append({j:(5 if (seed+edge)%3 else (1<<j)) for j in (0,2)})
  clauses=[[[((ci+k)%4),2*((seed+ci+k)%2)] for k in range(1+(ci%3))] for ci in range(seed%9)]
  got,w,st=state_dp([5]*4,tables,same,make_marks(order,D,clauses),len(clauses));expected=[0]*4;accepted=0
  for values in product((0,2),repeat=4):
   if not all(tables[i][values[i]]&(1<<values[(i+1)%4]) for i in order):continue
   if not all(any(values[v]!=j for v,j in c) for c in clauses):continue
   M=values[0];ok=True
   for i in range(1,4):
    M=max(M,values[i]) if same[i-1] else values[i]
    if M>values[i]+1:ok=False
   if not ok:continue
   accepted+=1
   for i,j in enumerate(values):expected[i]|=1<<j
  need(got==expected,'exhaustive multi-clause control');counts.append({'seed':seed,'clause_count':len(clauses),'accepted_assignments':accepted})
 return counts

def main():
 toy=controls();source='verify/out/n100-arc-third-nogood.json';old=next(c for c in load(source)['cases'] if c['source_node']==27);p=old['placement'];node=27;clauses=old['clauses'];model=next(c for c in load('verify/out/n100-arc-ordered-cycle.json')['cases'] if c['placement']==p and c['source_node']==node);base=next(c['result']['boxes'] for c in load('verify/out/n100-arc-center-projection.json')['cases'] if c['placement']==p and c['source_node']==node);core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});order=old['boundary_order'];D={int(v):b for v,b in model['globally_supported_domains'].items()};lookup={frozenset((r['v'],r['w'])):r for r in model['relations']};tables=[];same=[]
 for i,v in enumerate(order):
  z=order[(i+1)%len(order)];r=lookup[frozenset((v,z))];tables.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[z-100])
 signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3}
 def test(restrictions):
  B=[b[:] for b in base]
  for v,j in restrictions:
   b=intersect(B[v],independent_tile(j,256,signs[q[v-100]]));need(b is not None,'tile restriction');B[v]=b
  a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'bounded learner independent contractors');return a
 support,witnesses,stats=state_dp([D[v] for v in order],tables,same,make_marks(order,D,clauses),len(clauses));need(dict(zip(order,support))=={int(v):b for v,b in old['supported_domains'].items()},'starting support');history=[];stop='iteration_limit'
 for step in range(1,6):
  if not witnesses:stop='finite_model_empty';break
  witness=witnesses[0];assignment=[[v,s[0]] for v,s in zip(order,witness)];values=dict(assignment);need(all(any(values[v]!=j for v,j in c) for c in clauses),'new witness avoids learned conflicts');initial=test(assignment)
  if not initial['excluded']:history.append({'step':step,'learned':False,'assignment':assignment,'geometry':initial});stop='witness_not_excluded';break
  active=[a[:] for a in assignment];log=[]
  for r in assignment:
   trial=[a for a in active if a!=r];g=test(trial);log.append({'remove_trial':r,'remaining_count':len(trial),'excluded':g['excluded'],'result_sha256':hashlib.sha256(json.dumps(g,sort_keys=True).encode()).hexdigest()})
   if g['excluded']:active=trial
  proof=test(active);need(active and proof['excluded'],'confirmed learned conflict');need(all(set(map(tuple,active))!=set(map(tuple,c)) for c in clauses),'no duplicate conflict');before=sum(b.bit_count() for b in support);old_support=support[:];clauses=clauses+[active];support,witnesses,stats=state_dp([D[v] for v in order],tables,same,make_marks(order,D,clauses),len(clauses));need(all(b&~a==0 for a,b in zip(old_support,support)),'support must shrink monotonically')
  for w in witnesses:
   vals=dict(zip(order,(s[0] for s in w)));need(all(any(vals[v]!=j for v,j in c) for c in clauses),'all final conflicts satisfied')
  history.append({'step':step,'learned':True,'new_clause':active,'initial_assignment':assignment,'initial_assignment_proof':initial,'clause_proof':proof,'deletion_log':log,'clause_count':len(clauses),'labels_before':before,'labels_after':sum(b.bit_count() for b in support),'supported_domains':dict(zip(order,support)),'state_statistics':stats});print('LEARN',step,'new size',len(active),'clauses',len(clauses),'support',before,sum(b.bit_count() for b in support),'peak',stats['maximum_states_in_one_layer'],flush=True)
  if not witnesses:stop='finite_model_empty';break
 out=ROOT/'verify/out/n100-arc-bounded-learning.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-ordered-cycle.json','verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_nogood_reinjection.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-bounded-learning/v1','verified_integer_bounded_learning':True,'exhaustive_small_model_controls':toy,'all_geometry_alternate_results_equal':True,'placement':p,'source_node':node,'maximum_new_conflicts':5,'stop':stop,'history':history,'clauses':clauses,'final_supported_domains':dict(zip(order,support)),'final_supported_label_count':sum(b.bit_count() for b in support),'boundary_order':order,'final_anchor_witnesses':witnesses,'final_state_statistics':stats,'root_excluded':not any(support),'scope':'bounded learning on one inherited parent only; integer conflict proofs and support monotonicity; small-model brute oracle is not independent full 100-disk proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS bounded learning',stop,'clauses',len(clauses),'support',sum(b.bit_count() for b in support),'root',not any(support))
if __name__=='__main__':main()

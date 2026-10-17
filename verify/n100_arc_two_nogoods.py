"""Learn second geometric nogood per parent and compute exact two-clause support."""
from pathlib import Path
from itertools import product
import json,hashlib
from n100_arc_nogood_reinjection import ROOT,load,need,solve,setup,build,intersect,independent_tile,coupled,independent

def main():
 source='verify/out/n100-arc-nogood-reinjection.json';oldng=load('verify/out/n100-arc-nogoods.json')['cases'];models=load('verify/out/n100-arc-ordered-cycle.json')['cases'];baselines=load('verify/out/n100-arc-center-projection.json')['cases'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};rows=[]
 for inherited in load(source)['cases']:
  p=inherited['placement'];node=inherited['source_node'];case=next(c for c in models if c['placement']==p and c['source_node']==node);first=next(c for c in oldng if c['placement']==p and c['source_node']==node);base=next(c['result']['boxes'] for c in baselines if c['placement']==p and c['source_node']==node);_,E,q=setup(core,p,prior[tuple(p)]);_,IE,Iq=independent.setup(core,p,prior[tuple(p)]);order=inherited['boundary_order'];branch=inherited['branches'][0];need(branch['first_witness_geometry']['excluded'],'new witness rejected');w=branch['anchor_state_witnesses'][0];assignment=[[v,s//2] for v,s in zip(order,w)];need(any(dict(assignment)[v]!=j for v,j in first['nogood_restrictions']),'new witness avoids old clause');log=[]
  def test(restrictions):
   B=[b[:] for b in base]
   for v,j in restrictions:
    b=intersect(B[v],independent_tile(j,256,signs[q[v-100]]));need(b is not None,'restriction tile');B[v]=b
   a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'new nogood geometry alternate replay');return a
  active=[a[:] for a in assignment]
  for a in assignment:
   trial=[x for x in active if x!=a];r=test(trial);log.append({'removed_trial':a,'excluded':r['excluded'],'remaining':len(trial),'result_sha256':hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()})
   if r['excluded']:active=trial
  proof=test(active);need(active and proof['excluded'],'second nogood proof');need(set(map(tuple,active))!=set(map(tuple,first['nogood_restrictions'])),'new clause distinct');clauses=[first['nogood_restrictions'],active];D={int(v):b for v,b in case['globally_supported_domains'].items()};total={v:0 for v in D};subrows=[]
  # Exhaustive conjunction-of-disjunctions cover at Boolean literal-status level.
  for status in product((False,True),repeat=sum(map(len,clauses))):
   k=len(clauses[0]);need(((not all(status[:k])) and (not all(status[k:])))==any(not status[i] and not status[k+j] for i in range(k) for j in range(len(clauses[1]))),'two-clause Boolean cover')
  for picks in product(*clauses):
   sub=D.copy()
   for v,j in picks:sub[v]&=~(1<<j)
   supported,witnesses=solve(case,sub,order,q)
   for v,b in supported.items():total[v]|=b
   for witness in witnesses:
    values=dict(zip(order,(s//2 for s in witness)));need(all(any(values[v]!=j for v,j in c) for c in clauses),'witness satisfies both learned clauses')
   subrows.append({'forbidden_labels':list(picks),'supported_domains':supported,'witness_count':len(witnesses),'first_anchor_state_witness':witnesses[0] if witnesses else None})
  rows.append({'placement':p,'source_node':node,'clauses':clauses,'second_clause_proof':proof,'second_clause_deletion_log':log,'subdomains':subrows,'input_labels':sum(b.bit_count() for b in D.values()),'one_clause_supported_labels':inherited['union_supported_labels'],'two_clause_supported_labels':sum(b.bit_count() for b in total.values()),'two_clause_supported_domains':total,'root_excluded':not any(total.values())});print('CASE two clauses',p,node,'clause sizes',list(map(len,clauses)),'subdomains',len(subrows),'labels',rows[-1]['input_labels'],rows[-1]['one_clause_supported_labels'],rows[-1]['two_clause_supported_labels'],'root',rows[-1]['root_excluded'],flush=True)
 out=ROOT/'verify/out/n100-arc-two-nogoods.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-nogoods.json','verify/out/n100-arc-ordered-cycle.json','verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogood_reinjection.py','verify/n100_arc_cycle_support.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py','verify/n100_boundary_arc_tiles_audit.py'];out.write_text(json.dumps({'schema':'n100-arc-two-nogoods/v1','verified_integer_two_clause_tests':True,'all_new_nogood_alternate_geometry_equal':True,'all_subdomain_independent_dp_equal':True,'Boolean_conjunctive_cover_checked':True,'cases':rows,'scope':'two conditional geometric nogoods per inherited input, exact finite support under both; not all finite assignments geometrically tested','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS two cumulative nogoods')
if __name__=='__main__':main()

"""Learn a third conditional geometric nogood and verify accumulated support."""
from pathlib import Path
import json,hashlib
from n100_arc_nogood_state_dp import ROOT,load,need,state_dp,make_marks
from n100_arc_nogood_reinjection import setup,build,intersect,independent_tile,coupled,independent

def main():
 source='verify/out/n100-arc-nogood-state-dp.json';clausesource='verify/out/n100-arc-two-nogoods.json';models=load('verify/out/n100-arc-ordered-cycle.json')['cases'];priorclauses=load(clausesource)['cases'];baseline=load('verify/out/n100-arc-center-projection.json')['cases'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};rows=[]
 for old in load(source)['cases']:
  p=old['placement'];node=old['source_node'];clauses=next(c['clauses'] for c in priorclauses if c['placement']==p and c['source_node']==node);model=next(c for c in models if c['placement']==p and c['source_node']==node);base=next(c['result']['boxes'] for c in baseline if c['placement']==p and c['source_node']==node);_,E,q=setup(core,p,prior[tuple(p)]);_,IE,Iq=independent.setup(core,p,prior[tuple(p)]);order=old['boundary_order'];w=old['anchor_witnesses'][0];assignment=[[v,s[0]] for v,s in zip(order,w)];need(all(any(dict(assignment)[v]!=j for v,j in c) for c in clauses),'new witness avoids both prior clauses')
  def test(restrictions):
   B=[b[:] for b in base]
   for v,j in restrictions:
    b=intersect(B[v],independent_tile(j,256,signs[q[v-100]]));need(b is not None,'witness restriction');B[v]=b
   a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'third nogood alternate geometry');return a
  initial_proof=test(assignment)
  if not initial_proof['excluded']:
   rows.append({'placement':p,'source_node':node,'learned':False,'new_witness_result':initial_proof});print('NO NEW CONFLICT',p,node,flush=True);continue
  active=[a[:] for a in assignment];log=[]
  for r in assignment:
   trial=[a for a in active if a!=r];result=test(trial);log.append({'remove_trial':r,'excluded':result['excluded'],'remaining_count':len(trial),'result_sha256':hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()})
   if result['excluded']:active=trial
  proof=test(active);need(active and proof['excluded'],'confirmed third conditional conflict');need(all(set(map(tuple,active))!=set(map(tuple,c)) for c in clauses),'distinct new conflict');allclauses=clauses+[active];D={int(v):b for v,b in model['globally_supported_domains'].items()};lookup={frozenset((r['v'],r['w'])):r for r in model['relations']};tables=[];same=[]
  for i,v in enumerate(order):
   z=order[(i+1)%len(order)];r=lookup[frozenset((v,z))];tables.append({int(j):b for j,b in (r['forward'] if r['v']==v else r['reverse']).items()});same.append(q[v-100]==q[z-100])
  support,witnesses,stats=state_dp([D[v] for v in order],tables,same,make_marks(order,D,allclauses),3)
  # Differential encoding check: third clause is a union of literal-avoiding subdomains,
  # each solved with the previously oracle-checked two-bit solver.
  union=[0]*len(order);subrows=[]
  for v,j in active:
   sub=D.copy();sub[v]&=~(1<<j);a,sw,st=state_dp([sub[x] for x in order],tables,same,make_marks(order,sub,clauses),2);union=[x|y for x,y in zip(union,a)];subrows.append({'forbid':[v,j],'supported_domains':dict(zip(order,a))})
  need(union==support,'three-bit versus two-bit subdomain union');oldD={int(v):b for v,b in old['supported_domains'].items()};need(all(b&~oldD[v]==0 for v,b in zip(order,support)),'support monotone under learning')
  for witness in witnesses:
   values=dict(zip(order,(s[0] for s in witness)));need(all(any(values[v]!=j for v,j in c) for c in allclauses),'all three conflicts satisfied')
  rows.append({'placement':p,'source_node':node,'learned':True,'clauses':allclauses,'initial_assignment':assignment,'initial_assignment_proof':initial_proof,'third_clause_proof':proof,'deletion_log':log,'support_before':old['supported_label_count'],'support_after':sum(b.bit_count() for b in support),'supported_domains':dict(zip(order,support)),'boundary_order':order,'anchor_witnesses':witnesses,'state_statistics':stats,'differential_subdomains':subrows,'root_excluded':not any(support)});print('THREE CLAUSES',p,node,'sizes',list(map(len,allclauses)),'labels',old['supported_label_count'],rows[-1]['support_after'],'states',stats['maximum_states_in_one_layer'],'root',rows[-1]['root_excluded'],flush=True)
 out=ROOT/'verify/out/n100-arc-third-nogood.json';need(not out.exists(),'overwrite');paths=[source,clausesource,'verify/out/n100-arc-ordered-cycle.json','verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_nogood_state_dp.py','verify/n100_arc_nogood_reinjection.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py','verify/n100_boundary_arc_tiles_audit.py'];out.write_text(json.dumps({'schema':'n100-arc-third-nogood/v1','verified_integer_third_clause_tests':True,'all_geometry_alternate_results_equal':True,'all_learned_three_bit_supports_equal_two_bit_subdomain_unions':True,'cases':rows,'scope':'two inherited parent boxes, at most one learned conditional conflict each; differential state encoding uses same core DP, not independent end-to-end proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS third conflict learning')
if __name__=='__main__':main()

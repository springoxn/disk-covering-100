"""Extract root-specific multi-vertex nogoods from rejected arc assignments."""
from pathlib import Path
import json,hashlib
from n100_arc_witness_geometry import ROOT,load,need,setup,build,independent,independent_tile,intersect,coupled

def main():
 source='verify/out/n100-arc-witness-geometry.json';baseline=load('verify/out/n100-arc-center-projection.json')['cases'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};rows=[]
 for case in load(source)['cases']:
  p=case['placement'];node=case['source_node'];base=next(c['result']['boxes'] for c in baseline if c['placement']==p and c['source_node']==node);_,E,q=setup(core,p,prior[tuple(p)]);_,IE,Iq=independent.setup(core,p,prior[tuple(p)]);assignment=case['witnesses'][0]['assignment'];log=[]
  def test(restrictions):
   B=[b[:] for b in base]
   for v,j in restrictions:
    b=intersect(B[v],independent_tile(j,256,signs[q[v-100]]));need(b is not None,'input tile');B[v]=b
   a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'nogood replay');return a
  active=[r[:] for r in assignment]
  for restriction in assignment:
   trial=[r for r in active if r!=restriction];r=test(trial);log.append({'removed_trial':restriction,'remaining_count':len(trial),'excluded':r['excluded'],'fixed':r.get('fixed'),'result_sha256':hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()})
   if r['excluded']:active=trial
  proof=test(active);need(proof['excluded'] and active,'nonempty confirmed nogood');drops=[]
  for restriction in active:
   r=test([x for x in active if x!=restriction]);drops.append({'removed':restriction,'excluded':r['excluded'],'fixed':r.get('fixed'),'result_sha256':hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()})
  rows.append({'placement':p,'source_node':node,'original_restrictions':len(assignment),'nogood_restrictions':active,'restriction_count':len(active),'proof':proof,'deletion_log':log,'final_single_deletion_tests':drops,'irreducible_under_this_bounded_propagator':all(not r['excluded'] for r in drops)});print('nogood',p,node,'size',len(active),'irreducible',rows[-1]['irreducible_under_this_bounded_propagator'],'restrictions',active,flush=True)
 out=ROOT/'verify/out/n100-arc-nogoods.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_arc_witness_geometry.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-nogoods/v1','verified_integer_nogood_proofs':True,'all_alternate_results_equal':True,'cases':rows,'scope':'each nogood valid only in its inherited root/leaf boxes; non-exclusion after dropping a restriction does not prove feasibility or logical minimality','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS two conditional nogoods')
if __name__=='__main__':main()

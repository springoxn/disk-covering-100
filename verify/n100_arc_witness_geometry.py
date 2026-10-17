"""Test complete monotone finite witnesses against continuous interval geometry."""
from pathlib import Path
from collections import Counter
import json,hashlib
from n100_boundary_arc_tiles import ROOT,load,need,intersect,setup,build
from n100_boundary_arc_tiles_audit import independent_tile
from n100_circle_center_alternating import coupled,independent

def main():
 source='verify/out/n100-arc-monotone-cycle.json';prior_source='verify/out/n100-arc-center-projection.json';baseline=load(prior_source)['cases'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};rows=[]
 for case in load(source)['cases']:
  p=case['placement'];node=case['source_node'];base=next(c['result']['boxes'] for c in baseline if c['placement']==p and c['source_node']==node);_,E,q=setup(core,p,prior[tuple(p)]);IB,IE,Iq=independent.setup(core,p,prior[tuple(p)]);MB,ME,Mq=setup(core,p,prior[tuple(p)]);need((MB,ME,Mq)==(IB,IE,Iq),'independent topology setup');order=case['boundary_order'];results=[]
  for wi,witness in enumerate(case['anchor_state_witnesses']):
   B=[b[:] for b in base];assignment=[]
   for v,state in zip(order,witness):
    label=state//2;t=independent_tile(label,256,signs[q[v-100]]);b=intersect(B[v],t);need(b is not None,'nonempty witness tile');B[v]=b;assignment.append([v,label])
   a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'full alternate geometry replay');results.append({'witness_index':wi,'assignment':assignment,'input_vertex_boxes':[[v,B[v]] for v in order],'result':a});print('witness',p,'node',node,wi,'excluded',a['excluded'],'fixed',a.get('fixed'),'sweep',a.get('sweep',a.get('sweeps')),flush=True)
  counts={'excluded':sum(c['result']['excluded'] for c in results),'fixed':sum(not c['result']['excluded'] and c['result']['fixed'] for c in results),'capped':sum(not c['result']['excluded'] and not c['result']['fixed'] for c in results)};rows.append({'placement':p,'source_node':node,'counts':counts,'assignments_tested':len(results),'witnesses':results});print('CASE',p,node,counts,flush=True)
 out=ROOT/'verify/out/n100-arc-witness-geometry.json';need(not out.exists(),'overwrite');paths=[source,prior_source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_boundary_arc_tiles_audit.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_circle_propagation.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py'];out.write_text(json.dumps({'schema':'n100-arc-witness-geometry/v1','verified_integer_assignment_tests':True,'all_alternate_geometry_results_equal':True,'independent_topology_setup_equal':True,'cases':rows,'scope':'selected complete label assignments only; not an exhaustive partition of either source domain, no root elimination from rejecting witnesses','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS witness geometry',sum(c['assignments_tested'] for c in rows))
if __name__=='__main__':main()

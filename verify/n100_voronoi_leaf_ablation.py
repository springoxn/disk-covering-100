"""Ablation: compare64 equal-distance leaf results to adjacency-only alternation."""
from pathlib import Path
import json,hashlib
from n100_voronoi_bisector_vertex import ROOT,load,need,width
from n100_circle_center_alternating import coupled
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import build

def main():
 sp='verify/out/n100-voronoi-branch-leaves.json';z=load(sp);core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});rows=[]
 for tree in z['trees']:
  p=tree['placement'];source=load(tree['source']);_,E,q=setup(core,p,prior[tuple(p)])
  for leaf in tree['leaves']:
   B=source['nodes'][leaf['node']]['result']['boxes'];r=coupled(B,E,q,pairs,limit=40);alt=coupled(B,E,q,pairs,alt=True,limit=40);need(r==alt,'adjacency control replay');need(not r['excluded'] and r['fixed'],'control fixed');full=leaf['result'];need(not full['excluded'] and full['fixed'],'full fixed');equal=r['boxes']==full['boxes'];rows.append({'placement':p,'node':leaf['node'],'boxes_equal':equal,'control_width_reduction':width(B)-width(r['boxes']),'equal_distance_width_reduction':leaf['extra_width_reduction'],'full_trace_zero':all(x==0 for x in full['trace'])})
 out=ROOT/'verify/out/n100-voronoi-leaf-ablation.json';need(not out.exists(),'overwrite');paths=[sp,'verify/n100_voronoi_branch_leaves.py','verify/n100_voronoi_reverse_distance.py','verify/n100_circle_center_alternating.py','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json']+[t['source'] for t in z['trees']];result={'schema':'n100-voronoi-leaf-ablation/v1','verified_integer_comparison':True,'cases':len(rows),'identical_final_box_cases':sum(r['boxes_equal'] for r in rows),'control_total_width_reduction':sum(r['control_width_reduction'] for r in rows),'full_total_width_reduction':sum(r['equal_distance_width_reduction'] for r in rows),'rows':rows,'scope':'ablation on64 saved leaves; shared drivers, alternate arithmetic replay; no global claim','machine_verified_geometry':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS ablation identical',result['identical_final_box_cases'],'of64; total control/full',result['control_total_width_reduction'],result['full_total_width_reduction'])
if __name__=='__main__':main()

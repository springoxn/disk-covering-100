"""Test equal-distance geometry on conflict branches with distance-only ablation."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
from n100_voronoi_reverse_distance import ROOT,load,need,run,inverse_square,width,setup,build,coupled,equations

def main():
 controls=0
 for n in range(-80,81):
  x=Fraction(n,7);lo=x.numerator//x.denominator;hi=-((-x.numerator)//x.denominator);s=x*x;L=s.numerator//s.denominator;H=-((-s.numerator)//s.denominator)
  for interval in ((lo,hi),(lo-3,hi+3),(-20,20)):
   a=inverse_square(interval,L,H);b=inverse_square(interval,L,H,True);need(a==b and a is not None and a[0]<=x<=a[1],'rational reverse control');controls+=1
 source='verify/out/n100-arc-conflict-branch.json';z=load(source);p=z['placement'];node=z['source_node'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});rows=[]
 for child in z['children']:
  if child['excluded']:continue
  start=child['arc_result']['boxes'];baseline=coupled(start,E,q,pairs,limit=160);altbase=coupled(start,E,q,pairs,alt=True,limit=160);need(baseline==altbase and not baseline['excluded'] and baseline['fixed'],'distance baseline fixed replay');a=run(start,E,q,pairs,limit=80);b=run(start,E,q,pairs,alternative=True,limit=80);need(a==b,'alternate inverse roots and distance propagation');end=a.get('boxes',a.get('result',{}).get('boxes'));summary={'child':child['child'],'excluded':a['excluded'],'fixed':a.get('fixed'),'sweeps':a['sweeps'],'input_width':width(start),'distance_baseline_width':width(baseline['boxes']),'equal_distance_width':width(end),'additional_width_removed':width(baseline['boxes'])-width(end),'identical_to_distance_only':not a['excluded'] and end==baseline['boxes']};rows.append({'summary':summary,'distance_only_result':baseline,'equal_distance_result':a});print('EQUAL BRANCH',summary,flush=True)
 out=ROOT/'verify/out/n100-voronoi-conflict-branches.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_voronoi_reverse_distance.py','verify/n100_voronoi_bisector_vertex.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-voronoi-conflict-branches/v1','verified_integer_equal_distance_tests':True,'rational_controls':controls,'all_alternate_geometry_equal':True,'distance_only_ablation_per_branch':True,'placement':p,'source_node':node,'equation_count':len(equations(E)),'rows':rows,'strictly_excluded_children':sum(r['summary']['excluded'] for r in rows),'scope':'conditional Voronoi equalities on two inherited branches; ablation isolates equality benefit; shared driving and bisector code, not independent full proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS branch equal-distance ablation')
if __name__=='__main__':main()

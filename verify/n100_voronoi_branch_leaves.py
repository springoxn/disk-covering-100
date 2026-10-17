"""Apply exact equal-distance contractors to all64 saved branch leaves."""
from pathlib import Path
import json,hashlib
from n100_voronoi_reverse_distance import run
from n100_voronoi_bisector_vertex import ROOT,load,need,width
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import build

def finalboxes(r):return r.get('boxes',r.get('result',{}).get('boxes'))
def main():
 paths=['verify/out/n100-boundary-circle-branch-tree.json','verify/out/n100-boundary-circle-branch-tree-202709.json'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});trees=[]
 for path in paths:
  tree=load(path);p=tree['placement'];nodes=tree['nodes'];seen=set();leaves=[]
  def visit(i,depth):
   need(i not in seen and 0<=i<len(nodes),'unique node');seen.add(i);n=nodes[i];need(n['level']==depth,'depth')
   if n['kind']=='split':
    f,d=n['face'],n['coordinate'];lo,hi=n['result']['boxes'][f][2*d:2*d+2];need([lo,hi]==n['interval'] and lo<n['split']<hi,'parent interval');need(len(n['children'])==2,'binary');visit(n['children'][0],depth+1);visit(n['children'][1],depth+1)
   else:need(n['kind']=='unresolved' and not n['result']['excluded'],'expected unresolved leaf');leaves.append(i)
  visit(0,0);need(len(seen)==63 and len(leaves)==32,'complete32-leaf tree');_,E,q=setup(core,p,prior[tuple(p)]);rows=[]
  for i in leaves:
   B=nodes[i]['result']['boxes'];a=run(B,E,q,pairs);b=run(B,E,q,pairs,True);need(a==b,'alternative arithmetic mismatch');end=finalboxes(a);need(end is not None and len(B)==len(end),'boxes');need(all(x[2*k]<=y[2*k]<=y[2*k+1]<=x[2*k+1] for x,y in zip(B,end) for k in (0,1)),'nested');rows.append({'node':i,'extra_width_reduction':width(B)-width(end),'result':a});print('leaf',p,i,'excluded',a['excluded'],'fixed',a.get('fixed'),'shrink',rows[-1]['extra_width_reduction'],flush=True)
  excluded=sum(r['result']['excluded'] for r in rows);counts={'excluded':excluded,'fixed':sum(not r['result']['excluded'] and r['result']['fixed'] for r in rows),'capped':sum(not r['result']['excluded'] and not r['result']['fixed'] for r in rows),'contracted':sum(r['extra_width_reduction']>0 for r in rows)};trees.append({'source':path,'placement':p,'counts':counts,'root_excluded':excluded==len(leaves),'total_extra_width_reduction':sum(r['extra_width_reduction'] for r in rows),'leaves':rows});print('TREE',p,counts,flush=True)
 out=ROOT/'verify/out/n100-voronoi-branch-leaves.json';need(not out.exists(),'overwrite');bindings=paths+['verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_voronoi_reverse_distance.py','verify/n100_voronoi_bisector_vertex.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py','verify/n100_boundary_circle_propagation.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py'];out.write_text(json.dumps({'schema':'n100-voronoi-branch-leaves/v1','verified_integer_tests':True,'input_leaves':64,'alternative_arithmetic_all_results_equal':True,'all_output_boxes_nested':True,'trees':trees,'scope':'64 saved closed-cover leaves from two fixed-core representatives; source coverage inherited, Voronoi equality analytic; shared driving logic','machine_verified_geometry':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in bindings},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS64 leaf tests',[(t['placement'],t['counts'],t['root_excluded']) for t in trees])
if __name__=='__main__':main()

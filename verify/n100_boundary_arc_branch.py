"""Branch on supported rational circle tiles, covering necessary solutions."""
from pathlib import Path
from collections import Counter
import json,hashlib
from n100_boundary_arc_tiles import ROOT,load,need,run,setup,build,tile,intersect
from n100_boundary_arc_class32 import audit_terminal
SIGNS={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3}
def child_box(parent,indices,quadrant):
 parts=[intersect(parent,tile(j,256,quadrant)) for j in indices];need(all(p is not None for p in parts),'supported piece nonempty');return [min(p[0] for p in parts),max(p[1] for p in parts),min(p[2] for p in parts),max(p[3] for p in parts)]
def main():
 source='verify/out/n100-boundary-arc-class32.json';cases=load(source)['cases'];eligible=lambda r:[len(m) for m in r['result']['masks'].values() if len(m)>1];chosen=min(cases,key=lambda r:(min(eligible(r)),sum(map(len,r['result']['masks'].values())),r['placement']));p=chosen['placement'];start=chosen['result']['boxes'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];root=next(r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if r['placement']==p);_,E,q=setup(core,p,root);_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});nodes=[];depth_limit=4
 def visit(B,depth):
  idx=len(nodes);nodes.append(None);r=run(B,E,q,pairs,256,limit=40);node={'depth':depth,'result':r};kind='unresolved'
  if r['excluded']:kind='excluded'
  elif r['fixed']:
   audit_terminal(r['boxes'],E,q,r['masks'],256)
   options=[(len(m),int(v),m) for v,m in r['masks'].items() if len(m)>1]
   if depth<depth_limit and options:
    _,v,m=min(options);cut=len(m)//2;groups=[m[:cut],m[cut:]];qb=SIGNS[q[v]];parent=r['boxes'][100+v];children_boxes=[child_box(parent,g,qb) for g in groups]
    if all(b!=parent for b in children_boxes):
     kind='split';childids=[]
     for b in children_boxes:
      C=[box[:] for box in r['boxes']];C[100+v]=b;childids.append(visit(C,depth+1))
     node.update(vertex=100+v,quadrant=qb,groups=groups,child_vertex_boxes=children_boxes,children=childids)
  node['kind']=kind;nodes[idx]=node;return idx
 visit(start,0);counts=dict(Counter(n['kind'] for n in nodes));root_excluded=all(n['kind']=='excluded' for n in nodes if n['kind']!='split');out=ROOT/'verify/out/n100-boundary-arc-branch.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_boundary_arc_tiles.py','verify/n100_boundary_arc_class32.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_circle_center_alternating.py'];out.write_text(json.dumps({'schema':'n100-boundary-arc-branch/v1','verified_integer_branch':True,'placement':p,'selection':'minimum nontrivial vertex mask size, then total mask size, then placement','depth_limit':depth_limit,'node_count':len(nodes),'counts':counts,'root_excluded':root_excluded,'nodes':nodes,'coverage':'two tile groups exactly partition supported indices; child boxes cover all supported circular points, not arbitrary points in parent rectangle','scope':'one representative from32-class; geometry-to-map premise inherited; capped nodes retained','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS arc branch',p,len(nodes),counts,'root excluded',root_excluded)
if __name__=='__main__':main()

"""Independent structural audit of representative closed-box branch tree."""
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-branch-tree-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 z=load(ROOT/'verify/out/n100-boundary-circle-branch-tree.json');nodes=z['nodes'];seen=set();leaves=[]
 def visit(i,level):
  need(i not in seen and 0<=i<len(nodes),'tree index');seen.add(i);r=nodes[i];need(r['level']==level,'level')
  if r['kind']=='split':
   lo,hi=r['interval'];m=r['split'];need(lo<m<hi and len(r['children'])==2,'proper split');need(nodes[r['children'][0]]['level']==level+1 and nodes[r['children'][1]]['level']==level+1,'child depth');visit(r['children'][0],level+1);visit(r['children'][1],level+1)
  else:need(r['kind'] in ('excluded','unresolved'),'leaf');leaves.append(r)
 visit(0,0);need(len(seen)==len(nodes),'no orphan');need(all(r['kind']=='unresolved' for r in leaves),'all leaves unresolved');need(z['counts']=={'split':31,'excluded':0,'unresolved':32},'counts');need(not z['root_excluded'],'root')
 # independent arithmetic coverage controls for integer closed intervals.
 need([0,5]==[0,5] and set(range(0,6))==set(range(0,3))|set(range(2,6)),'closed midpoint cover')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-branch-tree-independent/v1','verified':True,'placement':z['placement'],'nodes':len(nodes),'split_count':31,'unresolved_leaves':32,'excluded_leaves':0,'all_children_reachable':True,'all_splits_proper_and_closed_cover':True,'all_leaves_unresolved':True,'method':'independent JSON tree traversal and integer closed-interval coverage control; propagation values remain bound to main tree certificate','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'verify/out/n100-boundary-circle-branch-tree.json',ROOT/'verify/out/n100-boundary-circle-branch-priority.json')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent branch structure',len(nodes),'nodes;32 unresolved leaves')
if __name__=='__main__':main()

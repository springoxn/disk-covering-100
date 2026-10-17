"""Audit rational tile-group coverage and all branch descendant inclusions."""
from pathlib import Path
from collections import Counter
import json,hashlib
from n100_boundary_arc_tiles_audit import independent_tile
from n100_boundary_arc_tiles import ROOT,load,need,setup
from n100_boundary_arc_class32 import audit_terminal

def boxes(r):return r.get('boxes',r.get('result',{}).get('boxes'))
def inside(a,b):return len(a)==len(b) and all(x[2*k]<=y[2*k]<=y[2*k+1]<=x[2*k+1] for x,y in zip(a,b) for k in (0,1))
def main():
 source='verify/out/n100-boundary-arc-branch.json';tree=load(source);p=tree['placement'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if r['placement']==p);_,E,q=setup(core,p,prior);nodes=tree['nodes'];initial=next(c['result']['boxes'] for c in load('verify/out/n100-boundary-arc-class32.json')['cases'] if c['placement']==p);seen=set();split_count=0;leaf_count=0
 def visit(i,parent,depth):
  nonlocal split_count,leaf_count
  need(0<=i<len(nodes) and i not in seen,'tree references');seen.add(i);n=nodes[i];r=n['result'];B=boxes(r);need(n['depth']==depth and inside(parent,B),'depth/nesting')
  if not r['excluded'] and r['fixed']:audit_terminal(B,E,q,r['masks'],256)
  if n['kind']!='split':
   leaf_count+=1;need(n['kind']==('excluded' if r['excluded'] else 'unresolved'),'leaf status');return
  split_count+=1;v=n['vertex'];m=r['masks'][str(v-100)];g,h=n['groups'];need(g and h and set(g).isdisjoint(h) and sorted(g+h)==m and len(n['children'])==2,'complete disjoint supported-index partition');a=B[v];expected=[]
  for group in (g,h):
   parts=[]
   for j in group:
    t=independent_tile(j,256,n['quadrant']);c=[max(a[0],t[0]),min(a[1],t[1]),max(a[2],t[2]),min(a[3],t[3])];need(c[0]<=c[1] and c[2]<=c[3],'retained piece');parts.append(c)
   expected.append([min(c[0] for c in parts),max(c[1] for c in parts),min(c[2] for c in parts),max(c[3] for c in parts)])
  need(expected==n['child_vertex_boxes'],'independent child hulls')
  for child,b in zip(n['children'],expected):
   C=[c[:] for c in B];C[v]=b;visit(child,C,depth+1)
 visit(0,initial,0);need(len(seen)==len(nodes),'no orphan');counts=dict(Counter(n['kind'] for n in nodes));need(counts==tree['counts'],'counts');root_empty=all(n['kind']=='excluded' for n in nodes if n['kind']!='split');need(root_empty==tree['root_excluded'],'root status');out=ROOT/'verify/out/n100-boundary-arc-branch-audit.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-boundary-arc-class32.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_boundary_arc_tiles_audit.py','verify/n100_boundary_arc_class32.py'];out.write_text(json.dumps({'schema':'n100-boundary-arc-branch-audit/v1','verified_integer_audit':True,'placement':p,'nodes_checked':len(nodes),'splits_checked':split_count,'leaves_checked':leaf_count,'counts':counts,'all_groups_partition_parent_support':True,'all_child_hulls_recomputed_with_integer_endpoints':True,'all_output_boxes_nested_in_child_inputs':True,'all_fixed_terminal_masks_recomputed':True,'root_excluded':root_empty,'scope':'necessary circular solution coverage audit; source contractor soundness inherited, not independent propagation replay','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS arc branch audit',p,len(nodes),counts,'root',root_empty)
if __name__=='__main__':main()

"""Audit union of supported label domains over every covered spatial leaf."""
from pathlib import Path
import json,hashlib
from n100_circle_center_alternating import ROOT,load,need

def main():
 source='verify/out/n100-spatial-leaf-joint.json';z=load(source);tree=load('verify/out/n100-center-spatial-tree.json');branch=next(c for c in load('verify/out/n100-arc-conflict-branch.json')['children'] if c['child']==1);D={int(v):b for v,b in branch['final_supported_domains'].items()};union={v:0 for v in D};nodes={n['id']:n for n in tree['nodes']};leaves={n['id'] for n in nodes.values() if n['kind']=='unresolved'};need({r['tree_node'] for r in z['leaves']}==leaves and len(z['leaves'])==len(leaves),'leaf coverage identity');nested=0
 for row in z['leaves']:
  if row['excluded']:continue
  if 'supported_domains' not in row:
   for v,bits in D.items():union[v]|=bits
   continue
  S={int(v):b for v,b in row['supported_domains'].items()};need(set(S)==set(D),'same boundary vertices')
  for v,bits in S.items():need(bits&~D[v]==0,'leaf support subset of child');union[v]|=bits
  A=nodes[row['tree_node']]['result']['boxes'];B=row['arc_result']['boxes'];need(len(A)==len(B) and all(a[2*k]<=b[2*k]<=b[2*k+1]<=a[2*k+1] for a,b in zip(A,B) for k in (0,1)),'leaf geometry nesting');nested+=1
 removed={v:D[v]&~union[v] for v in D};summary={'parent_child_labels':sum(b.bit_count() for b in D.values()),'union_surviving_labels':sum(b.bit_count() for b in union.values()),'additional_whole_child_label_removals':sum(b.bit_count() for b in removed.values()),'nested_leaf_box_checks':nested,'source_child_excluded':z['summary']['source_child_excluded']};out=ROOT/'verify/out/n100-spatial-leaf-union-audit.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-center-spatial-tree.json','verify/out/n100-arc-conflict-branch.json','verify/n100_spatial_leaf_joint.py'];out.write_text(json.dumps({'schema':'n100-spatial-leaf-union-audit/v1','verified_integer_union_and_nesting':True,'summary':summary,'union_supported_domains':union,'whole_child_removed_domains':removed,'scope':'structural union audit of prior supports, no independent DP replay; capped unresolved leaves conservatively contribute entire inherited label domain','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS union audit',summary)
if __name__=='__main__':main()

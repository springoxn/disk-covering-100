"""Covered continuous spatial tree on stage84 child1; all nodes double replayed."""
from pathlib import Path
import json,hashlib
from n100_circle_center_alternating import ROOT,load,need,coupled,independent
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import build

def nested(A,B):return len(A)==len(B) and all(a[2*k]<=b[2*k]<=b[2*k+1]<=a[2*k+1] for a,b in zip(A,B) for k in (0,1))
def main():
 source='verify/out/n100-arc-conflict-branch.json';z=load(source);child=next(c for c in z['children'] if c['child']==1);need(not child['excluded'],'unresolved child');start=child['arc_result']['boxes'];p=z['placement'];core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior=next(c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained'] if c['placement']==p);_,E,q=setup(core,p,prior);_,IE,Iq=independent.setup(core,p,prior);need((E,q)==(IE,Iq),'independent topology setup');_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});nodes=[]
 def visit(B,depth,parent):
  idx=len(nodes);node={'id':idx,'parent':parent,'depth':depth,'input_boxes':B};nodes.append(node);a=coupled(B,E,q,pairs,limit=160);b=coupled(B,IE,Iq,pairs,alt=True,limit=160);need(a==b,'node alternate full replay');node['result']=a
  if a['excluded']:node['kind']='excluded';print('EMPTY',idx,'depth',depth,flush=True);return idx
  C=a['boxes'];need(nested(B,C),'node contraction nesting')
  if depth==5:node['kind']='unresolved';return idx
  w,v,k=max((C[v][2*k+1]-C[v][2*k],v,k) for v in range(100) for k in (0,1))
  if w<2:node['kind']='unresolved';node['stop']='no integer midpoint in center coordinate';return idx
  lo,hi=C[v][2*k:2*k+2];m=(lo+hi)//2;L=[x[:] for x in C];R=[x[:] for x in C];L[v][2*k+1]=m;R[v][2*k]=m;node.update({'kind':'split','split':{'center':v,'coordinate':k,'lo':lo,'mid':m,'hi':hi}});left=visit(L,depth+1,idx);right=visit(R,depth+1,idx);node['children']=[left,right];return idx
 root=visit([b[:] for b in start],0,None);seen=set()
 def audit(i):
  need(i not in seen,'tree uniqueness');seen.add(i);n=nodes[i]
  if n['kind']!='split':return n['kind']=='excluded'
  C=n['result']['boxes'];s=n['split'];v,k=s['center'],s['coordinate'];lo,hi=C[v][2*k:2*k+2];m=s['mid'];need((lo,hi)==(s['lo'],s['hi']) and lo<m<hi,'proper split');expected=[]
  for side in (0,1):
   B=[b[:] for b in C];B[v][2*k+(1 if side==0 else 0)]=m;expected.append(B)
  flags=[]
  for j,c in enumerate(n['children']):need(nodes[c]['parent']==i and nodes[c]['input_boxes']==expected[j],'closed real interval cover replay');flags.append(audit(c))
  return all(flags)
 rootempty=audit(root);need(len(seen)==len(nodes),'all nodes reachable');counts={kind:sum(n['kind']==kind for n in nodes) for kind in ('split','excluded','unresolved')};out=ROOT/'verify/out/n100-center-spatial-tree.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py','verify/n100_boundary_circle_propagation.py'];out.write_text(json.dumps({'schema':'n100-center-spatial-tree/v1','verified_integer_continuous_tree':True,'all_node_alternate_replays_equal':True,'independent_topology_setup_equal':True,'all_splits_exact_closed_interval_cover':True,'all_nodes_reachable':True,'placement':p,'source_node':z['source_node'],'source_child':1,'max_depth':5,'branch_rule':'largest center coordinate width, lexicographic tie by center then coordinate','counts':counts,'source_child_excluded':rootempty,'nodes':nodes,'scope':'covers continuous box relaxation of stage84 child1; projected hull may include disallowed label combinations, so rejection is safe but retention is not feasibility; no global core enumeration','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS spatial tree',counts,'source child excluded',rootempty)
if __name__=='__main__':main()

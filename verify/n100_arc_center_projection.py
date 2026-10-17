"""Disjunctive projection from supported boundary arcs back to centers."""
from pathlib import Path
import json,hashlib
from n100_boundary_arc_tiles import ROOT,load,need,tile,intersect,support,width,setup,build,coupled,radiussquared
from n100_axis_coupled_boxes import contract
from n100_axis_coupled_boxes_independent import clip
from n100_boundary_arc_class32 import audit_terminal

def hull(parts):
 return [min(p[0] for p in parts),max(p[1] for p in parts),min(p[2] for p in parts),max(p[3] for p in parts)]
def checked_contract(a,b,r2):
 x=contract(a,b,r2);y=clip(a,b,r2);need(x==y,'independent projection contractor');return x

def run(start,E,q,pairs,n=256,limit=80):
 B=[b[:] for b in start];inc={}
 for f,v in E:inc.setdefault(v,[]).append(f)
 signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};parts={v:[tile(j,n,signs[sg]) for j in range(n)] for v,sg in q.items()};trace=[];masks={};r2=radiussquared(1)
 for sw in range(limit):
  old=[b[:] for b in B];center_changes=vertex_changes=0;projection_checks=0
  for v,tiles in sorted(parts.items()):
   idx=100+v;kept=[];mask=[]
   for j,t in enumerate(tiles):
    c=intersect(B[idx],t)
    if c is not None and all(support(c,B[f],r2) for f in inc[idx]):kept.append(c);mask.append(j)
   masks[str(v)]=mask
   if not kept:return {'excluded':True,'phase':'arc_support','vertex':idx,'sweeps':sw+1,'boxes':B,'trace':trace,'masks':masks}
   new=hull(kept)
   if new!=B[idx]:B[idx]=new;vertex_changes+=1
   for f in inc[idx]:
    projections=[]
    for c in kept:
     projection_checks+=1;new=checked_contract(B[f],c,r2)
     if new is not None:projections.append(new)
    if not projections:return {'excluded':True,'phase':'center_projection','failure':[idx,f],'sweeps':sw+1,'boxes':B,'trace':trace,'masks':masks}
    new=hull(projections)
    if new!=B[f]:B[f]=new;center_changes+=1
  r=coupled(B,E,q,pairs,limit=1)
  if r['excluded']:return {'excluded':True,'phase':'coupled','sweeps':sw+1,'result':r,'trace':trace,'masks':masks}
  B=r['boxes'];trace.append({'center_changes':center_changes,'vertex_changes':vertex_changes,'projection_checks':projection_checks})
  if B==old:return {'excluded':False,'fixed':True,'sweeps':sw+1,'boxes':B,'trace':trace,'masks':masks}
 return {'excluded':False,'fixed':False,'sweeps':limit,'boxes':B,'trace':trace,'masks':masks}

def main():
 # Disjunctive projection controls: retain both possible center regions; reject no support.
 point0=[0,0,0,0];point10=[10,10,0,0];root=[-5,15,-5,5];parts=[checked_contract(root,p,1) for p in (point0,point10)];need(hull(parts)==[-1,11,-1,1],'two-component hull');need(checked_contract([3,3,4,4],point0,24) is None and checked_contract([3,3,4,4],point0,25)==[3,3,4,4],'strict/tangent controls')
 core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});tree=load('verify/out/n100-boundary-arc-branch.json');cases=[{'placement':tree['placement'],'source_node':i,'boxes':r['result']['boxes']} for i,r in enumerate(tree['nodes']) if r['kind']=='unresolved'];need(len(cases)==16,'16 leaves');candidate=next(c for c in load('verify/out/n100-boundary-arc-tiles.json')['cases'] if c['placement']==[30,6,14,22] and c['tiles_per_quadrant']==256);cases.append({'placement':candidate['placement'],'source_node':None,'boxes':candidate['result']['boxes']});rows=[]
 for i,case in enumerate(cases,1):
  p=case['placement'];start=case['boxes'];_,E,q=setup(core,p,prior[tuple(p)]);r=run(start,E,q,pairs);end=r.get('boxes',r.get('result',{}).get('boxes'));need(len(start)==len(end) and all(a[2*k]<=b[2*k]<=b[2*k+1]<=a[2*k+1] for a,b in zip(start,end) for k in (0,1)),'nested boxes')
  if not r['excluded'] and r['fixed']:audit_terminal(end,E,q,r['masks'],256)
  rows.append({'placement':p,'source_node':case['source_node'],'extra_width_reduction':width(start)-width(end),'result':r});print('case',i,p,'node',case['source_node'],'excluded',r['excluded'],'fixed',r.get('fixed'),'shrink',rows[-1]['extra_width_reduction'],'sweeps',r['sweeps'],flush=True)
 need(not rows[-1]['result']['excluded'],'candidate rejected: investigate');leafrows=rows[:-1];counts={'excluded':sum(r['result']['excluded'] for r in leafrows),'fixed':sum(not r['result']['excluded'] and r['result']['fixed'] for r in leafrows),'capped':sum(not r['result']['excluded'] and not r['result']['fixed'] for r in leafrows)};out=ROOT/'verify/out/n100-arc-center-projection.json';need(not out.exists(),'overwrite');paths=['verify/out/n100-boundary-arc-branch.json','verify/out/n100-boundary-arc-tiles.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_boundary_arc_tiles.py','verify/n100_boundary_arc_class32.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_circle_propagation.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-arc-center-projection/v1','verified_integer_projection_tests':True,'projection_contractors_all_equal':True,'two_component_hull_control':True,'strict_and_tangent_controls':True,'leaf_counts':counts,'source_root_excluded':counts['excluded']==16,'candidate_retained':True,'cases':rows,'total_leaf_extra_width_reduction':sum(r['extra_width_reduction'] for r in leafrows),'scope':'16 covered leaves of one representative plus candidate control; all projection contractions checked with independent clip, terminal masks audited, not independent full replay','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS arc center projection',counts,'candidate retained')
if __name__=='__main__':main()

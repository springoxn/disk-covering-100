"""Full32-member class scan with256 rational arc tiles per quadrant."""
from pathlib import Path
from collections import Counter
import json,hashlib
from n100_boundary_arc_tiles import ROOT,load,need,run,width,setup,build,radiussquared
from n100_boundary_arc_tiles_audit import independent_tile

def audit_terminal(B,E,q,masks,n):
 inc={}
 for f,v in E:inc.setdefault(v,[]).append(f)
 quadrants={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};total=0
 for v,sg in q.items():
  found=[]
  for j in range(n):
   t=independent_tile(j,n,quadrants[sg]);b=B[100+v];c=[max(t[0],b[0]),min(t[1],b[1]),max(t[2],b[2]),min(t[3],b[3])]
   if c[0]>c[1] or c[2]>c[3]:continue
   accept=True
   for f in inc[100+v]:
    a=B[f];d=0
    for k in (0,1):
     if c[2*k+1]<a[2*k]:d+=(a[2*k]-c[2*k+1])**2
     elif a[2*k+1]<c[2*k]:d+=(c[2*k]-a[2*k+1])**2
    if d>radiussquared(1):accept=False;break
   if accept:found.append(j)
  need(found==masks[str(v)] and found,'terminal support mask');total+=len(found)
 return total

def main():
 source='verify/out/n100-boundary-order.json';core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};cases=[r for r in load(source)['cases'] if r['placement']!=[30,6,14,22]];need(len(cases)==32,'32 inputs');domain=load('verify/out/n100-boundary-circle-survivor-domain.json');members={tuple(p) for p in domain['survivor_axis_edge_placements'] if tuple((p[(i+1)%4]-p[i])%32 for i in range(4))==(7,7,7,11)};need(len(members)==32 and members=={tuple(r['placement']) for r in cases},'complete class');_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});rows=[];hist=Counter()
 for i,case in enumerate(cases,1):
  p=case['placement'];start=case['result']['boxes'];_,E,q=setup(core,p,prior[tuple(p)]);r=run(start,E,q,pairs,256);end=r.get('boxes',r.get('result',{}).get('boxes'));need(len(start)==len(end) and all(a[2*k]<=b[2*k]<=b[2*k+1]<=a[2*k+1] for a,b in zip(start,end) for k in (0,1)),'nested output');support_count=audit_terminal(end,E,q,r['masks'],256) if not r['excluded'] and r['fixed'] else None;reduction=width(start)-width(end);rows.append({'placement':p,'extra_width_reduction':reduction,'terminal_supported_tiles':support_count,'result':r});hist[r['sweeps']]+=1;print('case',i,p,'excluded',r['excluded'],'fixed',r.get('fixed'),'shrink',reduction,flush=True)
 counts={'excluded':sum(r['result']['excluded'] for r in rows),'fixed':sum(not r['result']['excluded'] and r['result']['fixed'] for r in rows),'capped':sum(not r['result']['excluded'] and not r['result']['fixed'] for r in rows),'contracted':sum(r['extra_width_reduction']>0 for r in rows)};out=ROOT/'verify/out/n100-boundary-arc-class32.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/out/n100-boundary-circle-survivor-domain.json','verify/n100_boundary_arc_tiles.py','verify/n100_boundary_arc_tiles_audit.py','verify/n100_circle_center_alternating.py','verify/n100_boundary_circle_propagation.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-boundary-arc-class32/v1','verified_integer_rational_scan':True,'gap_class':[7,7,7,11],'member_count':32,'tiles_per_quadrant':256,'counts':counts,'sweep_histogram':dict(sorted(hist.items())),'total_extra_width_reduction':sum(r['extra_width_reduction'] for r in rows),'minimum_extra_width_reduction':min(r['extra_width_reduction'] for r in rows),'maximum_extra_width_reduction':max(r['extra_width_reduction'] for r in rows),'all_fixed_terminal_masks_independently_recomputed':True,'cases':rows,'scope':'one complete32-member fixed-core gap class, source boxes inherited; terminal audit not independent full trajectory','machine_verified_geometry':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS arc full class',counts,'total shrink',sum(r['extra_width_reduction'] for r in rows),'sweeps',dict(hist))
if __name__=='__main__':main()

"""Independent integer endpoint and final mask audit of rational arc tile results."""
from pathlib import Path
import json,hashlib
from n100_boundary_arc_tiles import tile
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import Q,UN,UD
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def independent_tile(j,n,k):
 points=[]
 for h in (j,j+1):
  den=n*n+h*h;x=n*n-h*h;y=2*h*n
  for _ in range(k):x,y=-y,x
  points.append((x,y,den))
 out=[]
 for axis in (0,1):
  lows=[p[axis]*Q//p[2] for p in points];highs=[-((-p[axis]*Q)//p[2]) for p in points];out.extend((min(lows),max(highs)))
 return out
def main():
 source='verify/out/n100-boundary-arc-tiles.json';z=load(source);core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};r2=-(-((UN*Q)**2)//(UD*UD));tiles_checked=0
 for n in (64,256):
  for k in range(4):
   for j in range(n):need(independent_tile(j,n,k)==tile(j,n,k),'endpoint generation');tiles_checked+=1
 signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};summaries=[]
 for case in z['cases']:
  p=case['placement'];n=case['tiles_per_quadrant'];r=case['result'];need(not r['excluded'] and r['fixed'],'fixed case');B=r['boxes'];_,E,q=setup(core,p,prior[tuple(p)]);inc={}
  for f,v in E:inc.setdefault(v,[]).append(f)
  total=0
  for v,sg in q.items():
   expected=[]
   for j in range(n):
    t=independent_tile(j,n,signs[sg]);b=B[100+v];c=[max(t[0],b[0]),min(t[1],b[1]),max(t[2],b[2]),min(t[3],b[3])]
    if c[0]>c[1] or c[2]>c[3]:continue
    good=True
    for f in inc[100+v]:
     a=B[f];gapx=max(0,c[0]-a[1],a[0]-c[1]);gapy=max(0,c[2]-a[3],a[2]-c[3])
     if gapx*gapx+gapy*gapy>r2:good=False;break
    if good:expected.append(j)
   need(expected==r['masks'][str(v)] and expected,'final mask exact');total+=len(expected)
  summaries.append({'placement':p,'resolution':n,'final_supported_tiles':total})
 for p in {tuple(c['placement']) for c in z['cases']}:
  coarse=next(c['result']['boxes'] for c in z['cases'] if tuple(c['placement'])==p and c['tiles_per_quadrant']==64);fine=next(c['result']['boxes'] for c in z['cases'] if tuple(c['placement'])==p and c['tiles_per_quadrant']==256);need(all(a[2*k]<=b[2*k]<=b[2*k+1]<=a[2*k+1] for a,b in zip(coarse,fine) for k in (0,1)),'fine inside coarse')
 out=ROOT/'verify/out/n100-boundary-arc-tiles-audit.json';need(not out.exists(),'overwrite');paths=[source,'verify/n100_boundary_arc_tiles.py','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json'];out.write_text(json.dumps({'schema':'n100-boundary-arc-tiles-audit/v1','verified_integer_audit':True,'independent_endpoint_boxes_checked':tiles_checked,'all_final_masks_recomputed':True,'all_fine_boxes_nested_in_coarse':True,'cases':summaries,'scope':'independent endpoint arithmetic and terminal masks; no independent full propagation replay; setup shared','machine_verified_geometry':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS arc audit',tiles_checked,'tiles;6 final masks; fine nested')
if __name__=='__main__':main()

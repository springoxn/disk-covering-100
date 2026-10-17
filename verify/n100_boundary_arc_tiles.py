"""Exact rational arc tiles for unit-circle boundary vertices."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from n100_circle_center_alternating import ROOT,load,need,coupled
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import build,Q,radiussquared

def point(t,quadrant):
 x=(1-t*t)/(1+t*t);y=2*t/(1+t*t)
 for _ in range(quadrant):x,y=-y,x
 return x,y

def floor(x):return x.numerator//x.denominator
def ceil(x):return -((-x.numerator)//x.denominator)
def tile(j,n,k):
 a=point(F(j,n),k);b=point(F(j+1,n),k)
 return [floor(min(a[0],b[0])*Q),ceil(max(a[0],b[0])*Q),floor(min(a[1],b[1])*Q),ceil(max(a[1],b[1])*Q)]
def intersect(a,b):
 r=[max(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),min(a[3],b[3])]
 return r if r[0]<=r[1] and r[2]<=r[3] else None

def support(a,b,r2):
 gaps=[max(a[2*k]-b[2*k+1],b[2*k]-a[2*k+1],0) for k in (0,1)]
 first=sum(x*x for x in gaps)<=r2
 # Alternative exact coordinate interval separation computation.
 other=0
 for k in (0,1):
  if a[2*k+1]<b[2*k]:other+=(b[2*k]-a[2*k+1])**2
  elif b[2*k+1]<a[2*k]:other+=(a[2*k]-b[2*k+1])**2
 need(first==(other<=r2),'distance support audit');return first

def width(B):return sum(b[1]-b[0]+b[3]-b[2] for b in B)
def run(start,E,q,pairs,n,limit=40):
 B=[b[:] for b in start];inc={}
 for f,v in E:inc.setdefault(v,[]).append(f)
 signs={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3};tiles={v:[tile(j,n,signs[sg]) for j in range(n)] for v,sg in q.items()};trace=[];masks={}
 for sw in range(limit):
  old=[b[:] for b in B];supported_total=0;changes=0
  for v,parts in sorted(tiles.items()):
   idx=100+v;kept=[];mask=[]
   for j,t in enumerate(parts):
    c=intersect(B[idx],t)
    if c is not None and all(support(c,B[f],radiussquared(1)) for f in inc[idx]):kept.append(c);mask.append(j)
   masks[str(v)]=mask;supported_total+=len(mask)
   if not kept:return {'excluded':True,'phase':'arc_support','vertex':idx,'sweeps':sw+1,'boxes':B,'trace':trace,'masks':masks}
   new=[min(c[0] for c in kept),max(c[1] for c in kept),min(c[2] for c in kept),max(c[3] for c in kept)]
   if new!=B[idx]:changes+=1;B[idx]=new
  r=coupled(B,E,q,pairs,limit=1)
  if r['excluded']:return {'excluded':True,'phase':'coupled','sweeps':sw+1,'result':r,'trace':trace,'masks':masks}
  B=r['boxes'];trace.append({'supported_tiles':supported_total,'vertex_boxes_changed':changes})
  if B==old:return {'excluded':False,'fixed':True,'sweeps':sw+1,'boxes':B,'trace':trace,'masks':masks}
 return {'excluded':False,'fixed':False,'sweeps':limit,'boxes':B,'trace':trace,'masks':masks}

def main():
 controls=0
 for n in (64,256):
  for k in range(4):
   for j in range(n):
    box=tile(j,n,k)
    for s in (0,1,2):
     x,y=point(F(2*j+s,2*n),k);need(x*x+y*y==1 and box[0]<=x*Q<=box[1] and box[2]<=y*Q<=box[3],'rational arc enclosure');controls+=1
    if j+1<n:need(intersect(box,tile(j+1,n,k)) is not None,'shared endpoint cover')
 need(not support([0,0,0,0],[3,3,4,4],24) and support([0,0,0,0],[3,3,4,4],25),'distance reject/tangent')
 core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};baselines={tuple(r['placement']):r['result']['boxes'] for r in load('verify/out/n100-boundary-order.json')['cases']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});rows=[]
 for p in ([0,7,14,21],[20,27,2,9],[30,6,14,22]):
  start=baselines[tuple(p)];_,E,q=setup(core,p,prior[tuple(p)])
  for n in (64,256):
   r=run(start,E,q,pairs,n);end=r.get('boxes',r.get('result',{}).get('boxes'));rows.append({'placement':p,'tiles_per_quadrant':n,'extra_width_reduction':width(start)-width(end),'result':r});print('case',p,n,'excluded',r['excluded'],'fixed',r.get('fixed'),'shrink',rows[-1]['extra_width_reduction'],'sweeps',r['sweeps'],flush=True)
   if p==[30,6,14,22]:need(not r['excluded'],'candidate rejected: investigate')
 out=ROOT/'verify/out/n100-boundary-arc-tiles.json';need(not out.exists(),'overwrite');paths=['verify/out/n100-boundary-order.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_circle_center_alternating.py','verify/n100_boundary_circle_propagation.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-boundary-arc-tiles/v1','verified_integer_rational_tests':True,'rational_arc_point_controls':controls,'shared_endpoint_checks':True,'exact_support_comparisons_audited':True,'parameterization':'quadrant rotation of ((1-t^2)/(1+t^2),2t/(1+t^2)); t in [j/n,(j+1)/n]','rounding':'scaled rational coordinate endpoints floor lower, ceil upper; continuous real boxes','cases':rows,'scope':'two representatives plus candidate; per-vertex supports, hull union, no joint assignment proof or independent full replay','machine_verified_geometry':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS arc tile tests',len(rows),'controls',controls)
if __name__=='__main__':main()

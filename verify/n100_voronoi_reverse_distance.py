"""Reverse squared-distance contractor for equal-radius Voronoi incidences."""
from pathlib import Path
from math import isqrt
from fractions import Fraction
import json,hashlib
from n100_voronoi_bisector_vertex import ROOT,load,need,coord,sub,add,neg,square,equations,width,bisect_vertex
from n100_boundary_circle_propagation import setup
from n100_circle_center_alternating import coupled
from n100_axis_coupled_boxes import build,radiussquared

def floorroot(n):return isqrt(n)
def binaryroot(n):
 lo=0;hi=1
 while hi*hi<=n:hi*=2
 while hi-lo>1:
  m=(lo+hi)//2
  if m*m<=n:lo=m
  else:hi=m
 return lo

def inverse_square(interval,L,H,alternative=False):
 if H<0 or L>H:return None
 L=max(0,L);fn=binaryroot if alternative else floorroot;l=fn(L);u=fn(H);u+=u*u<H
 # Both signs must be intersected before taking the hull.
 parts=[]
 for a,b in ((-u,-l),(l,u)):
  lo=max(interval[0],a);hi=min(interval[1],b)
  if lo<=hi:parts.append((lo,hi))
 return None if not parts else (min(p[0] for p in parts),max(p[1] for p in parts))
def squared_distance(a,v):return add(square(sub(coord(a,0),coord(v,0))),square(sub(coord(a,1),coord(v,1))))
def reverse(a,v,target,alternative=False):
 a=a[:];v=v[:]
 for k in (0,1):
  other=square(sub(coord(a,1-k),coord(v,1-k)));L=max(0,target[0]-other[1]);H=target[1]-other[0];relative=sub(coord(a,k),coord(v,k));w=inverse_square(relative,L,H,alternative)
  if w is None:return None
  ac=add(coord(v,k),w);vc=sub(coord(a,k),w)
  a[2*k]=max(a[2*k],ac[0]);a[2*k+1]=min(a[2*k+1],ac[1]);v[2*k]=max(v[2*k],vc[0]);v[2*k+1]=min(v[2*k+1],vc[1])
  if a[2*k]>a[2*k+1] or v[2*k]>v[2*k+1]:return None
 return a,v

def run(start,E,q,pairs,alternative=False,limit=40):
 B=[b[:] for b in start];eq=equations(E);trace=[]
 for sw in range(limit):
  old=[b[:] for b in B];changes=0
  for v,a,b in eq:
   da=squared_distance(B[a],B[v]);db=squared_distance(B[b],B[v]);T=(max(da[0],db[0]),min(da[1],db[1],radiussquared(1)))
   if T[0]>T[1]:return {'excluded':True,'phase':'common_distance','failure':[v,a,b],'sweeps':sw+1,'boxes':B,'trace':trace}
   for f in (a,b):
    r=reverse(B[f],B[v],T,alternative)
    if r is None:return {'excluded':True,'phase':'reverse','failure':[v,a,b,f],'sweeps':sw+1,'boxes':B,'trace':trace}
    if r!=(B[f],B[v]):changes+=1
    B[f],B[v]=r
   z=bisect_vertex(B[v],B[a],B[b])
   if z is None:return {'excluded':True,'phase':'linear','failure':[v,a,b],'sweeps':sw+1,'boxes':B,'trace':trace}
   B[v]=z
  r=coupled(B,E,q,pairs,alt=alternative,limit=1)
  if r['excluded']:return {'excluded':True,'phase':'coupled','result':r,'sweeps':sw+1,'trace':trace}
  B=r['boxes'];trace.append(changes)
  if B==old:return {'excluded':False,'fixed':True,'sweeps':sw+1,'boxes':B,'trace':trace}
 return {'excluded':False,'fixed':False,'sweeps':limit,'boxes':B,'trace':trace}

def main():
 controls=0
 # Exhaustive rational-point enclosure controls, with integer squared-range bounds.
 for numerator in range(-80,81):
  x=Fraction(numerator,7);lo=x.numerator//x.denominator;hi=-((-x.numerator)//x.denominator);s=x*x;L=s.numerator//s.denominator;H=-((-s.numerator)//s.denominator)
  for interval in ((lo,hi),(lo-3,hi+3),(-20,20)):
   a=inverse_square(interval,L,H);b=inverse_square(interval,L,H,True);need(a==b and a is not None and a[0]<=x<=a[1],'rational control');controls+=1
 need(inverse_square((1,2),9,16) is None,'strict reject');need(inverse_square((-8,8),9,16)==(-4,4),'both signs hull');need(inverse_square((1,8),9,16)==(3,4),'positive branch')
 source='verify/out/n100-voronoi-bisector-vertex.json';core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});rows=[]
 for case in load(source)['cases']:
  p=case['placement'];start=case['result']['boxes'];_,E,q=setup(core,p,prior[tuple(p)]);a=run(start,E,q,pairs);b=run(start,E,q,pairs,True);need(a==b,'alternate square-root and distance replay');end=a.get('boxes',a.get('result',{}).get('boxes'));reduction=width(start)-width(end);rows.append({'placement':p,'extra_width_reduction':reduction,'result':a});print('case',p,'excluded',a['excluded'],'fixed',a.get('fixed'),'shrink',reduction,flush=True)
 need(not rows[-1]['result']['excluded'],'candidate rejected: investigate');counts={'excluded':sum(r['result']['excluded'] for r in rows),'fixed':sum(not r['result']['excluded'] and r['result']['fixed'] for r in rows),'capped':sum(not r['result']['excluded'] and not r['result']['fixed'] for r in rows),'contracted':sum(r['extra_width_reduction']>0 for r in rows)};out=ROOT/'verify/out/n100-voronoi-reverse-distance.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_voronoi_bisector_vertex.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-voronoi-reverse-distance/v1','verified_integer_replay':True,'rational_point_controls':controls,'strict_rejection_control':True,'two_branch_hull_control':True,'alternate_root_and_distance_results_equal':True,'counts':counts,'cases':rows,'total_extra_width_reduction':sum(r['extra_width_reduction'] for r in rows),'candidate_retained':True,'scope':'33 prior boxes on one fixed Voronoi core; shared driving logic; not independent end-to-end proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS reverse distance',counts,'total shrink',sum(r['extra_width_reduction'] for r in rows))
if __name__=='__main__':main()

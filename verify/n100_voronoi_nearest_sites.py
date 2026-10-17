"""Conditional Voronoi nearest-site inequalities against every other center."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
from n100_voronoi_bisector_vertex import ROOT,load,need,coord,add,sub,mul,square,neg,quotient,width
from n100_circle_center_alternating import coupled
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import build

def leq_vertex(v,a,b,alternative=False):
 # |v-a|^2 <= |v-b|^2, linear in v with interval-valued coefficients.
 C=[tuple(2*x for x in sub(coord(b,k),coord(a,k))) for k in (0,1)];T=(0,0)
 for k in (0,1):T=add(T,sub(square(coord(a,k)),square(coord(b,k))))
 out=v[:]
 for k in (0,1):
  residual=add(T,add(mul(C[0],coord(out,0)),mul(C[1],coord(out,1))))
  if residual[0]>0:return None
  if C[k][0]<=0<=C[k][1]:continue
  rest=add(T,mul(C[1-k],coord(out,1-k)));rhs=-rest[0]
  if alternative:
   values=[Fraction(rhs,d) for d in C[k]]
   if C[k][0]>0:
    hi=max(values);bound=-((-hi.numerator)//hi.denominator);out[2*k+1]=min(out[2*k+1],bound)
   else:
    lo=min(values);bound=lo.numerator//lo.denominator;out[2*k]=max(out[2*k],bound)
  else:
   lo,hi=quotient((rhs,rhs),C[k])
   # quotient is outward rounded; safe, slightly weaker integer outward bounds.
   if C[k][0]>0:out[2*k+1]=min(out[2*k+1],hi)
   else:out[2*k]=max(out[2*k],lo)
  if out[2*k]>out[2*k+1]:return None
 return out

def main():
 controls=0
 for xnum in range(-21,22):
  x=Fraction(xnum,7);v=[-4,4,-4,4]
  # Exact sites (-2,0),(2,0) imply x<=0. Include coincident/tangent controls.
  a=leq_vertex(v,[-2,-2,0,0],[2,2,0,0]);b=leq_vertex(v,[-2,-2,0,0],[2,2,0,0],True);need(a==b,'integer coefficient control')
  if x<=0:need(a[0]<=x<=a[1],'rational feasible point retained')
  controls+=1
 need(leq_vertex([1,2,0,0],[-2,-2,0,0],[2,2,0,0]) is None,'strict nearest reject');need(leq_vertex([-4,4,-4,4],[0,0,0,0],[0,0,0,0])==[-4,4,-4,4],'coincident sites')
 core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(c['placement']):c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});source='verify/out/n100-voronoi-conflict-branches.json';z=load(source);cases=[{'placement':z['placement'],'child':r['summary']['child'],'boxes':r['equal_distance_result']['boxes']} for r in z['rows']];control=next(c for c in load('verify/out/n100-arc-center-projection.json')['cases'] if c['source_node'] is None);cases.append({'placement':control['placement'],'child':None,'boxes':control['result']['boxes']});rows=[]
 for case in cases:
  p=case['placement'];_,E,q=setup(core,p,prior[tuple(p)]);inc={}
  for f,v in E:inc.setdefault(v,set()).add(f)
  # One owner suffices because other owner equalities are imposed in the Voronoi model.
  inequalities=[(v,min(owners),b) for v,owners in sorted(inc.items()) for b in range(100) if b not in owners];B=[b[:] for b in case['boxes']];trace=[];excluded=False;failure=None;fixed=False
  for sweep in range(1,41):
   before=[b[:] for b in B];changes=0
   for v,a,b in inequalities:
    n=leq_vertex(B[v],B[a],B[b]);alt=leq_vertex(B[v],B[a],B[b],True)
    need(n==alt,'rational quotient implementation equality')
    if n is None:excluded=True;failure=[v,a,b];break
    new=[max(n[0],alt[0]),min(n[1],alt[1]),max(n[2],alt[2]),min(n[3],alt[3])]
    if new[0]>new[1] or new[2]>new[3]:excluded=True;failure=[v,a,b];break
    if new!=B[v]:B[v]=new;changes+=1
   trace.append(changes)
   if excluded:break
   r=coupled(B,E,q,pairs,limit=1);alt=coupled(B,E,q,pairs,alt=True,limit=1);need(r==alt,'nearest distance baseline replay')
   if r['excluded']:excluded=True;failure={'coupled':r};break
   B=r['boxes']
   if B==before:fixed=True;break
  if case['child'] is None:need(not excluded,'candidate rejected: investigate')
  row={'placement':p,'child':case['child'],'inequality_count':len(inequalities),'excluded':excluded,'fixed':fixed,'sweeps':sweep,'failure':failure,'trace':trace,'width_before':width(case['boxes']),'width_after':width(B),'extra_width_reduction':width(case['boxes'])-width(B),'boxes':B};rows.append(row);print('NEAREST',p,case['child'],'inequalities',len(inequalities),'excluded',excluded,'fixed',fixed,'shrink',row['extra_width_reduction'],flush=True)
 out=ROOT/'verify/out/n100-voronoi-nearest-sites.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_voronoi_bisector_vertex.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py'];out.write_text(json.dumps({'schema':'n100-voronoi-nearest-sites/v1','verified_integer_rational_nearest_tests':True,'rational_point_controls':controls,'strict_rejection_control':True,'coincident_control':True,'candidate_retained':True,'rows':rows,'scope':'conditional nearest-owner inequalities on inherited Voronoi core, one owner per vertex; shared interval coefficients and driver, no independent full geometry proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS nearest sites')
if __name__=='__main__':main()

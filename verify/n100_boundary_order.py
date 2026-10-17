"""Monotone boundary order within quadrants, exact interval propagation."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
from n100_circle_center_alternating import ROOT,load,need,coupled,independent
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import build

def ordered_vertices(core,alternative=False):
 A=core['alpha'];P=core['phi'];F=independent.cyc(P);V=independent.cyc([P[A[d]] for d in range(len(A))]);owner={d:i for i,row in enumerate(V) for d in row};outer=next(row for row in F if core['core_tags'][row[0]][0]=='outer')
 if not alternative:bd=[A[d] for d in reversed(outer)]
 else:
  inverse=[None]*len(P)
  for i,j in enumerate(P):inverse[j]=i
  walk=[];d=outer[-1]
  while not walk or d!=outer[-1]:walk.append(d);d=inverse[d]
  bd=[A[d] for d in walk]
 need(len(bd)==32 and all(owner[A[bd[j]]]==owner[bd[(j+1)%32]] for j in range(32)),'CCW boundary continuity')
 return [100+owner[d] for d in bd]

def constraints(core,q,alternative=False):
 order=ordered_vertices(core,alternative);rows=[]
 # For CCW motion: dx/dtheta=-y, dy/dtheta=x.
 for a,b in zip(order,order[1:]+order[:1]):
  if q[a-100]!=q[b-100]:continue
  sx,sy=q[a-100]
  for k,increasing in ((0,sy<0),(1,sx>0)):
   rows.append((a,b,k) if increasing else (b,a,k))
 need(len(rows)==56,'28 same-quadrant neighbor pairs, two coords');return rows

def inequality(B,a,b,k,alternative=False):
 # x_a <= x_b; both endpoint contractions are necessary.
 ai=2*k;bi=ai+1
 if not alternative:
  lo=B[a][ai];hi=B[b][bi]
  if lo>hi:return False
  B[a][bi]=min(B[a][bi],hi);B[b][ai]=max(B[b][ai],lo)
 else:
  # Independent sign-reversal: -x_b <= -x_a.
  lower=-B[b][bi];upper=-B[a][ai]
  if lower>upper:return False
  new_left_upper=min(-B[b][ai],upper);new_right_lower=max(-B[a][bi],lower)
  B[b][ai]=-new_left_upper;B[a][bi]=-new_right_lower
 return True

def run(start,E,q,pairs,order,alternative=False,limit=160):
 B=[b[:] for b in start];trace=[]
 for sweep in range(limit):
  old=[b[:] for b in B]
  for a,b,k in order:
   if not inequality(B,a,b,k,alternative):return {'excluded':True,'phase':'order','failure':[a,b,k],'sweeps':sweep+1,'boxes':B,'trace':trace}
  order_changes=sum(x!=y for x,y in zip(old,B));r=coupled(B,E,q,pairs,alt=alternative,limit=1)
  if r['excluded']:return {'excluded':True,'phase':'coupled','sweeps':sweep+1,'result':r,'trace':trace}
  B=r['boxes'];trace.append(order_changes)
  if B==old:return {'excluded':False,'fixed':True,'sweeps':sweep+1,'boxes':B,'trace':trace}
 return {'excluded':False,'fixed':False,'sweeps':limit,'boxes':B,'trace':trace}

def width(B):return sum(b[1]-b[0]+b[3]-b[2] for b in B)
def main():
 # All rational witness pairs in enclosing integer intervals survive both updates.
 controls=0
 for i in range(-8,9):
  for j in range(i,9):
   x=Fraction(i,3);y=Fraction(j,3);floor=lambda z:z.numerator//z.denominator;ceil=lambda z:-((-z.numerator)//z.denominator);B=[[floor(x)-1,ceil(x)+1,0,0],[floor(y)-1,ceil(y)+1,0,0]];C=[b[:] for b in B];need(inequality(B,0,1,0) and inequality(C,0,1,0,True) and B==C and B[0][0]<=x<=B[0][1] and B[1][0]<=y<=B[1][1],'rational order witness');controls+=1
 need(not inequality([[2,3,0,0],[-2,1,0,0]],0,1,0),'strict order reject')
 core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});rows=[];source='verify/out/n100-voronoi-reverse-distance.json'
 for case in load(source)['cases']:
  p=case['placement'];start=case['result']['boxes'];B,E,q=setup(core,p,prior[tuple(p)]);IB,IE,Iq=independent.setup(core,p,prior[tuple(p)]);need((B,E,q)==(IB,IE,Iq),'independent setup');order=constraints(core,q);order2=constraints(core,Iq,True);need(order==order2,'independent boundary order');a=run(start,E,q,pairs,order);b=run(start,IE,Iq,pairs,order2,True);need(a==b,'alternate arithmetic full equality');end=a.get('boxes',a.get('result',{}).get('boxes'));need(end is not None,'result boxes');rows.append({'placement':p,'extra_width_reduction':width(start)-width(end),'result':a});print('case',p,'excluded',a['excluded'],'fixed',a.get('fixed'),'shrink',rows[-1]['extra_width_reduction'],flush=True)
 need(not rows[-1]['result']['excluded'],'candidate rejected: investigate');counts={'excluded':sum(r['result']['excluded'] for r in rows),'fixed':sum(not r['result']['excluded'] and r['result']['fixed'] for r in rows),'capped':sum(not r['result']['excluded'] and not r['result']['fixed'] for r in rows),'contracted':sum(r['extra_width_reduction']>0 for r in rows)};out=ROOT/'verify/out/n100-boundary-order.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_circle_center_alternating.py','verify/n100_boundary_circle_propagation.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py'];out.write_text(json.dumps({'schema':'n100-boundary-order/v1','verified_integer_replay':True,'rational_order_controls':controls,'strict_rejection_control':True,'constraints_per_case':56,'all_alternate_results_equal':True,'independent_inverse_boundary_order_equal':True,'counts':counts,'cases':rows,'total_extra_width_reduction':sum(r['extra_width_reduction'] for r in rows),'candidate_retained':True,'scope':'33 boxes on one fixed core, nonstrict same-quadrant CCW order, analytic map-to-circle premise; no cross-quadrant constraints','machine_verified_geometry':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS boundary order',counts,'total shrink',sum(r['extra_width_reduction'] for r in rows))
if __name__=='__main__':main()

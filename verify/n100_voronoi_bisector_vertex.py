"""Exact Voronoi bisector contractors on vertex boxes, with rational division audit."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import json, hashlib
from n100_boundary_circle_propagation import setup
from n100_circle_center_alternating import coupled,need,load,ROOT
from n100_axis_coupled_boxes import build

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[1],-a[0])
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 z=[x*y for x in a for y in b];return min(z),max(z)
def square(a):return (0 if a[0]<=0<=a[1] else min(x*x for x in a),max(x*x for x in a))
def coord(b,k):return tuple(b[2*k:2*k+2])
def quotient(n,d):
 need(not d[0]<=0<=d[1],'division across zero')
 # Cross multiplication computes endpoint floor/ceil without floating point.
 lower=min(x//y for x in n for y in d);upper=max(-((-x)//y) for x in n for y in d)
 independent=[Fraction(x,y) for x in n for y in d];lo=min(independent);hi=max(independent)
 need(lower==lo.numerator//lo.denominator and upper==-((-hi.numerator)//hi.denominator),'rational quotient audit')
 return lower,upper

def bisect_vertex(v,a,b):
 # |v-a|^2-|v-b|^2 = 2 v.(b-a) + |a|^2-|b|^2.
 C=[tuple(2*x for x in sub(coord(b,k),coord(a,k))) for k in (0,1)]
 T=(0,0)
 for k in (0,1):T=add(T,sub(square(coord(a,k)),square(coord(b,k))))
 out=v[:]
 residual=add(T,add(mul(C[0],coord(v,0)),mul(C[1],coord(v,1))))
 if residual[0]>0 or residual[1]<0:return None
 for k in (0,1):
  if C[k][0]<=0<=C[k][1]:continue
  rhs=neg(add(T,mul(C[1-k],coord(out,1-k))));lo,hi=quotient(rhs,C[k]);out[2*k]=max(out[2*k],lo);out[2*k+1]=min(out[2*k+1],hi)
  if out[2*k]>out[2*k+1]:return None
 return out

def equations(E):
 inc={}
 for f,v in E:inc.setdefault(v,set()).add(f)
 return [(v,a,b) for v,faces in sorted(inc.items()) for a,b in combinations(sorted(faces),2)]
def width(B):return sum(b[1]-b[0]+b[3]-b[2] for b in B)
def run(B,E,q,pairs,limit=40):
 B=[b[:] for b in B];eq=equations(E);trace=[]
 for sw in range(limit):
  old=[b[:] for b in B];changes=0
  for v,a,b in eq:
   new=bisect_vertex(B[v],B[a],B[b])
   if new is None:return {'excluded':True,'phase':'bisector','failure':[v,a,b],'boxes':B,'sweeps':sw+1,'trace':trace}
   if new!=B[v]:B[v]=new;changes+=1
  r=coupled(B,E,q,pairs,limit=1)
  if r['excluded']:return {'excluded':True,'phase':'coupled','result':r,'sweeps':sw+1,'trace':trace}
  B=r['boxes'];trace.append(changes)
  if B==old:return {'excluded':False,'fixed':True,'sweeps':sw+1,'boxes':B,'trace':trace}
 return {'excluded':False,'fixed':False,'sweeps':limit,'boxes':B,'trace':trace}

def main():
 # Exact rational equidistant points on x=0, incl nonintegral witnesses in real boxes.
 controls=0
 for yn in range(-12,13):
  y=Fraction(yn,7);v=[-3,4,y.numerator//y.denominator,-((-y.numerator)//y.denominator)];out=bisect_vertex(v,[-2,-2,0,0],[2,2,0,0]);need(out is not None and out[0]<=0<=out[1] and out[2]<=y<=out[3],'equidistant rational retained');controls+=1
 need(bisect_vertex([1,2,0,0],[-2,-2,0,0],[2,2,0,0]) is None,'strict bisector reject')
 need(bisect_vertex([-3,4,-2,5],[0,0,0,0],[0,0,0,0])==[-3,4,-2,5],'coincident sites retain')
 core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(r['placement']):r['boxes'] for r in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});cases=[(r['placement'],r['result']['boxes']) for r in load('verify/out/n100-circle-center-class32.json')['rows']];cases.append(( [30,6,14,22],load('verify/out/n100-circle-center-alternating.json')['cases'][0]['result']['boxes']));rows=[]
 for p,B in cases:
  _,E,q=setup(core,p,prior[tuple(p)]);r=run(B,E,q,pairs);final=r.get('boxes',r.get('result',{}).get('boxes'));reduction=width(B)-width(final);rows.append({'placement':p,'equation_count':len(equations(E)),'extra_width_reduction':reduction,'result':r});print('case',p,'excluded',r['excluded'],'fixed',r.get('fixed'),'reduction',reduction,flush=True)
 need(not rows[-1]['result']['excluded'],'candidate excluded: investigate')
 counts={'excluded':sum(r['result']['excluded'] for r in rows),'fixed':sum(not r['result']['excluded'] and r['result']['fixed'] for r in rows),'capped':sum(not r['result']['excluded'] and not r['result']['fixed'] for r in rows),'contracted':sum(r['extra_width_reduction']>0 for r in rows)};out=ROOT/'verify/out/n100-voronoi-bisector-vertex.json';need(not out.exists(),'overwrite');paths=['verify/out/n100-circle-center-class32.json','verify/out/n100-circle-center-alternating.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_circle_center_alternating.py','verify/n100_boundary_circle_propagation.py','verify/n100_axis_coupled_boxes.py'];out.write_text(json.dumps({'schema':'n100-voronoi-bisector-vertex/v1','verified_integer_contractors':True,'rational_enclosure_controls':controls,'strict_rejection_control':True,'coincident_site_control':True,'all_quotients_fraction_audited':True,'counts':counts,'cases':rows,'total_extra_width_reduction':sum(r['extra_width_reduction'] for r in rows),'candidate_retained':True,'scope':'32 class survivors plus candidate on one fixed Voronoi core; baseline provenance inherited; equality necessity analytic, no independent full replay','machine_verified_geometry':False,'global_optimality':False,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS bisector tests',counts,'total shrink',sum(r['extra_width_reduction'] for r in rows))
if __name__=='__main__':main()

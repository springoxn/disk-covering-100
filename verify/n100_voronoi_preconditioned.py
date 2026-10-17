"""Fixed midpoint-adjugate preconditioning of joint Voronoi bisectors."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import json,hashlib
from n100_voronoi_bisector_vertex import ROOT,load,need,add,sub,mul,square,coord,quotient,width
from n100_voronoi_joint_cramer import controls as cramer_controls
from n100_circle_center_alternating import coupled
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import build

def scale(n,a):return (n*a[0],n*a[1]) if n>=0 else (n*a[1],n*a[0])
def contract_joint(v,sites):
 origin=[(v[2*k]+v[2*k+1])//2 for k in (0,1)];a,b,c=sites
 # Doubled midpoints avoid fractions. Fixed adjugate row factors need no division.
 mids=[[s[2*k]+s[2*k+1] for k in (0,1)] for s in sites];A=[mids[1][k]-mids[0][k] for k in (0,1)];B=[mids[2][k]-mids[0][k] for k in (0,1)]
 if A[0]*B[1]-A[1]*B[0]==0:return v[:],0,False
 rows=[(B[1],-A[1]),(-B[0],A[0])];out=v[:];usable=0
 def norm(s):
  return add(square((s[0]-origin[0],s[1]-origin[0])),square((s[2]-origin[1],s[3]-origin[1])))
 for r,t in rows:
  weights=(-(r+t),r,t);C=[]
  for k in (0,1):
   u=(0,0)
   for w,s in zip(weights,sites):u=add(u,scale(2*w,coord(s,k)))
   C.append(u)
  rhs=(0,0)
  for w,s in zip(weights,sites):rhs=add(rhs,scale(w,norm(s)))
  X=[(out[2*k]-origin[k],out[2*k+1]-origin[k]) for k in (0,1)];residual=sub(add(mul(C[0],X[0]),mul(C[1],X[1])),rhs)
  if residual[0]>0 or residual[1]<0:return None,usable,True
  for k in (0,1):
   if C[k][0]<=0<=C[k][1]:continue
   usable+=1;other=(out[2*(1-k)]-origin[1-k],out[2*(1-k)+1]-origin[1-k]);target=sub(rhs,mul(C[1-k],other));bounds=quotient(target,C[k]);out[2*k]=max(out[2*k],origin[k]+bounds[0]);out[2*k+1]=min(out[2*k+1],origin[k]+bounds[1])
   if out[2*k]>out[2*k+1]:return None,usable,True
 return out,usable,True

def controls():
 count=0
 for ax in range(-3,4):
  for by in range(-3,4):
   for dx,dy in ((1,3),(2,5),(-3,2)):
    sites=[[ax,ax,by,by],[ax+dx,ax+dx,by,by],[ax,ax,by+dy,by+dy]];x=Fraction(2*ax+dx,2);y=Fraction(2*by+dy,2);v=[x.numerator//x.denominator-3,-((-x.numerator)//x.denominator)+3,y.numerator//y.denominator-3,-((-y.numerator)//y.denominator)+3]
    for padding in (0,1):
     padded=[[s[0]-padding,s[1]+padding,s[2]-padding,s[3]+padding] for s in sites];out,u,active=contract_joint(v,padded);need(out is not None and out[0]<=x<=out[1] and out[2]<=y<=out[3],'rational witness retained under center uncertainty');count+=1
 need(contract_joint([-2,2,-2,2],[[0,0,0,0],[1,1,0,0],[2,2,0,0]])==([-2,2,-2,2],0,False),'singular midpoint skip')
 need(contract_joint([5,6,5,6],[[0,0,0,0],[2,2,0,0],[0,0,2,2]])[0] is None,'strict rejection');return count

def main():
 c=controls();source='verify/out/n100-arc-conflict-branch.json';z=load(source);cases=[{'placement':z['placement'],'child':r['child'],'boxes':r['arc_result']['boxes']} for r in z['children'] if not r['excluded']];cand=next(c for c in load('verify/out/n100-arc-center-projection.json')['cases'] if c['source_node'] is None);cases.append({'placement':cand['placement'],'child':None,'boxes':cand['result']['boxes']});core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(c['placement']):c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});rows=[]
 for case in cases:
  p=case['placement'];_,E,q=setup(core,p,prior[tuple(p)]);inc={}
  for f,v in E:inc.setdefault(v,set()).add(f)
  triples=[(v,faces) for v,owners in sorted(inc.items()) for faces in combinations(sorted(owners),3)];baseline=coupled(case['boxes'],E,q,pairs,limit=160);altbase=coupled(case['boxes'],E,q,pairs,alt=True,limit=160);need(baseline==altbase and not baseline['excluded'] and baseline['fixed'],'distance baseline');B=[b[:] for b in case['boxes']];trace=[];failure=None;excluded=False;fixed=False
  for sweep in range(1,61):
   before=[b[:] for b in B];changed=usable=active=0
   for v,faces in triples:
    out,u,act=contract_joint(B[v],[B[f] for f in faces]);usable+=u;active+=act
    if out is None:excluded=True;failure={'vertex':v,'centers':faces};break
    if out!=B[v]:changed+=1;B[v]=out
   trace.append({'preconditioned_triples':active,'usable_scalar_coefficients':usable,'changed_vertices':changed})
   if excluded:break
   a=coupled(B,E,q,pairs,limit=1);b=coupled(B,E,q,pairs,alt=True,limit=1);need(a==b,'preconditioned distance replay')
   if a['excluded']:excluded=True;failure={'coupled':a};break
   B=a['boxes']
   if B==before:fixed=True;break
  if case['child'] is None:need(not excluded,'candidate rejected: investigate')
  summary={'placement':p,'child':case['child'],'excluded':excluded,'fixed':fixed,'sweeps':sweep,'baseline_width':width(baseline['boxes']),'final_width':width(B),'additional_width_removed':width(baseline['boxes'])-width(B),'identical_to_baseline':not excluded and B==baseline['boxes']};rows.append({'summary':summary,'trace':trace,'failure':failure,'boxes':B});print('PRECONDITIONED',summary,'first trace',trace[0],flush=True)
 out=ROOT/'verify/out/n100-voronoi-preconditioned.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_voronoi_bisector_vertex.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py'];out.write_text(json.dumps({'schema':'n100-voronoi-preconditioned/v1','verified_integer_fixed_preconditioner':True,'rational_point_controls_in_uncertain_center_boxes':c,'all_divisions_fraction_audited':True,'singular_midpoint_skip_control':True,'strict_rejection_control':True,'candidate_retained':True,'rows':rows,'scope':'fixed midpoint-adjugate linear combinations of conditional Voronoi equalities; independent linear coefficient range grouping; shared products, equations and driver, no independent full contractor replay','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS fixed preconditioned solve')
if __name__=='__main__':main()

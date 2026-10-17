"""Joint translated interval Cramer solve for Voronoi vertices of three sites."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import json,hashlib
from n100_voronoi_bisector_vertex import ROOT,load,need,add,sub,mul,square,coord,quotient,width
from n100_circle_center_alternating import coupled
from n100_boundary_circle_propagation import setup
from n100_axis_coupled_boxes import build

def joint(v,sites,alternative=False):
 origin=[(v[2*k]+v[2*k+1])//2 for k in (0,1)];S=[[[a[2*k]-origin[k],a[2*k+1]-origin[k]] for k in (0,1)] for a in sites];a,b,c=S
 def row(b):
  C=[tuple(2*t for t in sub(tuple(b[k]),tuple(a[k]))) for k in (0,1)];R=(0,0)
  for k in (0,1):R=add(R,sub(square(tuple(b[k])),square(tuple(a[k]))))
  return C,R
 C,r=row(b);D,s=row(c);det=sub(mul(C[0],D[1]),mul(C[1],D[0]));numerators=[sub(mul(r,D[1]),mul(C[1],s)),sub(mul(C[0],s),mul(r,D[0]))]
 # det can vanish: do not divide, and do not infer infeasibility from degeneracy.
 if det[0]<=0<=det[1]:return v[:],False
 out=v[:]
 for k,n in enumerate(numerators):
  if alternative:
   values=[Fraction(x,y) for x in n for y in det];lo=min(values);hi=max(values);bounds=(lo.numerator//lo.denominator,-((-hi.numerator)//hi.denominator))
  else:bounds=quotient(n,det)
  out[2*k]=max(out[2*k],origin[k]+bounds[0]);out[2*k+1]=min(out[2*k+1],origin[k]+bounds[1])
  if out[2*k]>out[2*k+1]:return None,True
 return out,True

def controls():
 count=0
 # Exact circumcenters for rational right triangles, with noninteger real vertices.
 for ax in range(-3,4):
  for by in range(-3,4):
   for dx,dy in ((1,3),(2,5),(-3,2)):
    sites=[[ax,ax,by,by],[ax+dx,ax+dx,by,by],[ax,ax,by+dy,by+dy]];x=Fraction(2*ax+dx,2);y=Fraction(2*by+dy,2);v=[x.numerator//x.denominator-2,-((-x.numerator)//x.denominator)+2,y.numerator//y.denominator-2,-((-y.numerator)//y.denominator)+2];a,usable=joint(v,sites);b,used=joint(v,sites,True);need((a,usable)==(b,used) and usable and a is not None and a[0]<=x<=a[1] and a[2]<=y<=a[3],'rational circumcenter retained');need(all((x-Fraction(s[0]))**2+(y-Fraction(s[2]))**2==(x-sites[0][0])**2+(y-sites[0][2])**2 for s in sites),'equidistant control geometry');count+=1
 need(joint([-2,2,-2,2],[[0,0,0,0],[1,1,0,0],[2,2,0,0]])==([-2,2,-2,2],False),'collinear skip')
 need(joint([5,6,5,6],[[0,0,0,0],[2,2,0,0],[0,0,2,2]])[0] is None,'strict joint reject')
 return count

def main():
 control_count=controls();source='verify/out/n100-arc-conflict-branch.json';z=load(source);cases=[{'placement':z['placement'],'child':r['child'],'boxes':r['arc_result']['boxes']} for r in z['children'] if not r['excluded']];candidate=next(c for c in load('verify/out/n100-arc-center-projection.json')['cases'] if c['source_node'] is None);cases.append({'placement':candidate['placement'],'child':None,'boxes':candidate['result']['boxes']});core=load('verify/out/n100-cubic-core-roundtrip.json')['core'];prior={tuple(c['placement']):c['boxes'] for c in load('verify/out/n100-axis-coupled-boxes.json')['retained']};_,adj,_=build(core);pairs=sorted({tuple(sorted((i,j))) for i,row in enumerate(adj) for j in row if i!=j});rows=[]
 for case in cases:
  p=case['placement'];_,E,q=setup(core,p,prior[tuple(p)]);inc={}
  for f,v in E:inc.setdefault(v,set()).add(f)
  triples=[(v,faces) for v,owners in sorted(inc.items()) for faces in combinations(sorted(owners),3)];baseline=coupled(case['boxes'],E,q,pairs,limit=160);altbase=coupled(case['boxes'],E,q,pairs,alt=True,limit=160);need(baseline==altbase and not baseline['excluded'] and baseline['fixed'],'baseline fixed and alternate');B=[b[:] for b in case['boxes']];trace=[];excluded=False;fixed=False;failure=None
  for sweep in range(1,61):
   before=[b[:] for b in B];changes=usable_count=0
   for v,faces in triples:
    a,u=joint(B[v],[B[f] for f in faces]);b,t=joint(B[v],[B[f] for f in faces],True);need((a,u)==(b,t),'joint independent rational endpoint replay');usable_count+=u
    if a is None:excluded=True;failure={'vertex':v,'centers':faces};break
    if a!=B[v]:B[v]=a;changes+=1
   trace.append({'usable_determinants':usable_count,'joint_changes':changes})
   if excluded:break
   result=coupled(B,E,q,pairs,limit=1);alt=coupled(B,E,q,pairs,alt=True,limit=1);need(result==alt,'joint coupled alternate replay')
   if result['excluded']:excluded=True;failure={'coupled':result};break
   B=result['boxes']
   if B==before:fixed=True;break
  if case['child'] is None:need(not excluded,'candidate rejection: investigate')
  summary={'child':case['child'],'placement':p,'triple_count':len(triples),'excluded':excluded,'fixed':fixed,'sweeps':sweep,'baseline_width':width(baseline['boxes']),'final_width':width(B),'extra_width_removed':width(baseline['boxes'])-width(B),'identical_to_distance_baseline':not excluded and B==baseline['boxes']};rows.append({'summary':summary,'trace':trace,'failure':failure,'boxes':B,'distance_only_result':baseline});print('JOINT CRAMER',summary,flush=True)
 out=ROOT/'verify/out/n100-voronoi-joint-cramer.json';need(not out.exists(),'overwrite');paths=[source,'verify/out/n100-arc-center-projection.json','verify/out/n100-cubic-core-roundtrip.json','verify/out/n100-axis-coupled-boxes.json','verify/n100_voronoi_bisector_vertex.py','verify/n100_circle_center_alternating.py','verify/n100_axis_coupled_boxes.py','verify/n100_axis_coupled_boxes_independent.py','verify/n100_boundary_circle_branch_tree.py','verify/n100_boundary_circle_branch_tree_independent_full.py'];out.write_text(json.dumps({'schema':'n100-voronoi-joint-cramer/v1','verified_integer_translated_joint_solve':True,'rational_circumcenter_controls':control_count,'singular_skip_control':True,'strict_rejection_control':True,'all_fraction_endpoint_replays_equal':True,'candidate_retained':True,'rows':rows,'scope':'conditional three-owner Voronoi equalities on two branches and candidate parent; midpoint translation exact integer, singular intervals skipped; shared topology and interval products, not independent global proof','machine_verified_geometry':False,'global_optimality':False,'bindings':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in paths},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS translated joint solve')
if __name__=='__main__':main()

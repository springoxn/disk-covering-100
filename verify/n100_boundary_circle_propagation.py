"""Boundary unit-circle equality contractors on real scaled interval boxes.
No grid restriction; floor lower roots / ceiling upper roots retain real solutions.
"""
from pathlib import Path
from math import isqrt
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops,need
from n100_axis_coupled_boxes import Q,contract,radiussquared
from n100_axis_coupled_boxes_independent import clip
ROOT=Path(__file__).resolve().parents[1]
def ceilroot(n):
 s=isqrt(n);return s+(s*s<n)
def circle(box,signs,independent=False):
 # Convert known quadrant to nonnegative magnitudes, then use x²+y²=Q².
 b=[]
 for k,s in enumerate(signs):
  lo,hi=box[2*k:2*k+2];b.extend((max(0,lo if s==1 else -hi),min(Q,hi if s==1 else -lo)))
 if b[0]>b[1] or b[2]>b[3]:return None
 if b[0]**2+b[2]**2>Q*Q or b[1]**2+b[3]**2<Q*Q:return None
 out=b[:]
 for k in (0,1):
  j=2*(1-k);low=max(0,Q*Q-b[j+1]**2);high=Q*Q-b[j]**2
  if high<0:return None
  # Independent variant uses division-free equivalent ceiling formula.
  upper=(isqrt(high-1)+1 if high else 0) if independent else ceilroot(high)
  out[2*k]=max(b[2*k],isqrt(low));out[2*k+1]=min(b[2*k+1],upper)
  if out[2*k]>out[2*k+1]:return None
 result=[]
 for k,s in enumerate(signs):
  lo,hi=out[2*k:2*k+2];result.extend((lo,hi) if s==1 else (-hi,-lo))
 return result

def setup(core,p,root):
 A=core['alpha'];fc=loops(core['phi']);vc=loops(core['sigma']);vo={d:i for i,row in enumerate(vc) for d in row};outer=next(i for i,row in enumerate(fc) if core['core_tags'][row[0]][0]=='outer');inner=[f for f in range(len(fc)) if f!=outer];boundary=[A[d] for d in reversed(fc[outer])];b=len(boundary);need(b==32,'32 boundary edges');quadrants={};signs=((1,1),(-1,1),(-1,-1),(1,-1))
 for i in range(4):
  gap=(p[(i+1)%4]-p[i])%b
  for offset in range(1,gap+1):
   j=(p[i]+offset)%b;v=vo[boundary[j]];need(v not in quadrants,'boundary assigned once');quadrants[v]=signs[i]
 need(len(quadrants)==32,'all32 vertices in quadrants')
 constraints=[(i,100+vo[d]) for i,f in enumerate(inner) for d in fc[f]];need(len(constraints)==562,'562 incidences')
 B=[row[:] for row in root]+[[-Q,Q,-Q,Q] for _ in vc]
 return B,constraints,quadrants

def run(core,p,root,independent=False,limit=40):
 B,edges,quads=setup(core,p,root);initial=[row[:] for row in B];dist=clip if independent else contract;steps=0;circle_tests=0
 for sweep in range(limit):
  changed=False
  for v,signs in sorted(quads.items()):
   idx=100+v;new=circle(B[idx],signs,independent);circle_tests+=1
   if new is None:return {'excluded':True,'failure':['circle',idx],'sweeps':sweep+1,'boxes':B}
   if new!=B[idx]:changed=True;B[idx]=new
  for a,b in edges:
   for x,y in ((a,b),(b,a)):
    new=dist(B[x],B[y],radiussquared(1));steps+=1
    if new is None:return {'excluded':True,'failure':['distance',x,y],'sweeps':sweep+1,'boxes':B}
    if new!=B[x]:changed=True;B[x]=new
  if not changed:break
 return {'excluded':False,'fixed':not changed,'sweeps':sweep+1,'distance_tests':steps,'circle_tests':circle_tests,'boundary_vertices':len(quads),'face_vertex_constraints':len(edges),'center_total_width_reduction':sum(initial[i][1]-initial[i][0]+initial[i][3]-initial[i][2]-B[i][1]+B[i][0]-B[i][3]+B[i][2] for i in range(100)),'boxes':B}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-propagation.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';apath=ROOT/'verify/out/n100-axis-subdivision-pruning.json';core=load(cp)['core'];prior=load(bp);cand=load(apath)['candidate_axis_edge_indices'];cases=[prior['retained'][0],next(row for row in prior['retained'] if row['placement']==cand)];rows=[]
 need(circle([0,0,0,0],(1,1)) is None,'origin cannot lie on circle');need(circle([Q,Q,0,0],(1,1))==[Q,Q,0,0],'axis tangent retained');need(circle([3*Q//4,Q,3*Q//4,Q],(1,1)) is None,'outside circle')
 for row in cases:
  first=run(core,row['placement'],row['boxes']);second=run(core,row['placement'],row['boxes'],True);need(first==second,'independent contractor replay');rows.append({'placement':row['placement'],'result':first})
 need(not rows[1]['result']['excluded'],'candidate root retained')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-propagation/v1','verified_integer_replay':True,'cases':rows,'scale':Q,'alternate_contractor_all_results_equal':True,'controls':['origin rejected','unit axis retained','outside-circle box rejected'],'scope':'two fixed-core placements; necessary quadrant and circle equations on32 original boundary vertices, no axis subdivision vertices or monotonic order constraints; graph setup and traversal shared between replays','rounding':'lower magnitude floor sqrt, upper magnitude ceiling sqrt; real interval boxes','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,apath,ROOT/'verify/n100_axis_coupled_boxes.py',ROOT/'verify/n100_axis_coupled_boxes_independent.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
 for row in rows:print('PASS circle propagation',row['placement'],{k:v for k,v in row['result'].items() if k!='boxes'})
if __name__=='__main__':main()

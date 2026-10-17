"""Independent boundary-cycle and integer-bisection circle replay.
No imports from the main propagation script. Lower sqrt rounds down, upper up.
"""
from pathlib import Path
import json,hashlib,argparse
from n100_axis_coupled_boxes_independent import clip
ROOT=Path(__file__).resolve().parents[1]
Q=2**20;UN=1154469548855829;UD=10**16
def need(x,m):
 if not x:raise ValueError(m)
def cycles(p):
 seen=set();ans=[]
 for d in range(len(p)):
  if d in seen:continue
  row=[];j=d
  while j not in seen:seen.add(j);row.append(j);j=p[j]
  need(j==d,'cycles');ans.append(row)
 return ans
def floorroot(n):
 need(n>=0,'root domain');a=0;b=Q+1
 while a+1<b:
  m=(a+b)//2
  if m*m<=n:a=m
  else:b=m
 return a
def circle(b,sgn):
 ranges=[]
 for k,s in enumerate(sgn):
  ends=sorted((s*b[2*k],s*b[2*k+1]));ranges.append([max(0,ends[0]),min(Q,ends[1])])
 if any(lo>hi for lo,hi in ranges):return None
 if sum(lo*lo for lo,hi in ranges)>Q*Q or sum(hi*hi for lo,hi in ranges)<Q*Q:return None
 result=[]
 for k in (0,1):
  lo,hi=ranges[k];a,b=ranges[1-k];lower=floorroot(max(0,Q*Q-b*b));v=Q*Q-a*a
  if v<0:return None
  upper=floorroot(v);upper+=upper*upper<v
  low=max(lo,lower);high=min(hi,upper)
  if low>high:return None
  result.extend((low,high) if sgn[k]>0 else (-high,-low))
 return result

def replay(core,placement,root,limit=40):
 A=core['alpha'];P=core['phi'];faces=cycles(P);vertices=cycles([P[A[d]] for d in range(len(A))]);vertex={d:v for v,row in enumerate(vertices) for d in row};outer=next(f for f,row in enumerate(faces) if core['core_tags'][row[0]][0]=='outer');inner=[f for f in range(len(faces)) if f!=outer]
 # Build CCW boundary by following inverse outer-face permutation then taking twins.
 inv=[None]*len(P)
 for d,e in enumerate(P):inv[e]=d
 first=faces[outer][-1];walk=[];d=first
 while not walk or d!=first:
  walk.append(d);d=inv[d]
 boundary=[A[d] for d in walk];need(len(boundary)==32,'32 boundary darts')
 need(all(vertex[A[boundary[j]]]==vertex[boundary[(j+1)%32]] for j in range(32)),'boundary endpoints follow CCW cycle')
 quads={};signs=((1,1),(-1,1),(-1,-1),(1,-1))
 for edge in range(32):
  # The origin of edge j lies after axis on previous edge. Find the unique enclosing cyclic axis interval.
  choices=[i for i in range(4) if 0<(edge-placement[i])%32<=(placement[(i+1)%4]-placement[i])%32]
  need(len(choices)==1,'unique quadrant for boundary origin');quads[vertex[boundary[edge]]]=signs[choices[0]]
 need(len(quads)==32,'32 distinct boundary vertices')
 edges=[(i,100+vertex[d]) for i,f in enumerate(inner) for d in faces[f]];need(len(edges)==562,'562 incident constraints')
 B=[b[:] for b in root]+[[-Q,Q,-Q,Q] for row in vertices];initial=[b[:] for b in B];r2=-(-((UN*Q)**2)//UD**2);steps=0;ct=0
 for sw in range(limit):
  changed=False
  for v,sgn in sorted(quads.items()):
   idx=100+v;new=circle(B[idx],sgn);ct+=1
   if new is None:return {'excluded':True,'failure':['circle',idx],'sweeps':sw+1,'boxes':B},None
   if new!=B[idx]:changed=True;B[idx]=new
  for a,b in edges:
   for x,y in ((a,b),(b,a)):
    old=B[x];other=B[y];new=clip(old,other,r2);steps+=1
    if new is None:
     witness={'index':x,'other_index':y,'box':old,'other_box':other,'radius_squared_upper':r2}
     return {'excluded':True,'failure':['distance',x,y],'sweeps':sw+1,'boxes':B},witness
    if new!=old:changed=True;B[x]=new
  if not changed:break
 return {'excluded':False,'fixed':not changed,'sweeps':sw+1,'distance_tests':steps,'circle_tests':ct,'boundary_vertices':len(quads),'face_vertex_constraints':len(edges),'center_total_width_reduction':sum(initial[i][1]-initial[i][0]+initial[i][3]-initial[i][2]-B[i][1]+B[i][0]-B[i][3]+B[i][2] for i in range(100)),'boxes':B},None

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';sp=ROOT/'verify/out/n100-boundary-circle-propagation.json';core=load(cp)['core'];prior=load(bp);z=load(sp);rows=[]
 need(circle([0,0,0,0],(1,1)) is None and circle([Q,Q,0,0],(1,1))==[Q,Q,0,0],'origin/axis controls')
 for case in z['cases']:
  p=case['placement'];root=next(r['boxes'] for r in prior['retained'] if r['placement']==p);actual,witness=replay(core,p,root);need(actual==case['result'],'all replay fields and boxes')
  rows.append({'placement':p,'excluded':actual['excluded'],'sweeps':actual['sweeps'],'strict_distance_failure':witness})
 need(rows[0]['excluded'] and not rows[1]['excluded'],'one exclusion and candidate survives')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-independent/v1','verified_integer_replay':True,'cases':rows,'boundary_vertices_checked_per_case':32,'incidences_checked_per_case':562,'all_saved_boxes_equal':True,'boundary_endpoint_continuity_checked':True,'method':'inverse outer-face walk, per-edge quadrant membership, integer bisection sqrt, prior independent distance contractor; no import of main script','scope':'two fixed-core axis placements; conditional on geometric map-to-circle order reduction, not complete covering-domain exclusion','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,sp,ROOT/'verify/n100_axis_coupled_boxes_independent.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent circle-order replay',rows)
if __name__=='__main__':main()

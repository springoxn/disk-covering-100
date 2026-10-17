"""Independent numerical replay of all 63 representative branch nodes."""
from pathlib import Path
from math import isqrt
import json,hashlib,argparse
from n100_dart_independent_canonicalization import loops
from n100_axis_coupled_boxes_independent import clip
ROOT=Path(__file__).resolve().parents[1];Q=2**20;UN=1154469548855829;UD=10**16
def need(x,m):
 if not x:raise ValueError(m)
def cyc(p):
 seen=set();a=[]
 for d in range(len(p)):
  if d in seen:continue
  r=[];q=d
  while q not in seen:seen.add(q);r.append(q);q=p[q]
  need(q==d,'cycle');a.append(r)
 return a
def root(n):s=isqrt(n);return s+(s*s<n)
def circle(box,sg):
 b=[]
 for k,s in enumerate(sg):
  x,y=sorted((s*box[2*k],s*box[2*k+1]));b += [max(0,x),min(Q,y)]
 if b[0]>b[1] or b[2]>b[3] or b[0]*b[0]+b[2]*b[2]>Q*Q or b[1]*b[1]+b[3]*b[3]<Q*Q:return None
 o=b[:]
 for k in (0,1):
  j=2*(1-k);lo=max(0,Q*Q-b[j+1]**2);hi=Q*Q-b[j]**2
  if hi<0:return None
  l=isqrt(lo);u=root(hi);o[2*k]=max(o[2*k],l);o[2*k+1]=min(o[2*k+1],u)
  if o[2*k]>o[2*k+1]:return None
 r=[]
 for k,s in enumerate(sg):r += (o[2*k],o[2*k+1]) if s==1 else (-o[2*k+1],-o[2*k])
 return r
def setup(core,p,rootboxes):
 A=core['alpha'];P=core['phi'];F=cyc(P);V=cyc([P[A[d]] for d in range(len(A))]);vo={d:i for i,r in enumerate(V) for d in r};outer=next(f for f,r in enumerate(F) if core['core_tags'][r[0]][0]=='outer');inner=[f for f in range(len(F)) if f!=outer];bd=[A[d] for d in reversed(F[outer])];sg=((1,1),(-1,1),(-1,-1),(1,-1));q={}
 for i in range(4):
  for off in range(1,(p[(i+1)%4]-p[i])%32+1):q[vo[bd[(p[i]+off)%32]]]=sg[i]
 need(len(q)==32,'quadrants');edges=[(i,100+vo[d]) for i,f in enumerate(inner) for d in F[f]];need(len(edges)==562,'edges');return [b[:] for b in rootboxes]+[[-Q,Q,-Q,Q] for _ in V],edges,q
def propagate(B,edges,q,limit=80):
 B=[b[:] for b in B];steps=ct=0
 for sw in range(limit):
  changed=False
  for v,s in sorted(q.items()):
   i=100+v;new=circle(B[i],s);ct+=1
   if new is None:return {'excluded':True,'failure':['circle',i],'sweeps':sw+1,'boxes':B,'steps':steps,'circle_tests':ct}
   if new!=B[i]:B[i]=new;changed=True
  for a,b in edges:
   for x,y in ((a,b),(b,a)):
    new=clip(B[x],B[y],-(-((UN*Q)**2)//UD**2));steps+=1
    if new is None:return {'excluded':True,'failure':['distance',x,y],'sweeps':sw+1,'boxes':B,'steps':steps,'circle_tests':ct}
    if new!=B[x]:B[x]=new;changed=True
  if not changed:return {'excluded':False,'fixed':True,'sweeps':sw+1,'boxes':B,'steps':steps,'circle_tests':ct}
 return {'excluded':False,'fixed':False,'sweeps':limit,'boxes':B,'steps':steps,'circle_tests':ct}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-circle-branch-tree-independent-full.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';tp=ROOT/'verify/out/n100-boundary-circle-branch-tree-202709.json';core=load(cp)['core'];tree=load(tp);p=tree['placement'];rootboxes=next(r['boxes'] for r in load(bp)['retained'] if r['placement']==p);B0,edges,q=setup(core,p,rootboxes);nodes=tree['nodes'];seen=set()
 def visit(i,B):
  need(i not in seen,'duplicate');seen.add(i);n=nodes[i];actual=propagate(B,edges,q);need(actual==n['result'],'node propagation mismatch');
  if n['kind']=='split':
   f,d=n['face'],n['coordinate'];lo,hi=actual['boxes'][f][2*d:2*d+2];need([lo,hi]==n['interval'] and lo<n['split']<hi,'split parent');m=n['split'];L=[b[:] for b in actual['boxes']];R=[b[:] for b in actual['boxes']];L[f][2*d+1]=m;R[f][2*d]=m;visit(n['children'][0],L);visit(n['children'][1],R)
 visit(0,B0);need(len(seen)==63,'all nodes');out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-branch-tree-independent-full/v1','verified':True,'nodes_replayed':len(seen),'all_propagation_results_equal':True,'all_splits_reconstructed':True,'excluded_leaves':0,'unresolved_leaves':32,'method':'independent cycles, circle contractor, Floyd-free prior clip contractor, exact replay of every node','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,tp,ROOT/'verify/n100_axis_coupled_boxes_independent.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent full branch replay',len(seen),'nodes')
if __name__=='__main__':main()

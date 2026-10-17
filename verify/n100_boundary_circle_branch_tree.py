"""Depth-5 closed-box branch tree for the largest survivor gap representative."""
from pathlib import Path
import json,hashlib,argparse
from n100_boundary_circle_propagation import setup,circle,Q,contract,radiussquared
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def propagate(B,edges,quads,limit=80):
 B=[b[:] for b in B];steps=0;ct=0
 for sw in range(limit):
  changed=False
  for v,sgn in sorted(quads.items()):
   idx=100+v;new=circle(B[idx],sgn);ct+=1
   if new is None:return {'excluded':True,'failure':['circle',idx],'sweeps':sw+1,'boxes':B,'steps':steps,'circle_tests':ct}
   if new!=B[idx]:B[idx]=new;changed=True
  for a,b in edges:
   for x,y in ((a,b),(b,a)):
    new=contract(B[x],B[y],radiussquared(1));steps+=1
    if new is None:return {'excluded':True,'failure':['distance',x,y],'sweeps':sw+1,'boxes':B,'steps':steps,'circle_tests':ct}
    if new!=B[x]:B[x]=new;changed=True
  if not changed:return {'excluded':False,'fixed':True,'sweeps':sw+1,'boxes':B,'steps':steps,'circle_tests':ct}
 return {'excluded':False,'fixed':False,'sweeps':limit,'boxes':B,'steps':steps,'circle_tests':ct}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=5);ap.add_argument('--out',default='verify/out/n100-boundary-circle-branch-tree.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';prio=load(ROOT/'verify/out/n100-boundary-circle-branch-priority.json');core=load(cp)['core'];p=[20,27,2,9];root=next(r['boxes'] for r in load(bp)['retained'] if r['placement']==p);B0,edges,quads=setup(core,p,root);nodes=[]
 def visit(B,level):
  idx=len(nodes);nodes.append(None);r=propagate(B,edges,quads);rec={'level':level,'result':r}
  if r['excluded']:rec['kind']='excluded'
  elif level>=args.depth:rec['kind']='unresolved'
  else:
   choices=[]
   for i in range(100):
    wx=r['boxes'][i][1]-r['boxes'][i][0];wy=r['boxes'][i][3]-r['boxes'][i][2];choices.append((max(wx,wy),-i,0 if wx>=wy else 1))
   width,negf,d=max(choices);f=-negf
   if width<=1:rec['kind']='unresolved'
   else:
    lo,hi=r['boxes'][f][2*d:2*d+2];mid=(lo+hi)//2;left=[b[:] for b in r['boxes']];right=[b[:] for b in r['boxes']];left[f][2*d+1]=mid;right[f][2*d]=mid;rec.update(kind='split',face=f,coordinate=d,interval=[lo,hi],split=mid,children=[visit(left,level+1),visit(right,level+1)])
  nodes[idx]=rec;return idx
 visit(B0,0);counts={k:sum(r['kind']==k for r in nodes) for k in ('split','excluded','unresolved')};need(counts['unresolved']>0,'tree unexpectedly full exclusion');out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-circle-branch-tree/v1','verified_integer_branch_tree':True,'placement':p,'depth':args.depth,'node_count':len(nodes),'counts':counts,'nodes':nodes,'split_semantics':'closed [lo,mid] and [mid,hi] exactly cover parent','root_excluded':False,'scope':'one fixed-core representative survivor [0,7,14,21]; necessary circle/quadrant/shared-vertex relaxation; unresolved leaves retained','machine_verified_geometry':False,'global_optimality':False,'bindings':{str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in (cp,bp,ROOT/'verify/out/n100-boundary-circle-branch-priority.json',ROOT/'verify/n100_boundary_circle_propagation.py')},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS representative branch',p,counts)
if __name__=='__main__':main()

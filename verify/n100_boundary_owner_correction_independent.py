"""Independent corrected annulus replay; derive owners from edge-side incidence."""
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(x,m):
 if not x:raise ValueError(m)
def facecycles(p):
 unseen=set(range(len(p)));out=[]
 while unseen:
  d=min(unseen);row=[];q=d
  while q in unseen:unseen.remove(q);row.append(q);q=p[q]
  need(q==d,'face cycle');out.append(row)
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-boundary-owner-correction-independent.json');args=ap.parse_args();load=lambda p:json.loads(p.read_text(encoding='utf-8'))
 cp=ROOT/'verify/out/n100-cubic-core-roundtrip.json';bp=ROOT/'verify/out/n100-axis-coupled-boxes.json';sp=ROOT/'verify/out/n100-boundary-owner-correction.json';core=load(cp)['core'];boxes=load(bp);z=load(sp);A=core['alpha'];P=core['phi'];fc=facecycles(P);own={d:f for f,row in enumerate(fc) for d in row};of=[f for f,row in enumerate(fc) if all(core['core_tags'][d][0]=='outer' for d in row)];need(len(of)==1,'unique outside');outer=of[0];boundary=set()
 for d in range(len(A)):
  e=A[d]
  if d>e:continue
  sides=(own[d],own[e])
  if sides[0]==outer:boundary.add(sides[1])
  if sides[1]==outer:boundary.add(sides[0])
 need(len(boundary)==32 and sorted(boundary)==z['boundary_face_ids'],'nonempty owner inventory')
 idx={f:i for i,f in enumerate(f for f in range(len(fc)) if f!=outer)};need({str(f):idx[f] for f in boundary}==z['center_index_by_boundary_face'],'center index')
 un=1154469548855829;ud=10**16;scale=2**20;limit=(ud-un)**2*scale**2;failed=[];minimum=None;count=0
 for row in boxes['retained']:
  faces=[]
  for f in sorted(boundary):
   a,b,c,d=row['boxes'][idx[f]]
   # Maximum convex squared norm occurs at one of4 corners; separate independent expression.
   mx=max(x*x+y*y for x in (a,b) for y in (c,d));slack=mx*ud**2-limit
   minimum=slack if minimum is None else min(minimum,slack);count+=1
   if slack<0:faces.append(f)
  if faces:failed.append((row['placement'],faces))
 need(not failed and z['excluded']==[] and z['annulus_excluded_count']==0,'empty exclusions')
 need(count==152832==z['annulus_checks'] and minimum==z['minimum_signed_annulus_slack'],'full actual comparisons')
 # Validate published automorphisms directly; completeness separately checked by independent alpha/sigma root propagation.
 accepted=[];sigma=[P[A[d]] for d in range(len(A))]
 for target in range(len(A)):
  M={0:target};todo=[0];ok=True
  while todo and ok:
   d=todo.pop();e=M[d]
   if core['core_tags'][d]!=core['core_tags'][e]:ok=False;break
   for u,v in ((sigma[d],sigma[e]),(A[d],A[e])):
    if u in M:
     if M[u]!=v:ok=False;break
    else:M[u]=v;todo.append(u)
  if ok:
   need(len(M)==len(A) and len(set(M.values()))==len(A),'bijection');accepted.append([M[d] for d in range(len(A))])
 need(accepted==z['automorphism_maps']==[list(range(len(A)))],'independent complete auto set')
 need(len(boxes['retained'])==z['retained_count']==4776,'complete domains')
 out=ROOT/args.out;need(not out.exists(),'overwrite');out.write_text(json.dumps({'schema':'n100-boundary-owner-correction-independent/v1','verified':True,'actual_boundary_faces':32,'placements':4776,'annulus_comparisons':count,'excluded_count':0,'all_corner_maxima_match':True,'minimum_signed_annulus_slack':minimum,'automorphism_search_method':'DFS alpha/sigma versus primary BFS alpha/phi, all594 root images','automorphism_count':len(accepted),'historical_empty_owner_list_rejected_by_inventory_assertion':True,'machine_verified_geometry':False,'global_optimality':False,'scope':'fixed-core annulus and oriented automorphisms only','bindings':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp,bp,sp)},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8');print('PASS independent edge-side owners32, corner norm comparisons',count,'exclusions0; all594 alpha/sigma root images give1 auto')
if __name__=='__main__':main()

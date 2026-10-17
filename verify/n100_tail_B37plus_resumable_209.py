"""Resumable exact capped-pair cover for B>=37 at target radius."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,argparse,time
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'threshold_11305_components')]
import verify_capped_pair_B36plus_0p11323 as u

def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 ap=argparse.ArgumentParser();ap.add_argument('--budget',type=int,default=350000);ap.add_argument('--resume');ap.add_argument('--output',required=True);args=ap.parse_args();R=F(2831,25000);L=F(7511,10**6);mu=u.MU;lam=u.LAM;m=u.m;b=m.b;m.R=R;b.R,b.R2,b.LAM=b.ci(R),b.ci(R*R),b.ci(lam);caps=m.triangle_checks_34();M=b.ci(mu);threshold=b.ci(L)[0];original=b.bound
 bindings={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),W/'pair_bound_certificate_20261004/verify_pair_bound.py',W/'verify_capped_pair_B36plus_0p11323.py',W/'threshold_11305_components/verify_remaining_cases.py')}
 todo=[(0,b.D,0,b.D)];visited=accepted=skipped=0;chain=[]
 if args.resume:
  prev=ROOT/args.resume;j=json.loads(prev.read_text(encoding='utf-8'));assert j['bindings']==bindings and j['radius']==str(R) and j['intercept']==str(L);assert j['status']=='PENDING';todo=list(map(tuple,j['pending_boxes']));visited=j['visited'];accepted=j['accepted'];skipped=j['symmetry_skipped'];chain=j['chain']+[{'path':args.resume,'sha256':hashlib.sha256(prev.read_bytes()).hexdigest()}]
 before=visited;start=time.monotonic()
 while todo and visited-before<args.budget:
  box=todo.pop();visited+=1
  if box[0]>box[3]:skipped+=1;continue
  sa,ha,ua,va,pa,Ha=b.state((box[0],box[1]),-1);sb,hb,ub,vb,pb,Hb=b.state((box[2],box[3]),1);direct=b.sub(b.add(b.mul(b.scal(b.LAM,4),b.R2),b.half(b.add(Ha,Hb))),b.mul(M,b.half(b.add(b.asin(sa),b.asin(sb)))))[1]
  if direct<=threshold or original(box,M)<=threshold:accepted+=1;continue
  axis=0 if box[1]-box[0]>=box[3]-box[2] else 2;mid=(box[axis]+box[axis+1])//2;assert box[axis]<mid<box[axis+1],('unresolved_fixed_point',box);left=list(box);right=list(box);left[axis+1]=mid;right[axis]=mid;todo.extend((tuple(left),tuple(right)))
 margin=(1-mu)*m.v.PL-((198-37)*b.A_UP+37*u.K)*R*R-37*L;gain=(b.A_UP-u.K)*R*R-L;assert margin>0 and gain>0
 status='PASS' if not todo else 'PENDING';out=ROOT/args.output;assert not out.exists();out.write_text(json.dumps({'schema':'n100-tail-B37plus-resumable/v1','status':status,'radius':str(R),'intercept':str(L),'slope':str(mu),'penalty':str(lam),'marked_constant':str(u.K),'boundary_counts':'37..99','all_q_triangle_supports':caps,'visited':visited,'accepted':accepted,'symmetry_skipped':skipped,'pending_boxes':todo,'minimum_area_margin_at_B37':str(margin),'additional_margin_per_B':str(gain),'full_square_covered':not todo,'chain':chain,'bindings':bindings,'full_B36plus_closed':False,'global_bound_improved':False},indent=2)+'\n',encoding='utf-8');print('B37plus',status,'visited',visited,'pending',len(todo),'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()

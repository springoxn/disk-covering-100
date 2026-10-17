"""Budgeted new-radius capped-pair trial; unresolved is never exclusion.
Uses exact original backend, new explicit R and candidate support intercept.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,argparse,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'threshold_11305_components')]
import verify_capped_pair_B36plus_0p11323 as upstream

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--radius',default='0.11324');ap.add_argument('--intercept',default='0.007505');ap.add_argument('--max-boxes',type=int,default=250000);ap.add_argument('--output',default='verify/out/n100-tail-new-radius-trial-139.json');a=ap.parse_args();r=F(a.radius);L=F(a.intercept);mu=upstream.MU;lam=upstream.LAM;m=upstream.m;b=m.b;m.R=r;b.R,b.R2,b.LAM=b.ci(r),b.ci(r*r),b.ci(lam);caps=m.triangle_checks_34();margin=(1-mu)*m.v.PL-((198-36)*b.A_UP+36*upstream.K)*r*r-36*L;gain=(b.A_UP-upstream.K)*r*r-L;original=b.bound;M=b.ci(mu);threshold=b.ci(L)[0]
 def bound(box):
  sa,ha,ua,va,pa,Ha=b.state((box[0],box[1]),-1);sb,hb,ub,vb,pb,Hb=b.state((box[2],box[3]),1);direct=b.add(b.mul(b.scal(b.LAM,4),b.R2),b.half(b.add(Ha,Hb)));direct=b.sub(direct,b.mul(M,b.half(b.add(b.asin(sa),b.asin(sb)))))[1];return direct if direct<=threshold else min(direct,original(box,M))
 todo=[(0,b.D,0,b.D)];visited=accepted=skipped=0;failure=None;start=time.perf_counter_ns()
 while todo and visited<a.max_boxes:
  box=todo.pop();visited+=1
  if box[0]>box[3]:skipped+=1;continue
  if bound(box)<=threshold:accepted+=1;continue
  axis=0 if box[1]-box[0]>=box[3]-box[2] else 2;mid=(box[axis]+box[axis+1])//2
  if not box[axis]<mid<box[axis+1]:failure=list(box);break
  left=list(box);right=list(box);left[axis+1]=mid;right[axis]=mid;todo.extend((tuple(left),tuple(right)))
 status='CERTIFIED_LOCAL_SUPPORT' if not todo and failure is None else 'UNDECIDED';out=ROOT/a.output;assert not out.exists();backend=W/'pair_bound_certificate_20261004/verify_pair_bound.py';receipt={'schema':'n100-new-radius-capped-pair-trial/v1','radius':str(r),'intercept':str(L),'slope':str(mu),'penalty':str(lam),'marked_constant':str(upstream.K),'status':status,'all_q_triangle_supports':caps,'conditional_total_area_margin':str(margin),'conditional_per_B_gain':str(gain),'visited':visited,'accepted':accepted,'symmetry_skipped':skipped,'remaining_stack_size':len(todo),'failure_box':failure,'box_budget':a.max_boxes,'elapsed_ns':time.perf_counter_ns()-start,'full_sine_square_covered':not todo and failure is None,'global_bound_improved':False,'scope':'same universal capped-pair local objective at explicit new radius; budget exhaustion/unresolved leaf is not mathematical counterexample; complete support plus positive scalar margins would close only B>=36','bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),backend,W/'verify_capped_pair_B36plus_0p11323.py',W/'threshold_11305_components/verify_remaining_cases.py')}};out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(status,'visited',visited,'accepted',accepted,'pending',len(todo),'conditional scalar margin',str(margin),flush=True)
if __name__=='__main__':main()

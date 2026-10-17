"""Exact point witness against old capped-pair support target, not covering."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'threshold_11305_components')]
import verify_capped_pair_B36plus_0p11323 as upstream

def main():
 if not __debug__:raise RuntimeError('Assertions must remain enabled')
 R=F(2831,25000);mu=upstream.MU;lam=upstream.LAM;L=F(1501,200000);m=upstream.m;b=m.b;m.R=R;b.R,b.R2,b.LAM=b.ci(R),b.ci(R*R),b.ci(lam)
 x=F(79368264,10**8);assert (x*b.D).denominator==1;t=int(x*b.D);box=(t,t,t,t);M=b.ci(mu)
 sa,ha,ua,va,pa,Ha=b.state((t,t),-1);sb,hb,ub,vb,pb,Hb=b.state((t,t),1)
 direct=b.sub(b.add(b.mul(b.scal(b.LAM,4),b.R2),b.half(b.add(Ha,Hb))),b.mul(M,b.half(b.add(b.asin(sa),b.asin(sb)))))
 # The backend bound is an upper bound only. Reconstruct its point expression
 # using outward interval operations to enclose the relaxation itself.
 d=b.vs(pa,pb);w=b.va(b.vm(d,b.scal(b.LAM,2)),b.vm(ua,b.sub(b.mul(b.scal(b.LAM,4),ha),b.half(sa))));v=b.va(b.vm(d,b.scal(b.LAM,-2)),b.vm(ub,b.sub(b.mul(b.scal(b.LAM,4),hb),b.half(sb))))
 def supp(w,s,h,u,v):
  wr=b.dot(w,u);wt=b.ab(b.dot(w,v))
  if wr[1]<=0 and b.mul(wt,h)[1]<=b.mul(b.neg(wr),s)[0]:return (0,0)
  raw=b.add(b.sub(b.mul(wr,h),b.mul(wt,s)),b.mul(b.R,b.sqrt(b.add(b.sq(w[0]),b.sq(w[1])))))
  return (max(0,raw[0]),max(0,raw[1]))
 original=b.sub(b.add(b.add(b.mul(b.LAM,b.add(b.sq(d[0]),b.sq(d[1]))),b.half(b.add(Ha,Hb))),b.add(supp(w,sa,ha,ua,va),supp(v,sb,hb,ub,vb))),b.mul(M,b.half(b.add(b.asin(sa),b.asin(sb)))))
 point=(min(original[0],direct[0]),min(original[1],direct[1]));lower=F(point[0],b.D);upper=F(point[1],b.D);assert lower>L
 # The total-area margin allows only a small intercept increase.
 allowed=((1-mu)*m.v.PL-((198-36)*b.A_UP+36*upstream.K)*R*R)/36
 assert allowed>L and lower>allowed
 out=ROOT/'verify/out/n100-tail-support-obstruction-206.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-tail-support-obstruction/v1','status':'PASS_OBSTRUCTION_TO_OLD_RELAXATION','radius':str(R),'x':str(x),'y':str(x),'slope':str(mu),'penalty':str(lam),'old_intercept':str(L),'point_relaxation_interval':[str(lower),str(upper)],'point_lower_excess_over_old_intercept':str(lower-L),'max_intercept_allowed_by_B36_area':str(allowed),'point_lower_excess_over_area_budget':str(lower-allowed),'full_B36plus_closed':False,'global_bound_improved':False,'scope':'Exact point obstruction to the existing capped-pair relaxation with fixedMU/LAM/K. This is not a covering configuration or a counterexample to target lower bound. Raising L alone cannot repair the current proof with these constants.','bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),W/'verify_capped_pair_B36plus_0p11323.py',W/'pair_bound_certificate_20261004/verify_pair_bound.py',W/'threshold_11305_components/verify_remaining_cases.py')}},indent=2)+'\n',encoding='utf-8');print('TAIL EXACT OBSTRUCTION PASS point lower exceeds area-permitted intercept',flush=True)
if __name__=='__main__':main()

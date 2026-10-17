"""Engineering scan of the old B36 scalar budget and exact obstruction point."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'runtime/disk100-release-lf-67ebf1c/certified_bounds_11323/working';sys.path[:0]=[str(W),str(W/'threshold_11305_components')]
import verify_remaining_cases as m

def point_upper(R):
 m.b.R=m.b.ci(R);m.b.R2=m.b.ci(R*R);m.b.LAM=m.b.ci(F(3,50));x=F(9921033,12500000);t=int(x*m.b.D);s,h,u,v,c,H=m.b.state((t,t),-1);S,j,U,V,C,J=m.b.state((t,t),1);d=m.b.vs(c,C);dist=m.b.add(m.b.sq(d[0]),m.b.sq(d[1]));direct=m.b.sub(m.b.add(m.b.mul(m.b.LAM,dist),m.b.half(m.b.add(H,J))),m.b.mul(m.b.ci(F(92531,10**7)),m.b.half(m.b.add(m.b.asin(s),m.b.asin(S)))));return F(direct[1],m.b.D)
def allowed(R):
 return ((1-F(92531,10**7))*m.v.PL-((198-36)*m.b.A_UP+36*F(973,3125))*R*R)/36
def main():
 rows=[]
 lo=F(1132301,10**7);hi=F(2831,25000)
 for k in range(101):
  r=lo+(hi-lo)*k/100;u=point_upper(r);a=allowed(r);rows.append({'radius':str(r),'point_upper':str(u),'allowed_intercept':str(a),'gap_allowed_minus_point':str(a-u),'point_obstructs':u>a})
 feasible=[x for x in rows if not x['point_obstructs']];out=ROOT/'verify/out/n100-radius-scan-219.json';assert not out.exists();out.write_text(json.dumps({'schema':'n100-radius-scan/v1','status':'PASS_SCAN','range':[str(lo),str(hi)],'samples':len(rows),'constants':{'lambda':'3/50','mu':'92531/10000000','K':'973/3125','point_x':'9921033/12500000'},'rows':rows,'largest_sample_not_point_obstructed':feasible[-1] if feasible else None,'scope':'Diagnostic scan only. A sample not obstructed by this one point is not a global B36 certificate; full pair-domain replay and all six branches remain required.','source_bindings':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),W/'threshold_11305_components/verify_remaining_cases.py',W/'pair_bound_certificate_20261004/verify_pair_bound.py')}},indent=2)+'\n');print('RADIUS SCAN PASS samples',len(rows),'feasible samples',len(feasible),flush=True)
if __name__=='__main__':main()

"""Exact endpoint arithmetic for a universal nonnegative single-disk dual obstruction.
Analytic averaging proof is in docs/result-n100-round16-witness-dual-obstruction.md.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def cap(r):return (1+r)**2/(r*r)
def require(v,msg):
    if not v:raise ValueError(msg)
def main():
    L=F(11323,100000);U=F(1154469548855829,10**16);threshold=F(1,9)
    require(threshold<L<U,'endpoint order')
    require(cap(U)<cap(L)<100,'dual obstruction throughout interval')
    require(cap(threshold)==100,'critical radius')
    # At r=1/9, inequality expands to (1+r)^2-100r^2=(1-9r)(1+11r).
    for r in (F(1,10),threshold,L,U,F(1,2),F(1)):
        require((1+r)**2-100*r*r==(1-9*r)*(1+11*r),'factorization')
    # More than a sampled monotonicity assertion: for arbitrary 0<a<b,
    # cap(a)-cap(b)=(b-a)*(a+b+2*a*b)/(a*a*b*b).
    a,b=L,U
    require(cap(a)-cap(b)==(b-a)*(a+b+2*a*b)/(a*a*b*b)>0,'difference identity')
    rejected=[]
    for name,r in [('area_radius_1over10',F(1,10)),('critical_closed_endpoint',threshold)]:
        try:require(cap(r)<100,'strict below100 required')
        except ValueError:rejected.append(name)
        else:raise RuntimeError('negative accepted')
    require(cap(F(1,10))==121,'subthreshold control')
    op=R/'verify/out/n100-witness-dual-obstruction.json';require(not op.exists(),'overwrite')
    out={'schema':'n100-witness-dual-obstruction/v1','verified':True,
      'lower_radius':str(L),'upper_radius':str(U),'critical_radius':'1/9',
      'dual_weight_upper_at_lower':str(cap(L)),'dual_weight_upper_at_upper':str(cap(U)),
      'strict_gap_below_100_at_lower':str(100-cap(L)),
      'strict_gap_below_100_at_upper':str(100-cap(U)),
      'rejected_controls':rejected,
      'theorem':'For any nonnegative finite measure supported in D, if every radius-r disk has measure at most1, then total measure <=(1+r)^2/r^2. Consequently no unrestricted nonnegative single-disk weighted witness dual can exclude100 disks for r>1/9.',
      'analytic_dependency':'finite-sum integration or Tonelli; every serving-center disk B(p,r) is contained in D_(1+r); center projection into D cannot decrease served weight',
      'scope':'global unrestricted identical per-disk weighted-capacity dual; not branch-specific capacities, signed witnesses or integer set-cover arguments',
      'formal_kernel_verified':False,'global_optimality':False,'minimal_polynomial_obtained':False,
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    op.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('PASS arbitrary nonnegative single-disk dual obstruction: both endpoint capacities <100; threshold exactly1/9')
if __name__=='__main__':main()

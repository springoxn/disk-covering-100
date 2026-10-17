"""Rational step support for arc/cap tradeoff; no trigonometric arithmetic.
phi <= sin(phi)/sqrt(1-r^2), since phi<=asin(r).
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sqrt_bounds(v):
    need(v>=0,'sqrt domain');s=10**24;n=isqrt(v.numerator*s*s//v.denominator)
    lo,hi=F(n,s),F(n+1,s);need(lo*lo<=v<hi*hi,'rounding');return lo,hi
def cap_upper(r,z):
    # sqrt(1-x/(2r)) <= 1-x/(4r); integrate from 0 to z.
    need(0<=z<=2*r,'cap range')
    return sqrt_bounds(2*r*z**3)[1]*(F(4,3)-z/(5*r))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='verify/out/n100-arc-cap-rational-support.json');args=ap.parse_args()
    r=F(1154469548855829,10**16);delta=F(1,50);c2=1-r*r;c=sqrt_bounds(c2)[0];M=r/c;a=F(18,1000)
    rows=[];N=2000
    for j in range(N):
        u0=delta*j/N;u1=delta*(j+1)/N;d=1-r+u1
        cos=(c2+d*d)/(2*d);need(d*d<c2 and 0<cos<=1,'monotone arc branch')
        phi_upper=sqrt_bounds(1-cos*cos)[1]/c
        cap=cap_upper(r,delta-u0);gap=a*(M-phi_upper)-cap
        need(gap>0,'support failed at '+str(j))
        rows.append({'u_lower':str(u0),'u_upper':str(u1),'arc_half_upper':str(phi_upper),'cap_upper':str(cap),'gap':str(gap)})
    # For u>=delta cap vanishes and phi<=M. All service centers are normalized.
    # Sum phi>=pi; cap sum <= a*(k*M-pi).
    pl=F(314159,100000);ph=F(314160,100000)
    def atan(q,n):return sum(((-1)**j*F(1,q)**(2*j+1)/(2*j+1) for j in range(n)),F(0))
    need(pl<16*atan(5,8)-4*atan(239,7) and ph>16*atan(5,7)-4*atan(239,8),'pi')
    k=55;s=1-2*r+delta;cap_sum=a*(k*M-pl);margin=pl*s*s-(100-k)*ph*r*r-cap_sum
    need(margin>0 and ph*r*r>a*M,'area gap and count monotonicity')
    out=ROOT/args.out;need(not out.exists(),'overwrite')
    out.write_text(json.dumps({'schema':'n100-arc-cap-rational-support/v1','verified_rational_bounds':True,'radius':str(r),'delta':str(delta),'slope':str(a),'maximum_half_arc_upper':str(M),'steps':rows,'k55_cap_sum_upper':str(cap_sum),'k55_area_margin_lower':str(margin),'excludes_service_count_at_least':55,
        'analytic_dependencies':['whole-cover norm-cap normalization; count services anew','service center d>=1-r','half arc cosine=(1-r^2+d^2)/(2d); increasing half arc for d<sqrt(1-r^2)','phi<=sin(phi)/sqrt(1-r^2) for phi<=asin(r)','inner target intersection contained in disk cap of depth delta-u','sqrt(1-x)<=1-x/2 and exact cap integration','arc-length and area subadditivity','Machin formula'],
        'machine_verified_geometry':False,'global_optimality':False,'count_families_excluded':0,'scope':'conditional on explicitly stated elementary geometry, k>=55 impossible at U; no optimality or m,B family exclusion','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
    print('PASS',N,'rational arc-cap supports; k>=55 area gap:',str(margin),'approx reporting',float(margin))
if __name__=='__main__':main()

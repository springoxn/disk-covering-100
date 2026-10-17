"""Exact cap-area strengthening for a boundary-service count branch.
Analytic cap integral upper bounds, rational sqrt rounding and atan pi brackets.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,hashlib
R=Path(__file__).resolve().parents[1]
def need(x,m):
    if not x:raise ValueError(m)
def atan_bracket(q):
    x=F(1,q);lo=sum((-1)**j*x**(2*j+1)/(2*j+1) for j in range(8));hi=sum((-1)**j*x**(2*j+1)/(2*j+1) for j in range(7));return lo,hi

def sqrt_up(x):
    scale=10**20;integer=isqrt(x.numerator*scale*scale//x.denominator);up=F(integer+1,scale);need(up*up>x,'sqrt rounding');return up

def certificate(radius,m,k,delta,pi):
    need(0<radius<F(1,2) and 0<=k<=m and 0<delta<2*radius,'parameters');s=1-2*radius+delta;need(s<=1,'inner radius')
    cap=F(4,3)*sqrt_up(2*radius*delta**3)
    lo,hi=pi;margin=lo*s*s-(m-k)*hi*radius*radius-k*cap
    return {'radius_cut':str(radius),'total_disks':m,'circle_serving_disks':k,'non_serving_disks':m-k,'delta':str(delta),'inner_radius':str(s),'one_boundary_disk_cap_area_upper':str(cap),'inner_area_lower':str(lo*s*s),'non_serving_area_upper':str((m-k)*hi*radius*radius),'area_deficit_lower':str(margin),'excluded':margin>0}
if __name__=='__main__':
    a,b=atan_bracket(5),atan_bracket(239);pi=(16*a[0]-4*b[1],16*a[1]-4*b[0]);need(F(314159,100000)<pi[0]<pi[1]<F(314160,100000),'pi brackets')
    cut=F(23,200);delta=F(1,125);C=certificate(cut,100,55,delta,pi);need(C['excluded'],'55 branch not excluded at cut')
    # Earlier zero-penetration area fails at this cut; new cap inequality is stronger.
    need((1-2*cut)**2<45*cut**2,'baseline already excludes')
    U=F(1154469548855829,10**16);control=certificate(U,100,55,delta,pi);need(not control['excluded'],'unexpected full endpoint exclusion')
    cases=[]
    for m in range(96,101):
        for k in (53,54,55):
            cases.append(certificate(cut,m,k,delta,pi))
    op=R/'verify/out/n100-boundary-cap-area-branch.json';need(not op.exists(),'overwrite')
    op.write_text(json.dumps({'verified_rational_bounds':True,'pi_interval':list(map(str,pi)),'main_certificate':C,'count_branch_cases':cases,'candidate_endpoint_control':control,'baseline_zero_penetration_does_not_exclude_main_branch':True,'analytic_dependencies':['circle-serving center norm>=1-r','radial projection target inner disk x<=s','disk cap height<=2 sqrt(2r z)','integral0delta 2sqrt(2r z) dz=(4/3)sqrt(2r delta^3)','area subadditivity','Machin identity and alternating series'],'scope':'m<=100,k=55 branch excluded for r<=23/200; no exclusion of all k branches or candidate endpoint; not an r_D100 minimal polynomial','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'global_optimality':False,'minimal_polynomial_obtained':False},indent=2)+'\n',encoding='utf-8')
    print('PASS strengthened area cap:100-disk k55 branch impossible at r<=0.115;baseline fails there;candidate upper endpoint NOT excluded')

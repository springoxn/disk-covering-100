#!/usr/bin/env python3
"""Exact normalized B33/M>=26 reduction: every interior degree is six or more."""
from pathlib import Path
from fractions import Fraction as F
import sys,itertools,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT if (ROOT/'lower_bounds_extension_20261004'/'verify_extension.py').exists() else ROOT.parent/'working'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'lower_bounds_extension_20261004'))
import verify_extension as geometry
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_linear_halfside_marked_conjugate import conjugate
from exact_range_one_face_support import face_bound
from verify_jensen_slab_ear_support import cap as ear_cap
from verify_global_star_anchor_degree_window import verify as check_degrees
import verify_B33_marked_hinge_charges_0p11322 as hinge
R=F(5661,50000);B=33;K=F(11,25);A=3*q(3).sqrt()/4;ANG=PI/3
D=10**10;PD=10**8
LABELS=[F(-38035915,PD),F(-28793429,PD),F(0)]
CHARGES=[F(272367458,D),F(156750957,D),F(500,D)]
TA=F(196028847,D)
NU=[-8803591500,-8488906872,-7405397995,-8181345399,-7126913797,
    -6175710778,-7879342900,-6848754427,-5905159993,-5000000000]

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    geometry.R=R;geometry.check_kappa();geometry.check_concavity_factorization()
    n99=geometry.exclude_all(99,R)
    old=((198-B)*geometry.AH+B*geometry.KAPPA)*R*R+B*geometry.H_upper(R,2*geometry.PL/B,2*geometry.PH/B)
    deficit=(old-geometry.PL)/(R*R)
    deg=check_degrees();degree_margin=F(deg['degree4_loss_lower'])-deficit
    assert degree_margin>0 and 100-B>1
    hs=hinge.verify();assert hs['status']=='PASS' and hs['radius']==str(R)
    assert F(hs['required_center_norm_squared_upper'])==1-R*R
    rr=q(R);mu=PI/B;s=sine(mu);rho=cosine(mu)-(rr.sq()-s.sq()).sqrt()
    Q=B*(mu-s*rho+q(K)*rr*s*rho);C0=conjugate(K,F(0))
    facegaps=[]
    triples=list(itertools.combinations_with_replacement(range(3),3));assert len(triples)==len(NU)==10
    for ids,nu in zip(triples,NU):
        ls=[LABELS[i] for i in ids];cap,acute,vertex=face_bound(ls,F(nu,D))
        credit=TA*sum({ids[j],ids[(j+1)%3]}=={0,1} for j in range(3))
        upper=A+q(sum((CHARGES[i] for i in ids),F(0))-credit)
        gap=F(upper.l-cap.u,S);assert gap>0,('face',ids,gap)
        facegaps.append(gap)
    u0=q(F(200000,D));beta=q(F(2616668073,D));eta=q(F(-1834026504,D));lb=-LABELS[1]
    gaps=[];low=[]
    for d in range(5,9):
        for p in range(d):
            ix=0 if d>=7 else 2;lv=LABELS[ix]
            score=p*(conjugate(K,lv+lb)-C0)-q(lv)*(6-d+p)*ANG+(d-p)*q(CHARGES[ix])-q(hinge.charge(p))
            if p and ix==0:score-=q(2*TA)
            upper=u0+p*beta+(d-6)*eta
            gap=F(upper.l-score.u,S);assert gap>0,('vertex',p,d,gap)
            gaps.append(gap)
            if d==5:low.append(gap)
    assert len(gaps)==26 and len(low)==5
    slope=-eta+q(CHARGES[1])-q(lb)*ANG;assert slope.u<0
    shifted=A-2*C0+ear_cap(R,K)-2*beta+eta+q(lb)*PI+2*slope
    width=q(2)/(1+(1-2*rr).sqrt());y=(q(K)+q(K*K+8).sqrt())/4
    bad=width+(1-y.sq()).sqrt()*(y-q(K))-C0-beta-eta
    assert shifted.u<0 and bad.u<0
    def center(M):
        return 132*A+B*C0+67*u0+B*beta+(27-M)*eta+M*q(CHARGES[1])-q(lb)*(2*PI+M*ANG)
    raw=PI-(rr.sq()*center(26)+Q)
    contradiction=raw+rr.sq()*q(min(low));assert contradiction.l>0
    # This is only a minimum-degree conclusion. The ordinary cap may still
    # permit a covering, so Euler's surviving cases are kept explicitly.
    surviving=[]
    for M in range(26,29):
        for e in range(3):
            for b in range(3):
                excess=27-M-e-b
                if excess>=0:surviving.append(dict(M=M,ears=e,bad_q1=b,degree_excess=excess))
    assert len(surviving)==4
    # A bad marked face has its own paid coefficient; no footprint is used.
    bad_contradiction=raw-rr.sq()*bad;assert bad_contradiction.l>0
    surviving=[z for z in surviving if z['bad_q1']==0]
    return dict(status='PASS',radius=str(R),B=B,m=100,M_domain='M>=26',
        scope='Minimum interior degree six and no all-boundary q1 face; not a radius exclusion',
        required_center_norm_squared_upper=str(1-R*R),n99_exclusion=n99,
        initial_degree_window=[5,8],initial_degree_window_margin=str(degree_margin),
        final_minimum_interior_degree=6,face_supports=len(facegaps),vertex_supports=len(gaps),
        minimum_face_slack=str(min(facegaps)),minimum_vertex_slack=str(min(gaps)),
        minimum_degree5_slack=str(min(low)),M_slope_upper=str(F(slope.u,S)),
        shifted_ear_upper=str(F(shifted.u,S)),bad_q1_upper=str(F(bad.u,S)),
        raw_M26_area_margin=str(F(raw.l,S)),degree5_contradiction_margin=str(F(contradiction.l,S)),
        bad_q1_contradiction_margin=str(F(bad_contradiction.l,S)),
        hinge_allocation=hs,remaining_Euler_cases=surviving)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

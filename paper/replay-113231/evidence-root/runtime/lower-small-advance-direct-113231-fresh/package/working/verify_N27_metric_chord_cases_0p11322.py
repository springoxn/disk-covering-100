#!/usr/bin/env python3
"""Exact metric exclusion of an all-six P27/F105 core with at most two chords."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT if (ROOT/'verify_star_lp_duals.py').exists() else ROOT.parent/'working'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'lower_bounds_extension_20261004'))
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_signed_sine_full_face_support import face_bound
from exact_linear_halfside_marked_conjugate import conjugate
import verify_exact_lens_boundary_0p11322 as boundary
R=F(5661,50000);K=F(11,25);TAU=F(49,100);A=3*q(3).sqrt()/4
LR=F(-13,100);LB=F(-14,25)
PATTERNS=[(0,0,-5000000000),(1,0,-5421489759),(2,1,-6742560941),
          (2,0,-5853367990),(3,2,-8021619699),(3,1,-7210097425)]
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    boundary.R=R;boundary.B=33;boundary.K=K;boundary.CURVATURE=F(0)
    bs=boundary.verify();assert bs['status']=='PASS'
    assert F(bs['required_center_norm_squared_upper'])==1-R*R
    # Integer topology: one simple core; any remaining chord has a side
    # without deep vertices, hence an ear can be removed. Three removals
    # would contradict the nonnegative-curvature disk isoperimetry.
    assert F(23**2,6)<107 and F(25**2,6)<105 and F(3**2+24**2,6)<105
    for t in range(3):assert F(6**2+(23-t)**2,6)<105-t
    assert F(24**2,6)<102
    caps=[];guards=[]
    for j,k,nu in PATTERNS:
        labels=[F(0)]*(3-j)+[LR]*j;edges=[F(0)]*3
        if j==2 and k==1:edges[0]=-TAU
        if j==3:
            for a in range(k):edges[a]=-TAU
        guards.append(1-(max(labels)-min(labels)+sum(max(-x,F(0)) for x in edges)/2))
        bound,acute,edgecaps=face_bound(labels,edges,F(nu,10**10))
        assert all(bound.u>=z.u for z in [acute]+edgecaps)
        caps.append(F(bound.u,S))
    al=F(A.l,S);eps=F(1,10**8);u=eps
    ring_charge=caps[1]-al+eps
    boundary_charge=caps[2]-al-2*ring_charge+eps
    chord_charge=max(F(0),max((cap-al-u-j*ring_charge-k*boundary_charge)/(j*(j-1)//2-k)
        for (j,k,nu),cap in zip(PATTERNS,caps) if j*(j-1)//2-k>0))+eps
    gaps=[]
    for (j,k,nu),cap in zip(PATTERNS,caps):
        h=j*(j-1)//2-k
        gap=al+u+j*ring_charge+k*boundary_charge+h*chord_charge-cap
        assert gap>0;gaps.append(gap)
    outer,acute,edgecaps=face_bound([LR,LR,LB],[F(0),F(0),TAU],F(-6814893127,10**10))
    r=q(R);mu=PI/33;s=sine(mu);rho=cosine(mu)-(r.sq()-s.sq()).sqrt()
    Q=33*(mu-s*rho+q(K)*r*s*rho)
    cases=[]
    for chords in range(3):
        center=105*A+q(105*u+75*ring_charge+27*boundary_charge+2*chords*chord_charge)+27*outer
        center+=33*conjugate(K,LR-LB)-q(33*LR)*PI/3+q(LB)*(2*PI+27*PI/3)
        margin=PI-(r.sq()*center+Q);assert margin.l>0
        cases.append(dict(core_chords=chords,center_upper=str(F(center.u,S)),area_margin=str(F(margin.l,S))))
    return dict(status='PASS',radius=str(R),B=33,
        scope='Conditional M27/e0 profile with all original interior degrees six; no graph catalog or quadratic radial premise',
        required_center_norm_squared_upper=str(1-R*R),core_vertices=67,core_boundary=27,core_faces=105,
        core_chords_upper=2,core_ring_angle_incidences=75,core_deep_angle_incidences=240,
        face_supports=7,shared_edge_multiplier=str(TAU),minimum_localization_guard=str(min(guards)),
        minimum_core_face_slack=str(min(gaps)),core_allowance_coefficients=list(map(str,[u,ring_charge,boundary_charge,chord_charge])),
        hinge_charge_spent=False,minimum_area_margin=str(min(F(z['area_margin']) for z in cases)),cases=cases)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

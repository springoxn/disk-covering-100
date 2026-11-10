#!/usr/bin/env python3
"""Five metric face patterns for the all-six M26 one-ear profile."""
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
from verify_jensen_slab_ear_support import cap as ear_cap
import verify_exact_lens_boundary_0p11322 as boundary
R=F(113231,1000000);K=F(11,25);LR=F(-1,5);LB=F(-7,10);TAU=F(16,25)
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    boundary.R=R;boundary.B=33;boundary.K=K;boundary.CURVATURE=F(0)
    bs=boundary.verify();assert bs['status']=='PASS'
    # c1 follows from the /6 component inequality. If n3=1 then the
    # frontier25 and faces107 are impossible, so n2=1,n3=0.
    assert F(22**2,6)<108 and F(25**2,6)<107
    assert F(24**2,6)<106 and F(3**2+23**2,6)<106 and F(3**2+25**2,6)<106
    patterns=[([0,0,0],[0,0,0],60,-5000000000),
        ([0,0,LR],[0,0,0],20,-5639410298),
        ([0,LR,LR],[-TAU,0,0],26,-7488270501),
        ([LR,LR,LB],[0,0,TAU],26,-7481753493),
        ([LR,LB,LB],[0,0,0],1,-10090169944)]
    total=q(0);guards=[]
    for labels,edges,count,nu in patterns:
        labels=list(map(F,labels));edges=list(map(F,edges))
        guards.append(1-(max(labels)-min(labels)+sum(max(-x,F(0)) for x in edges)/2))
        cap,acute,edgecaps=face_bound(labels,edges,F(nu,10**10));assert all(cap.u>=z.u for z in [acute]+edgecaps)
        total+=count*cap
    assert min(guards)>0 and sum(x[2] for x in patterns)==133
    center=total+31*conjugate(K,LR-LB)+ear_cap(R,K)-q(31*LR)*PI/3+q(LB)*(PI+28*PI/3)
    rr=q(R);mu=PI/33;s=sine(mu);rho=cosine(mu)-(rr.sq()-s.sq()).sqrt()
    Q=33*(mu-s*rho+q(K)*rr*s*rho);margin=PI-(rr.sq()*center+Q);assert margin.l>0
    return dict(status='PASS',radius=str(R),B=33,M=26,ears=1,bad_q1=0,
        scope='Conditional all67 original interior degrees six; one q2 ear',
        required_center_norm_squared_upper=str(1-R*R),core_boundary=26,core_faces=106,
        q0_one_boundary_faces=26,q0_two_boundary_faces=1,q0_three_boundary_faces=0,
        face_supports=5,pattern_counts=[60,20,26,26,1],marked_faces=31,
        shared_edge_multiplier=str(TAU),minimum_localization_guard=str(min(guards)),
        center_upper=str(F(center.u,S)),area_margin=str(F(margin.l,S)),hinge_charge_spent=False)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

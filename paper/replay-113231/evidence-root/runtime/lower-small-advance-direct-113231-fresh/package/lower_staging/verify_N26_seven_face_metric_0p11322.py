#!/usr/bin/env python3
"""Seven exact metric face supports exclude the conditional P26/F106 profile."""
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
R=F(5661,50000);K=F(11,25);B=33;A=3*q(3).sqrt()/4;ANG=PI/3
LABELS=[F(0),F(-13,100),F(-12,25),F(-14,25)];TAU=F(49,100)
PATTERNS=[('bulk',(0,0,0)),('bulk',(0,0,1)),('bulk',(0,0,2)),
          ('interface',(0,1,1)),('interface',(0,1,2)),
          ('ring',(1,1,3)),('ring',(1,2,3))]
NU=[-5000000000,-5421489759,-6458236434,-6742560941,-7749680130,-6814893127,-8003405868]
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    boundary.R=R;boundary.B=B;boundary.K=K;boundary.CURVATURE=F(0)
    bs=boundary.verify();assert bs['status']=='PASS'
    assert F(bs['required_center_norm_squared_upper'])==1-R*R
    caps=[];guards=[]
    for (region,ids),nu in zip(PATTERNS,NU):
        edges=[F(0)]*3
        if region=='interface':edges[0]=-TAU
        if region=='ring':edges[2]=TAU
        labels=[LABELS[i] for i in ids]
        guards.append(1-(max(labels)-min(labels)+sum(max(-x,F(0)) for x in edges)/2))
        bound,acute,edgecaps=face_bound(labels,edges,F(nu,10**10))
        assert all(bound.u>=z.u for z in [acute]+edgecaps)
        caps.append(F(bound.u,S))
    assert min(guards)>0
    eps=F(1,10**8);al=F(A.l,S)
    bulk=eps;cr=caps[1]-al+eps;ch=caps[2]-al+eps
    interface=max(caps[3]-al-2*cr,caps[4]-al-cr-ch)+eps
    rr=(caps[5]-al)/2+eps;rh=caps[6]-al-rr+eps
    coefficients=[bulk,interface,cr,ch,F(0),rr,rh]
    gaps=[]
    for (region,ids),cap in zip(PATTERNS,caps):
        upper=al
        if region=='bulk':upper+=bulk+ids.count(1)*cr+ids.count(2)*ch
        elif region=='interface':upper+=interface+ids.count(1)*cr+ids.count(2)*ch
        else:upper+=ids.count(1)*rr+ids.count(2)*rh
        gap=upper-cap;assert gap>0;gaps.append(gap)
    r=q(R);mu=PI/B;s=sine(mu);rho=cosine(mu)-(r.sq()-s.sq()).sqrt()
    Q=B*(mu-s*rho+q(K)*r*s*rho)
    lR,lH,lb=LABELS[1],LABELS[2],-LABELS[3]
    cases=[]
    for p in range(4):
        # Core:80 bulk,26 interface,246 deep,67+p ordinary-ring,
        # 5-p special-ring incidences. Outer ring:26 BC,50 ordinary,2 special.
        assert 246+(67+p)+(5-p)==3*106
        center=132*A+q(80*bulk+26*interface+(67+p)*cr+(5-p)*ch+50*rr+2*rh)
        center+=(33-p)*conjugate(K,lR+lb)+p*conjugate(K,lH+lb)
        center-=q((33-p)*lR+(p-1)*lH)*ANG+q(lb)*(2*PI+26*ANG)
        margin=PI-(r.sq()*center+Q);assert margin.l>0
        cases.append(dict(special_marked_count=p,center_upper=str(F(center.u,S)),area_margin=str(F(margin.l,S))))
    return dict(status='PASS',radius=str(R),B=B,
        scope='Conditional simple chordless P26/F106 core, one ring degree7, all other interior degree6; no catalog enumeration',
        required_center_norm_squared_upper=str(1-R*R),core_vertices=67,core_boundary=26,core_faces=106,
        face_regions=dict(bulk=80,interface=26,outer_ring=26),face_supports=7,
        shared_edge_multiplier=str(TAU),corner_labels=list(map(str,LABELS)),
        minimum_localization_guard=str(min(guards)),minimum_face_slack=str(min(gaps)),
        region_coefficients=list(map(str,coefficients)),hinge_charge_spent=False,
        minimum_area_margin=str(min(F(z['area_margin']) for z in cases)),cases=cases)
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

#!/usr/bin/env python3
"""Joint ordinary-apex/ear hinge allocation removes the high-M ear profile."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT if (ROOT/'verify_star_lp_duals.py').exists() else ROOT.parent/'working'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'lower_bounds_extension_20261004'))
import verify_B33_highM_minimum_degree6_0p11322 as old
import verify_exact_lens_hinge_deficit as local
from verify_star_lp_duals import q,S
from verify_potential_star_duals import sine
R=F(5661,50000);C=F(7,200);T=F(23,250);EARSPAN=F(457,2000)
def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    previous=old.verify();assert previous['status']=='PASS' and previous['radius']==str(R)
    local.R=R;local.B=33;local.K=F(11,25);local.CURVATURE=F(0);local.CUTOFF=T;local.SLOPE=C
    support=local.verify();assert support['status']=='PASS' and C>F(3,100)
    footprint=sine(q(EARSPAN))-q(2*R);assert footprint.l>0
    assert 3*T>EARSPAN
    charge=C*(3*T-EARSPAN)/2
    raw=F(previous['raw_M26_area_margin']);shift=F(previous['shifted_ear_upper'])
    margin=raw-R*R*shift+charge;assert margin>0
    cases=[z for z in previous['remaining_Euler_cases'] if z['ears']==0]
    assert len(cases)==2
    return dict(status='PASS',radius=str(R),B=33,M_domain='M>=26',
        scope='Structural reduction only: no ears and minimum interior degree six; two profiles remain',
        required_center_norm_squared_upper=str(1-R*R),
        joint_owner_membership_upper=2,hinge_slope=str(C),hinge_zero=str(T),
        ordinary_charges_retained_from_slope='3/100',ear_halfarc_sum_upper=str(EARSPAN),
        ear_footprint_sine_margin=str(F(footprint.l,S)),ear_area_charge=str(charge),
        ear_contradiction_margin=str(margin),remaining_Euler_cases=cases,
        strong_hinge_boxes=support['bad_arc_boxes'],
        minimum_strong_hinge_margin=support['minimum_bad_arc_margin'],
        previous_degree6_status=previous['status'])
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

#!/usr/bin/env python3
"""Sharper angle comparison within the independently bootstrapped B32 window."""
from fractions import Fraction as F
import json
from check_tight_B32_boundary_window_0p11325 import verify as initial,R,HALF
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine
from exact_angle_conjugates import acos_interval
def asin(x):
    z=acos_interval(x);assert z is not None
    return PI/2-z
def verify():
    result=initial();assert result['status']=='PASS'
    rr=q(R);t=q(HALF);s=sine(t)
    assert s.l>rr.sq().u
    eta_min=asin(s/rr)-t
    eta_max=PI/2-asin(rr)
    E=PI/2+(eta_max-eta_min)/2
    assert 0<E.l<E.u<PI.l
    ratio=E/(2*sine(E/2))
    actual=F(9,10);reference=F(19,20);angle=F(13,10);difference=F(11,100);X=F(27,50)
    guard=q(angle)*(q(actual*reference)).sqrt()-ratio
    assert guard.l>0
    residual=X*X-2*angle*difference;assert residual==F(7,1250)>0
    result.update(orientation_error_constant=str(angle),
        adjacent_boundary_weight_difference_upper=str(difference),absorption_residual=str(residual),
        angle_lift_absolute_upper=str(F(E.u,S)),
        sharp_chord_ratio_upper=str(F(ratio.u,S)),
        sharp_angle_comparison_margin=str(F(guard.l,S)),
        radius_monotonicity_guard='sin(HALF)>R^2',
        refinement='Uses the actual/reference lifted-angle range before bounding e/(2 sin(e/2))')
    return result
if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

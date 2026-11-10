#!/usr/bin/env python3
"""Conditional B32 window from the tighter pure center cap229.8."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import verify_extension as geometry
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_angle_conjugates import acos_interval
R=F(453,4000);CENTER_SUPPORT=F(1149,5);HALF=F(307,5000)

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    geometry.check_concavity_factorization()
    rr=q(R);mu=PI/32
    def H(t):
        s=sine(t)
        return s*(rr.sq()-s.sq()).sqrt()+t-s*cosine(t)
    slack=rr.sq()*q(CENTER_SUPPORT)+32*H(mu)-PI
    assert 0<slack.l and slack.u<q(F(4,1000)).l
    t=q(HALF);other=(PI-t)/31
    assert t.u<mu.l and sine(other).u<rr.l
    arc_margin=PI-rr.sq()*q(CENTER_SUPPORT)-H(t)-31*H(other)
    assert arc_margin.l>0
    x=q(F(9,20));h=(1-x.sq()).sqrt()
    assert (1+2*h-2*x.sq()/h).l>0
    a=PI/2-acos_interval(x)
    acute=x*(1+2*h)+q(F(3,10))*a
    obtuse=x+q(F(3,10))*PI
    support_lower=q(3).sqrt()+PI/15
    local_gap=q(F(support_lower.l-max(acute.u,obtuse.u),S))
    edge_margin=rr.sq()*local_gap-slack
    assert edge_margin.l>0
    X=F(27,50);reference=F(19,20);angle=F(17,10);difference=F(17,200)
    assert (sine(t)/rr).l>q(X).u
    assert 2*(1-R)*X>reference
    assert PI.sq().u<q(4*F(9,10)*reference*angle*angle).l
    residual=X*X-2*angle*difference;assert residual==F(13,5000)>0
    assert (8*x.sq()/PI.sq()).l>q(F(4,25)).u
    return dict(status='PASS',B=32,radius_upper=str(R),normalized_center_upper_bound=str(CENTER_SUPPORT),
        scope='Uniform conditional metric window only; each graph must independently verify its pure center cap and local supports',
        required_marked_apex_potential_range=['-3/10','-1/5'],
        required_initial_boundary_angle_weights='all zero',
        required_initial_shared_edge_terms='all cancel exactly',
        half_arc_lower=str(HALF),full_arc_lower=str(2*HALF),
        normalized_arc_sine_lower=str(X),actual_edge_over_radius_lower='9/10',
        reference_edge_over_radius_lower=str(reference),orientation_error_constant=str(angle),
        adjacent_boundary_weight_difference_upper=str(difference),absorption_residual=str(residual),
        marked_potential_difference_penalty='25/16',
        total_surplus_upper=str(F(slack.u,S)),short_arc_contradiction_margin=str(F(arc_margin.l,S)),
        short_marked_edge_contradiction_margin=str(F(edge_margin.l,S)))

if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

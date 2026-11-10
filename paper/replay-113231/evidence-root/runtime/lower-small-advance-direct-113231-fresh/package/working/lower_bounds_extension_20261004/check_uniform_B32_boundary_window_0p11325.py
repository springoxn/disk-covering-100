#!/usr/bin/env python3
"""Uniform conditional metric window for B32 through .11325, center support<=230.

The caller must independently prove the center-support bound, all local
support validity/cancellation, and the marked-apex potential range. This
checker supplies only their common scalar geometric consequences.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import verify_extension as geometry
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_angle_conjugates import acos_interval

R=F(453,4000)
CENTER_SUPPORT=F(230)


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    geometry.check_concavity_factorization()
    radius=q(R)
    def H(t):
        s=sine(t)
        return s*(radius.sq()-s.sq()).sqrt()+t-s*cosine(t)
    mu=PI/32
    slack=radius.sq()*q(CENTER_SUPPORT)+32*H(mu)-PI
    assert 0<slack.l and slack.u<q(F(64,10000)).l
    short=q(F(1,25));other=(PI-short)/31
    assert short.u<mu.l and sine(other).u<radius.l
    loss=32*H(mu)-H(short)-31*H(other)
    arc_margin=loss-slack
    assert arc_margin.l>q(F(15,10000)).u
    x=q(F(9,20));y=(1-x.sq()).sqrt()
    assert (1+2*y-2*x.sq()/y).l>0
    arcsin_x=PI/2-acos_interval(x)
    acute=x*(1+2*y)+q(F(3,10))*arcsin_x
    obtuse=x+q(F(3,10))*PI
    support_lower=q(3).sqrt()+PI/15
    gap=q(F(support_lower.l-max(acute.u,obtuse.u),S))
    edge_margin=radius.sq()*gap-slack
    assert edge_margin.l>q(F(65,100000)).u
    s=sine(short);c=cosine(short);h=(radius.sq()-s.sq()).sqrt()
    sin_eta=s*(c-h)/radius
    assert sin_eta.l>q(F(3,10)).u
    assert (s/radius).l>q(F(353,1000)).u
    assert q(F(353,1000)).sq().l>q(F(9,80)).u
    assert PI.sq().u<q(4*F(9,10)*F(3,5)*F(9,4)**2).l
    assert (8*q(F(9,20)).sq()/PI.sq()).l>q(F(4,25)).u
    return {'status':'PASS','radius_upper':str(R),'B':32,
            'scope':'Uniform conditional boundary metric-window lemma only; no graph or global radius exclusion',
            'required_premises':[
                'A valid no-ear center triangulation with 32 ordinary marked boundary faces',
                'A radius-independent signed center/anchor support sum at most 230, with all local supports valid on their full actual domains',
                'Every shared-edge term cancels and all boundary angle potentials of this initial dual are zero',
                'Every marked-apex potential u belongs to [-3/10,-1/5]; no such range is required for unmarked deep vertices',
                'Each marked local support is the valid conjugate of Gbar(gamma)-u*gamma'],
            'normalized_center_upper_bound':'230',
            'new_radius_total_slack_upper':str(F(slack.u,S)),
            'full_arc_lower':'2/25','short_arc_contradiction_margin':str(F(arc_margin.l,S)),
            'actual_edge_over_radius_lower':'9/10',
            'short_marked_edge_contradiction_margin':str(F(edge_margin.l,S)),
            'reference_edge_over_radius_lower':'3/5',
            'normalized_arc_sine_lower':'353/1000',
            'adjacent_boundary_weight_difference_upper':'1/40',
            'orientation_error_constant':'9/4',
            'marked_base_variance_coefficient':'4/25',
            'marked_potential_difference_penalty':'25/16'}


if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

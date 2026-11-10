#!/usr/bin/env python3
"""Graph-specific metric window at .1132 from a replayed signed-edge dual.

This establishes premises for a later joint boundary-angle certificate. It
does not itself exclude the graph at .1132 or prove a global radius bound.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(ROOT),str(ROOT/'signed_edge_metric_20261004')]
import verify_signed_graph_wide as signed
import verify_extension as geometry
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_angle_conjugates import acos_interval

R=F(283,2500)


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    directory=ROOT/'signed_edge_metric_20261004'
    gp=directory/'graph_N27_0009.json'
    cp=directory/'certificate_N27_0009_wide_11310.json'
    certificate=json.loads(cp.read_text())
    assert certificate['family_id']=='flat_N27_0009'
    assert F(*certificate['radius'])==F(1131,10000)
    # This replay establishes the dimensionless center-support sum. That
    # sum and its all-shape signed-edge proofs are radius-independent.
    previous=signed.verify(gp,certificate)
    assert previous['status']=='PASS'
    normalized=F(previous['normalized_upper_bound'])
    us=[F(x,certificate['denominator']) for x in certificate['u']]
    assert all(F(-3,10)<=u<=F(-1,5) for u in us)
    geometry.check_concavity_factorization()
    radius=q(R)
    def H(t):
        s=sine(t)
        return s*(radius.sq()-s.sq()).sqrt()+t-s*cosine(t)
    mu=PI/33
    upper=radius.sq()*q(normalized)+33*H(mu)
    slack=upper-PI
    assert 0<slack.l and slack.u<q(F(43,10000)).l
    # A short full arc is at most .08, so its half arc is at most .04.
    short=q(F(1,25));other=(PI-short)/32
    assert short.u<mu.l and sine(other).u<radius.l
    loss=33*H(mu)-H(short)-32*H(other)
    arc_margin=loss-slack
    assert arc_margin.l>q(F(1,1000)).u
    # Fixed-base convexity gives the acute and obtuse endpoint caps.
    x=q(F(9,20));y=(1-x.sq()).sqrt()
    assert (1+2*y-2*x.sq()/y).l>0
    arcsin_x=PI/2-acos_interval(x)
    acute=x*(1+2*y)+q(F(3,10))*arcsin_x
    obtuse=x+q(F(3,10))*PI
    support_lower=q(3).sqrt()+PI/15
    gap=q(F(support_lower.l-max(acute.u,obtuse.u),S))
    edge_margin=radius.sq()*gap-slack
    assert edge_margin.l>q(F(2,1000)).u
    # Repeat all radius-dependent constants in the radial reduction.
    s=sine(short);c=cosine(short);h=(radius.sq()-s.sq()).sqrt()
    sin_eta=s*(c-h)/radius
    assert sin_eta.l>q(F(3,10)).u
    assert (s/radius).l>q(F(353,1000)).u
    assert q(F(353,1000)).sq().l>q(F(9,80)).u
    assert PI.sq().u<q(4*F(9,10)*F(3,5)*F(9,4)**2).l
    assert (8*q(F(9,20)).sq()/PI.sq()).l>q(F(4,25)).u
    return {'status':'PASS','family_id':'flat_N27_0009','radius_upper':str(R),
            'scope':'Graph-specific boundary metric-window premises only; no .1132 graph exclusion or global radius theorem',
            'graph_sha256':hashlib.sha256(gp.read_bytes()).hexdigest(),
            'pure_certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
            'pure_signed_support_replayed':True,
            'normalized_center_upper_bound':str(normalized),
            'new_radius_total_slack_upper':str(F(slack.u,S)),
            'full_arc_lower':'2/25','short_arc_contradiction_margin':str(F(arc_margin.l,S)),
            'actual_edge_over_radius_lower':'9/10',
            'short_marked_edge_contradiction_margin':str(F(edge_margin.l,S)),
            'reference_edge_over_radius_lower':'3/5',
            'normalized_arc_sine_lower':'353/1000',
            'adjacent_boundary_weight_difference_upper':'1/40',
            'orientation_error_constant':'9/4',
            'marked_base_variance_coefficient':'4/25',
            'marked_potential_difference_penalty':'25/16',
            'required_graph_premise':'The covering has the specified validated no-ear graph and its marked bases'}


if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

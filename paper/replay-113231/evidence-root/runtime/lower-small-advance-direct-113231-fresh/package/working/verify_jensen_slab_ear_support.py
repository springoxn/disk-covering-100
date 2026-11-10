#!/usr/bin/env python3
"""Exact constants for the stronger Jensen-plus-slab ear support.

The continuous lemma applies to 0<r<=1400/11449 and 0<=k<=1.
This is a local actual-boundary-ear support, not a global covering theorem.
"""
from fractions import Fraction as F
import json
from verify_star_lp_duals import q,S


def cap(radius,multiplier):
    r,k=F(radius),F(multiplier)
    assert 0<r<=F(1400,11449) and 0<=k<=1
    ri,ki=q(r),q(k)
    w=q(2)/(1+(1-2*ri).sqrt())
    assert w.l>q(1).u
    value=w+(2*w-w.sq()).sqrt()-ki*(2*w).sqrt()
    return value


def quadratic_cap(radius,penalty):
    r,lam=F(radius),F(penalty)
    assert 0<r<=F(1400,11449) and 0<=lam<=F(1,5)
    ri=q(r);w=q(2)/(1+(1-2*ri).sqrt())
    return w+(2*w-w.sq()).sqrt()-4*q(lam)*w


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    # This lower bound holds for F'_k(w), every 1<=w<=1.07, k<=1.
    derivative=1-q(7)/q(9951).sqrt()-q(1)/q(2).sqrt()
    assert derivative.l>0
    quadratic_derivative=1-q(7)/q(9951).sqrt()-q(F(4,5))
    assert quadratic_derivative.l>0
    assert F(1)-2*F(1400,11449)==F(93,107)**2
    rows=[];quadratic_rows=[]
    for r in (F(707,6250),F(2263,20000),F(113231,1000000),F(1155018241946,10**13)):
        for k in (F(0),F(6,25),F(1,4),F(7,20),F(1,2),F(1)):
            value=cap(r,k)
            rows.append({'radius':str(r),'halfside_multiplier':str(k),
                         'ear_score_upper':str(F(value.u,S))})
        for lam in (F(37,1000),F(1,25),F(3,50)):
            value=quadratic_cap(r,lam)
            quadratic_rows.append({'radius':str(r),'squared_edge_penalty':str(lam),
                                   'ear_score_upper':str(F(value.u,S))})
    return {'status':'PASS','radius_domain':'0<r<=1400/11449','multiplier_domain':'0<=k<=1',
            'increasing_left_branch_derivative_margin':str(F(derivative.l,S)),
            'quadratic_penalty_derivative_margin':str(F(quadratic_derivative.l,S)),
            'cases':rows,'quadratic_cases':quadratic_rows,
            'scope':'Local actual-boundary-ear score supports only'}


if __name__=='__main__':print(json.dumps(verify(),indent=2))

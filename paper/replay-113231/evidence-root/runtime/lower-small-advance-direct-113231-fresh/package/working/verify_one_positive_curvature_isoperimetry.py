#!/usr/bin/env python3
"""Exact arithmetic consequences of the separate K<=1 disk proof."""
from fractions import Fraction as F
import json


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    for b in (3,4):assert b-2<=F(b*b,5)
    for b in range(5,101):
        assert 9+(b-1)**2<=b*b
        assert b+(b-5)+F((b-5)**2,5)==F(b*b,5)
    rows=[]
    for B in range(32,39):
        base=198-2*B
        limit=max(M for M in range(100) if 5*(base-M)-M*M>0)
        margins=[5*(base-M)-M*M for M in range(limit+1)]
        assert min(margins)>0
        rows.append({'m':100,'B':B,'M_upper':limit,'required_unmarked_positive_curvature':2,
                     'endpoint_integer_margin':min(margins)})
    assert next(r for r in rows if r['B']==33)['M_upper']==23
    return {'status':'PASS','scope':'Weighted core-curvature obstruction only, not a radius exclusion',
            'required_analytic_theorem':'Total positive interior curvature<=1 implies F<=b^2/5',
            'cases':rows}


if __name__=='__main__':print(json.dumps(verify(),indent=2))

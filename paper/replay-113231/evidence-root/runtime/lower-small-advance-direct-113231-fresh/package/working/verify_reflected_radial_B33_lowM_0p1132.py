#!/usr/bin/env python3
"""Conditional low-M B33 radial support at R=.1132."""
from fractions import Fraction as F
import json
from reflected_radial_stability_backend import ReflectedRadialStability

SUPPORT=ReflectedRadialStability(
    F(283,2500),F(7,125),F(554,1250),
    F(-615539,50000000),F(10526931,10**9),F(3,2),
    quadratic_factor=F(67349,20000))

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    node=SUPPORT.node_guard(F(251,2500))
    pair=SUPPORT.exhaustive_pair()
    assert node['status']=='PASS' and pair['status']=='PASS'
    return {'status':'PASS','radius':str(SUPPORT.radius),'B':SUPPORT.B,
            'lambda':str(SUPPORT.penalty),'sine_lower':str(SUPPORT.sine_lower),
            'quadratic_factor':str(SUPPORT.factor),'stability':str(SUPPORT.stability),
            'intercept':str(SUPPORT.intercept),'slope':str(SUPPORT.slope),
            'node':node,'pair':pair,
            'scope':'Boundary functional only. Requires reflected-center normalization and the independent low-M full-arc lower bound251/2500. This file does not establish any global covering threshold.'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))

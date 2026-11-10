#!/usr/bin/env python3
"""Final high-M B33 support using an independent stability arc bootstrap."""
from fractions import Fraction as F
import json
from reflected_radial_stability_backend import ReflectedRadialStability

SUPPORT=ReflectedRadialStability(
    F(283,2500),F(11,100),F(2031,5000),
    F(101904,12500000),F(166667,20000000),F(0),
    quadratic_factor=F(173537,50000))

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    node=SUPPORT.node_guard(F(23,250))
    pair=SUPPORT.exhaustive_pair()
    assert node['status']=='PASS' and pair['status']=='PASS'
    return {'status':'PASS','radius':str(SUPPORT.radius),'B':SUPPORT.B,
            'lambda':str(SUPPORT.penalty),'sine_lower':str(SUPPORT.sine_lower),
            'quadratic_factor':str(SUPPORT.factor),'stability':str(SUPPORT.stability),
            'intercept':str(SUPPORT.intercept),'slope':str(SUPPORT.slope),
            'node':node,'pair':pair,
            'scope':'Final high-M boundary functional only. Requires reflected-center normalization and a separate unspent-variance full-arc lower bound23/250. This support has no remaining variance charge.'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))

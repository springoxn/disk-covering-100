#!/usr/bin/env python3
"""Initial high-M stability support at R=.1132; variance is unspent."""
from fractions import Fraction as F
import json
from reflected_radial_stability_backend import ReflectedRadialStability

SUPPORT=ReflectedRadialStability(
    F(283,2500),F(9,100),F(121,400),
    F(286697,500000000),F(2286447,250000000),F(1,4),
    quadratic_factor=F(370909,100000))

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    node=SUPPORT.node_guard(F(137,2000))
    pair=SUPPORT.exhaustive_pair()
    assert node['status']=='PASS' and pair['status']=='PASS'
    return {'status':'PASS','radius':str(SUPPORT.radius),'B':SUPPORT.B,
            'lambda':str(SUPPORT.penalty),'sine_lower':str(SUPPORT.sine_lower),
            'quadratic_factor':str(SUPPORT.factor),'stability':str(SUPPORT.stability),
            'intercept':str(SUPPORT.intercept),'slope':str(SUPPORT.slope),
            'node':node,'pair':pair,
            'scope':'Conditional boundary functional for a fresh high-M variance/arc bootstrap. Requires reflected-center normalization and independent full arc137/2000. Its gamma variance must not also be spent on fan or ear penalties in that bootstrap.'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))

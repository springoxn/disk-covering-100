#!/usr/bin/env python3
"""Exact constants for sharp complete-star area caps."""
from fractions import Fraction as F
import json
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine

def cap(degree):
    assert type(degree) is int and degree>=3
    A=3*q(3).sqrt()/4
    if degree==3:return q(2)
    if degree==4:return q(4)
    if degree==5:return (25*(25+11*q(5).sqrt())/32).sqrt()
    if degree==6:return 6*A
    angle=2*PI/degree
    return degree*sine(angle)*(1+cosine(angle))

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    A=3*q(3).sqrt()/4
    assert (cap(5)-4*A).l>0 and (cap(6)-2*PI).l>0
    rows=[];previous=cap(4)
    for degree in range(4,100):
        value=cap(degree)
        if degree>4:assert value.l>previous.u
        deficit=degree*A-value
        if degree!=6:assert deficit.l>0
        rows.append({'degree':degree,'cap_interval':[str(F(value.l,S)),str(F(value.u,S))],
                     'old_equilateral_allowance_deficit_lower':str(F(deficit.l,S))})
        previous=value
    return {'status':'PASS','sample_degrees':[4,99],
            'three_angle_cap':'2','five_angle_cap_squared':'25*(25+11sqrt(5))/32',
            'cases':rows,'scope':'Complete-star area lemma and sample exact constants; no global covering-radius claim'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))

#!/usr/bin/env python3
"""Exact unconditional-angle interior degree restrictions."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
from verify_star_lp_duals import q,S,PI
from verify_potential_star_duals import sine,cosine
from verify_complete_star_area_caps import cap
sys.path.insert(0,str(Path(__file__).resolve().parent/'lower_bounds_extension_20261004'))
import verify_extension as geometry

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    geometry.check_kappa()
    A=3*q(3).sqrt()/4;anchor_gap=q(F(1,2)-geometry.KAPPA)
    D3=3*A-cap(3)-2*anchor_gap
    D4=4*A-cap(4)-3*anchor_gap
    D9=9*A-cap(9)-8*anchor_gap
    assert anchor_gap.l>0 and D3.l>D4.u>0 and D9.l>D4.u
    angle=2*PI/9
    Q=sine(angle)*(1+cosine(angle))
    Qprime=cosine(angle)+cosine(2*angle)
    monotonic_margin=A-anchor_gap-(Q-angle*Qprime)
    assert monotonic_margin.l>0
    rows=[]
    for radius in (F(5659,50000),F(11319,100000),F(283,2500),F(113231,1000000)):
        upper=((198-33)*geometry.AH+33*geometry.KAPPA)*radius*radius
        upper+=33*geometry.H_upper(radius,2*geometry.PL/33,2*geometry.PH/33)
        budget=(upper-geometry.PL)/(radius*radius)
        margin=F(D4.l,S)-budget
        assert margin>0
        rows.append({'radius':str(radius),'B':33,'old_normalized_budget_upper':str(budget),
                     'degree_window_margin_lower':str(margin)})
    return {'status':'PASS','required_interior_count':'greater than1',
            'minimum_interior_degree':5,'maximum_interior_degree':8,
            'degree3_loss_lower':str(F(D3.l,S)),'degree4_loss_lower':str(F(D4.l,S)),
            'degree_at_least9_loss_lower':str(F(D9.l,S)),
            'large_degree_monotonic_margin_lower':str(F(monotonic_margin.l,S)),
            'cases':rows,'scope':'Conditional global degree restriction only; no covering-radius exclusion'}

if __name__=='__main__':print(json.dumps(verify(),indent=2))

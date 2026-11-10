#!/usr/bin/env python3
"""Exact constants for degree >=5 without marked-apex acuteness."""
from fractions import Fraction as F
import json
import verify_extension as v


def verify():
    r5l,r5h=v.sqrt_bounds(F(5))
    cl,ch=(r5l-1)/4,(r5h-1)/4
    sl=v.sqrt_bounds(1-ch*ch)[0];sh=v.sqrt_bounds(1-cl*cl)[1]
    kl=sl*(1+cl)+v.PL/5;kh=sh*(1+ch)+v.PH/5
    v.need(kl>v.PH/2,'global q0 tangent dominates at pi')
    ll=v.sqrt_bounds(F(3))[0]+v.PL/6
    lh=v.sqrt_bounds(F(3))[1]+v.PH/6
    v.need(v.AH-kl<0,'A-K negative')
    v.need(v.KAPPA+kl-lh>0,'marked coefficient nonnegative')
    deficit=v.PL+4*(v.AL-kh)
    v.need(deficit>F(4,5),'all degree at most four stars have deficit>.8')
    lo,hi=v.outward(deficit,deficit,25)
    return {'status':'PASS','q0_angle_domain':'[0,pi]',
            'marked_apex_domain':'[0,pi]','old_normalized_loss_budget_required_less_than':'4/5',
            'minimum_interior_degree':5,'degree_at_most_four_deficit_lower_interval':[str(lo),str(hi)],
            'common_tangent_slope':'-1/2','q0_tangent_angle':'2*pi/5',
            'scope':'A conditional minimum-degree lemma, not a radius theorem'}


if __name__=='__main__':print(json.dumps(verify(),indent=2))

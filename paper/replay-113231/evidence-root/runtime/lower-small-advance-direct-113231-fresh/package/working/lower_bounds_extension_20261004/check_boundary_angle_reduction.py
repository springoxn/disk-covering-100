#!/usr/bin/env python3
"""Exact constants and polynomial identity for the boundary-angle reduction."""
from fractions import Fraction as F
import json
import verify_extension as v
import check_ear_star_premises_0p1131 as base


def verify():
    premises=base.verify()
    R=F(1131,10000)
    x=F(9,20)
    g_upper=x*(1+2*v.sqrt_bounds(1-x*x)[1])
    v.need(g_upper<v.AL+v.KAPPA-F(471,1000),'ordinary marked edge>.9r')
    t=F(1,25)
    sl,sh=v.sin_at(t)
    cl,ch=v.cos_at(t)
    hupper=v.sqrt_bounds(R*R-sl*sl)[1]
    sin_eta_lower=sl*(cl-hupper)/R
    v.need(sin_eta_lower>F(3,10),'reference marked edge>.6r')
    v.need(sl/R>F(707,2000),'normalized arc sine lower')
    v.need(v.PH*v.PH<4*F(9,10)*F(3,5)*F(9,4)**2,'angle Lipschitz constant')
    v.need(F(707,2000)**2>F(9,80),'angular displacement absorbed by outer loss')
    v.need(8*F(9,20)**2/v.PH**2>F(4,25),'marked base-imbalance coefficient')
    # The difference has individual degree at most three in each variable;
    # its vanishing on this 4^4 Cartesian grid verifies the polynomial identity.
    checks=0
    for T in range(4):
        for a in range(4):
            for b in range(4):
                for u in range(4):
                    left=(2*u-b-a)**2*(T-u)-(1-u)*(T-2*u+b)**2
                    right=(4*(a-1)*u*u
                           +(-4*T*(a+b)-(a+b)**2+4*(T+b)+(T+b)**2)*u
                           +T*(a+b)**2-(T+b)**2)
                    v.need(left==right,'stationary quadratic identity')
                    checks+=1
    return {'status':'PASS','radius_upper':str(R),'B':33,
            'required_extra_premise':'Every boundary edge is an ordinary q1 base; no ears or all-boundary marked faces',
            'full_arc_lower':'2/25','actual_edge_over_radius_lower':'9/10',
            'reference_edge_over_radius_lower':'3/5',
            'adjacent_boundary_weight_difference_upper':'1/40',
            'orientation_error_constant':'9/4','marked_base_variance_coefficient':'4/25',
            'marked_potential_difference_penalty':'25/16','polynomial_grid_checks':checks,
            'base_premises_status':premises['status'],
            'scope':'Local metric/dual reduction constants only; no assembled graph or global radius exclusion'}


if __name__=='__main__':
    print(json.dumps(verify(),indent=2))

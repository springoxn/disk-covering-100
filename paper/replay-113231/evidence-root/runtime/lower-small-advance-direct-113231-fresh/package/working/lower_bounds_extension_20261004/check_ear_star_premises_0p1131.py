#!/usr/bin/env python3
"""Ear/bad-q1-compatible B33 angle premises at radius .1131."""
from fractions import Fraction as F
import json
import verify_extension as v


def verify():
    r=F(1131,10000)
    B=33
    v.R=r
    v.check_kappa()
    n99=v.exclude_all(99,r)
    survivors=[b for b in range(3,100) if v.classify(100,b,r)['status']=='not excluded']
    v.need(survivors==list(range(32,38)),'old count bridge')
    center=((198-B)*v.AH+B*v.KAPPA)*r*r
    slack=center+B*v.H_upper(r,2*v.PL/B,2*v.PH/B)-v.PL
    d=slack/(r*r)
    v.need(d<F(471,1000),'normalized loss budget')
    a=F(11,25)
    eps=F(17,100)
    qlo=v.sin_at(a)[1]*(1+v.cos_at(a)[1])
    qhi=v.cos_at(eps)[1]*(1-v.sin_at(eps)[0])
    v.need(max(qlo,qhi)<v.AL-d,'q0 angle window')
    glo=v.sin_at(a)[1]*(1+2*v.cos_at(a)[1])
    v.need(glo<v.AL+v.KAPPA-d,'good q1 apex lower angle')
    v.need((1+v.sqrt_bounds(F(2))[1])/2<v.AL+v.KAPPA-d,'good q1 apex acute')
    v.need(15*a>2*v.PH,'interior degree at most fourteen')
    v.need(3*(v.PH/2+eps)<2*v.PL,'interior degree at least four')
    v.need(v.sin_at(eps)[1]<F(1,4),'Q concavity endpoint')
    v.need(v.PL/2-3*eps>v.PH/3,'marked mean in linear Gbar branch')
    degree4=[]
    for p in range(4):
        j=4-p
        score=p*(v.sqrt_bounds(F(3))[1]-v.PL/12)+j*(1+eps/2)
        gap=4*v.AL+p*v.KAPPA-score-d
        v.need(gap>F(1,3),'degree-four star exclusion')
        degree4.append({'p':p,'contradiction_margin_greater_than':'1/3'})
    fans=v.cluster_exclusion(B,5,F(6931,10000),3,F(1,200))
    L=F(2,25)
    v.need(L<2*v.PL/B,'one-arc Jensen monotonicity branch')
    upper=(center+v.H_upper(r,L,L)
           +(B-1)*v.H_upper(r,(2*v.PL-L)/(B-1),(2*v.PH-L)/(B-1)))
    gap=v.PL-upper
    v.need(gap>F(1,5000),'full arc angle greater than .08')
    lo,hi=v.outward(gap,gap,25)
    return {'status':'PASS','radius':str(r),'B':B,'m':100,'I':67,'F':165,
            'exclusion_of_99':n99,'remaining_boundary_counts':survivors,
            'normalized_deficit_upper':'471/1000',
            'q0_angle_window':['11/25','pi/2+17/100'],
            'good_q1_apex_angle_window':['11/25','pi/2'],
            'interior_degree_range':[5,14],'degree_four_exclusions':degree4,
            'maximum_good_marked_incidences':3,'fan_cluster':fans,
            'full_assigned_arc_lower':'2/25','one_arc_exclusion_margin_interval':[str(lo),str(hi)],
            'allowed':['q2 ears','all-boundary q1 faces','all-boundary q0 faces','boundary chords'],
            'incidence_identities':{'good_q1_faces':'33-2e-b','q0_faces':'132+e',
                                    'sum_q':'33-2e-b','sum_d_minus_6':'27+e-b-N',
                                    'q0_boundary_angle_sum':'Gamma+(e-2)pi'},
            'N_bound_from_degree_minimum':'N<=94+e-b',
            'scope':'Base premises only; ear/bad-face angular supports and all scalar branches remain separate'}


if __name__=='__main__':
    print(json.dumps(verify(),indent=2))

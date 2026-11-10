#!/usr/bin/env python3
"""Exact full-domain capped-pair test for every B>=36 at radius .11323.

This is a conditional boundary-count exclusion, not a global radius theorem.
The new cap uses the common covered boundary point of each adjacent pair.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'threshold_11305_components'))
import verify_remaining_cases as m
R=F(113231,1000000);LAM=F(3,50);K=F(3892,12500)
MU=F(92531,10**7);L=F(751,100000)


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    m.R=R;b=m.b
    assert m.LAMBDA34==LAM and m.K34==K
    caps=m.triangle_checks_34()
    original=b.bound;threshold=b.ci(L)[0]
    def capped(box,mu):
        sa,ha,ua,va,pa,Ha=b.state((box[0],box[1]),-1)
        sb,hb,ub,vb,pb,Hb=b.state((box[2],box[3]),1)
        # Adjacent centers both lie within R of their common boundary
        # endpoint, so their squared distance is at most 4R^2.
        direct=b.add(b.mul(b.scal(b.LAM,4),b.R2),b.half(b.add(Ha,Hb)))
        direct=b.sub(direct,b.mul(mu,b.half(b.add(b.asin(sa),b.asin(sb)))))[1]
        if direct<=threshold:return direct
        return min(direct,original(box,mu))
    b.bound=capped
    try:
        pair=m.pair_replay(36,LAM,MU,L,F(0))
    finally:
        b.bound=original
    assert 0<MU<1
    margin=(1-MU)*m.v.PL-((198-36)*b.A_UP+36*K)*R*R-36*L
    per_boundary_gain=(b.A_UP-K)*R*R-L
    assert margin>0 and per_boundary_gain>0
    return {'status':'PASS','radius':str(R),'m_at_most':100,'boundary_counts':'36 through 99',
            'scope':'Every B>=36 branch only; smaller B and the exact optimum remain separate',
            'penalty':str(LAM),'marked_constant':str(K),'slope':str(MU),'intercept':str(L),
            'all_q_triangle_supports':caps,'complete_capped_pair':pair,
            'minimum_area_margin_at_B36':str(margin),
            'additional_margin_per_boundary_cell':str(per_boundary_gain)}


if __name__=='__main__':print(json.dumps(verify(),indent=2),flush=True)

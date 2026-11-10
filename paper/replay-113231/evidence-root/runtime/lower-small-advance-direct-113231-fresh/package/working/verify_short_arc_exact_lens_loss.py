#!/usr/bin/env python3
"""Exact single-short-arc loss relative to a globally certified lens tangent."""
from fractions import Fraction as F
import json,math
from verify_star_lp_duals import I,q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_angle_conjugates import acos_interval
R=F(5661,50000);B=34;K=F(1,2);CURVATURE=F(0);CUTOFF=F(1,20)

def asin(x):
    z=acos_interval(x);assert z is not None
    return PI/2-z

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    rr=q(R);T=rr.sq();kk=q(K);mu=PI/B;ar=asin(rr)
    sm=sine(mu);cm=cosine(mu);hm=(T-sm.sq()).sqrt()
    b=T*kk*(hm*cm+sm.sq())/rr
    assert 0<b.l<b.u<T.l
    tc=asin(rr*kk.sqrt());assert tc.u<mu.l
    def outer(t):
        s=sine(t);c=cosine(t);h=(T-s.sq()).sqrt()
        val=s*h+t-s*c+b*(asin(s/rr)-t)
        der=c*(T-2*s.sq())/h+2*s.sq()+b*(c/h-1)
        return val,der
    fm,dm=outer(mu)
    # Previously proved exact lower bound for -F''/2 on t>=tc.
    good=kk.sqrt()*(1-T)*(1-b/T)/(2*(1-kk)*(1-kk).sqrt())
    assert good.l>q(CURVATURE).u
    count=1000;end=q(CUTOFF).u;minimum=None;root_cases=endpoint_cases=0
    assert 0<end<tc.l
    for j in range(count):
        lo=end*j//count;hi=(end*(j+1)+count-1)//count
        box=I(lo,hi);mid=I((lo+hi)//2)
        u=sine(box)/rr;a=asin(u)
        Z=(PI/2-ar+box-a)/2
        assert Z.l>=0 and 2*Z.u+a.u<PI.l//2
        # A proposal chooses the tangent only. No floating comparison is
        # used to accept a bound, a root, or a domain assertion.
        mt=(lo+hi)/(2*S);uf=math.sin(mt)/float(R)
        af=math.asin(uf);zf=(math.pi/2-math.asin(float(R))+mt-af)/2
        left=0.;right=zf
        def df(z):return float(K)*math.cos(z)-uf*math.sin(2*z+af)
        if df(right)>=0:zproposal=right;endpoint_cases+=1
        elif df(left)<=0:zproposal=0.;endpoint_cases+=1
        else:
            for _ in range(45):
                mm=(left+right)/2
                if df(mm)>0:left=mm
                else:right=mm
            zproposal=(left+right)/2;root_cases+=1
        raw=max(0,min(int(round(zproposal*10**12)),Z.u*10**12//S))
        z=q(F(raw,10**12))
        assert z.l>=0 and 2*z.u+a.u<PI.l//2
        val=2*T*sine(z)*(kk-u*sine(z+a))
        der=2*T*(kk*cosine(z)-u*sine(2*z+a))
        displacement=I(-z.u,Z.u-z.l)
        penalty=val+der*displacement
        # The actual domain includes z=0, so its upper support must be >=0.
        penalty=I(0,max(0,penalty.u))
        f0,d0=outer(mid)
        gap=fm+dm*(mid-mu)-f0+(dm-d0)*(box-mid)
        gap-=q(CURVATURE)*(box-mu).sq()+penalty
        assert gap.l>0,('bad interval',j,F(lo,S),F(hi,S),F(gap.l,S))
        minimum=gap.l if minimum is None else min(minimum,gap.l)
    # The exact endpoint formula is also checked algebraically in radicals.
    endpoint=kk*T*(2*(1-rr)).sqrt()
    z0=(PI/2-ar)/2
    trig_endpoint=2*T*kk*sine(z0)
    assert max(endpoint.l,trig_endpoint.l)<=min(endpoint.u,trig_endpoint.u)
    return dict(status='PASS',radius=str(R),B=B,halfside_multiplier=str(K),
        scope='Pointwise loss only on0<=halfarc<=CUTOFF; caller must independently prove nonnegative deficits elsewhere',
        short_half_arc_upper=str(CUTOFF),
        required_center_norm_squared_upper=str(1-R*R),variance_coefficient=str(CURVATURE),
        bad_arc_boxes=count,root_tangent_proposals=root_cases,endpoint_tangent_proposals=endpoint_cases,
        minimum_bad_arc_margin=str(F(minimum,S)),
        good_arc_curvature_margin=str(F(good.l-q(CURVATURE).u,S)),
        zero_arc_penalty_interval=[str(F(endpoint.l,S)),str(F(endpoint.u,S))],
        floating_acceptance=False)
if __name__=='__main__':print(json.dumps(verify(),indent=2))

#!/usr/bin/env python3
"""Exact normalized small-arc envelope at B35, R=.11322, k=.33."""
from fractions import Fraction as F
import json
from verify_star_lp_duals import I,q,S,PI
from verify_potential_star_duals import sine,cosine
from exact_angle_conjugates import acos_interval
R=F(5661,50000);B=35;K=F(33,100);CURVATURE=F(1,20)

def arcsine(x):
    z=acos_interval(x);assert z is not None
    return PI/2-z

def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    assert 0<R<1 and 0<K<=F(1,2)
    # Derivative and endpoint bounds for the small-arc penalty numerator.
    derivative=9-12*K-2*R*R*(14+K)*K
    endpoint=2*(1-K)*(3*K-1+2*R*R*K*(1-2*K))
    assert derivative>0 and endpoint<0
    rr=q(R);kk=q(K);T=rr.sq();mu=PI/B
    sm=sine(mu);cm=cosine(mu);hm=(T-sm.sq()).sqrt()
    b=T*kk*(hm*cm+sm.sq())/rr
    beta=(2*(1-rr*(1-kk).sqrt()/(1-T*kk).sqrt())).sqrt()
    assert 0<beta.l<beta.u<q(2).l and b.u<T.l
    tc=arcsine(rr*kk.sqrt())
    assert tc.u<mu.l
    def function(t):
        s=sine(t);c=cosine(t);h=(T-s.sq()).sqrt()
        f=s*h+t-s*c+b*(arcsine(s/rr)-t)
        df=c*(T-2*s.sq())/h+2*s.sq()+b*(c/h-1)
        return f,df
    fm,dm=function(mu)
    good=kk.sqrt()*(1-T)*(1-b/T)/(2*(1-kk)*(1-kk).sqrt())
    assert good.l>q(CURVATURE).u
    points=[q(0)]
    for j in range(1,100):
        t=q(F(j,200))
        if t.u<tc.l:points.append(t)
        else:break
    points.append(tc)
    margins=[]
    for lo,hi in zip(points,points[1:]):
        p=(lo+hi)/2;assert 0<p.l<=p.u<tc.l
        f,df=function(p);s=sine(p);c=cosine(p);u=s/rr;v=(1-u.sq()).sqrt()
        penalty=beta*T*v*(kk-u.sq())
        dp=beta*rr*u*c*(3*u.sq()-kk-2)/v
        for t in(lo,hi):
            gap=fm+dm*(t-mu)-q(CURVATURE)*(t-mu).sq()
            gap-=f+penalty+(df+dp)*(t-p)
            assert gap.l>0,('normalized bad arc',F(gap.l,S))
            margins.append(F(gap.l,S))
    assert endpoint==(-6*K*K+8*K-2+R*R*K*(9*K*K-(14+K)*K+2*K+4))
    # Polynomial identity for the whole-cover reflection, in variables
    # X=|x|^2, d, v=x.u, T=R^2, after multiplication by d^2.
    def add(*polys):
        out={}
        for poly in polys:
            for power,value in poly.items():out[power]=out.get(power,0)+value
        return {power:value for power,value in out.items() if value}
    def mul(a,c):
        out={}
        for p,x in a.items():
            for z,y in c.items():
                power=tuple(i+j for i,j in zip(p,z))
                out[power]=out.get(power,0)+x*y
        return {power:value for power,value in out.items() if value}
    one={(0,0,0,0):1};tt={(0,0,0,1):1};d2={(0,2,0,0):1}
    xx={(1,0,0,0):1};dv={(0,1,1,0):-2}
    minus_t={(0,0,0,1):-1};cc=add(one,minus_t)
    lhs=add(mul(d2,xx),mul(cc,dv),mul(cc,cc),mul(d2,minus_t))
    rhs=add(mul(cc,add(xx,dv,d2,minus_t)),
            mul(add(d2,{(0,0,0,0):-1},tt),add(xx,{(0,0,0,0):-1})))
    assert lhs==rhs
    return {'status':'PASS','radius':str(R),'B':B,'halfside_multiplier':str(K),
            'scope':'Conditional globally normalized boundary envelope; no full covering exclusion',
            'required_center_norm_squared_upper':str(1-R*R),
            'reflection_polynomial_identity':'PASS',
            'displacement_factor_interval':[str(F(beta.l,S)),str(F(beta.u,S))],
            'penalty_numerator_derivative_lower':str(derivative),
            'penalty_numerator_endpoint_upper':str(endpoint),
            'variance_coefficient':str(CURVATURE),
            'good_arc_curvature_margin':str(F(good.l-q(CURVATURE).u,S)),
            'bad_arc_subintervals':len(points)-1,'endpoint_comparisons':len(margins),
            'minimum_bad_arc_margin':str(min(margins))}
if __name__=='__main__':print(json.dumps(verify(),indent=2))

"""Closed-form exact angle conjugates with rational Taylor remainders.

These are interchangeable scalar support implementations, not cached solver
answers. Every call encloses its value using the audited integer interval
type. Rare near-endpoint inputs fall back to concave root isolation.
"""
from functools import lru_cache
from verify_potential_star_duals import I,q,S,PI,sine,cosine,concave_maximum,score_envelope

def atan_positive(z):
    assert 0<=z.l<=z.u<=3*S//4
    n=32 if z.u<=S//2 else 80
    total=q(0);term=z;z2=z.sq()
    for k in range(n):
        total+=term/(2*k+1) if k%2==0 else -term/(2*k+1)
        term*=z2
    # n is even, so the next term is positive and the truncated series is
    # below atan(z). The alternating remainder is at most that next term.
    error=(term/(2*n+1)).u
    return total+I(0,error)

def atan_interval(z):
    if z.l>=0:return atan_positive(z)
    if z.u<=0:return -atan_positive(-z)
    v=atan_positive(I(0,max(-z.l,z.u)))
    return I(-v.u,v.u)

def acos_interval(x):
    assert -S<x.l<=x.u<S
    root=(q(1)-x.sq()).sqrt()
    half=x/(1+root)
    if max(abs(half.l),abs(half.u))>3*S//4:
        return None
    return PI/2-2*atan_interval(half)

def tangent_sine(angle,derivative=False):
    """Concave sine support extended by its slope -1 tangent after pi/2."""
    join=PI/2
    linear=-q(1) if derivative else join-angle
    if angle.l>=join.u:return linear
    exact=cosine(2*angle) if derivative else sine(2*angle)/2
    if angle.u<=join.l:return exact
    return I(min(exact.l,linear.l),max(exact.u,linear.u))

def root_sine_conjugate(t):
    if t.l>=S:return q(0)
    if t.u<=-S:return -t*PI/2
    return concave_maximum(lambda a:tangent_sine(a)-t*a,
                           lambda a:tangent_sine(a,True)-t,q(0),PI/2)

@lru_cache(maxsize=100000)
def sine_point(raw):
    t=I(raw)
    if raw>=S:return q(0)
    if raw<=-S:return -t*PI/2
    a=acos_interval(t)
    if a is None:return root_sine_conjugate(t)
    return ((q(1)-t.sq()).sqrt()-t*a)/2

def sine_conjugate(t):
    # H'(t)=-acos(t)/2 on (-1,1), with the matching endpoint branches.
    lower=sine_point(t.u);upper=sine_point(t.l)
    return I(lower.l,upper.u)

def root_marked_conjugate(t):
    return concave_maximum(lambda g:score_envelope(g)-t*g,
                           lambda g:score_envelope(g,True)-t,q(0),PI/2)

@lru_cache(maxsize=100000)
def marked_point(raw):
    assert -S//2<raw<3*S
    t=I(raw)
    y=(-1+(33+16*t).sqrt())/8
    assert 0<y.l<=y.u<S
    a=acos_interval(y)
    if a is None:return root_marked_conjugate(t)
    x=(q(1)-y.sq()).sqrt()
    return x*(1+2*y)-t*a

def marked_conjugate(t):
    assert -S//2<t.l<=t.u<3*S
    # A supremum of Gbar(g)-tg for g>=0 is decreasing in t.
    lower=marked_point(t.u);upper=marked_point(t.l)
    return I(lower.l,upper.u)

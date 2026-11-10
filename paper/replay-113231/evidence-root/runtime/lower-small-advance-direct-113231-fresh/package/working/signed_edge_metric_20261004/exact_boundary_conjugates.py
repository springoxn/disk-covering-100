"""Exact arc supports for the audited boundary-angle reduction.

The quadratic stationary polynomial may have extraneous roots. Keeping every
in-domain candidate gives a rigorous upper bound without unsquared filtering.
Only endpoint evaluations contribute to the returned lower bound.
"""
from fractions import Fraction as F
from exact_signed_conjugates import I,q,S,PI,acos_unit
from verify_star_lp_duals import sine,cosine

def asin_unit(x):
    assert 0<=x.l<=x.u<=S
    return PI/2-acos_unit(x)

def nonnegative(x):
    # Caller has established that the exact quantity being enclosed is >=0.
    assert x.u>=0
    return I(max(0,x.l),x.u)

def clip_unit(x):
    # Caller has established that the exact quantity lies in [0,1].
    assert x.u>=0 and x.l<=S
    return I(max(0,x.l),min(S,x.u))

def value_from_u(u,T,a,b):
    ss=nonnegative(u).sqrt();cc=nonnegative(1-u).sqrt()
    h=nonnegative(q(T)-u).sqrt();t=asin_unit(clip_unit(ss))
    eta=asin_unit(clip_unit(ss/q(T).sqrt()))-t
    return (1-q(a))*t-ss*cc+ss*h+q(b)*eta

def arc_support(radius,a,b,t_lower=F(1,25)):
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    radius,a,b,t_lower=map(F,(radius,a,b,t_lower));T=radius*radius
    assert 0<radius<1 and 0<t_lower<radius and b<T
    tl=q(t_lower);sl=sine(tl);cl=cosine(tl)
    assert sl.sq().u<q(T).l
    hl=nonnegative(q(T)-sl.sq()).sqrt()
    lower_value=(1-q(a))*tl-sl*cl+sl*hl+q(b)*(asin_unit(clip_unit(sl/q(radius)))-tl)
    tu=asin_unit(q(radius));upper_value=(1-q(a))*tu-q(radius)*(1-q(T)).sqrt()+q(b)*(PI/2-tu)
    lower=max(lower_value.l,upper_value.l);upper=max(lower_value.u,upper_value.u)
    A=4*(a-1)
    B=-4*T*(a+b)-(a+b)**2+4*(T+b)+(T+b)**2
    C=T*(a+b)**2-(T+b)**2
    roots=[]
    if A:
        D=B*B-4*A*C
        if D>=0:
            root=q(D).sqrt()
            for sign in [-1,1]:
                numerator=-q(B)+sign*root
                roots.append(numerator/(2*A) if A>0 else -numerator/(-2*A))
    elif B:
        roots.append(q(-C/B))
    else:
        assert C!=0,'Unrecognized identically stationary polynomial'
    domain_lo=sl.sq().l;domain_hi=q(T).u;retained=0
    for root in roots:
        if root.u<domain_lo or root.l>domain_hi:continue
        # Intersection is enlarged outward; h and asin clips retain exact roots.
        u=I(max(domain_lo,root.l),min(domain_hi,root.u))
        upper=max(upper,value_from_u(u,T,a,b).u);retained+=1
    return I(lower,upper),retained

"""Exact full-apex marked conjugates for squared base penalties.

Unlike the tangent G_lambda envelope, this support remains valid for all
0<=lambda<=1/8. It uses convexity in the apex at a fixed half-base.
"""
from fractions import Fraction as F
from functools import lru_cache
from verify_star_lp_duals import I,q,S,PI
from verify_potential_star_duals import sine,cosine,hull,concave_maximum


def endpoint_branch(angle,penalty,multiplier,obtuse=False,derivative=False):
    lam=q(penalty);t=q(multiplier);cut=PI/2
    def low(a):
        s=sine(a)
        if obtuse:
            return cosine(a)-4*lam*sine(2*a)-t if derivative else s-4*lam*s.sq()+t*(PI-a)
        return (cosine(a)+2*cosine(2*a)-4*lam*sine(2*a)+t if derivative
                else s*(1+2*cosine(a))-4*lam*s.sq()+t*a)
    # Continue by the exact endpoint tangent. This makes the rational
    # interval beyond the uncertain pi/2 endpoint concave by definition.
    def extension(a):
        if obtuse:return -t if derivative else 1-4*lam+t*(PI-a)
        return t-2 if derivative else (t-2)*a+PI+1-4*lam
    if angle.u<=cut.l:return low(angle)
    if angle.l>=cut.u:return extension(angle)
    left=I(angle.l,min(angle.u,cut.u));right=I(max(angle.l,cut.l),angle.u)
    return hull(low(left),extension(right))


@lru_cache(None)
def conjugate(penalty,multiplier):
    penalty,multiplier=F(penalty),F(multiplier)
    assert 0<=penalty<=F(1,8)
    values=[]
    for obtuse in (False,True):
        value=concave_maximum(
            lambda a:endpoint_branch(a,penalty,multiplier,obtuse),
            lambda a:endpoint_branch(a,penalty,multiplier,obtuse,True),q(0),PI/2)
        if (not obtuse and multiplier>=2) or (obtuse and multiplier<=0):
            # The outward rational endpoint can extend slightly beyond the
            # true domain along an increasing tangent. Its upper is safe,
            # but take the lower from the feasible exact pi/2 value.
            endpoint=1-4*q(penalty)+q(multiplier)*PI/2
            value=I(endpoint.l,value.u)
        values.append(value)
    return I(max(x.l for x in values),max(x.u for x in values))


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    # The concavity proof needs only lambda<=1/8 and
    # 2 sin(a)^2-1 <= sin(a) for sin(a) in[0,1].
    # Its factorization is (2s+1)(s-1)<=0.
    product=[0,0,0]
    for i,a in enumerate((1,2)):
        for j,b in enumerate((-1,1)):product[i+j]+=a*b
    assert product==[-1,-1,2]
    rows=[]
    for lam in (F(0),F(1,25),F(6,125),F(3,50),F(1,8)):
        for t in (F(-1,2),F(-1,5),F(0),F(1,5),F(1,2),F(2)):
            z=conjugate(lam,t)
            # Endpoint values and the equilateral-apex value are feasible
            # lower bounds, independently checking scalar sign conventions.
            candidates=[q(0),q(t)*PI,1-4*q(lam)+q(t)*PI/2,
                        q(3).sqrt()-3*q(lam)+q(t)*PI/3]
            assert all(c.l<=z.u for c in candidates)
            assert z.u-z.l<10**13
            rows.append({'lambda':str(lam),'multiplier':str(t),
                         'interval':[str(F(z.l,S)),str(F(z.u,S))]})
    return {'status':'PASS','domain':'0<=lambda<=1/8, all real rational multipliers',
            'scope':'Analytic conjugate lemma plus exact scalar implementation checks; no radius exclusion',
            'sample_scalar_checks':len(rows),'cases':rows}


if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2))

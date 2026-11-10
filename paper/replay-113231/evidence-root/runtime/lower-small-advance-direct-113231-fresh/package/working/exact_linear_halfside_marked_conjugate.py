"""Exact full-apex marked support with a linear half-side penalty.

All acceptance uses rational intervals. The parameter k is in [0,1].
"""
from fractions import Fraction as F
from functools import lru_cache
from verify_star_lp_duals import I,q,S,PI
from verify_potential_star_duals import sine,cosine,hull,concave_maximum


def branch(angle,k,multiplier,obtuse=False,derivative=False):
    kk=q(k);s=q(multiplier);cut=PI/2
    def low(a):
        if obtuse:
            return ((1-kk)*cosine(a)-s if derivative
                    else (1-kk)*sine(a)+s*(PI-a))
        return ((1-kk)*cosine(a)+2*cosine(2*a)+s if derivative
                else (1-kk)*sine(a)+sine(2*a)+s*a)
    def extension(a):
        if obtuse:return -s if derivative else 1-kk+s*(PI-a)
        return s-2 if derivative else (s-2)*a+PI+1-kk
    if angle.u<=cut.l:return low(angle)
    if angle.l>=cut.u:return extension(angle)
    left=I(angle.l,min(angle.u,cut.u))
    right=I(max(angle.l,cut.l),angle.u)
    return hull(low(left),extension(right))


@lru_cache(None)
def conjugate(k,multiplier):
    k,multiplier=F(k),F(multiplier)
    assert 0<=k<=1
    values=[]
    for obtuse in (False,True):
        value=concave_maximum(
            lambda a:branch(a,k,multiplier,obtuse),
            lambda a:branch(a,k,multiplier,obtuse,True),q(0),PI/2)
        if (not obtuse and multiplier>=2) or (obtuse and multiplier<=0):
            endpoint=1-q(k)+q(multiplier)*PI/2
            value=I(endpoint.l,value.u)
        values.append(value)
    return I(max(z.l for z in values),max(z.u for z in values))


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    from exact_quadratic_marked_conjugate import conjugate as quadratic
    results=[]
    for k in (F(0),F(6,25),F(1)):
        for s in (F(-1),F(-1,5),F(0),F(1,5),F(1,2),F(2)):
            value=conjugate(k,s)
            candidates=[q(0),q(s)*PI,1-q(k)+q(s)*PI/2,
                        q(3).sqrt()*(1-q(k)/2)+q(s)*PI/3]
            assert all(z.l<=value.u for z in candidates)
            assert value.u-value.l<10**13
            if k==0:
                other=quadratic(F(0),s)
                assert max(value.l,other.l)<=min(value.u,other.u)
            results.append({'k':str(k),'multiplier':str(s),
                            'interval':[str(F(value.l,S)),str(F(value.u,S))]})
    return {'status':'PASS','domain':'0<=k<=1, all real rational apex multipliers',
            'scope':'Full-apex scalar support only; no covering exclusion',
            'sample_checks':len(results),'cases':results}


if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2))

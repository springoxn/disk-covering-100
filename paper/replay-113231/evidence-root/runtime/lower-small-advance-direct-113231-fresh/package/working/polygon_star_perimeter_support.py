"""Recovered exact helper for the audited complete-star polygon theorem.

The formulas are unchanged. This recovered source has its own hash and
must not be represented as the lost byte-identical original file.
"""
from fractions import Fraction as F
from functools import lru_cache
from verify_star_lp_duals import I,q,S,PI
from verify_potential_star_duals import sine,cosine


@lru_cache(maxsize=10000)
def constants(degree):
    assert isinstance(degree,int) and degree>=3
    angle=2*PI/degree
    sd=degree*sine(angle)*(1+cosine(angle))
    td=degree*sine(angle)
    return sd,td


def support(degree,a,b):
    a,b=F(a),F(b)
    assert a>=0
    sd,td=constants(degree)
    value=q(a)*sd+q(b)*td
    return I(max(0,value.l),max(0,value.u))


def verify():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    cases=[]
    sd3,td3=constants(3);radical=3*q(3).sqrt()/4
    assert max(sd3.l,radical.l)<=min(sd3.u,radical.u)
    for degree in range(3,100):
        sd,td=constants(degree)
        assert sd.l>0 and td.l>0
        for a,b in ((F(1),F(0)),(F(1),F(-1,5)),(F(1),F(-7,10)),
                    (F(1),F(-13,10)),(F(0),F(1)),(F(0),F(-1))):
            z=support(degree,a,b)
            direct=q(a)*sd+q(b)*td
            assert z.l==max(0,direct.l) and z.u==max(0,direct.u)
            assert z.l>=0 and z.l<=z.u
            cases.append({'degree':degree,'area_weight':str(a),'perimeter_weight':str(b),
                          'interval':[str(F(z.l,S)),str(F(z.u,S))]})
    assert len(cases)==582
    return {'status':'PASS','sample_supports':len(cases),
            'source_identity':'recovered equivalent formulas; new source hash',
            'scope':'Exact local polygon-star scalar support only; no global covering threshold',
            'cases':cases}


if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2))

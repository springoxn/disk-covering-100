#!/usr/bin/env python3
"""Exact rational dual replay for the acute interior-star relaxation.

Conditional B=33 certificate, not by itself a universal radius lower bound.
The input coefficients were proposed numerically, but every accepted inequality
and final margin is recomputed using exact outward-rounded integer intervals.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import time
from math import isqrt

S = 10**24


class I:
    def __init__(self, lo, hi=None):
        self.l, self.u = int(lo), int(lo if hi is None else hi)
        assert self.l <= self.u

    def __add__(a, z):
        z = z if isinstance(z, I) else q(z)
        return I(a.l+z.l, a.u+z.u)

    __radd__ = __add__

    def __neg__(a):
        return I(-a.u, -a.l)

    def __sub__(a, z):
        return a+-(z if isinstance(z, I) else q(z))

    def __rsub__(a, z):
        return q(z)+-a

    def __mul__(a, z):
        z = z if isinstance(z, I) else q(z)
        values = [a.l*z.l, a.l*z.u, a.u*z.l, a.u*z.u]
        return I(min(values)//S, -((-max(values))//S))

    __rmul__ = __mul__

    def __truediv__(a, z):
        z = z if isinstance(z, I) else q(z)
        assert z.l > 0
        values = [F(a.l*S, z.l), F(a.l*S, z.u), F(a.u*S, z.l), F(a.u*S, z.u)]
        low, high = min(values), max(values)
        return I(low.numerator//low.denominator, -((-high.numerator)//high.denominator))

    def sq(a):
        low = 0 if a.l <= 0 <= a.u else min(a.l*a.l, a.u*a.u)
        high = max(a.l*a.l, a.u*a.u)
        return I(low//S, -((-high)//S))

    def sqrt(a):
        assert a.l >= 0
        low, high = isqrt(a.l*S), isqrt(a.u*S)
        high += high*high < a.u*S
        assert low*low <= a.l*S and high*high >= a.u*S
        return I(low, high)


def q(value):
    value = F(value)
    return I(value.numerator*S//value.denominator,
             -((-value.numerator*S)//value.denominator))


def atan_bounds(denominator, terms=40):
    x = F(1, denominator)
    total = sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(terms)), F(0))
    other = total+(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(total, other), max(total, other)


al, ah = atan_bounds(5)
bl, bh = atan_bounds(239)
PI = I(q(16*al-4*bh).l, q(16*ah-4*bl).u)
assert 3*S < PI.l < PI.u < q(F(22, 7)).u
A = 3*q(3).sqrt()/4
C = q(F(17, 25))
R = q(F(2261, 20000))
R2 = R.sq()
B, INTERIOR, FACES = 33, 67, 165
TYPES = [(p, j) for p in range(4) for j in range(5-p, 12-p)]
TRIG = {}


def point_trig(x, cosine=False):
    assert 0 <= x <= 3*S
    key = (x, cosine)
    if key in TRIG:
        return TRIG[key]
    z = I(x)
    z2 = z.sq()
    term = q(1) if cosine else z
    out = term
    for j in range(1, 25):
        denominator = (2*j-1)*(2*j) if cosine else (2*j)*(2*j+1)
        term = term*z2/denominator
        out += -term if j % 2 else term
    denominator = 49*50 if cosine else 50*51
    remainder = term*z2/denominator
    result = I(out.l-remainder.u, out.u+remainder.u)
    TRIG[key] = result
    return result


def sine(z):
    assert 0 <= z.l <= z.u <= 11*S//10  # below pi/2, hence increasing
    return I(point_trig(z.l).l, point_trig(z.u).u)


def cosine(z):
    assert 0 <= z.l <= z.u <= 22*S//10  # below pi, hence decreasing
    return I(point_trig(z.u, True).l, point_trig(z.l, True).u)


def hull(a, c):
    return I(min(a.l, c.l), max(a.u, c.u))


def score_envelope(gamma, derivative=False):
    cut = PI/3
    if derivative:
        linear = q(F(-1, 2))
        trig = lambda z: cosine(z)+2*cosine(2*z)
    else:
        linear = q(3).sqrt()-(gamma-cut)/2
        trig = lambda z: sine(z)*(1+2*cosine(z))
    if gamma.l >= cut.u:
        return linear
    if gamma.u <= cut.l:
        return trig(gamma)
    # The two expressions agree at pi/3; retain both around its tiny enclosure.
    return hull(linear, trig(gamma))


def maximum_star_score(p, j, eta):
    target = 2*PI-j*PI/3
    if p == 0:
        return -C*target.sq()/j

    def value(gamma):
        return p*score_envelope(gamma)-C*(target-p*gamma).sq()/j+eta*p*gamma

    def derivative(gamma):
        return p*(score_envelope(gamma, True)+2*C*(target-p*gamma)/j+eta)

    left, right = 0, (PI/2).u
    d0 = derivative(I(left))
    if d0.u <= 0:
        return value(I(left))
    dend = derivative(PI/2)
    if dend.l >= 0:
        return value(PI/2)
    for _ in range(100):
        middle = (left+right)//2
        dm = derivative(I(middle))
        if dm.l > 0:
            left = middle
        elif dm.u < 0:
            right = middle
        else:
            # A concave-function tangent gives a global upper bound even when
            # the derivative sign is numerically unresolved by the enclosure.
            vm = value(I(middle))
            error = q(F(max(abs(dm.l), abs(dm.u)), S))*(PI/2)
            return I(vm.l, (vm+error).u)
        if right-left < S//10**13:
            return value(I(left, right))
    raise ValueError('Unresolved concave scalar maximum')


def verify_rows(rows):
    assert [v['N'] for v in rows] == list(range(11, 95))
    transition_margin = (q(3).sqrt()-PI/30-(5+2*q(5).sqrt()).sqrt()/2).l
    endpoint_margin = (q(3).sqrt()-PI/12-(1+q(2).sqrt())/2).l
    assert transition_margin > 0 and endpoint_margin > 0
    mu = 2*PI/B
    s = sine(mu/2)
    h = (R2-s.sq()).sqrt()
    boundary_term = s*h+(mu-sine(mu))/2
    results = []
    smallest = None
    start = time.time()
    for row in rows:
        n, den = row['N'], row['denominator']
        eta, u0, u1, u2, v = [q(F(row[k], den)) for k in ('eta', 'u0', 'u1', 'u2', 'v')]
        assert v.l >= 0
        least_dual_slack = None
        for p, j in TYPES:
            upper = maximum_star_score(p, j, eta).u
            dual = u0+u1*p+u2*j+(v if p else 0)
            slack = dual.l-upper
            assert slack > 0, ('Scalar dual inequality failed', n, p, j, F(slack, S))
            least_dual_slack = slack if least_dual_slack is None else min(least_dual_slack, slack)
        dual_value = INTERIOR*u0+B*u1+(3*(FACES-B)-n)*u2+n*v
        angular_value = dual_value-eta*(n+6)*PI/3+n*eta.sq()/(4*C)
        upper_area = R2*((FACES-B)*A+angular_value)+B*boundary_term
        margin = PI.l-upper_area.u
        assert margin > 0, ('Final area exclusion failed', n, F(margin, S))
        smallest = (margin, n) if smallest is None or margin < smallest[0] else smallest
        results.append({'N': n, 'scalar_inequalities': len(TYPES),
                        'minimum_dual_slack': str(F(least_dual_slack, S)),
                        'area_margin': str(F(margin, S))})
    return {'status': 'PASS', 'radius': '2261/20000', 'B': B,
            'N_range': [11, 94], 'types': TYPES, 'case_count': len(rows),
            'scalar_inequality_count': len(rows)*len(TYPES),
            'tightest_N': smallest[1], 'minimum_area_margin': str(F(smallest[0], S)),
            'envelope_transition_margin': str(F(transition_margin, S)),
            'envelope_endpoint_margin': str(F(endpoint_margin, S)),
            'seconds_reporting_only': time.time()-start, 'cases': results,
            'scope': 'Conditional on the separately proved acute, chordless B=33 structure and variance coefficient17/25. Not alone a universal lower bound.'}


def main():
    data = json.loads(Path(__file__).with_name('star_dual_proposals.json').read_text())
    assert data['types'] == [list(z) for z in TYPES]
    result = verify_rows(data['rows'])
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    main()

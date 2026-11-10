#!/usr/bin/env python3
"""Exact face-potential star certificate for the B33 branch at r=.11307.

The geometric .11307 premises are required separately. The finite rational
dual replay, concave splice and scalar maxima use no floating acceptance.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import time
from verify_star_lp_duals import I, q, S, PI, score_envelope

K = q(F(1, 2))
CENTER = PI/3
JOIN = q(F(11483, 10000))
ANGLE_MAX = PI/2+q(F(1, 25))
R = q(F(11307, 100000))
R2 = R.sq()
TYPES = [(p, j) for p in range(4) for j in range(4-p, 12-p)]
TRIG = {}


def point_trig(x, cosine=False):
    assert 0 <= x <= 4*S
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
    remainder = term*z2/(49*50 if cosine else 50*51)
    result = I(out.l-remainder.u, out.u+remainder.u)
    TRIG[key] = result
    return result


def sine(z):
    assert 0 <= z.l <= z.u <= 4*S
    a, b = point_trig(z.l), point_trig(z.u)
    lo, hi = min(a.l, b.l), max(a.u, b.u)
    peak = PI/2
    if z.l <= peak.u and z.u >= peak.l:
        hi = S
    # On [0,4], sine has this single maximum and no minimum.
    return I(lo, hi)


def cosine(z):
    assert 0 <= z.l <= z.u <= 4*S
    a, b = point_trig(z.l, True), point_trig(z.u, True)
    lo, hi = min(a.l, b.l), max(a.u, b.u)
    if z.l <= PI.u and z.u >= PI.l:
        lo = -S
    return I(lo, hi)


def positive_part(value):
    return I(max(value.l, 0), max(value.u, 0))


def negative_part(value):
    return I(min(value.l, 0), min(value.u, 0))


def potential(angle):
    delta = angle-CENTER
    return sine(2*angle)/2+K*(positive_part(delta).sq()-negative_part(delta).sq()/2)


def potential_derivative(angle):
    delta = angle-CENTER
    return cosine(2*angle)+2*K*positive_part(delta)-K*negative_part(delta)


JOIN_VALUE = potential(JOIN)
JOIN_SLOPE = potential_derivative(JOIN)


def hull(a, b):
    return I(min(a.l, b.l), max(a.u, b.u))


def envelope(angle, derivative=False):
    linear = JOIN_SLOPE if derivative else JOIN_VALUE+JOIN_SLOPE*(angle-JOIN)
    if angle.l >= JOIN.u:
        return linear
    value = potential_derivative(angle) if derivative else potential(angle)
    if angle.u <= JOIN.l:
        return value
    return hull(value, linear)


def validate_envelope():
    assert CENTER.u < JOIN.l
    assert sine(2*JOIN).l > K.u
    tail_cos = cosine(I(2*JOIN.l, 2*ANGLE_MAX.u))
    assert tail_cos.u < 0  # F'''=-4cos(2a)>0 on the positive-branch tail.
    margin = (JOIN_VALUE+JOIN_SLOPE*(ANGLE_MAX-JOIN)-potential(ANGLE_MAX)).l
    assert margin > 0
    return margin


def concave_maximum(value, derivative, lower, upper):
    left, right = lower.l, upper.u
    assert 0 <= left <= right
    if derivative(I(left)).u <= 0:
        return value(I(left))
    if derivative(I(right)).l >= 0:
        return value(I(right))
    for _ in range(100):
        middle = (left+right)//2
        dm = derivative(I(middle))
        if dm.l > 0:
            left = middle
        elif dm.u < 0:
            right = middle
        else:
            vm = value(I(middle))
            error = q(F(max(abs(dm.l), abs(dm.u)), S))*q(F(right, S))
            return I(vm.l, (vm+error).u)
        if right-left < S//10**13:
            return value(I(left, right))
    raise ValueError('Unresolved concave scalar maximum')


def maximum_star(p, j, eta):
    if p == 0:
        return j*envelope(2*PI/j)
    candidate = (2*PI-j*ANGLE_MAX)/p
    lower = I(max(0, candidate.l), max(0, candidate.u))
    upper = PI/2
    assert lower.l <= upper.u

    def value(gamma):
        mean = (2*PI-p*gamma)/j
        return p*score_envelope(gamma)+j*envelope(mean)+eta*p*gamma

    def derivative(gamma):
        mean = (2*PI-p*gamma)/j
        return p*(score_envelope(gamma, True)-envelope(mean, True)+eta)

    return concave_maximum(value, derivative, lower, upper)


def boundary_conjugate(eta):
    return concave_maximum(lambda angle: envelope(angle)-eta*angle,
                           lambda angle: envelope(angle, True)-eta,
                           q(0), ANGLE_MAX)


def verify_rows(rows):
    assert [z['N'] for z in rows] == list(range(11, 96))
    splice_margin = validate_envelope()
    mu = 2*PI/33
    s = sine(mu/2)
    h = (R2-s.sq()).sqrt()
    boundary_term = s*h+(mu-sine(mu))/2
    results, smallest = [], None
    start = time.time()
    for row in rows:
        n, denominator = row['N'], row['denominator']
        eta, u0, u1, u2, v, w = [q(F(row[k], denominator)) for k in ('eta', 'u0', 'u1', 'u2', 'v', 'w')]
        assert v.l >= 0 and w.l >= 0
        least_slack = None
        for p, j in TYPES:
            bound = maximum_star(p, j, eta).u
            dual = u0+p*u1+j*u2+(v if p else 0)+(w if p+j == 4 else 0)
            slack = dual.l-bound
            assert slack > 0, ('Scalar dual failed', n, p, j, F(slack, S))
            least_slack = slack if least_slack is None else min(least_slack, slack)
        dual_value = 67*u0+33*u1+(396-n)*u2+n*v+w
        normalized = dual_value+n*boundary_conjugate(eta)-2*PI*eta
        upper_area = R2*normalized+33*boundary_term
        margin = PI.l-upper_area.u
        assert margin > 0, ('Area exclusion failed', n, F(margin, S))
        smallest = (margin, n) if smallest is None or margin < smallest[0] else smallest
        results.append({'N': n, 'scalar_inequalities': len(TYPES),
                        'minimum_dual_slack': str(F(least_slack, S)),
                        'area_margin': str(F(margin, S))})
    return {'status': 'PASS', 'radius': '11307/100000', 'B': 33,
            'potential_coefficient': '1/2', 'splice': '11483/10000',
            'maximum_q0_angle': 'pi/2+1/25', 'splice_endpoint_margin': str(F(splice_margin, S)),
            'N_range': [11, 95], 'case_count': 85,
            'scalar_inequality_count': len(TYPES)*85,
            'tightest_N': smallest[1], 'minimum_area_margin': str(F(smallest[0], S)),
            'seconds_reporting_only': time.time()-start, 'cases': results,
            'scope': 'Conditional B33 proof, requiring the separate .11307 no-three-boundary-face, degree and angle premises. Other B cases are independent.'}


def main():
    data = json.loads(Path(__file__).with_name('potential_star_dual_proposals.json').read_text())
    assert data['types'] == [list(z) for z in TYPES]
    print(json.dumps(verify_rows(data['rows']), indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    main()

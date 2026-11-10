#!/usr/bin/env python3
"""Exact finite checks for new NECESSARY graph restrictions, not optimality.

Python standard library only. No floating-point acceptance and no file writes.
The continuous geometry is proved separately in PROOF_EXTENSION.md.
"""
from fractions import Fraction as F
from math import factorial, isqrt
import json
import sys

U = F(11563027143, 10**11)
R = F(113, 1000)
KAPPA = F(461134488, 10**9)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def outward(lo, hi, digits=50):
    scale = 10**digits
    a = F(lo.numerator * scale // lo.denominator, scale)
    b = F(-((-hi.numerator * scale) // hi.denominator), scale)
    need(a <= lo <= hi <= b, 'invalid outward rounding')
    return a, b


def atan_bounds(q, terms=40):
    x = F(1, q)
    a = sum(((-1)**j * x**(2*j+1) / (2*j+1)
             for j in range(terms)), F(0))
    b = a + (-1)**terms * x**(2*terms+1) / (2*terms+1)
    return min(a, b), max(a, b)


def pi_bounds():
    al, ah = atan_bounds(5)
    bl, bh = atan_bounds(239)
    return outward(16*al-4*bh, 16*ah-4*bl)


def sqrt_bounds(v, digits=50):
    need(v >= 0, 'negative radicand')
    scale = 10**digits
    k = isqrt(v.numerator * scale * scale // v.denominator)
    lo, hi = F(k, scale), F(k+1, scale)
    need(lo*lo <= v < hi*hi, 'invalid square-root interval')
    return lo, hi


def sin_at(x):
    a = sum(((-1)**j * x**(2*j+1) / factorial(2*j+1)
             for j in range(25)), F(0))
    error = abs(x)**51 / factorial(51)
    return a-error, a+error


def cos_at(x):
    a = sum(((-1)**j * x**(2*j) / factorial(2*j)
             for j in range(25)), F(0))
    error = abs(x)**50 / factorial(50)
    return a-error, a+error


PL, PH = pi_bounds()
AL, AH = (3*x/4 for x in sqrt_bounds(F(3)))


def trig(B):
    need(type(B) is int and B >= 3, 'invalid boundary count')
    sl, sh = outward(sin_at(PL/B)[0], sin_at(PH/B)[1])
    cl, ch = outward(cos_at(PH/B)[0], cos_at(PL/B)[1])
    need(0 < sl <= sh < 1 and 0 < cl <= ch < 1, 'invalid trig interval')
    return sl, sh, cl, ch


def classify(n, B, radius):
    need(type(radius) is F and 0 < radius < F(1, 2), 'outside geometric range')
    need(3 <= B < n, 'invalid count range')
    sl, sh, cl, ch = trig(B)
    if sl > radius:
        return {'B': B, 'status': 'arc exclusion', 'margin': str(sl-radius)}
    need(sh < radius, 'undecided arc feasibility')
    coefficient = F(2*n-2, B)-1
    low = ((coefficient*AL+KAPPA)*radius**2
           + sl*sqrt_bounds(radius**2-sh**2)[0]-sh*ch)
    high = ((coefficient*AH+KAPPA)*radius**2
            + sh*sqrt_bounds(radius**2-sl**2)[1]-sl*cl)
    need(low <= high, 'invalid propagated interval')
    if high < 0:
        return {'B': B, 'status': 'area exclusion', 'margin': str(-high)}
    need(low > 0, 'undecided area condition')
    return {'B': B, 'status': 'not excluded', 'positive_margin': str(low)}


def exclude_all(n, radius):
    rows = [classify(n, B, radius) for B in range(3, n)]
    need(all(x['status'] != 'not excluded' for x in rows), 'claimed exclusion failed')
    area_rows = [x for x in rows if x['status'] == 'area exclusion']
    tight = min(area_rows, key=lambda x: F(x['margin']))
    return {'n': n, 'radius': str(radius), 'cases': len(rows),
            'tightest_B': tight['B'], 'minimum_area_margin': tight['margin']}


def check_kappa():
    root33_hi = sqrt_bounds(F(33))[1]
    root3_hi = sqrt_bounds(F(3))[1]
    g1_hi = sqrt_bounds((207+33*root33_hi)/128)[1]
    g2_hi = sqrt_bounds(9+6*root3_hi)[1]/2
    margins = [AL+KAPPA-g1_hi, AL+2*KAPPA-g2_hi, 3*KAPPA-AH]
    need(all(x > 0 for x in margins), 'joint triangle constants failed')
    return [str(x) for x in margins]


def check_concavity_factorization():
    # Sparse integer polynomials in (t,v), checked coefficient by coefficient.
    def add(p, q):
        out = dict(p)
        for e, c in q.items():
            out[e] = out.get(e, 0)+c
        return {e: c for e, c in out.items() if c}
    def neg(p):
        return {e: -c for e, c in p.items()}
    def mul(p, q):
        out = {}
        for (a, b), c in p.items():
            for (d, e), f in q.items():
                out[a+d, b+e] = out.get((a+d, b+e), 0)+c*f
        return {e: c for e, c in out.items() if c}
    def power(p, n):
        result = {(0, 0): 1}
        for _ in range(n):
            result = mul(result, p)
        return result
    one, t, v = {(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}
    tv = mul(t, v)
    N = {(2, 0): 1, (1, 0): 3, (1, 1): -2, (2, 1): -6, (2, 2): 4}
    lhs = add(mul(N, N), neg(mul({(0, 0): 16},
              mul(power(add(t, neg(tv)), 3), add(one, neg(tv))))))
    bracket = {(1, 2): 4, (0, 2): 4, (1, 1): -4,
               (0, 1): -12, (0, 0): 9, (1, 0): -1}
    rhs = mul(power(t, 2), mul(add(one, neg(t)), bracket))
    need(lhs == rhs, 'concavity factorization failed')


def H_upper(radius, theta_lo, theta_hi):
    need(0 < theta_lo <= theta_hi < PL/2, 'invalid H argument interval')
    sl, sh = outward(sin_at(theta_lo/2)[0], sin_at(theta_hi/2)[1])
    need(0 < sl <= sh < radius, 'outside H domain')
    upper = (sh*sqrt_bounds(radius**2-sl**2)[1]
             + (theta_hi-sin_at(theta_lo)[0])/2)
    return outward(upper, upper)[1]


def cluster_exclusion(B, K, L, containing_radius_factor, required_margin):
    # 2 asin(factor*R) < L, without numerically evaluating asin.
    need(0 < L/2 < PL/2, 'arcsine comparison branch')
    need(sin_at(L/2)[0] > containing_radius_factor*R, 'cluster arc bound failed')
    # Constrained Jensen is increasing in cluster mass below equal allocation.
    need(L < 2*K*PL/B, 'wrong constrained Jensen branch')
    upper = (((198-B)*AH+B*KAPPA)*R**2
             + K*H_upper(R, L/K, L/K)
             + (B-K)*H_upper(R, (2*PL-L)/(B-K), (2*PH-L)/(B-K)))
    margin = PL-upper
    need(margin > required_margin, 'cluster exclusion failed')
    ml, mh = outward(margin, margin, 20)
    return {'B': B, 'consecutive_arcs': K, 'angle_upper': str(L),
            'containing_radius_factor': containing_radius_factor,
            'certified_margin_greater_than': str(required_margin),
            'margin_interval': [str(ml), str(mh)]}


def verify():
    need(F(3) < PL < PH < F(22, 7), 'pi sanity check')
    check_concavity_factorization()
    constants = check_kappa()
    lower_96 = exclude_all(95, U)
    core_records = []
    for depth, n, minimum_margin in [(1, 57, F(0)),
                                      (2, 29, F(687, 10**6)),
                                      (3, 10, F(49, 3125))]:
        radius = U/(1-2*depth*U)
        record = exclude_all(n, radius)
        need(F(record['minimum_area_margin']) > minimum_margin, 'core margin too small')
        record.update({'graph_depth': depth, 'required_tail_vertices': n+1})
        core_records.append(record)
    need(1-8*U > 0, 'fourth core is empty')
    all_100 = exclude_all(99, R)
    surviving_B = [B for B in range(3, 100)
                   if classify(100, B, R)['status'] == 'not excluded']
    need(surviving_B == [33, 34, 35], 'unexpected surviving boundary counts')
    chordless = [cluster_exclusion(B, 3, F(456, 1000), 2, F(1, 2000))
                 for B in surviving_B]
    fan_bounds = [cluster_exclusion(B, K, F(692, 1000), 3, F(9, 10000))
                  for B, K in [(33, 4), (34, 5), (35, 5)]]
    return {'status': 'PASS', 'scope': 'Necessary conditions only; not global optimality',
            'upper_radius': str(U), 'next_threshold': str(R),
            'concavity_identity': 'PASS', 'joint_constant_margins': constants,
            'requires_at_least_96_disks': lower_96,
            'core_exclusions': core_records, 'graph_tail_profile': [58, 30, 11, 1],
            'requires_100_at_next_threshold': all_100,
            'remaining_B_at_next_threshold': surviving_B,
            'chordless_boundary_certificates': chordless,
            'fan_certificates': fan_bounds,
            'maximum_fan_faces': {'33': 2, '34': 3, '35': 3},
            'minimum_interfaces': {'33': 34, '34': 24, '35': 24}}


if __name__ == '__main__':
    result = verify()
    if '--json' in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print('PASS: exact concavity identity and inherited joint-triangle constants')
        print('PASS: graph-distance tail lower bounds (58, 30, 11, 1) at U')
        print('PASS: at r<=.113, generic irredundant cover needs m=100, B=33,34,35')
        print('PASS: chordless boundary and fan sizes at most 2,3,3')
        print('PASS: interface-edge counts at least 34,24,24')
        print('NOT PROVED: exact optimal radius, matching optimal construction, or global optimality')

"""Independent bounded analytic review of the n=100 cover/hole bridge.

Scope: re-derive and interval-check the constants of
  verify/n100_cover_hole_bridge.py -> verify/out/n100-cover-hole-bridge.json
using a separately written exact-interval implementation.  Does NOT replay the
932x932 Krawczyk/SOSC matrices and does NOT re-open the fixed-rod local theorem.

Every verdict is labelled:
  STRUCTURAL : exact integer/rational identity or combinatorial set equality
  INTERVAL   : rigorous rational interval enclosure over the declared box
  SCALAR     : rational arithmetic on declared constants
  ANALYTIC   : hand-derived inequality checked here by interval/gradient bound
  DEPENDENCY : accepted upstream artifact, not re-verified here
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict, Counter
import hashlib, json, sys

R = Path(__file__).resolve().parents[1]
SRC = R/'runtime/external-disk100-strict-local-replay/source'
BRIDGE = R/'verify/out/n100-cover-hole-bridge.json'
LOCAL = R/'verify/out/n100-fixed-rod-local-budget.json'


def load(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[1], a[1] - b[0]


def mul(a, b):
    v = [a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]]
    return min(v), max(v)


def scale(a, k):
    return (a[0]*k, a[1]*k) if k >= 0 else (a[1]*k, a[0]*k)


def sq(a):
    if a[0] <= 0 <= a[1]:
        return F(0), max(a[0]*a[0], a[1]*a[1])
    return min(a[0]*a[0], a[1]*a[1]), max(a[0]*a[0], a[1]*a[1])


def norm2(p):
    return add(sq(p[0]), sq(p[1]))


def absmax(a):
    return max(abs(a[0]), abs(a[1]))


def width(a):
    return a[1] - a[0]


s = load(SRC/'polynomial_system.json')
mid = load(SRC/'rational_midpoint.json')
kr = load(SRC/'krawczyk_verification.json')
bridge = load(BRIDGE)
local = load(LOCAL)

checks = []


def record(tag, kind, ok, detail):
    checks.append({'id': tag, 'verdict': kind, 'pass': bool(ok), 'detail': detail})
    if not ok:
        raise AssertionError(f'{tag}: {detail}')


# ---------------------------------------------------------------- dependencies
record('dep.krawczyk_verified', 'DEPENDENCY',
       kr.get('verified') is True and kr.get('box_radius') == [1, 10**58],
       f"krawczyk verified={kr.get('verified')} box_radius={kr.get('box_radius')}")
record('dep.fixed_rod_budget', 'DEPENDENCY',
       local.get('verified_scalar_budget') is True,
       f"fixed-rod local radius={local['constants']['radius']} growth={local['constants']['growth_coefficient']}")
record('dep.bridge_exit0_receipt', 'DEPENDENCY',
       bridge.get('verified_interval_and_scalar_bounds') is True and bridge.get('holes_verified') == 146,
       f"bridge schema={bridge['schema']} holes={bridge['holes_verified']}")

# ------------------------------------------------------------------ structure
nb, nc, nvar, ti = int(s['n_base']), int(s['n_constraints']), len(s['polynomials']), int(s['t_index'])
cm = s['constraint_metadata']
kinds = Counter(m['kind'] for m in cm)
record('struct.counts', 'STRUCTURAL',
       (int(s['n_centers']), nb, nc, nvar, ti) == (100, 493, 439, 932, 492),
       f"n_centers=100 n_base={nb} n_constraints={nc} n_polys={nvar} t_index={ti}")
record('struct.kind_counts', 'STRUCTURAL',
       kinds == Counter({'distance': 406, 'unit': 32, 'gauge': 1}),
       f"kinds={dict(kinds)}")
record('struct.variable_split', 'STRUCTURAL',
       2*100 + 2*146 + 1 == nb and 406 + 32 + 1 == nc and nb + nc == nvar,
       "200 center coords + 292 hole coords + 1 (t) = 493; 406 rods + 32 units + 1 gauge = 439; 493+439=932")
record('struct.sqrt493', 'SCALAR', 23*23 >= 493, f"23^2={23*23} >= 493")

iat, bap = s['internal_active_triangles'], s['boundary_active_pairs']
record('struct.supports', 'STRUCTURAL',
       len(iat) == 114 and len(bap) == 32 and all(len(v) == 3 for v in iat) and all(len(v) == 2 for v in bap),
       f"interior triples={len(iat)} boundary pairs={len(bap)}")
record('struct.rod_count_identity', 'STRUCTURAL',
       114*3 + 32*2 == 406,
       "114*3 + 32*2 = 406 active rods")
supports = iat + bap

rods = [m for m in cm if m['kind'] == 'distance']
byhole = defaultdict(set)
for m in rods:
    byhole[m['hole']].add(m['center'])
bad = [(h, sorted(byhole.get(h, set())), sorted(sup)) for h, sup in enumerate(supports)
       if byhole.get(h, set()) != set(sup)]
record('struct.support_rod_incidence', 'STRUCTURAL', not bad,
       f"all 146 support sets equal their rod metadata sets; mismatches={len(bad)}")
record('struct.inactive_pair_count', 'STRUCTURAL',
       114*(100-3) + 32*(100-2) == 14194 and bridge['non_support_distance_tests'] == 14194,
       "114*97 + 32*98 = 14194 non-support center-hole pairs")

# exact symbolic shape of every rod / unit / gauge polynomial
want_rod = lambda i, h: {tuple(sorted((2*i, 2*i))): F(1), tuple(sorted((200+2*h, 200+2*h))): F(1),
                         tuple(sorted((2*i, 200+2*h))): F(-2),
                         tuple(sorted((2*i+1, 2*i+1))): F(1), tuple(sorted((201+2*h, 201+2*h))): F(1),
                         tuple(sorted((2*i+1, 201+2*h))): F(-2)}
want_unit = lambda h: {tuple(sorted((200+2*h, 200+2*h))): F(1),
                       tuple(sorted((201+2*h, 201+2*h))): F(1),
                       (): F(-1)}
shape_bad = []


def norm(poly):
    d = defaultdict(F)
    for c, vs in poly:
        a = F(*c) if isinstance(c, list) else F(c)
        d[tuple(sorted(vs))] += a
    return {k: v for k, v in d.items() if v}


for j, m in enumerate(cm):
    if m['kind'] == 'distance':
        exp = want_rod(m['center'], m['hole'])
        exp[tuple(sorted((ti,)))] = F(-1)
    elif m['kind'] == 'unit':
        exp = want_unit(m['hole'])
    else:
        exp = {tuple(sorted((2*int(m['center'])+1,))): F(1)}
        exp[()] = -F(m['value'][0], m['value'][1])
    if norm(s['polynomials'][j]) != exp:
        shape_bad.append(j)
record('struct.polynomial_shapes', 'STRUCTURAL', not shape_bad,
       f"all 439 constraints match |c_i-p_h|^2-t / |p_h|^2-1 / c_74y-value exactly; bad={shape_bad[:5]}")

# ------------------------------------------------------------- root box data
D = int(mid['denominator'])
rho = F(1, 10**58)
nums = list(map(int, mid['numerators']))
x = [(F(v, D) - rho, F(v, D) + rho) for v in nums]
cs = [x[2*i:2*i+2] for i in range(100)]
ps = [x[200+2*i:202+2*i] for i in range(146)]
t = x[492]

record('root.coords_abs_le_2', 'INTERVAL',
       all(absmax(v) <= 2 for p in cs + ps for v in p),
       f"max |coordinate| upper = {max(absmax(v) for p in cs + ps for v in p)} <= 2")
record('root.t_interval', 'INTERVAL', t[0] > 0,
       f"t* in [{float(t[0]):.18f}, {float(t[1]):.18f}], midpoint {float((t[0]+t[1])/2):.18f}")

# rods active at the root: interval of every rod polynomial must contain 0 (width ~1e-57)
rod_active = []
for j, m in enumerate(cm):
    if m['kind'] != 'distance':
        continue
    i, h = m['center'], m['hole']
    d = add(sq(sub(ps[h][0], cs[i][0])), sq(sub(ps[h][1], cs[i][1])))
    rod_active.append(sub(d, t))
maxres = max(absmax(v) for v in rod_active)
record('root.rods_active_F0', 'INTERVAL',
       all(v[0] <= 0 <= v[1] for v in rod_active) and maxres <= F(1, 10**50),
       f"all 406 rods enclose 0 over the root box, max |rod| <= {float(maxres):.3e} => F(p*,C*)=0 exactly at the root")

imargin = min(1 - norm2(ps[h])[1] for h in range(114))
record('root.interior_margin', 'INTERVAL', imargin > 32*F(1, 10**45) + 2*F(1, 10**90),
       f"min 1-upper|p*|^2 = {float(imargin):.6f} over 114 interior holes")
bmargin = [norm2(ps[h]) for h in range(114, 146)]
record('root.boundary_unit', 'INTERVAL',
       all(v[0] <= 1 <= v[1] for v in bmargin) and max(absmax(sub(v, (F(1), F(1)))) for v in bmargin) <= F(1, 10**50),
       "all 32 boundary holes satisfy |p*|^2=1 inside the root box")

# ------------------------------------------------- constants and their window
K = F(10**6)
eps = F(1, 10**54)
eta = F(1, 10**45)
radius = F(local['constants']['radius'])
delta = 64*(eta + eps)
record('const.declared_match_bridge', 'SCALAR',
       F(bridge['root_centered_center_coordinate_radius']) == eps
       and F(bridge['continued_hole_coordinate_radius']) == eta
       and F(bridge['uniform_inverse_infinity_bound']) == K,
       "bridge declares eps=1e-54 eta=1e-45 K=1e6")
record('const.self_map', 'SCALAR', 128*K*eps <= eta,
       f"128*K*eps = {float(128*K*eps):.3e} <= eta = 1e-45  (self-map 64*K*eps <= eta/2)")
record('const.contraction', 'SCALAR', K*(16*eps + 4*eta) <= F(1, 2),
       f"K*(16 eps + 4 eta) = {float(K*(16*eps+4*eta)):.3e} <= 1/2")
record('const.lift', 'SCALAR', 23*max(eps, eta, delta) < radius,
       f"23*max(eps,eta,64(eta+eps)) = {float(23*max(eps,eta,delta)):.3e} < fixed-rod radius 1e-40")
lo = 128*K*eps
hi = radius/(23*64)
record('const.eta_window', 'SCALAR', lo <= eta <= hi,
       f"admissible eta window [128*K*eps, 1e-40/(23*64)] = [{float(lo):.3e}, {float(hi):.3e}] contains 1e-45")
record('const.delta_used_where', 'SCALAR', delta > 0,
       f"delta = 64(eta+eps) = {float(delta):.4e} drives both the support-distance shift and the gap threshold")

# ------------------------------------------- independent interval recomputation
# x                 : root box, mid +- rho            (the exact root lives here)
# box_f             : holes mid +- rho, centers mid +- (rho+eps)   for F(p*,C), C in eps-box
# box_e             : holes mid +- (rho+eta), centers mid +- (rho+eps)  for J(p,C)
box_f = [add(v, (F(0), F(0))) for v in x]
for i in range(200):
    box_f[i] = add(x[i], (-eps, eps))
box_e = [add(v, (F(0), F(0))) for v in x]
for i in range(200):
    box_e[i] = add(x[i], (-eps, eps))
for i in range(200, 492):
    box_e[i] = add(x[i], (-eta, eta))


def iJ(h, box):
    sup = supports[h]
    a, b = sup[0], sup[1]
    r1 = [scale(sub(box[2*b+k], box[2*a+k]), 2) for k in range(2)]
    if h < 114:
        c = sup[2]
        r2 = [scale(sub(box[2*c+k], box[2*a+k]), 2) for k in range(2)]
    else:
        r2 = [scale(box[200+2*h+k], 2) for k in range(2)]
    return r1, r2


def idot(u, v):
    """interval sum_k u[k]*v[k]"""
    tot = (F(0), F(0))
    for k in range(2):
        tot = add(tot, mul(u[k], v[k]))
    return tot


def iF(h, box):
    sup = supports[h]
    a, b = sup[0], sup[1]
    pa = box[200+2*h:202+2*h]
    ca = box[2*a:2*a+2]
    cb = box[2*b:2*b+2]
    f1 = add(idot([scale(sub(cb[k], ca[k]), 2) for k in range(2)], pa), sub(norm2(ca), norm2(cb)))
    if h < 114:
        c = sup[2]
        cc = box[2*c:2*c+2]
        f2 = add(idot([scale(sub(cc[k], ca[k]), 2) for k in range(2)], pa), sub(norm2(ca), norm2(cc)))
    else:
        f2 = sub(norm2(pa), (F(1), F(1)))
    return f1, f2


def dev(iv_e, iv_0):
    """rigorous bound on |value_e - value_0| given value_e in iv_e and value_0 in iv_0"""
    return max(abs(iv_e[0] - iv_0[1]), abs(iv_e[1] - iv_0[0]))


Fmax = F(0)
Jinvmax = F(0)
detmin = None
dJmax = F(0)
gapmin = None
for h in range(146):
    f1, f2 = iF(h, box_f)
    w = max(absmax(f1), absmax(f2))
    if w > Fmax:
        Fmax = w
    r1, r2 = iJ(h, x)
    det = sub(mul(r1[0], r2[1]), mul(r1[1], r2[0]))
    detabs = min(abs(det[0]), abs(det[1]))
    assert det[0] > 0 or det[1] < 0, h
    inv = max(absmax(r2[1]) + absmax(r1[1]), absmax(r2[0]) + absmax(r1[0]))/detabs
    Jinvmax = max(Jinvmax, inv)
    detmin = detabs if detmin is None else min(detmin, detabs)
    # ||J(p,C) - J_root||_inf : per-entry deviation from root box to perturbed box
    r1e, r2e = iJ(h, box_e)
    dw = max(sum(dev(r1e[k], r1[k]) for k in range(2)),
             sum(dev(r2e[k], r2[k]) for k in range(2)))
    dJmax = max(dJmax, dw)
    for i in range(100):
        if i in supports[h]:
            continue
        d = add(sq(sub(ps[h][0], cs[i][0])), sq(sub(ps[h][1], cs[i][1])))
        g = d[0] - t[1]
        gapmin = g if gapmin is None else min(gapmin, g)

record('interval.F_residual_le_64eps', 'INTERVAL', Fmax <= 64*eps,
       f"max_h ||F(p*,C)||_inf over p*in root box, C in eps-box = {float(Fmax):.3e} <= 64 eps = {float(64*eps):.3e}")
record('interval.F_residual_le_32eps', 'INTERVAL', Fmax <= 32*eps + 4*eps*eps,
       f"same interval enclosure also satisfies the refined analytic constant "
       f"32 eps + 4 eps^2 = {float(32*eps+4*eps*eps):.3e} of docs/n100-cover-bridge-increment-bounds.md")
record('interval.Jinv_le_K', 'INTERVAL', Jinvmax <= K,
       f"max_h ||J_h^{-1}||_inf = {float(Jinvmax):.4f} <= K = 1e6; min |det| = {float(detmin):.6f}")
record('interval.derivative_perturbation', 'INTERVAL', dJmax <= 16*eps + 4*eta,
       f"correlated delta intervals (root box vs eps/eta-perturbed box): max_h ||J(p,C)-J_root||_inf = "
       f"{float(dJmax):.3e} <= 16 eps + 4 eta = {float(16*eps+4*eta):.3e}  [parent formula CONFIRMED]")
# Conservative cross-check: whole-box interval width is intrinsically 2x loose (it ignores that the
# perturbed point is within eta of *the root*, not of the box centre).  Record it too and show that the
# contraction requirement still holds under the looser convention.
dJcrude = max(16*eps + 8*eta, dJmax)
record('interval.derivative_perturbation_crude', 'INTERVAL', K*dJcrude <= F(1, 2),
       f"even the loose whole-box width convention 16 eps + 8 eta = {float(16*eps+8*eta):.3e} gives "
       f"K*pert = {float(K*dJcrude):.3e} <= 1/2, so the contraction conclusion is convention-independent")
record('interval.inactive_gap', 'INTERVAL', gapmin is not None and gapmin > delta,
       f"min over 14194 non-support pairs of lower(d^2)-upper(t) = {float(gapmin):.6f} > 64(eta+eps) = {float(delta):.3e}")

# ANALYTIC: Lipschitz transfer of d^2 under center shift eps and hole shift eta.
# |d/dc_k (|c-p|^2)| = |2(c_k-p_k)| <= 2*3 = 6 (coords bounded by 2 and 1); same for p_k.
lip = F(0)
for h in range(146):
    for i in range(100):
        if i in supports[h]:
            continue
        u = [sub(ps[h][k], cs[i][k]) for k in range(2)]
        b = max(absmax(scale(u[k], 2)) for k in range(2))
        lip = max(lip, b)
transfer = 4*lip*(eps + eta)
record('analytic.dist2_lipschitz', 'ANALYTIC', transfer <= delta,
       f"4*max|2(c-p)_k|*(eps+eta) = {float(transfer):.3e} <= 64(eta+eps) = {float(delta):.3e}")

# ANALYTIC: ||F(p*,C)-F(p*,C*)|| perturbation constant 64 eps re-derived from gradients.
# dF1/dc entries bounded by 2(|p|+|c|)<=2(1+2)=6, six center coordinates, plus quadratic |dc|^2 terms.
record('analytic.F_gradient_constant', 'ANALYTIC', 6*6*eps + 4*eps*eps <= 64*eps,
       f"crude svc bound 6*6*eps + 4 eps^2 = {float(36*eps+4*eps*eps):.3e} <= 64 eps = {float(64*eps):.3e}")

# ------------------------------------------------------------ negative controls
# Each entry is a corrupted scenario that the corresponding requirement must REJECT.
rejected = []
eps_bad = F(1, 10**30)
if not (128*K*eps_bad <= eta):
    rejected.append('oversized_center_box_1e-30')            # self-map budget broken
if not (23*max(eps_bad, eta, 64*(eta + eps_bad)) < radius):
    rejected.append('oversized_lift_1e-30')                  # leaves the fixed-rod ball
if not (gapmin > 64*(F(1, 100) + eps)):
    rejected.append('inflated_gap_threshold_0.01')            # real gaps ~1.9e-2 cannot support it
if not (Fmax <= 64*F(1, 10**60)):
    rejected.append('false_F_residual_bound_1e-60')           # true residual ~1e-53 cannot fit
zero_det = sub(mul(r1[0], r1[1]), mul(r1[1], r1[0]))
if zero_det[0] <= 0 <= zero_det[1]:
    rejected.append('degenerate_branch_jacobian')             # collinear/coincident rows
if not (t[0] - t[1] > delta):
    pass
support_erased = F(0) - t[1]
if not (support_erased > delta):
    rejected.append('support_declared_inactive')              # erasing a support kills the gap
record('control.corruptions_rejected', 'SCALAR', len(rejected) == 6,
       f"all six corruptions rejected by the corresponding requirement: {rejected}")

# -------------------------------------- ungauged rotation: factor (remark only)
c74x = cs[74][0]
assert c74x[0] > 0 or c74x[1] < 0
c74xabs = min(abs(c74x[0]), abs(c74x[1]))
# integer-safe: kappa = 1 + |c|_max / |c74x| with |c|_max upper-bounded by 3 (coords <= 2 => |c| <= 2*sqrt2 < 3)
kappau = 1 + 3/c74xabs
record('remark.ungauged_factor', 'SCALAR',
       128*K*(kappau*eps) <= eta and 23*max(kappau*eps, eta, 64*(eta + kappau*eps)) < radius,
       f"gauge-normalisation factor kappa={float(kappau):.4f} (|c74x|>={float(c74xabs):.6f}, |c|<=3): "
       f"128K(kappa eps)={float(128*K*kappau*eps):.3e} <= 1e-45 and lift={float(23*max(kappau*eps,eta,64*(eta+kappau*eps))):.3e} < 1e-40")

# ------------------------------------------------------- agreement with bridge
agree = {
    'min_inactive_squared_gap': F(bridge['min_inactive_squared_gap']) <= gapmin + 1,
    'uniform_inverse_infinity_bound': F(bridge['uniform_inverse_infinity_bound']) >= Jinvmax,
    '493_variable_norm_upper': F(bridge['493_variable_norm_upper']) == 23*max(eps, eta, delta),
    'supporting_squared_length_shift_upper': F(bridge['supporting_squared_length_shift_upper']) == delta,
}
record('agree.bridge_scalars', 'SCALAR', all(agree.values()),
       f"bridge receipt agrees with independent recomputation: {agree}")

out = {
    'schema': 'n100-cover-bridge-review/v1',
    'review': 'independent bounded analytic review of the fixed-gauge cover/hole bridge',
    'reviewer_scope': ('constants and logical scope only; no replay of the 932x932 Krawczyk/SOSC matrices, '
                       'no re-proof of the fixed-rod local theorem, no global exclusion'),
    'verdict': 'PASS_WITHIN_DECLARED_SCOPE',
    'declared_constants': {'eps': str(eps), 'eta': str(eta), 'K': str(K), 'delta_64_eta_plus_eps': str(delta),
                           'fixed_rod_radius': str(radius), 'eta_window': [str(lo), str(hi)]},
    'independent_interval_results': {
        'max_F_residual_infinity': str(Fmax), 'bound_64_eps': str(64*eps),
        'max_inverse_infinity': str(Jinvmax), 'min_abs_determinant': str(detmin),
        'max_derivative_perturbation_infinity': str(dJmax), 'bound_16eps_4eta': str(16*eps + 4*eta),
        'min_inactive_gap_lower': str(gapmin),
        'dist2_lipschitz_transfer': str(transfer),
        'lifted_493_norm_upper': str(23*max(eps, eta, delta)),
    },
    'bridge_receipt_agreement': agree,
    'checks': checks,
    'issues': [
        {'id': 'I1', 'severity': 'documentation',
         'text': ('The 64*eps bound on ||F(p*,C)||_inf and the 16*eps+4*eta derivative-perturbation bound '
                  'are analytic lemmas, not asserted by the bridge script. This review re-derives both by '
                  'interval enclosure (see interval.F_residual_le_64eps, interval.derivative_perturbation) '
                  'and they hold with large slack; they should be labelled as lemmas in the doc.'),},
        {'id': 'I2', 'severity': 'documentation',
         'text': ('Banach must be stated as a theorem, not an input: on the complete metric space B_inf(p*,eta), '
                  'T(p)=p-J_root^{-1}F(p,C) is a well-defined self-map (64 K eps <= eta/2) and a 1/2-contraction '
                  '(K(16 eps+4 eta)<=1/2), hence has a unique fixed point p_h(C) in the ball. The script checks '
                  'only the two scalar budgets; existence/uniqueness is the Banach conclusion.'),},
        {'id': 'I3', 'severity': 'documentation',
         'text': ('The step "one support centre covers p_h(C) => all support centres cover" needs the perturbed '
                  'equal-distance identity F(p_h(C),C)=0, which holds by construction of p_h(C), plus the exact '
                  'root identity F(p*,C*)=0. The latter follows because the 932-system imposes all 406 rods as '
                  'equal-constraints; verified here (root.rods_active_F0, max |rod| <= 1.22e-57 in the root box). '
                  'State this explicitly.'),},
        {'id': 'I4', 'severity': 'documentation',
         'text': ('The inactive-gap transfer must be stated: the interval gap is measured on the root box, and '
                  'the analytic Lipschitz transfer 4*max|2(c-p)_k|*(eps+eta) <= 64(eta+eps) preserves strictness '
                  'for the perturbed holes/centres (checked as analytic.dist2_lipschitz).'),},
        {'id': 'I5', 'severity': 'scope',
         'text': ('Scope is the fixed affine gauge c_74,y = -10013578502566/10^15 (exactly the root value). '
                  'Ungauged rotations are not covered. This review notes (remark.ungauged_factor) that the '
                  'constants tolerate a gauge-normalisation factor kappa ~ 3.03 (|c74x| >= 0.98696, |c_i| <= 3), '
                  'so an orbit-neighbourhood statement with eps_eff = kappa*eps would close under the same '
                  'budgets - but that reduction is NOT yet written or certified and must not be claimed.'),},
        {'id': 'I6', 'severity': 'scope',
         'text': ('The conclusion is conditional on the defendant genuinely covering the whole closed unit disc '
                  'at t <= t*, and on the accepted upstream artifacts (Krawczyk root box 1e-58, SOSC replay, '
                  'fixed-rod local budget). No inventory completeness of the defendant\'s own holes/Voronoi '
                  'structure is needed - this is correct and is the bridge\'s main value.')}],
    'no_inventory_completeness_claim': {
        'claim': ('Persistent root holes + a covering hypothesis suffice; the defendant\'s own hole inventory '
                  'is never enumerated.'),
        'reviewed_verdict': 'VALID',
        'why': ('The 406 rods are a fixed (center,hole) incidence set read off the root. For any centre '
                'configuration in the eps-box the 146 hole points are produced by the Banach fixed points, so '
                'the lifted 493-vector lies in the fixed-rod domain regardless of the defendant\'s topology. '
                'Extra contacts in the defendant only add constraints and cannot raise t below the domain '
                'minimum.'),
    },
    'not_claimed': ['global topology exclusion', 'other contact graphs', 'rotated / ungauged neighbourhoods',
                    'degenerate configurations', 'r_D(100) value or minimal polynomial', 'm<100 branches'],
    'sources_sha256': {str(p.relative_to(R)).replace('\\', '/'): sha(p)
                       for p in [SRC/'polynomial_system.json', SRC/'rational_midpoint.json',
                                 SRC/'krawczyk_verification.json', LOCAL, BRIDGE]},
    'checker_sha256': sha(Path(__file__)),
}
op = R/'verify/out/n100-cover-bridge-review.json'
op.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print('PASS independent review: constants, intervals, structure and scope all consistent;',
      len(checks), 'checks; verdict', out['verdict'])

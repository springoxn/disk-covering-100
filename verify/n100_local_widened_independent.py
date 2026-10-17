"""Independent exact scalar audit of the widened n100 fixed-rod LOCAL certificate.

Target
------
    verify/n100_local_widened_budget.py  ->  verify/out/n100-local-widened-budget.json

Design
------
* Standalone: Python standard library only, exact ``Fraction`` arithmetic.  No
  floating point value ever decides a check; ``Decimal`` appears only in the
  display-only ``diagnostics`` block.
* Independent: the parent budget script is never imported, exec'd or shelled
  out.  Every constant is re-derived here from the raw source receipts
  (``replay_verification.json``, ``polynomial_system.json``,
  ``rational_midpoint.json``, ``krawczyk_verification.json``), and the 146 hole
  Jacobian inverse bounds, inactive squared-distance gaps and interior unit
  margins are *recomputed from the source polynomials* instead of being read
  from the bridge receipt.  The bridge receipt is then used only as the thing
  to agree with.
* Bounded: no 932x932 or 54x54 replay, no CAS.  146 2x2 interval Jacobians plus
  439 row-l1 derivative bounds; runs in seconds.
* The analytic lemmas behind the chain (Banach continuation of the 146 holes,
  rotation gauge slice, augmented-Lagrangian local exclusion, the exact
  quadratic Taylor split) are *consumed* from already reviewed receipts, bound
  by sha256.  They are not re-proved here and this script does not claim to.

Scope
-----
LOCAL only, fixed affine gauge, root-centred labelled neighbourhood.  Global
optimality, the other contact graphs, the 87 families, the universal lower
bound and the minimal polynomial all remain open.

Exit status 0 means: the widened certificate's constants are valid bounds on
the true-root quantities (as re-derived here), its scalar chain is
arithmetically valid, its dependency hashes match the files on disk, and its
negative controls (augmented here by the required wrong-R controls) are
genuinely rejected.
"""
from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time

getcontext().prec = 60

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'runtime/external-disk100-strict-local-replay'
SRCD = SRC / 'source'

PARENT_SCRIPT = ROOT / 'verify/n100_local_widened_budget.py'
PARENT_RECEIPT = ROOT / 'verify/out/n100-local-widened-budget.json'
OUT = ROOT / 'verify/out/n100-local-widened-independent.json'

REPLAY = SRC / 'replay_verification.json'
BRIDGE = ROOT / 'verify/out/n100-cover-hole-bridge.json'
BRIDGE_REVIEW = ROOT / 'verify/out/n100-cover-bridge-review.json'
AUGMENTED = ROOT / 'verify/out/n100-local-augmented-audit.json'
DUAL = ROOT / 'verify/out/n100-first-order-rod-dual.json'
POLYS = SRCD / 'polynomial_system.json'
MIDPOINT = SRCD / 'rational_midpoint.json'
KRAWCZYK = SRCD / 'krawczyk_verification.json'
SOURCE_BINDING = SRC / 'SOURCE_BINDING.json'
UPSTREAM_MANIFEST = SRC / 'UPSTREAM_MANIFEST_SHA256.json'


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return str(Path(p).resolve().relative_to(ROOT)).replace('\\', '/')


def qf(pair):
    """Exact Fraction from a [numerator, denominator] receipt entry."""
    return F(int(pair[0]), int(pair[1]))


def dec(fr):
    """Display only -- never used in a decision."""
    return str(+(Decimal(fr.numerator) / Decimal(fr.denominator)))


def ratio(a, b):
    """Exact ratio a/b (display only)."""
    return dec(F(a) / F(b))


def isqrt_floor(fr):
    """Exact floor(sqrt(fr)) for fr >= 0, integer arithmetic only."""
    assert fr >= 0
    n, d = fr.numerator, fr.denominator
    r = math.isqrt(n // d)
    while (r + 1) * (r + 1) * d <= n:
        r += 1
    while r * r * d > n:
        r -= 1
    return r


# interval arithmetic on closed rational intervals (a0 <= a1)
def iv_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def iv_sub(a, b):
    return (a[0] - b[1], a[1] - b[0])


def iv_scale(a, k):
    return (a[0] * k, a[1] * k) if k >= 0 else (a[1] * k, a[0] * k)


def iv_mul(a, b):
    v = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (min(v), max(v))


def iv_sq(a):
    lo = F(0) if a[0] <= 0 <= a[1] else min(a[0] * a[0], a[1] * a[1])
    hi = max(a[0] * a[0], a[1] * a[1])
    return (lo, hi)


def iv_absmax(a):
    return max(abs(a[0]), abs(a[1]))


# --------------------------------------------------------------------------
# 0. upstream gates and the root box
# --------------------------------------------------------------------------
t_start = time.time()
findings = []

replay = load(REPLAY)
bridge = load(BRIDGE)
bridge_review = load(BRIDGE_REVIEW)
augmented = load(AUGMENTED)
dual = load(DUAL)
psys = load(POLYS)
mid = load(MIDPOINT)
kraw = load(KRAWCZYK)
source_binding = load(SOURCE_BINDING)

assert replay['verified'] is True, 'replay not verified'
assert augmented['audit_verified'] is True, 'augmented audit not verified'
assert bridge_review['verdict'] == 'PASS_WITHIN_DECLARED_SCOPE', 'bridge review not PASS'
assert bridge['verified_interval_and_scalar_bounds'] is True, 'bridge receipt not verified'
assert dual['verified'] is True, 'dual receipt not verified'
assert kraw['verified'] is True, 'krawczyk receipt not verified'

# root enclosure radius, taken from the accepted Krawczyk receipt (not hardcoded)
assert kraw['box_radius'] == [1, 10 ** 58], kraw['box_radius']
RHO = F(1, 10 ** 58)

nbase = int(replay['n_base'])
ncon = int(replay['n_constraints'])
assert nbase == 493 and ncon == 439
assert int(psys['n_base']) == nbase and int(psys['n_constraints']) == ncon
assert int(psys['n_variables']) == len(mid['numerators'])
assert int(psys['t_index']) == nbase - 1

D = int(mid['denominator'])
assert len(mid['numerators']) >= nbase
x = [F(int(v), D) for v in mid['numerators'][:nbase]]
xint = [(v - RHO, v + RHO) for v in x]
T_IV = xint[int(psys['t_index'])]

ncent = int(psys['n_centers'])
assert 2 * ncent == 200


def point_iv(i):
    return (xint[2 * i], xint[2 * i + 1])


def hole_iv(h):
    return (xint[2 * ncent + 2 * h], xint[2 * ncent + 2 * h + 1])


# --------------------------------------------------------------------------
# 1. independent re-derivation of the true-root constant bounds
# --------------------------------------------------------------------------
b = replay['exact_bounds']

# H : ||H(z*)||_2 <= ||H(z*)||_inf <= midpoint_inf + root_perturbation
H_ub = qf(b['hessian_midpoint_infinity_norm']) + qf(b['hessian_root_perturbation_infinity_bound'])

# Z : ||Z(z*)||_2^2 <= ||Z||_inf ||Z^T||_inf <= (z+dz)(z^T+dz^T)
Z2_ub = ((qf(b['null_basis_midpoint_infinity_norm']) + qf(b['null_basis_error_infinity_bound']))
         * (qf(b['null_basis_midpoint_transpose_infinity_norm'])
            + qf(b['null_basis_error_transpose_infinity_bound'])))

# R : ||B^-1||_2 <= sqrt(ncon) ||B^-1||_inf  (the sqrt(ncon) route, not ncon)
Binf = qf(b['pivot_inverse_infinity_bound'])
R2_req = ncon * Binf * Binf

# mu : lambda_min(Z^T H Z) >= (1 - total_residual) / (||W||_inf ||W^T||_inf)
numerator = 1 - qf(b['transformed_total_identity_residual'])
mu_lb = numerator / (qf(b['cholesky_transform_infinity_norm'])
                     * qf(b['cholesky_transform_transpose_infinity_norm']))

# alpha : the distance-multiplier lower bound, cross-checked across two receipts
alpha_dual = F(dual['minimum_alpha_lower_bound'])
alpha_aug = F(augmented['constants']['alpha_min'])
assert alpha_dual == alpha_aug, (alpha_dual, alpha_aug)
alpha_src = alpha_dual


# --------------------------------------------------------------------------
# 2. Jacobian Frobenius bound, re-derived from the source polynomials
# --------------------------------------------------------------------------
# two independent code paths on the same raw monomials:
#   route A: product of per-variable maxima  prod (|mid_k| + rho)
#   route B: exact interval product over the root box, max abs taken at the end
def jacobian_rows_route_a():
    rows = []
    for poly in psys['polynomials'][:ncon]:
        row = [F(0)] * nbase
        for c, vs in poly:
            coeff = abs(F(*c) if isinstance(c, list) else F(c))
            for i, j in enumerate(vs):
                val = coeff
                for ii, v in enumerate(vs):
                    if ii != i:
                        val *= abs(x[v]) + RHO
                row[j] += val
        rows.append(sum(row))
    return rows


def jacobian_rows_route_b():
    rows = []
    for poly in psys['polynomials'][:ncon]:
        row = [F(0)] * nbase
        for c, vs in poly:
            coeff = abs(F(*c) if isinstance(c, list) else F(c))
            for i, j in enumerate(vs):
                iv = (coeff, coeff)
                for ii, v in enumerate(vs):
                    if ii != i:
                        iv = iv_mul(iv, xint[v])
                row[j] += iv_absmax(iv)
        rows.append(sum(row))
    return rows


rows_a = jacobian_rows_route_a()
rows_b = jacobian_rows_route_b()
J2_a = sum(v * v for v in rows_a)
J2_b = sum(v * v for v in rows_b)
assert J2_b <= J2_a, 'interval route must not be looser than the product route'
J_least_int = isqrt_floor(J2_a) + 1          # least integer J with J^2 > J2_a
J_least_int_interval = isqrt_floor(J2_b) + 1  # least integer J valid on route B

# q : ||Q(h)||_2 <= sqrt(ncon) * 2 ||h||^2  (disjoint-block quadratic bound)
q2_req = 4 * ncon


# --------------------------------------------------------------------------
# 3. the 146 holes recomputed from source (bridge receipt only for agreement)
# --------------------------------------------------------------------------
internal = [list(t) for t in psys['internal_active_triangles']]
boundary = [list(p) for p in psys['boundary_active_pairs']]
supports = internal + boundary
nholes = len(supports)
nint = len(internal)
assert 2 * ncent + 2 * nholes + 1 == nbase, '493 = 2*100 + 2*146 + 1'
assert nholes == int(bridge['holes_verified'])
assert nholes == len(bridge['holes'])

# the declared incidence set is read back independently from the constraint metadata
meta = psys['constraint_metadata']
assert len(meta) == ncon
holes_meta = {}
units_meta = []
gauge_meta = None
for e in meta:
    if e['kind'] == 'distance':
        holes_meta.setdefault(int(e['hole']), []).append(int(e['center']))
    elif e['kind'] == 'unit':
        units_meta.append(int(e['hole']))
    else:
        gauge_meta = e
assert gauge_meta is not None and gauge_meta['kind'] == 'gauge'
assert len(holes_meta) == nholes
assert all(sorted(set(v)) == sorted(s) for s, v in
           ((s, holes_meta[h]) for h, s in enumerate(supports)))
assert units_meta == list(range(nint, nholes)), 'unit rows must be the boundary holes in order'
assert len(units_meta) == len(boundary) == 32
assert all(len(holes_meta[h]) == (3 if h < nint else 2) for h in range(nholes))

# gauge row: pins one coordinate of one center; recover the pinned variable, the
# root target and the rotation pivot straight from the source polynomial
assert gauge_meta['center'] == int(psys['gauge_center'])
gauge_poly = psys['polynomials'][ncon - 1]
gauge_terms = [(F(*c) if isinstance(c, list) else F(c), list(vs)) for c, vs in gauge_poly]
var_terms = [(c, vs) for c, vs in gauge_terms if vs]
const_terms = [(c, vs) for c, vs in gauge_terms if not vs]
assert len(var_terms) == 1 and len(var_terms[0][1]) == 1 and len(const_terms) == 1, \
    'gauge row must be affine in exactly one coordinate'
gauge_coeff, gauge_var = var_terms[0][0], var_terms[0][1][0]
gauge_target = -const_terms[0][0] / gauge_coeff        # root value of the pinned coordinate
assert gauge_coeff == 1
assert gauge_var == 2 * gauge_meta['center'] + (1 if gauge_meta['coordinate'] == 'y' else 0)
pivot_var = 2 * gauge_meta['center'] + (0 if gauge_meta['coordinate'] == 'y' else 1)
assert xint[pivot_var][1] < 0, 'gauge pivot x-coordinate must be negative on the root box'
pivot_abs_lb = -xint[pivot_var][1]                       # |x| >= this on the root box
assert abs(gauge_target - x[gauge_var]) <= RHO

# per-hole interval Jacobian, inverse-infinity bound, inactive gap, unit margin
hole_rows = []
inv_max = F(0)
det_min = None
gap_min = None
margin_min = None
agree = {'inverse': 0, 'gap': 0, 'margin': 0, 'support': 0, 'kind': 0}
for h, centers in enumerate(supports):
    a, bx = centers[0], centers[1]
    ca, cb = point_iv(a), point_iv(bx)
    row1 = [iv_scale(iv_sub(cb[k], ca[k]), 2) for k in range(2)]
    ph = hole_iv(h)
    if h < nint:
        assert len(centers) == 3
        cc = point_iv(centers[2])
        row2 = [iv_scale(iv_sub(cc[k], ca[k]), 2) for k in range(2)]
        margin = 1 - (iv_sq(ph[0])[1] + iv_sq(ph[1])[1])
    else:
        assert len(centers) == 2
        row2 = [iv_scale(v, 2) for v in ph]
        margin = None
    det = iv_sub(iv_mul(row1[0], row2[1]), iv_mul(row1[1], row2[0]))
    assert det[0] > 0 or det[1] < 0, ('degenerate branch Jacobian', h, det)
    detabs = min(abs(det[0]), abs(det[1]))
    det_min = detabs if det_min is None else min(det_min, detabs)
    inv = max(iv_absmax(row2[1]) + iv_absmax(row1[1]),
              iv_absmax(row2[0]) + iv_absmax(row1[0])) / detabs
    inv_max = max(inv_max, inv)

    gmin = None
    for i in range(ncent):
        if i in centers:
            continue
        ci = point_iv(i)
        d2 = iv_add(iv_sq(iv_sub(ph[0], ci[0])), iv_sq(iv_sub(ph[1], ci[1])))
        g = d2[0] - T_IV[1]
        if gmin is None or g < gmin:
            gmin = g
    assert gmin is not None and gmin > 0, ('inactive gap must be positive', h)
    gap_min = gmin if gap_min is None else min(gap_min, gmin)
    if margin is not None:
        margin_min = margin if margin_min is None else min(margin_min, margin)

    # agreement with the bridge receipt it is audited against
    brow = bridge['holes'][h]
    agree['support'] += int(brow['support_centers'] == centers)
    agree['kind'] += int(brow['kind'] == ('interior' if h < nint else 'boundary'))
    agree['inverse'] += int(F(brow['inverse_infinity_upper']) == inv)
    agree['gap'] += int(F(brow['inactive_squared_distance_gap_lower']) == gmin)
    if margin is None:
        agree['margin'] += int(brow['interior_unit_margin_lower'] is None)
    else:
        agree['margin'] += int(brow['interior_unit_margin_lower'] is not None
                               and F(brow['interior_unit_margin_lower']) == margin)
    hole_rows.append({'hole': h, 'kind': 'interior' if h < nint else 'boundary',
                      'inverse_infinity_upper': str(inv),
                      'inactive_squared_distance_gap_lower': str(gmin),
                      'interior_unit_margin_lower': None if margin is None else str(margin)})

assert all(v == nholes for v in agree.values()), agree
assert gap_min == F(bridge['min_inactive_squared_gap']), 'bridge min gap disagrees'
assert margin_min == F(bridge['min_interior_unit_margin']), 'bridge min margin disagrees'
assert inv_max == max(F(v['inverse_infinity_upper']) for v in bridge['holes']), \
    'bridge max inverse-infinity disagrees'

# --------------------------------------------------------------------------
# 4. the scalar chain, as a reusable predicate (declared constants *and* controls)
# --------------------------------------------------------------------------
CENTER_COORD_MAX = max(abs(x[v]) + RHO for i in range(ncent) for v in (2 * i, 2 * i + 1))


def chain(H, Z, RR, mu, J, q, kappa, m, radius, K, eps, eta, ungauged, alpha,
          gap_lb, margin_lb):
    """Return (violated-condition ids, diagnostics) for one candidate constant tuple.

    The first block re-checks that each declared constant really dominates the
    bound derived here for the true-root quantity it names; the second block is
    the arithmetic chain of the reviewed proof note.
    """
    bad = []
    if not H_ub <= H:
        bad.append('H_dominates_derived_root_hessian_bound')
    if not Z2_ub <= Z * Z:
        bad.append('Z_dominates_derived_2norm_squared_bound')
    if not R2_req <= RR * RR:
        bad.append('R_dominates_derived_right_inverse_2norm_bound')
    if not mu_lb >= mu:
        bad.append('mu_below_derived_reduced_curvature_bound')
    if not J2_a <= J * J:
        bad.append('J_below_derived_frobenius_jacobian_bound')
    if not q2_req <= q * q:
        bad.append('Q_below_derived_quadratic_remainder_bound')
    if not alpha_src >= alpha:
        bad.append('alpha_not_certified_by_source_receipts')
    if not inv_max <= K:
        bad.append('K_below_recomputed_146_hole_inverse_bounds')

    Kyoung = 2 * H * H * Z * Z * RR * RR / mu + H * RR * RR
    if not 2 * kappa - Kyoung >= 1:
        bad.append('young_2kappa_minus_K_ge_1')
    if not (m <= mu / (4 * Z * Z) and m <= 1 / (2 * RR * RR)):
        bad.append('m_within_reduced_coordinate_bounds')
    if not 2 * kappa * J * q * radius <= m / 4:
        bad.append('local_radius_linear_term')
    if not kappa * (J * radius + 2 * radius * radius) <= alpha:
        bad.append('local_radius_alpha_band')
    if not gap_lb > 64 * (eta + eps):
        bad.append('inactive_gap_dominates_rod_shift')
    if not margin_lb > 32 * eta + 2 * eta * eta:
        bad.append('interior_unit_margin_dominates_shift')
    if not 23 * max(eps, eta, 64 * (eta + eps)) < radius:
        bad.append('493_variable_lift_inside_local_radius')
    if not 128 * K * eps <= eta:
        bad.append('banach_self_map_forcing_128K_eps_le_eta')
    if not K * (16 * eps + 4 * eta) <= F(1, 2):
        bad.append('banach_contraction_K_16eps_4eta_le_half')
    if not CENTER_COORD_MAX + ungauged <= 2:
        bad.append('centre_coordinate_box_le_2')
    if not pivot_abs_lb - ungauged >= F(9, 10):
        bad.append('gauge_pivot_abs_ge_9over10')
    theta = 2 * (ungauged + RHO)
    if not F(9, 10) * (1 - theta * theta / 2) - 2 * theta > F(1, 2):
        bad.append('gauge_rotation_derivative_dominates')
    if not (ungauged + RHO) + 2 * theta + theta * theta < eps:
        bad.append('rotation_normalized_inside_fixed_gauge_box')
    return bad, Kyoung


# --------------------------------------------------------------------------
# 5. dependency-link integrity across the whole local certificate chain
# --------------------------------------------------------------------------
link_problems = []
link_ok = []


def bind(relmap, label, base=ROOT):
    for k, v in relmap.items():
        p = Path(base) / k
        if not p.exists():
            link_problems.append({'link': label, 'path': k, 'issue': 'missing'})
        elif sha(p) != v:
            link_problems.append({'link': label, 'path': k, 'issue': 'sha256_mismatch'})
        else:
            link_ok.append(f'{label}:{k}')


bind(bridge['sources_sha256'], 'bridge_receipt.sources_sha256')
bind(bridge_review['sources_sha256'], 'bridge_review.sources_sha256')
bind(augmented['dependencies'], 'augmented_audit.dependencies')
bind(dual['source_sha256'], 'dual_receipt.source_sha256')
for name, entry in augmented['reviewed'].items():
    p = ROOT / entry['path']
    if not p.exists():
        link_problems.append({'link': f'augmented_audit.reviewed.{name}',
                              'path': entry['path'], 'issue': 'missing'})
    elif sha(p) != entry['sha256']:
        link_problems.append({'link': f'augmented_audit.reviewed.{name}',
                              'path': entry['path'], 'issue': 'sha256_mismatch'})
    else:
        link_ok.append(f'augmented_audit.reviewed.{name}:{entry["path"]}')

bind(replay['source_binding']['files'], 'replay.source_binding.files', base=SRCD)
if sha(UPSTREAM_MANIFEST) != replay['source_binding']['upstream_manifest_sha256']:
    link_problems.append({'link': 'replay.source_binding.upstream_manifest',
                          'path': rel(UPSTREAM_MANIFEST), 'issue': 'sha256_mismatch'})
else:
    link_ok.append('replay.source_binding.upstream_manifest')
bind(source_binding['files'], 'SOURCE_BINDING.files', base=SRCD)

# the bridge review must bind the bridge receipt itself, and the bridge must
# bind the fixed-rod local budget receipt it lifts into
assert 'verify/out/n100-cover-hole-bridge.json' in bridge_review['sources_sha256'], \
    'bridge review does not bind the bridge receipt'
assert 'verify/out/n100-fixed-rod-local-budget.json' in bridge['sources_sha256'], \
    'bridge receipt does not bind the fixed-rod local budget receipt'
assert 'replay.source_binding.files:polynomial_system.json' in link_ok, \
    'replay source binding does not match the on-disk polynomial system'
assert 'replay.source_binding.files:rational_midpoint.json' in link_ok, \
    'replay source binding does not match the on-disk rational midpoint'
assert ('bridge_receipt.sources_sha256:'
        'runtime/external-disk100-strict-local-replay/source/polynomial_system.json') in link_ok
assert not link_problems, link_problems

# --------------------------------------------------------------------------
# 6. the parent certificate: hash, declared constants, derived fields
# --------------------------------------------------------------------------
assert PARENT_RECEIPT.exists(), 'widened budget receipt missing: nothing to audit'
assert PARENT_SCRIPT.exists(), 'widened budget script missing'
parent = load(PARENT_RECEIPT)
assert parent['schema'] == 'n100-local-widened-budget/v1', parent.get('schema')
assert parent['verified'] is True
assert parent['checker_sha256'] == sha(PARENT_SCRIPT), 'parent receipt is not bound to its script'
bind(parent['dependencies_sha256'], 'parent_receipt.dependencies_sha256')

CC = {k: F(v) for k, v in parent['constants'].items()}
H, Z = CC['H'], CC['Z']
RRp, mu = CC['R'], CC['mu']
J, q = CC['J'], CC['Q']
kappa, m = CC['kappa'], CC['ambient_m']
radius = CC['fixed_rod_radius']
K = CC['branch_inverse']
eps = CC['fixed_gauge_center_radius']
eta = CC['hole_radius']
ungauged = CC['ungauged_center_radius']

bad_declared, Kyoung_declared = chain(H, Z, RRp, mu, J, q, kappa, m, radius, K,
                                      eps, eta, ungauged, alpha_src, gap_min, margin_min)
assert not bad_declared, bad_declared
assert CC['growth_coefficient'] == m / 4

# every derived field of the parent receipt is recomputed here from its own
# declared constants (exact equality required)
derived = {}
derived['young_negative_normal_term'] = (F(parent['young_negative_normal_term']), Kyoung_declared)
derived['493_lift_norm_bound'] = (F(parent['493_lift_norm_bound']),
                                 23 * max(eps, eta, 64 * (eta + eps)))
derived['rotation_normalized_coordinate_error_bound'] = (
    F(parent['rotation_normalized_coordinate_error_bound']),
    ungauged + 2 * (2 * ungauged) + (2 * ungauged) ** 2)
derived['fixed_rod_radius_improvement_factor'] = (
    F(parent['fixed_rod_radius_improvement_factor']), radius / F(1, 10 ** 40))
derived['ungauged_center_radius_improvement_factor'] = (
    F(parent['ungauged_center_radius_improvement_factor']), ungauged / F(1, 10 ** 55))
derived_disagree = [k for k, (a, bb) in derived.items() if a != bb]
assert not derived_disagree, derived_disagree

assert parent['global_optimality'] is False
assert parent['all_topology_domains_excluded'] is False
assert parent['minimal_polynomial_obtained'] is False
assert isinstance(parent['local_covering_conclusion'], str) and parent['local_covering_conclusion']

if 'oversized_local_radius' not in ' '.join(parent['negative_controls']):
    findings.append({
        'id': 'F1',
        'severity': 'completeness',
        'text': ('The widened receipt lists oversized-radius controls '
                 '("oversized_fixed_rod_radius_1e-20", "oversized_center_radius_1e-30") but no '
                 'wrong-R control. The required wrong-R controls are supplied by this audit '
                 '(drop the sqrt(439) factor, the just-below-threshold floor, and the old loose '
                 '439*||B^-1||_inf route); all three are rejected.'),
    })
findings.append({
    'id': 'F2',
    'severity': 'documentation',
    'text': ('The parent rotation bound uses theta = 2*ungauged and omits the 1e-58 root-box '
             'radius; this audit re-runs the same step with theta = 2*(ungauged + rho). The '
             'conclusion still holds (5.00001e-37 < 1e-36), so this is a presentation gap, not '
             'an arithmetic error.'),
})

# --------------------------------------------------------------------------
# 7. negative controls, evaluated through the same chain predicate
# --------------------------------------------------------------------------
R_floor = F(isqrt_floor(R2_req))                 # just below sqrt(439)*||B^-1||_inf
R_old = ncon * Binf                              # pre-widening loose route
controls = []


def control(cid, required, why, **over):
    args = dict(H=H, Z=Z, RR=RRp, mu=mu, J=J, q=q, kappa=kappa, m=m, radius=radius,
                K=K, eps=eps, eta=eta, ungauged=ungauged, alpha=alpha_src,
                gap_lb=gap_min, margin_lb=margin_min)
    args.update(over)
    badc, _ = chain(**args)
    controls.append({'id': cid, 'required': required, 'rationale': why,
                     'rejected': bool(badc), 'violated': badc,
                     'value': {k: str(v) for k, v in over.items()}})
    return badc


assert control('oversized_fixed_rod_radius_1e-20', True,
               'task-required oversized local radius', radius=F(1, 10 ** 20))
assert control('oversized_fixed_rod_radius_1e-25', True,
               'oversized local radius, second decade', radius=F(1, 10 ** 25))
assert control('wrong_R_drop_sqrt439', True,
               'task-required wrong R: forget the sqrt(439) factor', RR=Binf)
assert control('wrong_R_floor_sqrt439_route', True,
               'task-required wrong R: largest integer below sqrt(439)*||B^-1||_inf', RR=R_floor)
assert control('wrong_R_old_loose_439_times_Binf', True,
               'wrong R: pre-widening loose route 439*||B^-1||_inf passes the R check but '
               'breaks Young and the m bound', RR=R_old)
assert control('wrong_J_164', False, 'J one below the least valid integer', J=F(164))
assert control('wrong_Q_41', False, 'q^2 < 4*ncon', q=F(41))
assert control('wrong_K_pre_widening_1e6', False,
               'pre-widening branch inverse bound breaks 128*K*eps <= eta', K=F(10 ** 6))
assert control('wrong_m_2e-9', False, 'm above 1/(2R^2)', m=F(2, 10 ** 9))
assert control('wrong_kappa_1e13', False, 'kappa below Young requirement', kappa=F(10 ** 13))
assert control('oversized_ungauged_center_radius', False,
               'ungauged radius too large to normalize into the fixed gauge box',
               ungauged=F(1, 10 ** 30))
assert all(c['rejected'] for c in controls), [c for c in controls if not c['rejected']]

# --------------------------------------------------------------------------
# 8. tightness inventory (exact ratios, display only)
# --------------------------------------------------------------------------
radius_same_algebra = m / (8 * kappa * J * q)
tight = {
    'H_margin_ratio': ratio(H, H_ub),
    'Z2_margin_ratio': ratio(Z * Z, Z2_ub),
    'R2_margin_ratio': ratio(RRp * RRp, R2_req),
    'mu_margin_ratio': ratio(mu_lb, mu),
    'J2_margin_ratio': ratio(J * J, J2_a),
    'least_valid_integer_J_route_A': J_least_int,
    'least_valid_integer_J_route_B': J_least_int_interval,
    'm_margin_ratio': ratio(min(mu / (4 * Z * Z), 1 / (2 * RRp * RRp)), m),
    'young_slack': str(2 * kappa - 1 - Kyoung_declared),
    'branch_forcing_margin_ratio': ratio(eta, 128 * K * eps),
    'K_margin_ratio': ratio(K, inv_max),
    'gap_margin_ratio': 'gap/min-shift = ' + ratio(gap_min, 64 * (eta + eps)),
    'margin_margin_ratio': 'margin/min-shift = ' + ratio(margin_min, 32 * eta + 2 * eta * eta),
    'lift_margin_ratio': ratio(radius, 23 * max(eps, eta, 64 * (eta + eps))),
    'rotation_margin_ratio': ratio(eps, (ungauged + RHO) + 2 * (2 * (ungauged + RHO))
                                   + (2 * (ungauged + RHO)) ** 2),
    'max_local_radius_same_algebra_declared_constants': str(radius_same_algebra),
    'declared_radius_over_same_algebra_radius': ratio(radius_same_algebra, radius),
}

# --------------------------------------------------------------------------
# 9. write the receipt
# --------------------------------------------------------------------------
elapsed = time.time() - t_start
receipt = {
    'schema': 'n100-local-widened-independent/v1',
    'audit_verified': True,
    'role': 'independent exact scalar audit of the widened n100 local certificate '
            '(verify/n100_local_widened_budget.py -> verify/out/n100-local-widened-budget.json)',
    'method': 'separate stdlib Fraction re-implementation; constants re-derived from raw source '
              'receipts; all 146 hole Jacobian inverse bounds, inactive gaps and interior margins '
              'recomputed from polynomial_system.json + rational_midpoint.json; the audited '
              'receipt is never imported or executed',
    'independently_derived_bounds': {
        'root_box_coordinate_radius': str(RHO),
        'H_root_infinity_upper': str(H_ub),
        'H_root_infinity_upper_decimal': dec(H_ub),
        'Z_2norm_squared_upper': str(Z2_ub),
        'Z_2norm_squared_upper_decimal': dec(Z2_ub),
        'right_inverse_infinity_norm': {'exact': str(Binf), 'decimal': dec(Binf)},
        'R_2norm_squared_requirement_439_Binf_squared': str(R2_req),
        'R_2norm_squared_requirement_decimal': dec(R2_req),
        'reduced_curvature_mu_lower': {'exact': str(mu_lb), 'decimal': dec(mu_lb)},
        'J_frobenius_squared_route_A_product': str(J2_a),
        'J_frobenius_squared_route_A_decimal': dec(J2_a),
        'J_frobenius_squared_route_B_interval': str(J2_b),
        'J_frobenius_squared_route_B_decimal': dec(J2_b),
        'Q_squared_requirement_4_ncon': q2_req,
        'alpha_min_from_dual_and_augmented_receipts': {'exact': str(alpha_src),
                                                       'decimal': dec(alpha_src),
                                                       'two_receipts_agree': alpha_dual == alpha_aug},
    },
    'recomputed_146_holes': {
        'hole_count': nholes,
        'interior_count': nint,
        'boundary_count': len(boundary),
        'max_inverse_infinity_bound': {'exact': str(inv_max), 'decimal': dec(inv_max)},
        'min_det_absolute': str(det_min),
        'min_inactive_squared_gap': {'exact': str(gap_min), 'decimal': dec(gap_min)},
        'min_interior_unit_margin': {'exact': str(margin_min), 'decimal': dec(margin_min)},
        'agreement_with_bridge_receipt_all_146': agree,
        'recomputed_hole_table_sha256': hashlib.sha256(
            json.dumps(hole_rows, sort_keys=True).encode('utf-8')).hexdigest(),
        'gauge_row': {'center': int(gauge_meta['center']),
                      'coordinate': gauge_meta['coordinate'],
                      'pinned_variable': gauge_var,
                      'pivot_variable_for_rotation': pivot_var,
                      'pivot_abs_lower_bound': str(pivot_abs_lb)},
    },
    'declared_constants_accepted': {k: str(v) for k, v in CC.items()},
    'chain': {
        'violated_conditions': bad_declared,
        'young_negative_normal_term_recomputed': str(Kyoung_declared),
        'conditions_checked': [
            'H_dominates_derived_root_hessian_bound', 'Z_dominates_derived_2norm_squared_bound',
            'R_dominates_derived_right_inverse_2norm_bound',
            'mu_below_derived_reduced_curvature_bound',
            'J_below_derived_frobenius_jacobian_bound',
            'Q_below_derived_quadratic_remainder_bound',
            'alpha_not_certified_by_source_receipts',
            'K_below_recomputed_146_hole_inverse_bounds',
            'young_2kappa_minus_K_ge_1', 'm_within_reduced_coordinate_bounds',
            'local_radius_linear_term', 'local_radius_alpha_band',
            'inactive_gap_dominates_rod_shift', 'interior_unit_margin_dominates_shift',
            '493_variable_lift_inside_local_radius', 'banach_self_map_forcing_128K_eps_le_eta',
            'banach_contraction_K_16eps_4eta_le_half', 'centre_coordinate_box_le_2',
            'gauge_pivot_abs_ge_9over10', 'gauge_rotation_derivative_dominates',
            'rotation_normalized_inside_fixed_gauge_box'],
    },
    'negative_controls': controls,
    'tightness': tight,
    'dependency_links': {
        'verified_links': link_ok,
        'problems': link_problems,
        'chain': ('widened budget -> replay_verification, cover-hole bridge, augmented audit, '
                  'bridge review, polynomial_system, rational_midpoint; bridge -> source polys, '
                  'midpoint, krawczyk, fixed-rod budget; bridge review -> bridge receipt itself; '
                  'augmented audit -> reviewed note/script/receipt; replay source_binding -> '
                  'source files + upstream manifest; dual -> source polys/midpoint/krawczyk'),
        'replay_source_binding_polys_midpoint_match': True,
        'upstream_manifest_matches_disk': True,
    },
    'parent_certificate': {
        'script': rel(PARENT_SCRIPT),
        'script_sha256': sha(PARENT_SCRIPT),
        'receipt': rel(PARENT_RECEIPT),
        'receipt_sha256': sha(PARENT_RECEIPT),
        'checker_sha256_matches_script': True,
        'declared_constants_validated': not bad_declared,
        'derived_fields_recomputed_exactly': {k: {'receipt': str(a), 'recomputed': str(bb),
                                                  'equal': a == bb}
                                              for k, (a, bb) in derived.items()},
        'claims_confirmed_within_scope': True,
        'findings': findings,
    },
    'scope': {
        'LOCAL_only': True,
        'fixed_affine_gauge': True,
        'root_centred_labelled_neighbourhood': True,
        'analytic_lemmas_reproved_here': False,
        'consumed_analytic_lemmas': ['Banach continuation of the 146 holes (bridge receipt + review)',
                                     'rotation gauge slice (local rotation gauge receipt)',
                                     'augmented-Lagrangian local exclusion / exact quadratic Taylor '
                                     'split (fixed-rod local budget + augmented audit)',
                                     'accepted Krawczyk/SOSC replay (not re-run here)'],
        'global_optimality': False,
        'other_contact_graphs_excluded': False,
        'universal_lower_bound_closed': False,
        'minimal_polynomial': False,
        'no_floating_acceptance': True,
    },
    'diagnostics_display_only': {
        'H_ub': dec(H_ub), 'Z2_ub': dec(Z2_ub), 'Binf': dec(Binf), 'R2_req': dec(R2_req),
        'mu_lb': dec(mu_lb), 'J2_route_A': dec(J2_a), 'J2_route_B': dec(J2_b),
        'inv_max_146': dec(inv_max), 'min_gap': dec(gap_min), 'min_margin': dec(margin_min),
        'declared': {'H': dec(H), 'Z': dec(Z), 'R': dec(RRp), 'mu': dec(mu), 'J': dec(J),
                     'Q': dec(q), 'kappa': dec(kappa), 'm': dec(m), 'radius': dec(radius),
                     'K': dec(K), 'eps': dec(eps), 'eta': dec(eta), 'ungauged': dec(ungauged)},
    },
    'sources_sha256': {rel(p): sha(p) for p in
                       [REPLAY, BRIDGE, BRIDGE_REVIEW, AUGMENTED, DUAL, POLYS, MIDPOINT,
                        KRAWCZYK, SOURCE_BINDING, UPSTREAM_MANIFEST, PARENT_SCRIPT,
                        PARENT_RECEIPT]},
    'elapsed_seconds': round(elapsed, 6),
    'checker_sha256': sha(Path(__file__)),
}

if OUT.exists():
    stamp = time.strftime('%Y%m%d-%H%M%S')
    backup = OUT.with_name(f'{OUT.name}.bak-{stamp}')
    n = 0
    while backup.exists():
        n += 1
        backup = OUT.with_name(f'{OUT.name}.bak-{stamp}-{n}')
    OUT.rename(backup)
    receipt['previous_receipt_backup'] = rel(backup)

OUT.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')

print(f'PASS independent exact audit: H<={dec(H_ub)}<=2/25, Z^2<={dec(Z2_ub)}<=44^2, '
      f'439*||B^-1||inf^2={dec(R2_req)}<=22000^2, mu>={dec(mu_lb)}>=1e-4, '
      f'J_F^2={dec(J2_a)}<=165^2 (least integer {J_least_int}), q^2>=4*439')
print(f'PASS 146 holes recomputed from source: max||J^-1||inf={dec(inv_max)}<=7, '
      f'min gap={dec(gap_min)}>64(eta+eps), min margin={dec(margin_min)}>32eta+2eta^2; '
      f'per-hole agreement with bridge receipt {agree}')
print(f'PASS chain: {len(receipt["chain"]["conditions_checked"])} conditions, '
      f'0 violations; young term {Kyoung_declared} vs 2kappa-1={2 * kappa - 1}')
print(f'PASS {len(controls)} negative controls all rejected '
      f'(required: oversized local radius, wrong R x3)')
print(f'PASS dependency links: {len(link_ok)} hashes verified, 0 problems; '
      f'parent receipt bound to script {sha(PARENT_SCRIPT)[:12]}')
print(f'written {rel(OUT)} in {elapsed:.3f}s; LOCAL only, global/minpoly open')

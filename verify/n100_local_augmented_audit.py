"""Standalone independent audit of the n100 fixed-rod augmented-Lagrangian LOCAL budget.

Review objects (read only, never rewritten here):
  docs/n100-fixed-rod-local-exclusion.md
  verify/n100_fixed_rod_local_budget.py  ->  verify/out/n100-fixed-rod-local-budget.json
  dependency: runtime/external-disk100-strict-local-replay/replay_verification.json
              verify/out/n100-first-order-rod-dual.json

The audit re-derives every scalar inequality of the derivation from the accepted
replay receipt, checks each declared constant against the certificate field that is
supposed to bound it, and verifies the algebraic identities the derivation needs
(exact Taylor for quadratic constraints, augmented-Lagrangian cancellation, the
Z/R assembly and the Young step) with exact rational arithmetic in the standard
library only.  Display decimals are diagnostics, never acceptance decisions.

Scope of what this audit can and cannot confirm is recorded in the receipt under
`scope`/`assumptions`/`gaps`.  It confirms nothing about the true covering problem,
other contact graphs, or global optimality.
"""
import hashlib
import json
import math
import time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'runtime/external-disk100-strict-local-replay'
P_REPLAY = DIR / 'replay_verification.json'
P_SYS = DIR / 'source/polynomial_system.json'
P_MID = DIR / 'source/rational_midpoint.json'
P_DUAL = ROOT / 'verify/out/n100-first-order-rod-dual.json'
P_BUDGET = ROOT / 'verify/out/n100-fixed-rod-local-budget.json'
P_NOTE = ROOT / 'docs/n100-fixed-rod-local-exclusion.md'
OUT = ROOT / 'verify/out/n100-local-augmented-audit.json'


def req(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def dec(q, digits=14):
    with localcontext() as ctx:
        ctx.prec = 34
        return str(+(Decimal(q.numerator) / Decimal(q.denominator)))


def ceil_sqrt(q):
    """Smallest integer J with J*J >= q (q >= 0 rational)."""
    num, den = q.numerator, q.denominator
    r = math.isqrt(num // den)
    while F(r * r) < q:
        r += 1
    while r > 0 and F((r - 1) * (r - 1)) >= q:
        r -= 1
    return r


# ---------------------------------------------------------------- exact polys
# Minimal multivariate polynomial arithmetic over Fraction (exponents tuples).
def p_add(a, b):
    out = dict(a)
    for key, val in b.items():
        nv = out.get(key, F(0)) + val
        if nv:
            out[key] = nv
        elif key in out:
            del out[key]
    return out


def p_scale(a, c):
    if not c:
        return {}
    return {k: v * c for k, v in a.items() if v * c}


def p_sub(a, b):
    return p_add(a, {k: -v for k, v in b.items()})


def p_mul(a, b):
    out = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            key = tuple(x + y for x, y in zip(k1, k2))
            out[key] = out.get(key, F(0)) + v1 * v2
    return {k: v for k, v in out.items() if v}


def p_var(i, nv):
    exp = [0] * nv
    exp[i] = 1
    return {tuple(exp): F(1)}


def p_const(c, nv):
    return {(0,) * nv: F(c)} if c else {}


def p_pow(a, k):
    out = {(0,) * len(next(iter(a))): F(1)}
    for _ in range(k):
        out = p_mul(out, a)
    return out


def p_diff(a, i):
    out = {}
    for key, val in a.items():
        if key[i]:
            nk = list(key)
            nk[i] -= 1
            out[tuple(nk)] = out.get(tuple(nk), F(0)) + val * key[i]
    return {k: v for k, v in out.items() if v}


def p_shift(poly, target, nv):
    """Substitute x_k -> target_k + h_k, returning a polynomial in h."""
    out = {}
    for key, val in poly.items():
        term = p_const(val, nv)
        for i, exp in enumerate(key):
            if exp:
                term = p_mul(term, p_pow(p_add(p_const(target[i], nv), p_var(i, nv)), exp))
        out = p_add(out, term)
    return out


def p_eval(poly, point):
    total = F(0)
    for key, val in poly.items():
        term = val
        for i, exp in enumerate(key):
            term *= point[i] ** exp
        total += term
    return total


def p_is_zero(poly):
    return not poly


def p_sum(polys):
    out = {}
    for poly in polys:
        out = p_add(out, poly)
    return out


# ---------------------------------------------------------------- main audit
def main():
    started = time.time()
    replay = load(P_REPLAY)
    system = load(P_SYS)
    mid = load(P_MID)
    dual = load(P_DUAL)
    budget = load(P_BUDGET)
    req(replay['verified'] is True, 'replay receipt not verified')
    req(dual['verified'] is True, 'rod dual receipt not verified')
    req(budget['verified_scalar_budget'] is True, 'scalar budget receipt not verified')

    b = replay['exact_bounds']
    get = lambda key: F(*b[key])
    checks = {}

    # 0. dependency integrity
    req(dual['source_sha256']['runtime/external-disk100-strict-local-replay/source/polynomial_system.json'] == sha(P_SYS),
        'polynomial_system hash mismatch vs dual receipt')
    req(dual['source_sha256']['runtime/external-disk100-strict-local-replay/source/rational_midpoint.json'] == sha(P_MID),
        'rational_midpoint hash mismatch vs dual receipt')
    checks['dependency_sha256_match'] = True
    dual_alpha = F(dual['minimum_alpha_lower_bound'])
    replay_alpha = F(*replay['minimum_distance_multiplier_lower_bound'])
    req(dual_alpha == replay_alpha, 'alpha lower bounds disagree between receipts')
    checks['alpha_bounds_agree'] = True

    # 1. source structure: exact-Taylor needs deg <= 2 on every constraint row
    nc = system['n_constraints']
    nb = system['n_base']
    kinds = {}
    degrees = []
    for row, poly in enumerate(system['polynomials'][:nc]):
        degrees.append(max((len(vs) for _, vs in poly), default=0))
        kinds[system['constraint_metadata'][row]['kind']] = kinds.get(system['constraint_metadata'][row]['kind'], 0) + 1
    req(max(degrees) <= 2, 'constraint row of degree >= 3 found: exact Taylor fails')
    req(kinds.get('distance') == 406 and kinds.get('unit') == 32 and kinds.get('gauge') == 1, 'unexpected constraint kinds')
    req(nc == 439 and nb == 493 and system['t_index'] == 492, 'unexpected system dimensions')
    checks['constraints_all_degree_le_2'] = True

    # 2. exact Jacobian at the midpoint and box Lipschitz row bounds
    D = int(mid['denominator'])
    x = [F(int(v), D) for v in mid['numerators']]
    rho_box = F(1, 10 ** 58)
    jac = [{} for _ in range(nc)]
    row_bound = []
    for row, poly in enumerate(system['polynomials'][:nc]):
        deriv = [F(0)] * nb
        for coeff, vs in poly:
            cf = abs(F(*coeff) if isinstance(coeff, list) else F(coeff))
            if not vs:
                continue
            for i, col in enumerate(vs):
                prod = cf
                for j, other in enumerate(vs):
                    if j != i:
                        prod *= abs(x[other]) + rho_box
                deriv[col] += prod
            if len(vs) == 1:
                jac[row][vs[0]] = jac[row].get(vs[0], F(0)) + (F(*coeff) if isinstance(coeff, list) else F(coeff))
            elif len(vs) == 2:
                i, j = vs
                ai = F(*coeff) if isinstance(coeff, list) else F(coeff)
                if i == j:
                    jac[row][i] = jac[row].get(i, F(0)) + 2 * ai * x[i]
                else:
                    jac[row][i] = jac[row].get(i, F(0)) + ai * x[j]
                    jac[row][j] = jac[row].get(j, F(0)) + ai * x[i]
            else:
                raise ValueError('constraint degree exceeds two')
        row_bound.append(sum(deriv))
    frob2 = sum(rb * rb for rb in row_bound)          # ||J||_F^2 >= ||J||_2^2 over the box

    # 3. declared constants as bounds on true-root quantities
    H_decl, Z_decl, R_decl, mu_decl, J_decl, q_decl = F(1), F(110), F(500000), F(1, 10000), F(1000), F(42)
    kappa, m_decl, radius = F(10 ** 21), F(1, 10 ** 12), F(1, 10 ** 40)
    H_box = get('hessian_midpoint_infinity_norm') + get('hessian_root_perturbation_infinity_bound')
    req(H_box <= H_decl, 'H bound fails')
    Z2_box = (get('null_basis_midpoint_infinity_norm') + get('null_basis_error_infinity_bound')) * \
             (get('null_basis_midpoint_transpose_infinity_norm') + get('null_basis_error_transpose_infinity_bound'))
    req(Z2_box <= Z_decl ** 2, 'Z bound fails')
    binv = get('pivot_inverse_infinity_bound')        # ||A^{-1}||_inf at the true root (Neumann)
    req(439 * binv <= R_decl, 'parent 439*||A^-1||_inf assertion fails')
    req(439 * binv * binv <= R_decl ** 2, 'R 2-norm chain fails')   # ||R||_2^2 <= ||R||_inf*||R^T||_inf <= 439*binv^2
    mu_tight = (1 - get('transformed_total_identity_residual')) / \
               (get('cholesky_transform_infinity_norm') * get('cholesky_transform_transpose_infinity_norm'))
    req(mu_tight >= mu_decl, 'mu bound fails')
    req(frob2 <= J_decl ** 2, 'Jacobian Frobenius bound fails')
    req(4 * nc <= q_decl ** 2, 'q bound fails')        # 4*439 = 1756 <= 1764
    checks['H_bound_is_true_root_bound'] = True        # ||H||_2 <= ||H||_inf <= H_decl (H symmetric)
    checks['Z_bound_is_2norm_bound'] = True            # ||Z||_2^2 <= ||Z||_inf*||Z^T||_inf <= Z_decl^2
    checks['R_right_inverse_2norm_bound'] = True
    checks['mu_is_reduced_curvature_bound'] = True
    checks['J_frobenius_dominates_spectral'] = True
    checks['q_covers_quadratic_term'] = True

    # 4. assembly: A = H + 2 kappa J^T J
    K_const = 2 * H_decl ** 2 * Z_decl ** 2 * R_decl ** 2 / mu_decl + H_decl * R_decl ** 2
    req(2 * kappa - K_const >= 1, 'kappa does not dominate the Young loss')
    req(m_decl <= mu_decl / (4 * Z_decl ** 2), 'm exceeds mu/(4Z^2)')
    req(m_decl <= 1 / (2 * R_decl ** 2), 'm exceeds 1/(2R^2)')
    checks['kappa_dominates_young_loss'] = True
    checks['m_within_both_assembly_bounds'] = True

    # 5. radius requirements
    req(2 * kappa * J_decl * q_decl * radius <= m_decl / 4, 'radius exceeds m/(8 kappa J q)')
    req(kappa * (J_decl * radius + 2 * radius ** 2) <= replay_alpha, 'rod band exceeds alpha_min/kappa')
    checks['radius_meets_linear_term_bound'] = True
    checks['radius_keeps_rods_in_alpha_band'] = True

    # 6. negative controls: oversized radii must violate a radius requirement
    rejected = []
    for bad in (F(1, 10 ** 30), F(1, 10 ** 10)):
        if not (2 * kappa * J_decl * q_decl * bad <= m_decl / 4 and kappa * (J_decl * bad + 2 * bad ** 2) <= replay_alpha):
            rejected.append(str(bad))
    req(len(rejected) == 2, 'oversized-radius controls did not fail')
    checks['oversized_radii_rejected'] = True

    # 7. exact-root convention: midpoint multipliers do NOT satisfy stationarity
    lam0 = [F(int(v), D) for v in mid['numerators'][nb:]]
    resid = []
    for k in range(nb):
        val = sum(jac[row].get(k, F(0)) * lam0[row] for row in range(nc))
        if k == system['t_index']:
            val += 1
        resid.append(abs(val))
    midpoint_residual = max(resid) if resid else F(0)
    req(midpoint_residual > 0, 'midpoint unexpectedly stationary; exact-root convention unchecked')
    checks['midpoint_multipliers_not_stationary'] = True

    # 8. exact algebra: Young step
    amu = p_var(0, 2)
    a2 = p_var(1, 2)
    young_lhs = p_mul(p_const(1, 2), p_pow(p_sub(p_scale(amu, mu_decl), p_scale(a2, 2)), 2))
    young_lhs = p_scale(young_lhs, 1 / (2 * mu_decl))
    young_rhs = p_sub(p_add(p_scale(p_pow(amu, 2), mu_decl / 2), p_scale(p_pow(a2, 2), 2 / mu_decl)),
                      p_scale(p_mul(amu, a2), 2))
    req(p_is_zero(p_sub(young_lhs, young_rhs)), 'Young identity failed')
    checks['young_identity_exact'] = True

    # 9. exact algebra: Z/R assembly split
    u2, e2 = p_var(0, 2), p_var(1, 2)
    lo = p_add(p_scale(p_pow(u2, 2), mu_decl / 2), p_pow(e2, 2))
    hi = p_scale(p_add(p_scale(p_pow(u2, 2), 2 * Z_decl ** 2), p_scale(p_pow(e2, 2), 2 * R_decl ** 2)), m_decl)
    split = p_sub(lo, hi)
    coef_u = mu_decl / 2 - 2 * m_decl * Z_decl ** 2
    coef_e = 1 - 2 * m_decl * R_decl ** 2
    req(coef_u >= 0 and coef_e >= 0, 'assembly coefficients not nonnegative')
    req(p_is_zero(p_sub(split, p_add(p_scale(p_pow(u2, 2), coef_u), p_scale(p_pow(e2, 2), coef_e)))),
        'assembly split identity failed')
    checks['assembly_split_exact_and_nonnegative'] = True

    # 10. exact model: quadratic constraints give remainder-free Taylor and the
    #     augmented identity holds (3 variables, 3 constraints, equidistant rods).
    nv = 3
    zt_star = [F(1), F(1), F(0)]                       # (t,a,b)
    c1, c2 = (F(0), F(0)), (F(2), F(0))
    xv = [p_var(i, nv) for i in range(nv)]
    t_x, a_x, b_x = xv[0], xv[1], xv[2]
    model = [
        p_sub(p_add(p_pow(p_sub(a_x, p_const(c1[0], nv)), 2), p_pow(p_sub(b_x, p_const(c1[1], nv)), 2)), t_x),
        p_sub(p_add(p_pow(p_sub(a_x, p_const(c2[0], nv)), 2), p_pow(p_sub(b_x, p_const(c2[1], nv)), 2)), t_x),
        b_x,
    ]
    lam = [F(1, 2), F(1, 2), F(0)]
    grad = [[p_eval(p_diff(fj, k), zt_star) for k in range(nv)] for fj in model]
    hess = [[[p_eval(p_diff(p_diff(fj, k), l), zt_star) for l in range(nv)] for k in range(nv)] for fj in model]
    stationarity = [sum(lam[j] * grad[j][k] for j in range(3)) + (1 if k == 0 else 0) for k in range(nv)]
    req(all(v == 0 for v in stationarity), 'model stationarity failed')
    H_model = [[sum(lam[j] * hess[j][k][l] for j in range(3)) for l in range(nv)] for k in range(nv)]
    shift = [p_shift(fj, zt_star, nv) for fj in model]
    for j in range(3):
        taylor = p_const(p_eval(model[j], zt_star), nv)
        for k in range(nv):
            taylor = p_add(taylor, p_scale(p_var(k, nv), grad[j][k]))
        for k in range(nv):
            for l in range(nv):
                taylor = p_add(taylor, p_scale(p_mul(xv[k], xv[l]), hess[j][k][l] / 2))
        req(p_is_zero(p_sub(shift[j], taylor)), 'model exact Taylor identity failed')
    quad_model = {}
    for k in range(nv):
        for l in range(nv):
            quad_model = p_add(quad_model, p_scale(p_mul(xv[k], xv[l]), H_model[k][l] / 2))
    kappa_model = F(7, 3)
    penalty2 = p_sum(p_pow(shift[j], 2) for j in range(3))
    lag_linear = p_sum(p_scale(shift[j], lam[j]) for j in range(3))
    phi = p_add(p_add(p_const(zt_star[0], nv), p_var(0, nv)), p_add(lag_linear, p_scale(penalty2, kappa_model)))
    rhs = p_add(quad_model, p_scale(penalty2, kappa_model))
    req(p_is_zero(p_sub(p_sub(phi, p_const(zt_star[0], nv)), rhs)), 'model augmented identity failed')
    checks['model_exact_taylor_remainder_free'] = True
    checks['model_augmented_identity_exact'] = True

    # 11. domain sign lemma: lam*f + kappa*f^2 <= 0 under f<=0, lam>=alpha, f>=-alpha/kappa
    alpha = replay_alpha
    sign_ok = True
    for fval in (F(0), -alpha / kappa, -alpha / (2 * kappa), -alpha / (kappa * 10 ** 9)):
        for lam_j in (alpha, alpha * 2, alpha * 10 ** 6):
            lb = lam_j * fval + kappa * fval ** 2
            sign_ok = sign_ok and lb <= 0 and (lam_j * fval + kappa * fval ** 2) == fval * (lam_j + kappa * fval)
    req(sign_ok, 'domain sign lemma failed')
    checks['domain_sign_lemma_exact'] = True

    # 12. diagnostics only (never acceptance): tight constants from the same receipt
    Z2_t = Z2_box
    R2_t = 439 * binv * binv
    H_t = H_box
    mu_t = mu_tight
    K_t = 2 * H_t ** 2 * Z2_t * R2_t / mu_t + H_t * R2_t
    kappa_t = (K_t + 1) / 2
    m_t = min(mu_t / (4 * Z2_t), 1 / (2 * R2_t))
    J_t = ceil_sqrt(frob2)
    radius_t = m_t / (8 * kappa_t * J_t * q_decl)
    sigma_eq = get('ambient_tangent_quadratic_form_lower_bound')
    eps_tan = q_decl * ceil_sqrt(R2_t)
    radius_eq_route = sigma_eq / (16 * H_t * eps_tan)
    diagnostics = {
        'note': 'display/scale only; no acceptance decision uses these values',
        'H_true_root_infinity_bound': dec(H_t), 'Z_2norm_squared_bound': dec(Z2_t),
        'R_2norm_squared_bound': dec(R2_t), 'mu_tight': dec(mu_t),
        'J_frobenius_squared': dec(frob2), 'J_integer_spectral_bound': J_t,
        'K_tight': dec(K_t), 'kappa_tight_minimal': dec(kappa_t), 'm_tight': dec(m_t),
        'radius_tight_same_algebra': dec(radius_t),
        'radius_if_m_declared_and_kappa_declared': dec(m_decl / (8 * kappa * J_decl * q_decl)),
        'auditor_side_equality_route_radius': dec(radius_eq_route),
        'auditor_side_equality_route_formula': 'sigma_ambient/(16*H*q*ceil_sqrt(439)*||A^-1||_inf)',
        'midpoint_stationarity_residual_max': dec(midpoint_residual),
        'alpha_min_over_kappa': dec(alpha / kappa),
        'max_abs_rod_value_on_ball': dec(J_decl * radius + 2 * radius ** 2),
    }

    checks['all_exact_checks_passed'] = True
    receipt = {
        'schema': 'n100-local-augmented-audit/v1',
        'audit_verified': True,
        'reviewer': 'independent audit (derivation + exact scalar identities), separate from parent budget script',
        'reviewed': {
            'note': {'path': 'docs/n100-fixed-rod-local-exclusion.md', 'sha256': sha(P_NOTE)},
            'parent_budget_script': {'path': 'verify/n100_fixed_rod_local_budget.py',
                                     'sha256': sha(ROOT / 'verify/n100_fixed_rod_local_budget.py')},
            'parent_budget_receipt': {'path': 'verify/out/n100-fixed-rod-local-budget.json', 'sha256': sha(P_BUDGET)},
        },
        'dependencies': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p)
                         for p in (P_REPLAY, P_SYS, P_MID, P_DUAL)},
        'verdict': {
            'derivation_steps_sound': True,
            'declared_constants_valid_bounds_on_true_root_quantities': True,
            'scalar_budget_arithmetic_valid': True,
            'exact_taylor_remainder_free_required_and_met': True,
            'exact_root_multiplier_convention_required': True,
            'covers_true_covering_problem': False,
            'quantitative_LOCAL_leaf_for_domain_decomposition': False,
            'global_optimality_claimed': False,
        },
        'checks': checks,
        'constants': {'H': str(H_decl), 'Z': str(Z_decl), 'R_right_inverse': str(R_decl),
                      'reduced_mu': str(mu_decl), 'J': str(J_decl), 'Q': str(q_decl),
                      'kappa': str(kappa), 'ambient_m': str(m_decl), 'radius': str(radius),
                      'alpha_min': str(alpha), 'growth_coefficient': str(m_decl / 4)},
        'assembly': {'K': str(K_const), 'two_kappa_minus_K': str(2 * kappa - K_const),
                     'mu_over_4Z2': str(mu_decl / (4 * Z_decl ** 2)), 'one_over_2R2': str(1 / (2 * R_decl ** 2)),
                     'radius_requirement_m_over_8kJq': str(m_decl / (8 * kappa * J_decl * q_decl))},
        'bound_chains': {
            'H': '||H(z*)||_2 <= ||H(z*)||_inf <= midpoint_inf + root_perturbation <= 1 (H symmetric)',
            'Z': '||Z(z*)||_2^2 <= ||Z||_inf*||Z^T||_inf <= (z+dz)(z^T+dz^T) <= 110^2',
            'R': '||R||_2 = ||A^-1||_2 <= sqrt(||A^-1||_inf*439*||A^-1||_inf) <= 439*||A^-1||_inf <= 500000',
            'mu': 'lambda_min(Z^T H Z) >= (1-total)/(||W||_inf*||W^T||_inf) >= 1/10000',
            'J': '||J||_2 <= ||J||_F <= sqrt(sum of squared box row-l1 bounds) <= 1000',
            'q': '||Q(h)||_2 <= sqrt(439)*max_j|Q_j(h)| <= sqrt(439)*2||h||^2, (2*sqrt(439))^2 = 1756 <= 1764 = 42^2',
        },
        'negative_controls': {'oversized_radii_rejected': rejected,
                              'midpoint_stationarity_residual_max': str(midpoint_residual)},
        'assumptions': [
            'The exact KKT root z* exists and is unique in the certified box; ||z-z0||_inf <= 1e-58 (accepted Krawczyk replay).',
            'All 406 rod multipliers alpha_j at z* are >= alpha_min = min of the box lower bounds (positive multipliers, 4.234857...e-5).',
            'H, Z, R, mu, J in the chain are the true-root objects; the replay receipt perturbation fields transport every midpoint bound to z*.',
            'J^T lambda* + e_t = 0 holds at z* (multipliers fixed at the exact root, not at the midpoint).',
            'Every constraint polynomial has degree <= 2 (verified: 438 quadratic + 1 linear gauge), so f(z*+h) = Jh + Q(h) is exact.',
            'The audited domain is the fixed-rod system: 406 rods f_j <= 0, 32 unit equalities, 1 affine gauge, with |f_j| <= alpha_min/kappa.',
            'This audit consumes the accepted replay receipt; it does not re-run the 54-dimensional SOSC matrix verification.',
        ],
        'gaps': [
            'No bridge from the fixed-hole/fixed-rod system to the true covering functional Phi(C)=max_D min_i|u-c_i|^2: needs hole IFT branches (strict Delaunay, boundary determinant >= 0.6537), strict nearest-neighbour margins, local-max inventory, and an explicit C-space radius with ||x(C)-z*||_2 <= radius.',
            'No quantitative LOCAL leaf for a continuous-domain proof tree: radius 1e-40 (and even the tight 2.3e-27 same-algebra radius) is far below any domain-decomposition box scale.',
            'Other contact graphs, the 87 families, universal lower bound closure, minimal polynomial and its irreducibility remain untouched.',
            'The gauge slice / simultaneous-rotation quotient transfer is not re-derived here.',
        ],
        'diagnostics': diagnostics,
        'no_floating_acceptance': True,
        'elapsed_seconds': time.time() - started,
        'checker_sha256': sha(Path(__file__)),
    }
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding='utf-8'))
        old.pop('elapsed_seconds', None)
        new = dict(receipt)
        new.pop('elapsed_seconds', None)
        req(old == new, 'existing receipt differs; refusing to overwrite')
    OUT.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    try:
        rep = main()
        print('PASS n100 local augmented audit: identities exact, constants valid, radius 1e-40 chain holds')
        print('fixed-rod domain only; covering bridge, LOCAL-leaf scale and global optimality remain open')
        print('radius: %s  alpha/kappa: %s  max|f| on ball: %s' % (
            rep['constants']['radius'], dec(F(rep['constants']['alpha_min']) / F(rep['constants']['kappa'])),
            rep['diagnostics']['max_abs_rod_value_on_ball']))
    except Exception as exc:
        print(json.dumps({'audit_verified': False, 'error': type(exc).__name__ + ': ' + str(exc)}))
        raise SystemExit(1)

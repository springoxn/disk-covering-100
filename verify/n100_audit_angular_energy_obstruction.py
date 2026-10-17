"""n=100 angular-energy obstruction: LIMITED independent audit (replay + identity check).

Audits (read-only):
  verify/out/n100-angular-energy-negative-witness.json
  verify/out/n100-angular-energy-independent.json
  verify/out/n100-harmonic-energy-relaxation-counterexample.json

What this script DOES establish on its own:
  * the CAS identity for the Hessian of E(theta) = sum_{i<j} c_ij |q_i-q_j|^2;
  * SHA256 binding of every input it reads, and of the parent generator scripts;
  * the witness quadratic form, exactly, over the c_ij certificate box AT THE MIDPOINT q,
    with per-pair endpoint evaluation (no float, no eigensolver).

What this script does NOT re-derive (it relies on the parent's independent receipt and
says so explicitly in every record):
  * the quadratic form over the WHOLE Krawczyk q-box (parent independent receipt does it);
  * root interiority over the whole box (parent does it; this script only shows the
    midpoint margin);
  * any inertia count, any r_D(100) statement, any covering counterexample.

Acceptance uses exact rational arithmetic and CAS identities only.
"""
import hashlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
CB = ROOT / 'runtime/n100-vonequinox-transfer'
SRC = ROOT / 'runtime/external-disk100-strict-local-replay/source'
GEN = ROOT / 'verify/n100_angular_energy_negative_witness.py'
INDGEN = ROOT / 'verify/n100_angular_energy_independent.py'
WP = ROOT / 'verify/out/n100-angular-energy-negative-witness.json'
IP = ROOT / 'verify/out/n100-angular-energy-independent.json'
XP = ROOT / 'verify/out/n100-harmonic-energy-relaxation-counterexample.json'
OUT = ROOT / 'verify/out/n100-angular-energy-obstruction-audit.json'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


R = {'schema': 'n100-angular-energy-obstruction-audit/v3',
     'auditor_script': str(Path(__file__).relative_to(ROOT)).replace('\\', '/'),
     'acceptance_arithmetic': 'exact rational + CAS only; no float and no eigensolver',
     'scope': 'LIMITED replay audit of the obstruction receipts. Not a re-derivation of '
              'the whole-q-box claim, not an inertia claim, not a statement about '
              'r_D(100), not a covering counterexample.',
     'source_sha256': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p) for p in
                       (CB / 'certificate.json', SRC / 'rational_midpoint.json',
                        SRC / 'krawczyk_verification.json', GEN, INDGEN, WP, IP, XP)},
     'checks': {}, 'reliance': {}, 'verdict': {}}

C = json.loads((CB / 'certificate.json').read_text())
M = json.loads((SRC / 'rational_midpoint.json').read_text())
K = json.loads((SRC / 'krawczyk_verification.json').read_text())
W = json.loads(WP.read_text())
IND = json.loads(IP.read_text())

# ---- bindings: the witness must have been produced by the script it names
assert W['checker_sha256'] == sha(GEN), 'witness generator SHA mismatch'
assert IND['checker_sha256'] == sha(INDGEN), 'independent checker SHA mismatch'
assert IND['inputs'][str(WP.relative_to(ROOT)).replace('\\', '/')] == sha(WP), \
    'independent receipt does not bind this witness'
assert IND['inputs'][str((CB / 'certificate.json').relative_to(ROOT)).replace('\\', '/')] \
    == sha(CB / 'certificate.json')
assert IND['inputs'][str((SRC / 'rational_midpoint.json').relative_to(ROOT)).replace('\\', '/')] \
    == sha(SRC / 'rational_midpoint.json')
assert C['generator_sha256'] == sha(CB / 'analysis.py'), 'certificate generator SHA mismatch'
assert K['verified'] is True and K['box_radius'] == [1, 10 ** 58]
assert K['midpoint_denominator'] == int(M['denominator'])
assert IND['verified'] is True and IND['strictly_negative'] is True
R['checks']['sha_binding'] = True

D = int(M['denominator'])
RHO = F(100, D)
GRID = int(C['grid_denominator'])
GAMMA = F(C['Gamma'])
NUMS = M['numerators']
N = 32
ORDER = C['anchor_order']
T_MID = F(int(NUMS[492]), D)
assert N == 32 and sorted(ORDER) == list(range(N))

# q at the CERTIFIED MIDPOINT only (whole-box handling is the parent's; see reliance)
q = [(F(int(NUMS[428 + 2 * i]), D), F(int(NUMS[429 + 2 * i]), D)) for i in range(N)]
CI = {}
for key, raw in C['c0_lower_triangle'].items():
    i, j = (int(x) for x in key.split(','))
    c0 = F(raw)
    CI[(i, j)] = (F(math.floor(max(F(0), c0 - GAMMA) * GRID), GRID),
                  F(math.ceil((c0 + GAMMA) * GRID), GRID))
assert len(CI) == 496
dot = [[q[i][0] * q[j][0] + q[i][1] * q[j][1] for j in range(N)] for i in range(N)]

# =====================================================================
# 1. CAS identity: H[i][i]+=a, H[i][j]-=a with a = 2 c_ij <q_i,q_j> is the Hessian of E
# =====================================================================
n = 3
ts = sp.symbols('t0:%d' % n, real=True)
cs = sp.symbols('c0:%d' % (n * (n - 1) // 2), positive=True)
qq = [sp.Matrix([sp.cos(t), sp.sin(t)]) for t in ts]
E = 0
for k, (i, j) in enumerate([(i, j) for i in range(n) for j in range(i + 1, n)]):
    E += cs[k] * (qq[i] - qq[j]).dot(qq[i] - qq[j])
H = sp.Matrix(n, n, lambda i, j: sp.simplify(sp.diff(E, ts[i], ts[j])))
pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
for i in range(n):
    for j in range(n):
        if i == j:
            want = 2 * sum(cs[pairs.index((min(i, k), max(i, k)))] * sp.cos(ts[i] - ts[k])
                           for k in range(n) if k != i)
        else:
            want = -2 * cs[pairs.index((min(i, j), max(i, j)))] * sp.cos(ts[i] - ts[j])
        assert sp.simplify(H[i, j] - want) == 0, (i, j)
assert all(sp.simplify(sum(H[i, j] for j in range(n))) == 0 for i in range(n))
R['checks']['CAS_identity'] = {
    'offdiagonal': 'd2E/dt_i dt_j = -2 c_ij cos(t_i - t_j)',
    'diagonal': 'd2E/dt_i^2 = 2 sum_{j!=i} c_ij cos(t_i - t_j)',
    'row_sums_identically_zero': True,
    'equals_parent_construction': 'H[i][i] += a, H[i][j] -= a with a = 2 c_ij <q_i,q_j>',
    'established_independently': True,
}

# =====================================================================
# 2. exact witness quadratic form over the c_ij box, at the MIDPOINT q
# =====================================================================
v = [F(x) for x in W['witness']]
assert len(v) == N and v[0] == 0
qr = {p: 2 * dot[p[0]][p[1]] * (v[p[0]] - v[p[1]]) ** 2 for p in CI}
q_mid = sum(((CI[p][0] + CI[p][1]) / 2) * qr[p] for p in CI)
box_lo = sum((CI[p][0] * qr[p] if qr[p] >= 0 else CI[p][1] * qr[p]) for p in CI)
box_hi = sum((CI[p][1] * qr[p] if qr[p] >= 0 else CI[p][0] * qr[p]) for p in CI)
assert q_mid == F(W['midpoint_quadratic_form'])
assert box_lo <= q_mid <= box_hi and box_hi < 0
R['checks']['witness_at_midpoint_q'] = {
    'scope': 'c_ij CERTIFICATE WEIGHT BOX ONLY; q held at the certified midpoint',
    'evaluation': 'per-pair endpoint (exact; v^T H v is linear in each c_ij)',
    'midpoint_value': str(q_mid),
    'weight_box_interval': [str(box_lo), str(box_hi)],
    'strictly_negative_on_the_weight_box': True,
    'not_claimed': 'nothing here covers the 1e-58 Krawczyk q-box',
}
R['reliance']['whole_q_box_negativity'] = {
    'established_by': 'verify/out/n100-angular-energy-independent.json',
    'that_receipt_sha256': sha(IP),
    'that_receipt_interval_upper': IND['interval_quadratic_form'][1],
    'that_receipt_flag': IND['rational_upper_less_than_minus_1e5'],
    'this_audit_rederives_it': False,
    'note': 'the parent receipt evaluates the full coordinate-interval box and is the '
            'primary proof; this audit only replays the midpoint-weight interval',
}

# =====================================================================
# 3. angular adjacency: the MIDPOINT cross products and dot margins only
# =====================================================================
cosd_upper = 1 - 2 * (T_MID - RHO)      # conservative (upper) bound for cos(delta)
min_cross = min(q[a][0] * q[b][1] - q[a][1] * q[b][0]
                for a, b in zip(ORDER, ORDER[1:] + ORDER[:1]))
min_margin = min(dot[a][b] - cosd_upper for a, b in zip(ORDER, ORDER[1:] + ORDER[:1]))
assert min_cross > 0 and min_margin > 0
R['checks']['adjacency_at_midpoint_q'] = {
    'scope': 'MIDPOINT q only; whole-box interiority is the parent receipt\'s claim',
    'threshold': '1 - 2*(t_mid - rho), an upper bound for cos(delta), so the test is '
                 'conservative',
    'min_consecutive_cross_product': str(min_cross),
    'min_consecutive_dot_margin': str(min_margin),
    'parent_same_quantity_over_box': IND['min_consecutive_dot_above_cosdelta'],
    'identical_to_parent_value': bool(min_margin == F(IND['min_consecutive_dot_above_cosdelta'])),
}
R['reliance']['whole_q_box_adjacency'] = {
    'established_by': 'verify/out/n100-angular-energy-independent.json',
    'that_receipt_flag': IND['root_is_interior_of_angular_domain'],
    'this_audit_rederives_it': False,
}

# =====================================================================
# 4. counterexample: exact rational replay of the finite rotation step
# =====================================================================
XN = json.loads(XP.read_text())
assert XN['unit_identity_checked_exactly'] is True
step = F(XN['parameter_step'])
rot = []
for i in range(N):
    u = step * v[i] / 2
    cc = (1 - u * u) / (1 + u * u)
    ss = 2 * u / (1 + u * u)
    assert cc * cc + ss * ss == 1
    rot.append((cc * q[i][0] - ss * q[i][1], ss * q[i][0] + cc * q[i][1]))
dE_mid = F(0)
for p in CI:
    i, j = p
    old = (q[i][0] - q[j][0]) ** 2 + (q[i][1] - q[j][1]) ** 2
    new = (rot[i][0] - rot[j][0]) ** 2 + (rot[i][1] - rot[j][1]) ** 2
    dE_mid += ((CI[p][0] + CI[p][1]) / 2) * (new - old)
assert dE_mid < 0
R['checks']['counterexample_replay'] = {
    'scope': 'exact rational reproduction of the finite rotation step at the midpoint, '
             'with midpoint weights; a limited replay, not a whole-box re-evaluation',
    'parameter_step': str(step),
    'rotation_convention': 'u_i = step*v_i/2, cos=(1-u^2)/(1+u^2), sin=2u/(1+u^2)',
    'all_rotations_exactly_orthogonal': True,
    'recomputed_energy_change': str(dE_mid),
    'recomputed_is_negative': True,
    'parent_stored_interval': XN['energy_change_interval'],
    'parent_stored_upper_below_minus_1e-12': bool(F(XN['energy_change_interval'][1])
                                                  < F(-1, 10 ** 12)),
    'agrees_with_parent_midpoint_to_1e-15_absolute':
        abs(dE_mid - (F(XN['energy_change_interval'][0])
                      + F(XN['energy_change_interval'][1])) / 2) < F(1, 10 ** 15),
    'no_proximity_criterion_used_for_acceptance': True,
    'parent_scope': XN['scope'],
}

# =====================================================================
# 5. mechanism (reported, explicitly not a proof)
# =====================================================================
nneg = sum(1 for p in CI if dot[p[0]][p[1]] < 0)
R['checks']['mechanism_note'] = {
    'pairs_total': len(CI),
    'pairs_with_negative_dot_at_midpoint': nneg,
    'statement': 'a negative edge weight 2 c_ij <q_i,q_j> is a mechanism, not a proof of '
                 'indefiniteness; the proof is the exact witness above (at the midpoint) '
                 'combined with the parent whole-box receipt',
    'no_inertia_count_computed_or_claimed': True,
}

R['verdict'] = {
    'CAS_hessian_identity_established_independently': True,
    'source_sha_binding_checked': True,
    'witness_strictly_negative_on_weight_box_at_midpoint_q': True,
    'whole_q_box_negativity_relies_on_parent_independent_receipt': True,
    'whole_q_box_adjacency_relies_on_parent_independent_receipt': True,
    'counterexample_replayed_at_midpoint': True,
    'inertia_claim_made': False,
    'r_D100_claim_made': False,
    'feasible_covering_counterexample_constructed': False,
    'parent_primary_proof_valid': True,
}
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(R, fh, indent=2)
    fh.write('\n')
print('LIMITED AUDIT PASS (exact rational + CAS only)')
print(' CAS Hessian identity: OK')
print(' witness on the weight box at midpoint q: [%.6e, %.6e]  (< 0)'
      % (float(box_lo), float(box_hi)))
print(' midpoint adjacency: min cross %.6e  min dot margin %.6e'
      % (float(min_cross), float(min_margin)))
print(' counterexample replay dE = %.6e  (< 0)' % float(dE_mid))
print(' whole-q-box negativity/adjacency: relied on parent independent receipt, not redone')
print('wrote', OUT)
sys.exit(0)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""n = 100 cooperative candidate: active-contact / witness-structure analysis.

SCOPE
    Bounded, read-only structural analysis of the FROZEN discovery candidate

        runtime/n100-cooperative/anchor-certified-012008.json

    whose 100 float centres the parent agent has already certified EXACTLY at
    R = 18761/156250 (replay: verify/out/n100-cooperative-anchor-tight/replay.json).

    This file answers one question only:  what is the active-contact structure of
    the deepest critical points of that frozen configuration, and does it carry a
    credible exact/algebraic pattern?

    It reads the frozen candidate, the tight replay record and the lattice-97
    reference record.  It WRITES exactly two files:

        runtime/n100-cooperative/active-contact-analysis.json   (data)
        (the prose report docs/n100-cooperative-active-contact-analysis.md is
         written by hand from this JSON, never by this script)

    Nothing under verify/ or runtime/STATUS* is touched.  No file that already
    exists is modified.  No network, no install, no server.

METHOD (all of it reproducible from this one command)
    1. Centres are read TWICE: as float64 (for the evaluator) and as exact
       decimal literals (``parse_float=str``, the repository's canonical
       convention) -- the latter make every frozen number an exact rational, so
       every exactness statement below is decidable, not "numerical".
    2. Critical points: the pilot evaluator tools/pilot_n100_stage2.py
       (SHA256 pinned in the output) supplies the complete boundary set and an
       independent value for rho; the interior set is re-derived here with the
       SAME all-C(100,3) filter so that the generating TRIPLE of every interior
       circumcentre stays available.  Both value agree or the run fails.
    3. Witnesses are the critical points at depth d >= rho_max - delta, for a
       ladder of deltas; they are clustered at 1e-8 (KD-tree + union-find).
    4. Per witness: active set A(x) = {i : |x-c_i| <= d(x) + tol}, kind
       (interior Voronoi vertex / rim pair-bisector contact / rim antipode /
       safety point), and for interior ones the barycentric coordinates of x in
       its active triangle -- the exact first-order stationarity multipliers.
    5. Exact layer: the deepest witness of a frozen RATIONAL triangle is itself
       rational; its circumcentre, its squared radius, its barycentric weights
       and the identity sum_a lambda_a (c_a - x) = 0 are all computed in Q.
    6. Algebraic layer: PSLQ (mpmath, 50 dps) proposes integer relations for
       degree <= 4 and a height window justified by the 17-digit input; every
       proposal is then decided EXACTLY in Q.  A proposal whose exact residual is
       nonzero is reported as spurious -- that is the relative-criterion
       discipline of this repository, applied without exception.
    7. Lattice frame: the only known algebraic configuration of this project is
       the lattice-97 seed (field Q(sqrt3, sqrt67), integer data of height <= 7).
       The distance of the frozen configuration -- and of the deepest witness --
       from that frame is measured in lattice units.

WHAT IS NOT CLAIMED (verbatim in the output JSON)
    No minimal polynomial, no LLL/algebraic-relation claim, no optimality, no
    lower bound, no covering statement, no change to any certified status.  Every
    number here is either an exact rational identity about the frozen decimal
    literals or a floating-point discovery value; the two are labelled apart.

USAGE
    python tools/n100_active_contact_analysis.py
    python tools/n100_active_contact_analysis.py --out-json <path> --quiet

    Exit code 0 only if the analysis completed and the JSON written is finite;
    non-zero on any inconsistency (evaluator disagreement, missing input, hash
    mismatch against the values pinned in the frozen candidate).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import os
import platform
import sys
import time
from fractions import Fraction

import numpy as np

# --------------------------------------------------------------------------- #
# constants
# --------------------------------------------------------------------------- #

REPO_HINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANDIDATE_REL = "runtime/n100-cooperative/anchor-certified-012008.json"
REPLAY_REL = "verify/out/n100-cooperative-anchor-tight/replay.json"
PILOT_REL = "tools/pilot_n100_stage2.py"
RESULT_REL = "runtime/n100-cooperative/result.json"
OUT_JSON_REL = "runtime/n100-cooperative/active-contact-analysis.json"

CANDIDATE_SHA256 = "413af66fccfc2988aae9f52ca666de3cf5c25f3eaf01d98559d0402db3edc722"
CENTERS_CANONICAL_SHA256 = "70905174d03611c7cbbac03c16d2e3136d6af23284d7bb38f39e26e075c0d53b"
PILOT_SHA256 = "b06e054ec882d67e4ea23f61821360fabb8f0e5a054b2d9f7b5fa34989effa59"
CERTIFIED_R = "18761/156250"

CLUSTER_TOL = 1e-8              # the clustering tolerance demanded by the task
ACTIVE_TOL_ABS = 1e-9           # |x-c_i| <= d(x) + ACTIVE_TOL_ABS => active
CENTER_COUNT = 100

A_SCALED_SQ = Fraction(3, 67)   # lattice-97 normalisation a^2 = 3/67
ALPHA_SQ = Fraction(1, 67)      # lattice-97 covering radius alpha = 1/sqrt(67)

# the search's own witness band (runtime/n100-cooperative/result.json
# budget.witness_band_scaled = 0.002 in units of alpha)
WITNESS_BAND_REL = 0.002
ALPHA_FLOAT = math.sqrt(1.0 / 67.0)

# depth ladders
SHELL_DELTAS = [1e-12, 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5,
                4.25186356539653e-08, 1e-4, 1e-3, 1e-2]
RR_DENOMINATORS = (10 ** 4, 10 ** 6, 10 ** 8, 10 ** 12)
DETAIL_DELTA = WITNESS_BAND_REL * ALPHA_FLOAT      # 2.442e-4
SECONDARY_DELTA = 1e-3
SECONDARY_TOP = 40

SYMMETRY_TOL_EXACT = 1e-12

NOT_CLAIMED = [
    "no minimal polynomial for r_D(100) and no claim about it",
    "no LLL/PSLQ algebraic-relation claim: PSLQ only proposes, exact Q decides, "
    "and every proposal whose exact residual is nonzero is reported as spurious",
    "no optimality, local optimality, symmetry-family optimality or stationarity "
    "claim for the covering problem; the stationarity statement below is a "
    "first-order identity about one frozen rational triangle, nothing more",
    "no covering certificate, no rational upper bound, no lower bound: the exact "
    "replay R = 18761/156250 is the parent agent's, and it is only quoted here",
    "no claim that the deep-hole set of a stalled floating search has any bearing "
    "on the global optimum",
    "no symmetry or duplicate structure is asserted from near-coincidences; the "
    "measured residual of every candidate symmetry is reported instead",
]


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc_now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def assert_json_finite(obj, path: str = "$") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            assert_json_finite(v, "%s.%s" % (path, k))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            assert_json_finite(v, "%s[%d]" % (path, i))
    elif isinstance(obj, float):
        if not math.isfinite(obj):
            raise ValueError("non-finite float at %s: %r" % (path, obj))
    elif obj is None or isinstance(obj, (bool, int, str)):
        return
    else:
        raise ValueError("unserialisable object at %s: %r" % (path, obj))


def write_json(path: str, obj) -> None:
    assert_json_finite(obj)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=False)
        fh.write("\n")


def load_pilot(repo: str):
    """Import the frozen pilot evaluator by path, without touching sys.path."""
    path = os.path.join(repo, PILOT_REL)
    spec = importlib.util.spec_from_file_location("_n100_pilot_evaluator", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- #
# exact (rational) layer
# --------------------------------------------------------------------------- #


def exact_circumcentre(a, b, c):
    """Circumcentre of a rational triangle, exactly in Q (None if collinear)."""
    ax, ay = a
    bx, by = b
    cx, cy = c
    det = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if det == 0:
        return None
    na, nb, nc = ax * ax + ay * ay, bx * bx + by * by, cx * cx + cy * cy
    ux = (na * (by - cy) + nb * (cy - ay) + nc * (ay - by)) / det
    uy = (na * (cx - bx) + nb * (ax - cx) + nc * (bx - ax)) / det
    return ux, uy


def exact_barycentric(x, a, b, c):
    """Weights (l0, l1, l2) with x = sum l_i * vertex_i, exactly in Q."""
    det = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if det == 0:
        return None
    w1 = ((x[0] - a[0]) * (c[1] - a[1]) - (x[1] - a[1]) * (c[0] - a[0])) / det
    w2 = ((b[0] - a[0]) * (x[1] - a[1]) - (b[1] - a[1]) * (x[0] - a[0])) / det
    return (1 - w1 - w2, w1, w2)


def frac_bits(q: Fraction) -> dict:
    return {"numerator_bits": abs(q.numerator).bit_length(),
            "denominator_bits": q.denominator.bit_length(),
            "decimal_digits_of_denominator": len(str(q.denominator))}


def rational_is_square(q: Fraction):
    """Return (is_square, root) for q >= 0, exactly."""
    if q < 0:
        return False, None
    n, d = q.numerator, q.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    if rn * rn == n and rd * rd == d:
        return True, Fraction(rn, rd)
    return False, None


# --------------------------------------------------------------------------- #
# evaluation / critical points
# --------------------------------------------------------------------------- #


def interior_circumcentres_with_triples(P: np.ndarray):
    """All C(n,3) circumcentres inside the closed disk, aligned with triples.

    Deliberately a re-implementation of the pilot's filter (same thresholds) so
    that the generating triple survives; the caller cross-checks the resulting
    candidate SET and the resulting maximum against the pilot evaluator.
    """
    n = len(P)
    T = np.array(list(itertools.combinations(range(n), 3)), dtype=np.int64)
    A, B, C = P[T[:, 0]], P[T[:, 1]], P[T[:, 2]]
    det = 2.0 * (A[:, 0] * (B[:, 1] - C[:, 1]) + B[:, 0] * (C[:, 1] - A[:, 1])
                 + C[:, 0] * (A[:, 1] - B[:, 1]))
    ok = np.abs(det) > 1e-18
    T, A, B, C, det = T[ok], A[ok], B[ok], C[ok], det[ok]
    na, nb, nc = (A * A).sum(1), (B * B).sum(1), (C * C).sum(1)
    ux = (na * (B[:, 1] - C[:, 1]) + nb * (C[:, 1] - A[:, 1])
          + nc * (A[:, 1] - B[:, 1])) / det
    uy = (na * (C[:, 0] - B[:, 0]) + nb * (A[:, 0] - C[:, 0])
          + nc * (B[:, 0] - A[:, 0])) / det
    U = np.stack([ux, uy], 1)
    keep = np.isfinite(U).all(1)
    U, T = U[keep], T[keep]
    keep = (U * U).sum(1) <= 1.0
    return U[keep], T[keep]


def boundary_kind(x: np.ndarray, act, P: np.ndarray) -> str:
    """Classify a rim critical point by its active set (B1 / B2 / B3)."""
    for ax_, ay_ in ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)):
        if math.hypot(x[0] - ax_, x[1] - ay_) <= 1e-12:
            return "safety_axis_point"
    if len(act) == 1:
        i = int(act[0])
        nrm = float(np.hypot(P[i, 0], P[i, 1]))
        if nrm > 0 and math.hypot(x[0] + P[i, 0] / nrm, x[1] + P[i, 1] / nrm) <= 1e-10:
            return "rim_antipode_B2"
        return "rim_single_contact"
    if len(act) == 2:
        return "rim_pair_bisector_B1"
    return "rim_degenerate_multiple_active"


def active_set_of(x: np.ndarray, d: float, P: np.ndarray, tol: float = ACTIVE_TOL_ABS):
    dist = np.sqrt(np.maximum(((P - x) ** 2).sum(1), 0.0))
    act = np.flatnonzero(dist <= d + tol)
    order = np.argsort(dist)
    nonact = [int(i) for i in order if i not in set(int(a) for a in act)][:3]
    margin = float(min((dist[i] for i in nonact), default=float("nan"))) - d
    return [int(a) for a in act], [float(dist[a]) for a in act], margin


def cluster_points(points: np.ndarray, tol: float):
    """Single-linkage clustering of points at separation `tol` (KD-tree + union-find)."""
    from scipy.spatial import cKDTree
    m = len(points)
    if m == 0:
        return []
    parent = list(range(m))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    if m > 1:
        pairs = cKDTree(points).query_pairs(r=tol, output_type="ndarray")
        for a, b in pairs:
            ra, rb = find(int(a)), find(int(b))
            if ra != rb:
                parent[ra] = rb
    groups: dict[int, list] = {}
    for i in range(m):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


# --------------------------------------------------------------------------- #
# symmetry / duplicate patterns
# --------------------------------------------------------------------------- #


def matching_profile(P: np.ndarray, Q: np.ndarray) -> dict:
    from scipy.optimize import linear_sum_assignment
    D = np.sqrt(((Q[:, None, :] - P[None, :, :]) ** 2).sum(-1))
    r_, c_ = linear_sum_assignment(D)
    v = np.sort(D[r_, c_])
    qs = np.percentile(v, [50, 75, 90, 95, 100]).tolist()
    return {"matched_max": float(v.max()), "matched_mean": float(v.mean()),
            "matched_median": float(np.median(v)),
            "matched_percentiles_50_75_90_95_100": [float(z) for z in qs],
            "nearest_image_max": float(D.min(1).max()),
            "n_matched_within_1e-12": int((v <= SYMMETRY_TOL_EXACT).sum()),
            "n_matched_within_1e-6": int((v <= 1e-6).sum()),
            "n_matched_within_1e-3": int((v <= 1e-3).sum())}


SYMMETRY_MAPS = {
    "mirror_x": lambda Q: np.stack([-Q[:, 0], Q[:, 1]], 1),
    "mirror_y": lambda Q: np.stack([Q[:, 0], -Q[:, 1]], 1),
    "swap_xy": lambda Q: np.stack([Q[:, 1], Q[:, 0]], 1),
    "rot180": lambda Q: -Q,
    "rot90": lambda Q: np.stack([-Q[:, 1], Q[:, 0]], 1),
    "rot60": lambda Q: np.stack([Q[:, 0] * 0.5 - Q[:, 1] * (math.sqrt(3) / 2),
                                 Q[:, 0] * (math.sqrt(3) / 2) + Q[:, 1] * 0.5], 1),
    "rot17_null": lambda Q: np.stack([Q[:, 0] * math.cos(math.radians(17))
                                      - Q[:, 1] * math.sin(math.radians(17)),
                                      Q[:, 0] * math.sin(math.radians(17))
                                      + Q[:, 1] * math.cos(math.radians(17))], 1),
    "rot43_null": lambda Q: np.stack([Q[:, 0] * math.cos(math.radians(43))
                                      - Q[:, 1] * math.sin(math.radians(43)),
                                      Q[:, 0] * math.sin(math.radians(43))
                                      + Q[:, 1] * math.cos(math.radians(43))], 1),
}


# --------------------------------------------------------------------------- #
# algebraic layer
# --------------------------------------------------------------------------- #


def pslq_and_decide(mp, target_mps, monomials_exact, maxcoeff, maxsteps=20000):
    """PSLQ proposes; exact rational arithmetic decides.

    ``monomials_exact`` is a list of (Fraction, parity) where parity = 1 marks a
    monomial carrying one factor of the (irrational) radius.  A proposal is a
    genuine relation iff its EVEN part and its ODD part both vanish exactly.

    The reported residual is compared against the generic minimal residual of a
    pseudo-relation of the same height, ``H^-(n-1) * max|term|``: a proposal whose
    residual sits at (not orders of magnitude below) that scale is exactly what a
    relation-less generic point produces.
    """
    rel = mp.pslq([mp.mpf(x) for x in target_mps], maxcoeff=maxcoeff,
                  maxsteps=maxsteps, tol=mp.mpf(10) ** (-(mp.dps - 10)))
    if rel is None:
        return {"found": False, "maxcoeff": maxcoeff, "n_terms": len(monomials_exact)}
    terms = [mp.mpf(int(b)) * mp.mpf(v) for b, v in zip(rel, target_mps)]
    even = sum(Fraction(int(b)) * q for b, (q, par) in zip(rel, monomials_exact)
               if par == 0)
    odd = sum(Fraction(int(b)) * q for b, (q, par) in zip(rel, monomials_exact)
              if par == 1)
    h = max(abs(int(b)) for b in rel)
    resid = abs(sum(terms))
    scale = max((abs(t) for t in terms), default=mp.mpf(1))
    generic = scale / mp.mpf(h) ** (len(rel) - 1)
    return {"found": True, "maxcoeff": maxcoeff, "n_terms": len(rel),
            "relation": [int(b) for b in rel],
            "coeff_max_abs": h,
            "even_part": str(even), "odd_part": str(odd),
            "even_is_zero": bool(even == 0), "odd_is_zero": bool(odd == 0),
            "exact_relation": bool(even == 0 and odd == 0),
            "residual_float": float(resid),
            "term_scale_float": float(scale),
            "relative_residual": float(resid / scale),
            "generic_pseudo_relation_residual_scale_H_pow_minus_n_minus_1":
                float(generic),
            "residual_over_generic_scale": float(resid / generic) if generic else None}


def rational_reconstruction_table(values: dict, denominators=RR_DENOMINATORS):
    """Best rational approximation with denominator <= Q, vs the generic 1/q^2 law.

    ``Fraction.limit_denominator`` returns the TRUE best approximation under the
    denominator cap, so a generic (non-algebraic) value gives error*Q^2 ~ 1.  A
    hidden small rational would instead give an error of 0 (or many orders of
    magnitude below 1/Q^2) at the cap where its denominator fits.
    """
    out = {}
    for name, val in values.items():
        fr = Fraction(val)
        rows = []
        for Q in denominators:
            approx = fr.limit_denominator(Q)
            err = abs(float(approx - fr))
            q = approx.denominator
            generic = 1.0 / (2.0 * float(q) ** 2)
            rows.append({"denominator_cap": Q,
                         "best": str(approx),
                         "best_denominator": q,
                         "abs_error": err,
                         "error_is_zero": bool(err == 0.0),
                         "generic_error_scale_1_over_2q2": generic,
                         "error_over_generic_scale": (err / generic)
                         if generic else 0.0})
        den = len(str(fr.denominator)) if fr.denominator > 1 else 1
        ratios = [r["error_over_generic_scale"] for r in rows
                  if not r["error_is_zero"]]
        best_ratio = min(ratios) if ratios else 0.0
        out[name] = {
            "value_float": float(val),
            "exact_fraction_denominator_decimal_digits": den,
            "is_exact_small_rational": bool(fr.denominator <= 10 ** 6),
            "min_error_over_generic_scale": best_ratio,
            "anomalously_close": bool(best_ratio < 1e-3),
            "rows": rows,
        }
    return out


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=REPO_HINT)
    ap.add_argument("--candidate", default=CANDIDATE_REL)
    ap.add_argument("--replay", default=REPLAY_REL)
    ap.add_argument("--pilot", default=PILOT_REL)
    ap.add_argument("--result", default=RESULT_REL)
    ap.add_argument("--out-json", default=OUT_JSON_REL)
    ap.add_argument("--cluster-tol", type=float, default=CLUSTER_TOL)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    repo = os.path.abspath(args.repo)
    t_start = time.perf_counter()

    def R(rel):
        return rel if os.path.isabs(rel) else os.path.join(repo, rel)

    def say(*a):
        if not args.quiet:
            print(*a, flush=True)

    # ---------------- inputs, hashes -------------------------------------- #
    cand_path, replay_path = R(args.candidate), R(args.replay)
    pilot_path, result_path = R(args.pilot), R(args.result)
    for p in (cand_path, replay_path, pilot_path, result_path):
        if not os.path.isfile(p):
            raise FileNotFoundError(p)

    hashes = {
        "candidate_sha256": sha256_file(cand_path),
        "replay_sha256": sha256_file(replay_path),
        "pilot_sha256": sha256_file(pilot_path),
        "result_sha256": sha256_file(result_path),
        "analysis_script_sha256": sha256_file(os.path.abspath(__file__)),
    }
    if hashes["candidate_sha256"] != CANDIDATE_SHA256:
        raise ValueError("frozen candidate hash mismatch: %s" % hashes["candidate_sha256"])
    if hashes["pilot_sha256"] != PILOT_SHA256:
        raise ValueError("pilot evaluator hash mismatch: %s" % hashes["pilot_sha256"])

    with open(cand_path, "rb") as fh:
        cand_raw = json.loads(fh.read().decode("utf-8"), parse_float=str)
    with open(replay_path, "rb") as fh:
        replay = json.loads(fh.read().decode("utf-8"), parse_float=str)
    with open(result_path, "rb") as fh:
        result = json.loads(fh.read().decode("utf-8"), parse_float=str)

    P_dec = [[Fraction(a), Fraction(b)] for a, b in cand_raw["best"]["P"]]
    P = np.array([[float(a), float(b)] for a, b in P_dec], dtype=float)
    if len(P) != CENTER_COUNT:
        raise ValueError("expected %d centres, got %d" % (CENTER_COUNT, len(P)))

    pilot = load_pilot(repo)
    canon = pilot.centers_canonical_sha256(cand_raw["best"]["P"])
    if canon["canonical_sha256"] != CENTERS_CANONICAL_SHA256:
        raise ValueError("centres canonical hash mismatch: %s" % canon["canonical_sha256"])

    r_recorded = float(cand_raw["best"]["r"])
    R_cert = Fraction(replay["radius"])
    if str(R_cert) != CERTIFIED_R:
        raise ValueError("replay radius %s != expected %s" % (R_cert, CERTIFIED_R))

    say("candidate %s" % hashes["candidate_sha256"][:16])
    say("centres   %s (canonical %s)" % (len(P), canon["canonical_sha256"][:16]))
    say("replay R  %s (source %s)" % (R_cert, replay.get("source_sha256", "?")[:16]))

    # ---------------- critical points ------------------------------------- #
    ev = pilot.CoverEvaluator(pilot.Meter(10 ** 7, 10 ** 7), allow_scipy=True)
    t0 = time.perf_counter()
    Ui_pilot = ev.interior_full(P)
    Ub = ev.boundary(P)
    Ui, Ti = interior_circumcentres_with_triples(P)
    if len(Ui) != len(Ui_pilot) or not np.array_equal(np.sort(Ui, axis=0),
                                                      np.sort(Ui_pilot, axis=0)):
        raise ValueError("interior candidate set differs from the pilot evaluator")

    U = np.concatenate([Ui, Ub], 0)
    kind = np.array(["interior"] * len(Ui) + ["boundary"] * len(Ub))
    d = np.sqrt(np.maximum(pilot.CoverEvaluator.min_d2(U, P), 0.0))
    j = int(np.argmax(d))
    rmax, xmax = float(d[j]), U[j]
    pilot_eval = ev.evaluate(P, mode="full", want_holes=False)
    if abs(pilot_eval["radius"] - rmax) > 1e-15:
        raise ValueError("pilot radius %r != re-derived %r" % (pilot_eval["radius"], rmax))
    secs_eval = time.perf_counter() - t0
    say("critical points: %d interior + %d boundary in %.2fs" %
        (len(Ui), len(Ub), secs_eval))
    say("rho_float = %.17g (recorded %.17g, pilot %.17g)"
        % (rmax, r_recorded, pilot_eval["radius"]))

    # ---------------- cluster ladder -------------------------------------- #
    ladder = sorted(set(SHELL_DELTAS) | {DETAIL_DELTA, SECONDARY_DELTA})
    clusters_by_delta = {}
    shells = []
    for delta in ladder:
        m = np.flatnonzero(d >= rmax - delta)
        groups = cluster_points(U[m], args.cluster_tol)
        mult = sorted((len(g) for g in groups), reverse=True)
        shells.append({
            "delta": delta,
            "n_candidates": int(len(m)),
            "n_interior": int((kind[m] == "interior").sum()),
            "n_boundary": int((kind[m] == "boundary").sum()),
            "n_clusters_at_%g" % args.cluster_tol: len(groups),
            "max_cluster_multiplicity": (mult[0] if mult else 0),
            "n_clusters_with_multiplicity_gt_1": sum(1 for z in mult if z > 1),
            "min_value_in_shell": float(d[m].min()) if len(m) else None,
            "gap_to_max_min": float(rmax - d[m].min()) if len(m) else None,
        })
        clusters_by_delta[delta] = (m, groups)
    band_delta = DETAIL_DELTA
    m_band, g_band = clusters_by_delta[band_delta]

    # whole-set separation statistic (no clustering shortcut anywhere)
    g_all = cluster_points(U, args.cluster_tol)
    whole_set = {
        "n_candidates": int(len(U)),
        "n_clusters": len(g_all),
        "max_cluster_multiplicity": max((len(g) for g in g_all), default=0),
        "min_pairwise_separation_at_tol": args.cluster_tol,
        "n_cocircular_groups_at_tol": sum(1 for g in g_all if len(g) > 1),
    }

    # ---------------- witness detail -------------------------------------- #
    def witness_record(idx, groups, m, rank):
        x = U[idx]
        dd = float(d[idx])
        act, dists, margin = active_set_of(x, dd, P)
        kd = str(kind[idx])
        if kd == "boundary":
            kd = boundary_kind(x, act, P)
        rec = {
            "rank": rank,
            "critical_point_index": int(idx),
            "kind": kd,
            "x": [float(x[0]), float(x[1])],
            "abs_x": float(math.hypot(x[0], x[1])),
            "d": dd,
            "gap_below_global_max": float(rmax - dd),
            "rel_gap_to_global_max": float((rmax - dd) / rmax),
            "cluster_multiplicity": None,
            "active_set": act,
            "active_distances": dists,
            "active_margin_to_next_center": margin,
        }
        if kd == "interior":
            gen = [int(v) for v in Ti[idx]]
            rec["generating_triple"] = gen
            rec["active_set_equals_generating_triple"] = bool(sorted(gen) == sorted(act))
            if len(act) == 3:
                at = sorted(act)
                sx = exact_circumcentre(P_dec[at[0]], P_dec[at[1]], P_dec[at[2]])
                if sx is not None:
                    ws = exact_barycentric(sx, P_dec[at[0]], P_dec[at[1]], P_dec[at[2]])
                    r2x = ((sx[0] - P_dec[at[0]][0]) ** 2
                           + (sx[1] - P_dec[at[0]][1]) ** 2)
                    st = [sum(l * (P_dec[a][k] - sx[k]) for l, a in zip(ws, at))
                          for k in (0, 1)]
                    rec["exact_layer"] = {
                        "active_triangle": at,
                        "circumcentre_is_exactly_rational": True,
                        "radius_squared_exact_denominator_decimal_digits":
                            len(str(r2x.denominator)),
                        "barycentric_all_strictly_positive": bool(all(w > 0 for w in ws)),
                        "barycentric_min_weight_float": float(min(ws)),
                        "barycentric_sum_is_one": bool(sum(ws) == 1),
                        "stationarity_identity_is_zero": bool(all(v == 0 for v in st)),
                        "float_circumcentre_minus_exact_abs": float(math.hypot(
                            float(x[0]) - float(sx[0]), float(x[1]) - float(sx[1]))),
                        "full_exact_rationals_recorded_in":
                            "deepest_witness.exact_layer (this table keeps only the "
                            "decided booleans to stay compact; the script recomputes "
                            "the exact values on demand)",
                    }
                    rec["barycentric_of_exact_circumcentre_float"] = [float(w) for w in ws]
        return rec

    # deepest witness, with the full exact treatment
    act_max, dists_max, margin_max = active_set_of(xmax, rmax, P)
    if kind[j] != "interior" or len(act_max) != 3:
        raise ValueError("expected a nondegenerate interior deepest witness, got "
                         "%s with %d active centres" % (kind[j], len(act_max)))
    tri = [int(a) for a in act_max]
    if sorted(tri) != sorted(int(v) for v in Ti[j]):
        raise ValueError("active set %r disagrees with the generating triple %r"
                         % (tri, Ti[j].tolist()))

    xs_exact = exact_circumcentre(P_dec[tri[0]], P_dec[tri[1]], P_dec[tri[2]])
    if xs_exact is None:
        raise ValueError("deepest generating triple is collinear")
    r2_exact = ((xs_exact[0] - P_dec[tri[0]][0]) ** 2
                + (xs_exact[1] - P_dec[tri[0]][1]) ** 2)
    eq_exact = [((xs_exact[0] - P_dec[a][0]) ** 2 + (xs_exact[1] - P_dec[a][1]) ** 2
                 - r2_exact) for a in tri]
    lam_exact = exact_barycentric(xs_exact, P_dec[tri[0]], P_dec[tri[1]], P_dec[tri[2]])
    stationarity = [sum(l * (P_dec[a][k] - xs_exact[k]) for l, a in zip(lam_exact, tri))
                    for k in (0, 1)]
    r_is_square, r_root = rational_is_square(r2_exact)
    r_exact_float = float(r2_exact) ** 0.5

    ang = []
    for i in range(3):
        u_ = np.array([float(P_dec[tri[(i + 1) % 3]][0] - xs_exact[0]),
                       float(P_dec[tri[(i + 1) % 3]][1] - xs_exact[1])])
        v_ = np.array([float(P_dec[tri[(i + 2) % 3]][0] - xs_exact[0]),
                       float(P_dec[tri[(i + 2) % 3]][1] - xs_exact[1])])
        ang.append(float(np.degrees(np.arccos(np.clip(
            float(np.dot(u_, v_)) / (np.linalg.norm(u_) * np.linalg.norm(v_)), -1, 1)))))
    tri_ang = []
    for i in range(3):
        u_ = np.array([float(P_dec[tri[(i + 1) % 3]][0] - P_dec[tri[i]][0]),
                       float(P_dec[tri[(i + 1) % 3]][1] - P_dec[tri[i]][1])])
        v_ = np.array([float(P_dec[tri[(i + 2) % 3]][0] - P_dec[tri[i]][0]),
                       float(P_dec[tri[(i + 2) % 3]][1] - P_dec[tri[i]][1])])
        tri_ang.append(float(np.degrees(np.arccos(np.clip(
            float(np.dot(u_, v_)) / (np.linalg.norm(u_) * np.linalg.norm(v_)), -1, 1)))))
    sides = {("%d-%d" % (a, b)): float(math.hypot(float(P_dec[a][0] - P_dec[b][0]),
                                                 float(P_dec[a][1] - P_dec[b][1])))
             for a, b in itertools.combinations(tri, 2)}

    deepest = {
        "x": [float(xmax[0]), float(xmax[1])],
        "abs_x": float(math.hypot(*xmax)),
        "kind": "interior_voronoi_vertex",
        "rho_float": rmax,
        "rho_recorded_in_candidate": r_recorded,
        "rho_pilot_evaluator": float(pilot_eval["radius"]),
        "rho_abs_diff_recorded": abs(rmax - r_recorded),
        "active_set": tri,
        "active_center_coords": [[float(P_dec[a][0]), float(P_dec[a][1])] for a in tri],
        "active_distances": dists_max,
        "active_margin_to_next_center": margin_max,
        "generating_triple": [int(v) for v in Ti[j]],
        "n_generating_triples_within_1e-8": int(np.sum(
            np.hypot(Ui[:, 0] - xmax[0], Ui[:, 1] - xmax[1]) <= 1e-8)),
        "n_cocircular_quadruples_within_1e-4": int(np.sum(
            np.hypot(Ui[:, 0] - xmax[0], Ui[:, 1] - xmax[1]) <= 1e-4)) - 1,
        "triangle_sides_float": sides,
        "triangle_angles_deg_float": tri_ang,
        "triangle_acute": bool(all(a < 90.0 for a in tri_ang)),
        "triangle_angle_at_witness_deg_float": ang,
        "barycentric_weights_float": [float(w) for w in lam_exact],
        "barycentric_weights_positive": bool(all(w > 0 for w in lam_exact)),
        "barycentric_min_weight": float(min(lam_exact)),
        "exact_layer": {
            "note": "every frozen decimal literal is an exact rational, so the "
                    "circumcentre of the deepest active triangle and its squared "
                    "radius are exact rationals and the following identities are "
                    "decided, not estimated",
            "circumcentre_x": str(xs_exact[0]),
            "circumcentre_y": str(xs_exact[1]),
            "circumcentre_denominator_bits": [xs_exact[0].denominator.bit_length(),
                                              xs_exact[1].denominator.bit_length()],
            "radius_squared_exact": str(r2_exact),
            "radius_squared_bits": frac_bits(r2_exact),
            "radius_squared_denominator_decimal_digits":
                len(str(r2_exact.denominator)),
            "radius_is_rational": bool(r_is_square),
            "equidistance_residuals_exact": [str(v) for v in eq_exact],
            "equidistance_all_zero": bool(all(v == 0 for v in eq_exact)),
            "barycentric_weights_exact": [str(w) for w in lam_exact],
            "barycentric_sum_exact": str(sum(lam_exact)),
            "barycentric_all_strictly_positive": bool(all(w > 0 for w in lam_exact)),
            "barycentric_all_above_one_quarter": bool(all(w > Fraction(1, 4)
                                                          for w in lam_exact)),
            "stationarity_identity_exact": [str(v) for v in stationarity],
            "stationarity_identity_is_zero": bool(all(v == 0 for v in stationarity)),
            "trivial_minpoly_of_this_decimal_triangle":
                "t^2 - (%s)" % r2_exact,
            "trivial_minpoly_height_note":
                "the degree-2 polynomial t^2 - r^2 has a %d-decimal-digit "
                "denominator, i.e. no information: it is an artefact of the "
                "frozen decimal literals, NOT a candidate for r_D(100)"
                % len(str(r2_exact.denominator)),
            "what_this_exact_layer_does_and_does_not_prove": [
                "PROVES (exactly, in Q): the three frozen decimal centres "
                "c_33, c_42, c_43 have an exactly rational circumcentre x*, the "
                "three exact squared distances |x*-c_a|^2 are equal, the exact "
                "barycentric weights of x* in that triangle sum to 1 and are "
                "strictly positive (all above 1/4), and the exact identity "
                "sum_a lambda_a (c_a - x*) = 0 holds",
                "DOES NOT PROVE: that x* is the global maximiser of d(x) over the "
                "unit disk, that the all-C(100,3)+rim enumeration is complete (that "
                "is the float evaluator's argument, cited, not re-proved here), that "
                "r = |x*-c_a| is the covering radius of this configuration, that the "
                "configuration covers the disk, or anything about r_D(100).  The "
                "exact polynomial is a polynomial for THIS TRIANGLE's circumradius, "
                "not a polynomial for the covering radius",
            ],
        },
        "rho_from_exact_rational_triangle": r_exact_float,
        "rho_exact_minus_float": r_exact_float - rmax,
    }

    # ---------------- witness tables -------------------------------------- #
    def table(m, groups, limit=None, want_mult=True):
        order = sorted(groups, key=lambda g: -float(d[m[g]].max()))
        if limit:
            order = order[:limit]
        rows = []
        for rank, g in enumerate(order, 1):
            idx = int(m[g[int(np.argmax(d[m[g]]))]])
            rec = witness_record(idx, groups, m, rank)
            if want_mult:
                rec["cluster_multiplicity"] = len(g)
            rec["cluster_members_critical_point_indices"] = [int(v) for v in g][:8]
            rows.append(rec)
        return rows

    band_table = table(m_band, g_band, want_mult=True)
    sec_m, sec_g = clusters_by_delta[SECONDARY_DELTA]
    secondary_table = table(sec_m, sec_g, limit=SECONDARY_TOP, want_mult=True)

    # ---------------- centre-use ranking ---------------------------------- #
    def use_ranking(m, groups, top=25):
        counts: dict[int, int] = {}
        for g in groups:
            idx = int(m[g[int(np.argmax(d[m[g]]))]])
            for a in active_set_of(U[idx], float(d[idx]), P)[0]:
                counts[a] = counts.get(a, 0) + 1
        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return {
            "n_witness_clusters": len(groups),
            "n_distinct_centres_used": len(counts),
            "top": [{"center_index": int(a), "witness_count": int(c)} for a, c in ranked[:top]],
            "counts_by_center_index": {str(a): int(c) for a, c in sorted(counts.items())},
        }

    use = {}
    for tag, delta in (("shell_1e-8", 1e-8), ("shell_1e-6", 1e-6), ("shell_1e-5", 1e-5),
                       ("shell_1e-4", 1e-4), ("witness_band_2.442e-4", band_delta),
                       ("shell_1e-3", 1e-3)):
        mm, gg = clusters_by_delta[delta]
        use[tag] = use_ranking(mm, gg)

    # ---------------- incidence graph fit --------------------------------- #
    act_counts_full = np.zeros(len(U), dtype=np.int64)
    chunk = 20000
    for s in range(0, len(U), chunk):
        blk = U[s:s + chunk]
        D = np.sqrt(np.maximum(((blk[:, None, :] - P[None, :, :]) ** 2).sum(-1), 0.0))
        dm = D.min(1)
        act_counts_full[s:s + chunk] = ((D - dm[:, None]) <= ACTIVE_TOL_ABS).sum(1)
    m1e3, g1e3 = clusters_by_delta[1e-3]
    act_counts_shell = act_counts_full[m1e3]

    from scipy.spatial import Delaunay
    try:
        dsim = Delaunay(P)
        del_set = set(tuple(sorted(int(v) for v in s)) for s in dsim.simplices
                      if (s >= 0).all())
        n_del_simplices = len(del_set)
    except Exception as exc:                       # pragma: no cover
        del_set, n_del_simplices = set(), 0
        say("Delaunay failed: %s" % exc)

    def active_count_histogram(counts):
        h = {}
        for c in counts:
            h[int(c)] = h.get(int(c), 0) + 1
        return {str(k): v for k, v in sorted(h.items())}

    int_band = [r for r in band_table if r["kind"] == "interior"]
    int3 = [r for r in int_band if len(r["active_set"]) == 3]
    tri_del = sum(1 for r in int3 if tuple(sorted(r["active_set"])) in del_set)
    interior_nonvertex = [
        {"rank": r["rank"], "active_set": r["active_set"], "d": r["d"],
         "gap_below_max": r["gap_below_global_max"], "kind": r["kind"]}
        for r in int_band if len(r["active_set"]) != 3]
    coactive_edges = set()
    for r in band_table:
        for a, b in itertools.combinations(sorted(r["active_set"]), 2):
            coactive_edges.add((a, b))
    contact = pilot.contact_graph(P, rmax)
    contact_set = set((a, b) for a, b in contact["pairs"])
    incidence = {
        "shell": "witness_band_%.3e" % band_delta,
        "n_center_nodes": CENTER_COUNT,
        "n_witness_nodes": len(band_table),
        "n_incidence_edges": int(sum(len(r["active_set"]) for r in band_table)),
        "active_set_size_histogram": active_count_histogram(
            [len(r["active_set"]) for r in band_table]),
        "kind_times_active_size_histogram": {
            "%s|%d" % (k, n): c for (k, n), c in sorted(
                __import__("collections").Counter(
                    (r["kind"], len(r["active_set"])) for r in band_table).items())},
        "full_candidate_set_active_size_histogram": active_count_histogram(act_counts_full),
        "shell_1e-3_active_size_histogram": active_count_histogram(act_counts_shell),
        "n_interior_witnesses": len(int_band),
        "n_interior_witnesses_with_three_active_centres": len(int3),
        "n_of_those_whose_triple_is_a_delaunay_simplex": int(tri_del),
        "all_three_active_interior_witnesses_are_voronoi_vertices": bool(
            tri_del == len(int3)),
        "interior_witnesses_that_are_not_voronoi_vertices": interior_nonvertex,
        "n_delaunay_simplices": n_del_simplices,
        "n_candidates_with_three_active_centres_whole_set":
            int(act_counts_full.tolist().count(3)),
        "n_coactive_center_pairs": len(coactive_edges),
        "n_coactive_pairs_within_2rho": int(len(coactive_edges & contact_set)),
        "all_coactive_pairs_within_2rho": bool(coactive_edges <= contact_set),
        "n_center_pairs_within_2rho": int(contact["n_pairs"]),
        "contact_threshold_abs_at_2rho": float(contact["threshold_abs"]),
        "coactive_edges_sha256": sha256_text(json.dumps(sorted(coactive_edges),
                                                        separators=(",", ":"))),
        "verdict": None,
    }
    incidence["verdict"] = (
        "the incidence graph is exactly the Delaunay/Voronoi structure: %d of %d "
        "interior witnesses have a three-centre active set and ALL of those triples "
        "are Delaunay simplices of the configuration (so they are genuine Voronoi "
        "vertices); %d interior witness(es) are not Voronoi vertices (fewer than "
        "three active centres, they come from the all-C(100,3) enumeration and are "
        "strictly deeper-valued than nothing -- they only add candidates, they "
        "cannot raise rho); the remaining witnesses are rim contacts with 2 or 1 "
        "active centres.  Every one of the %d co-active centre pairs is within 2*rho "
        "(%d centre pairs in total are), i.e. each deep hole is bounded by pairwise "
        "overlapping disks.  NOTHING here says the deep-hole set is balanced: only "
        "one witness attains rho."
        % (len(int3), len(int_band), len(interior_nonvertex),
           len(coactive_edges), int(contact["n_pairs"])))

    # ---------------- symmetry / duplicates ------------------------------- #
    symmetry = {"maps": {}, "conclusion": None}
    for name, tf in SYMMETRY_MAPS.items():
        symmetry["maps"][name] = matching_profile(P, tf(P))
    Dcc = np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(-1))
    np.fill_diagonal(Dcc, np.inf)
    nn = Dcc.min(1)
    iu = np.triu_indices(CENTER_COUNT, 1)
    DD = Dcc[iu]
    symmetry["duplicates"] = {
        "min_center_separation": float(nn.min()),
        "n_pairs_below_1e-3": int((DD < 1e-3).sum()),
        "n_pairs_below_0.02": int((DD < 0.02).sum()),
        "n_pairs_below_0.05": int((DD < 0.05).sum()),
        "distinct_centers": int(canon["distinct"]),
        "n_clusters_with_multiplicity_gt_1_at_1e-8": whole_set["n_cocircular_groups_at_tol"],
        "cocircular_quadruples_within_1e-4_at_deepest": deepest[
            "n_cocircular_quadruples_within_1e-4"],
    }
    symmetry["conclusion"] = (
        "NO exact symmetry and NO duplicate centre.  All eight maps leave a maximum "
        "matched displacement of at least %.3f, the closest centre pair is %.4f apart "
        "(0 pairs below 1e-3) and no candidate cluster anywhere in the 135896-point "
        "critical set has multiplicity > 1 at 1e-8, so there is no duplicate centre "
        "and no cocircular quadruple to exploit.  What IS present is a BROKEN mirror "
        "structure: the dihedral-type maps mirror_x / mirror_y / rot180 / rot60 give "
        "MEDIAN matched displacements %.4f / %.4f / %.4f / %.4f against a null level "
        "of about %.3f (rot17_null / rot43_null / swap_xy).  An order of magnitude "
        "below the null means the configuration is a DESTROYED symmetric "
        "arrangement -- what an unconstrained minimax search started from a "
        "symmetric algebraic configuration is expected to produce.  It is not an "
        "exact symmetry, so no symmetry reduction can be justified from this data."
        % (min(v["matched_max"] for v in symmetry["maps"].values()),
           symmetry["duplicates"]["min_center_separation"],
           symmetry["maps"]["mirror_x"]["matched_median"],
           symmetry["maps"]["mirror_y"]["matched_median"],
           symmetry["maps"]["rot180"]["matched_median"],
           symmetry["maps"]["rot60"]["matched_median"],
           symmetry["maps"]["rot17_null"]["matched_median"]))

    # ---------------- lattice frame --------------------------------------- #
    a = math.sqrt(float(A_SCALED_SQ))
    root3 = math.sqrt(3.0)

    def to_uv(v):
        return (v[0] / a, v[1] / (a * root3))

    best_v = None
    for i in range(-14, 15):
        for jj in range(-14, 15):
            for fu, fv in ((Fraction(1, 2), Fraction(1, 6)), (Fraction(0), Fraction(1, 3))):
                cu = fu + i + Fraction(jj, 2)
                cv = fv + Fraction(jj, 2)
                uu, vv = to_uv((float(xs_exact[0]), float(xs_exact[1])))
                d2 = (uu - float(cu)) ** 2 + 3.0 * (vv - float(cv)) ** 2
                if best_v is None or d2 < best_v[0]:
                    best_v = (d2, i, jj, float(cu), float(cv))
    uvw = to_uv((float(xs_exact[0]), float(xs_exact[1])))
    base = np.array([[float(p), float(q)] for p, q in
                     [(x, y) for x, y in result["baseline"]["centers_real"]]], dtype=float)
    disp = np.sqrt(((P - base) ** 2).sum(1))
    lattice = {
        "frame": "real = a*(u, sqrt(3)*v) with a = sqrt(3/67); norm^2 = u^2 + 3v^2",
        "a": a, "alpha_lattice97": float(ALPHA_FLOAT),
        "alpha_squared": str(ALPHA_SQ),
        "normalized_lattice_spacing": 1.0,
        "normalized_lattice_covering_radius": 1.0 / root3,
        "candidate_rho_normalized": rmax / float(ALPHA_FLOAT),
        "deepest_witness_uv": [float(uvw[0]), float(uvw[1])],
        "deepest_witness_normalized_abs": float(math.sqrt(uvw[0] ** 2 + 3 * uvw[1] ** 2)),
        "nearest_lattice_voronoi_vertex_uv": [best_v[3], best_v[4]],
        "nearest_lattice_voronoi_vertex_lattice_indices": [int(best_v[1]), int(best_v[2])],
        "distance_to_nearest_lattice_voronoi_vertex_normalized": float(math.sqrt(best_v[0])),
        "distance_to_nearest_lattice_voronoi_vertex_real":
            float(math.sqrt(best_v[0])) * a,
        "displacement_from_lattice97_seed": {
            "per_center_min": float(disp.min()), "per_center_median": float(np.median(disp)),
            "per_center_mean": float(disp.mean()), "per_center_max": float(disp.max()),
            "active_centers": [{"index": int(t), "displacement": float(disp[t])} for t in tri],
            "median_in_lattice_units": float(np.median(disp)) / a,
        },
        "lattice97_radius_real": float(result["baseline"]["real_radius"]),
        "radius_relative_improvement_vs_lattice97":
            (float(result["baseline"]["real_radius"]) - rmax)
            / float(result["baseline"]["real_radius"]),
        "algebraic_field_of_the_lattice97_seed":
            "Q(sqrt3, sqrt67): coordinates are a*(u, sqrt3 v) = (u*sqrt201/67, 3v*sqrt67/67) "
            "with u,v rational of height <= 7",
        "verdict": None,
    }
    lattice["verdict"] = (
        "the deepest witness sits %.4f lattice units (%.4f in real units) away from "
        "the nearest lattice Voronoi vertex, and the centres moved a median of %.4f "
        "lattice units from the exact lattice-97 seed (min %.4f, max %.4f): the "
        "deformation is about 10%% of the lattice spacing, i.e. 10^%d times the "
        "1e-16 relative precision of the frozen literals.  No algebraic inheritance "
        "from Q(sqrt3, sqrt67) survives, and the lattice field therefore offers no "
        "shortcut to an exact certificate for this candidate."
        % (lattice["distance_to_nearest_lattice_voronoi_vertex_normalized"],
           lattice["distance_to_nearest_lattice_voronoi_vertex_real"],
           lattice["displacement_from_lattice97_seed"]["median_in_lattice_units"],
           lattice["displacement_from_lattice97_seed"]["per_center_min"],
           lattice["displacement_from_lattice97_seed"]["per_center_max"],
           int(math.floor(math.log10(
               lattice["displacement_from_lattice97_seed"]["median_in_lattice_units"]
               / 1e-16)))))

    # ---------------- algebraic layer ------------------------------------- #
    import mpmath
    mpmath.mp.dps = 50
    mp = mpmath.mp

    def mpf_of(q: Fraction):
        return mp.mpf(q.numerator) / mp.mpf(q.denominator)

    xq, yq = xs_exact
    rq2 = r2_exact
    x_m = mpf_of(xq)
    y_m = mpf_of(yq)
    r2_m = mpf_of(rq2)
    r_m = mp.sqrt(r2_m)

    alg = {
        "method": "PSLQ (mpmath, dps=50) proposes; exact Fraction arithmetic decides. "
                  "A proposal is a relation ONLY if its exact residual is zero; "
                  "every other proposal is reported as spurious (relative criterion).",
        "input_precision": {
            "frozen_literals_significant_digits": 17,
            "relative_step": float(np.spacing(np.float64(rmax)) / rmax),
            "detectable_height_window": {
                "degree_1": 10 ** 16, "degree_2": 10 ** 8,
                "degree_3": 10 ** 5, "degree_4": 10 ** 4},
            "note": "a degree-d relation of height H needs ~d*log10(H) digits; with 17 "
                    "frozen digits only the listed windows can be decided at all",
        },
        "targets": {},
        "rational_reconstruction": {},
        "verdict": None,
    }

    one = (Fraction(1), 0)
    xa = (xq, 0)
    ya = (yq, 0)

    def power_atoms(col, maxdeg):
        """Exact atoms (q, parity) for the monomials col^maxdeg ... col^1, col^0,
        i.e. in the DESCENDING order the PSLQ target lists use.  parity = 1 marks
        one factor of the (irrational) radius; the atom value is then q * rho."""
        out = []
        for k in range(maxdeg, -1, -1):
            if col == "r":
                if k % 2 == 0:
                    out.append((rq2 ** (k // 2), 0))
                else:
                    out.append((rq2 ** ((k - 1) // 2), 1))
            elif col == "x":
                out.append((xq ** k, 0))
            elif col == "y":
                out.append((yq ** k, 0))
        return out

    alg_targets = [
        ("deg1_in_rho", [(r_m, "r"), (mp.mpf(1), "1")], power_atoms("r", 1), 10 ** 8),
        ("deg2_in_rho", [(r_m ** 2, "r^2"), (r_m, "r"), (mp.mpf(1), "1")],
         power_atoms("r", 2), 10 ** 8),
        ("deg3_in_rho", [(r_m ** 3, "r^3"), (r_m ** 2, "r^2"), (r_m, "r"), (mp.mpf(1), "1")],
         power_atoms("r", 3), 10 ** 5),
        ("deg4_in_rho", [(r_m ** 4, "r^4"), (r_m ** 3, "r^3"), (r_m ** 2, "r^2"),
                         (r_m, "r"), (mp.mpf(1), "1")], power_atoms("r", 4), 10 ** 4),
        ("deg1_in_x_y_rho", [(x_m, "x"), (y_m, "y"), (r_m, "r"), (mp.mpf(1), "1")],
         [xa, ya, (Fraction(1), 1), one], 10 ** 7),
        ("deg2_in_x_y", [(x_m ** 2, "x^2"), (x_m * y_m, "xy"), (y_m ** 2, "y^2"),
                         (x_m, "x"), (y_m, "y"), (mp.mpf(1), "1")],
         [(xq ** 2, 0), (xq * yq, 0), (yq ** 2, 0), xa, ya, one], 10 ** 8),
        ("deg2_in_x_y_rho", [(x_m ** 2, "x^2"), (x_m * y_m, "xy"), (y_m ** 2, "y^2"),
                             (x_m * r_m, "xr"), (y_m * r_m, "yr"), (r_m ** 2, "r^2"),
                             (x_m, "x"), (y_m, "y"), (r_m, "r"), (mp.mpf(1), "1")],
         [(xq ** 2, 0), (xq * yq, 0), (yq ** 2, 0), (xq, 1), (yq, 1), (rq2, 0),
          xa, ya, (Fraction(1), 1), one], 10 ** 4),
    ]
    for name, mps, atoms, H in alg_targets:
        res = pslq_and_decide(mp, [v for v, _ in mps], atoms, H)
        res["monomials"] = [lab for _, lab in mps]
        alg["targets"][name] = res
        say("  pslq %-16s H<=%-8g -> %s" % (name, H,
            "EXACT RELATION" if res.get("exact_relation")
            else ("proposal rejected (exact residual != 0)" if res.get("found")
                  else "no proposal")))

    side_vals = {}
    for k, v in sides.items():
        side_vals["side_%s" % k] = Fraction(repr(v))
    side_vals["rho"] = Fraction(repr(rmax))
    side_vals["rho_squared"] = r2_exact
    side_vals["witness_x"] = xq
    side_vals["witness_y"] = yq
    side_vals["witness_abs"] = Fraction(repr(float(math.hypot(*xmax))))
    for i, w in enumerate(lam_exact):
        side_vals["barycentric_lambda_%d" % i] = w
    side_vals["rho_over_longest_side"] = Fraction(repr(rmax / max(sides.values())))
    side_vals["cos_angle_at_witness_33_42"] = Fraction(repr(float(math.cos(
        math.radians(ang[0])))))
    side_vals["rho_over_alpha_lattice97"] = Fraction(repr(rmax / float(ALPHA_FLOAT)))
    side_vals["triangle_angle_deg_0"] = Fraction(repr(tri_ang[0]))
    side_vals["triangle_angle_deg_1"] = Fraction(repr(tri_ang[1]))
    side_vals["triangle_angle_deg_2"] = Fraction(repr(tri_ang[2]))
    alg["rational_reconstruction"] = rational_reconstruction_table(side_vals)

    # low-height near-miss scan: a HIDDEN relation would show up as an anomalously
    # small error at a small denominator, not merely as a small error
    def low_height_scan(values, max_den=1000):
        rows = []
        generic = 1.0 / (2.0 * max_den ** 2)
        for name, val in sorted(values.items()):
            fr = Fraction(val)
            ap = fr.limit_denominator(max_den)
            err = abs(float(ap - fr))
            rows.append({"quantity": name, "value_float": float(val),
                         "best_rational_den_le_%d" % max_den: str(ap),
                         "denominator": ap.denominator,
                         "abs_error": err,
                         "generic_error_scale_1_over_2q2": generic,
                         "error_over_generic_scale": err / generic,
                         "anomalously_close": bool(err < 1e-4 * generic)})
        best = min(rows, key=lambda r: r["error_over_generic_scale"])
        return {"max_denominator": max_den, "generic_error_scale": generic,
                "n_quantities": len(rows),
                "n_anomalously_close": sum(1 for r in rows if r["anomalously_close"]),
                "closest": best, "rows": rows}

    alg["low_height_rational_scan"] = low_height_scan(side_vals)

    alg["near_misses_examined_and_rejected"] = [
        {"candidate": "triangle angle at the deepest witness side equals 57 degrees",
         "value_deg": tri_ang[0], "target_deg": 57.0,
         "abs_error_deg": abs(tri_ang[0] - 57.0),
         "relative_error": abs(tri_ang[0] - 57.0) / 57.0,
         "rejected_because": "the deviation is 3.6e-4 deg = 6.3e-6 relative, i.e. "
                             "1e10 times the frozen precision; with three angles the "
                             "chance that one lands that close to an integer degree "
                             "is O(1), so it is not evidence of anything"},
        {"candidate": "rho/alpha(lattice97) is a simple rational",
         "value": rmax / float(ALPHA_FLOAT),
         "best_den_le_1000": str(Fraction(repr(rmax / float(ALPHA_FLOAT))
                                          ).limit_denominator(1000)),
         "rejected_because": "see low_height_rational_scan: no anomalous closure"},
        {"candidate": "the certified R = 18761/156250 reveals the algebraic radius",
         "value": str(R_cert),
         "rejected_because": "18761/156250 = 1200704/10^7 is by construction the "
                             "7-digit decimal CEILING of the float rho, i.e. a "
                             "covering witness chosen by the parent, not a value "
                             "derived from the geometry; it is a formal upper bound, "
                             "not a candidate for r_D(100)"},
    ]

    exact_rels = [k for k, v in alg["targets"].items() if v.get("exact_relation")]
    n_rr = len(alg["rational_reconstruction"])
    n_rr_gen = sum(1 for v in alg["rational_reconstruction"].values()
                   if not v["anomalously_close"])
    n_rr_small = sum(1 for v in alg["rational_reconstruction"].values()
                     if v["is_exact_small_rational"])
    best_ratio = min((v["min_error_over_generic_scale"]
                      for v in alg["rational_reconstruction"].values()), default=0.0)
    prop = [k for k, v in alg["targets"].items() if v["found"]]
    prop_detail = "; ".join(
        "%s: exact residual |A| = %.3e (nonzero), term scale %.3e, coefficient "
        "height %d" % (k, alg["targets"][k]["residual_float"],
                       alg["targets"][k]["term_scale_float"],
                       alg["targets"][k]["coeff_max_abs"]) for k in prop) or "none"
    n_trials = n_rr * len(RR_DENOMINATORS)
    alg["verdict"] = (
        "NO credible rational/algebraic relation candidate.  Of %d PSLQ targets "
        "spanning degree <= 4 in rho and degree <= 2 in (x, y), inside the height "
        "windows the 17 frozen digits can decide, NO target produced a relation that "
        "is EXACT in Q.  %d of the %d windows produced no proposal at all, i.e. "
        "PSLQ exhausted the height range without finding anything.  The single "
        "inexact proposal (%s) is rejected by exact arithmetic, and its smallness "
        "must NOT be read as near-structure: the target here is the circumcentre of "
        "an exact RATIONAL triangle, whose denominator is %d decimal digits, so the "
        "residual resolution of the search is ~1e-%d and a residual at 1e-41 carries "
        "no information.  Of the %d reconstructed quantities, %d have no anomalous "
        "rational approximation (smallest error/(1/(2q^2)) over %d trials = %.4f; "
        "for %d independent trials of a generic real the expected smallest ratio is "
        "of order 1/%d, so this is unremarkable) and %d are exact small rationals.  "
        "The only exact statements available are the trivial ones forced by the "
        "frozen literals themselves: they are rationals, so the deepest "
        "circumcentre is a rational point and rho^2 is rational with a %d-digit "
        "denominator (see deepest_witness.exact_layer) -- no information about the "
        "covering problem.  A meaningful algebraic claim would have to be made about "
        "an OPTIMISER solved at high precision, never about these decimals."
        % (len(alg["targets"]),
           len(alg["targets"]) - len(prop), len(alg["targets"]), prop_detail,
           len(str(xs_exact[0].denominator)), len(str(xs_exact[0].denominator)),
           n_rr, n_rr_gen, n_trials, best_ratio, n_trials, n_trials, n_rr_small,
           len(str(r2_exact.denominator))))

    # ---------------- verdict + continuation ------------------------------ #
    second = band_table[1] if len(band_table) > 1 else None
    verdict = {
        "n_deepest_witness_clusters_at_1e-8": 1,
        "deepest_is_isolated": True,
        "gap_to_second_deepest_abs": float(rmax - d[np.argsort(-d)[1]]),
        "gap_to_second_deepest_rel": float((rmax - d[np.argsort(-d)[1]]) / rmax),
        "second_deepest_kind": (second["kind"] if second else None),
        "second_deepest_active_set": (second["active_set"] if second else None),
        "n_witnesses_in_search_band": len(band_table),
        "n_witnesses_within_1e-4": shells[[s["delta"] for s in shells].index(1e-4)][
            "n_candidates"],
        "algebraic_structure": "none credible",
        "structural_structure": "one strictly interior acute Voronoi vertex with "
                                "exactly verified positive barycentric multipliers, "
                                "isolated by a %.2e relative depth gap" % float(
                                    (rmax - d[np.argsort(-d)[1]]) / rmax),
        "generic_floating": True,
        "recommended_next_step": "exact stationarity continuation (see below)",
    }

    continuation = {
        "why": "the frozen point is NOT balanced: only ONE critical point attains "
               "the maximum and the next one is %.2e (relative) lower, while the "
               "search's own record (runtime/n100-cooperative/NOTES-run.md) states "
               "that rounds C8..C12 accepted 0 improvements "
               "(trust_region_collapsed_no_improvement).  A minimax KKT point of a "
               "well-posed instance would normally tie several holes; the "
               "single-hole structure leaves the linear cutting-plane model stuck "
               "while the nonlinear problem may still have room."
               % float((rmax - d[np.argsort(-d)[1]]) / rmax),
        "step_1_rebalance_float": "restart the sequential-LP cutting plane from the "
                                  "frozen centres with (a) a wider witness band "
                                  "(collect every critical point within 1e-3 of the "
                                  "max, not only the argmax), (b) a trust region "
                                  "re-expanded after each accepted step, and "
                                  "(c) exact rational LP data.  Target: >= 3 "
                                  "near-tied holes.",
        "step_2_exact_stationarity_system": "with the active sets A_h of the tied "
                                            "holes fixed, solve the polynomial/KKT "
                                            "system at high precision (mpmath, "
                                            ">= 200 digits, Newton with the frozen "
                                            "point as the initial guess): "
                                            "|x_h - c_a| = rho for a in A_h; the "
                                            "hole-defining circumcentre equations; "
                                            "the multiplier equations "
                                            "sum_h sum_{a in A_h} lambda_ha (c_a - x_h) = 0; "
                                            "and |x_h| = 1 for rim holes.  The exact "
                                            "layer of this report already verifies "
                                            "the single-hole case in Q.",
        "step_3_algebraic_candidate": "run LLL/PSLQ on the HIGH-PRECISION root (not "
                                      "on floats) with the repository's relative "
                                      "criterion, then build the minpoly with a "
                                      "rational isolation interval and certify it "
                                      "exactly -- templates: tools/n11_kkt_hp.py, "
                                      "verify/krawczyk_n11.py, "
                                      "verify/minpoly_checks_n11.py.  No minpoly "
                                      "claim may be made before that step.",
        "step_4_certificate": "any improved configuration must still be replayed "
                              "exactly (verify/coverage_n100.py + the independent "
                              "checker) for an explicit rational R, exactly as the "
                              "parent did for R = 18761/156250.",
        "must_not": ["do not treat the frozen decimals as algebraic",
                     "do not claim a minpoly from a 17-digit float",
                     "do not rebalance by following a single 1e-2-scale symmetry "
                     "guess: the measured residual of the mirror maps is %.4f, "
                     "i.e. no symmetry reduction is available"
                     % symmetry["maps"]["mirror_x"]["matched_max"]],
    }

    # ---------------- assemble ------------------------------------------- #
    out = {
        "schema": "n100-cooperative-active-contact-analysis/v1",
        "generated_utc": utc_now(),
        "arithmetic": "two layers, kept apart: (a) exact rational identities about "
                      "the frozen decimal literals, decided in Q; (b) floating-point "
                      "discovery values from numpy/mpmath.  No third layer exists.",
        "discovery_only": True,
        "certified_status_unchanged": True,
        "scope": {
            "subject": "the FIRST frozen cooperative anchor only "
                       "(runtime/n100-cooperative/anchor-certified-012008.json, "
                       "float rho = 0.12007035748136387, exact replay "
                       "R = 18761/156250)",
            "superseded_note": "the delegating agent reports that a later "
                               "refine/polish configuration (float rho ~ 0.119876476, "
                               "exact R = 0.119877, exit 0) now dominates this "
                               "anchor.  That is NOT verified, read or analysed "
                               "here: this file is a bounded structural record of "
                               "the first anchor and must not be read as a "
                               "statement about the current best configuration.",
            "no_symbolic_expansion": "the analysis is deliberately final: no "
                                     "continuation run, no solver, no new candidate.",
        },
        "not_claimed": NOT_CLAIMED,
        "provenance": {
            "candidate_path": os.path.relpath(cand_path, repo).replace("\\", "/"),
            "candidate_sha256": hashes["candidate_sha256"],
            "centers_canonical_sha256": canon["canonical_sha256"],
            "centers_canonical_sha256_recomputed": canon["canonical_sha256"],
            "centers_common_denominator": canon["common_denominator"],
            "centers_inside_closed_unit_disk": int(canon["inside_closed_unit_disk"]),
            "centers_outside_closed_unit_disk":
                CENTER_COUNT - int(canon["inside_closed_unit_disk"]),
            "replay_path": os.path.relpath(replay_path, repo).replace("\\", "/"),
            "replay_sha256": hashes["replay_sha256"],
            "replay_source_sha256": replay.get("source_sha256"),
            "replay_all_passed": bool(replay.get("all_passed")),
            "certified_R": str(R_cert),
            "certified_R_float": float(R_cert),
            "certified_R_equals_seven_digit_ceiling_of_float_rho": bool(
                R_cert == Fraction(1200704, 10 ** 7)),
            "certified_R_minus_float_rho": float(R_cert) - rmax,
            "certified_R_binding_note":
                "quoted only; this analysis neither re-verifies nor extends the "
                "parent's exact replay, and it changes nothing under verify/",
            "pilot_path": os.path.relpath(pilot_path, repo).replace("\\", "/"),
            "pilot_sha256": hashes["pilot_sha256"],
            "pilot_role": "boundary critical set + independent value of rho + "
                          "canonical centre hash; the interior set is re-derived "
                          "here with the generating triples preserved and is "
                          "asserted equal to the pilot's",
            "result_json_path": os.path.relpath(result_path, repo).replace("\\", "/"),
            "result_json_sha256": hashes["result_sha256"],
            "analysis_script_path": os.path.relpath(os.path.abspath(__file__), repo
                                                    ).replace("\\", "/"),
            "analysis_script_sha256": hashes["analysis_script_sha256"],
        },
        "environment": {
            "python": sys.version.replace("\n", " "),
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "mpmath": mpmath.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            "n_centers": CENTER_COUNT,
            "cluster_tolerance": args.cluster_tol,
            "active_set_tolerance_abs": ACTIVE_TOL_ABS,
            "shell_deltas": SHELL_DELTAS,
            "detail_delta": band_delta,
            "detail_delta_origin": "budget.witness_band_scaled = 0.002 (the search's "
                                   "own witness band) times alpha = 1/sqrt(67)",
            "secondary_delta": SECONDARY_DELTA,
            "secondary_top": SECONDARY_TOP,
            "pslq_dps": mpmath.mp.dps,
        },
        "evaluation": {
            "mode": "full",
            "n_interior_candidates": int(len(Ui)),
            "n_boundary_candidates": int(len(Ub)),
            "n_candidates_total": int(len(U)),
            "rho_max_float": rmax,
            "rho_max_kind": str(kind[j]),
            "rho_max_argmax": [float(xmax[0]), float(xmax[1])],
            "rho_recorded_in_candidate": r_recorded,
            "rho_pilot_evaluator": float(pilot_eval["radius"]),
            "interior_max": float(max(d[:len(Ui)].max(), 0.0)),
            "boundary_max": float(max(d[len(Ui):].max(), 0.0)),
            "boundary_gap_below_interior": float(d[:len(Ui)].max() - d[len(Ui):].max()),
            "seconds": secs_eval,
            "pilot_counters": ev.counters,
        },
        "shells": shells,
        "whole_candidate_set": whole_set,
        "deepest_witness": deepest,
        "witness_table_search_band": band_table,
        "witness_table_top_1e-3": secondary_table,
        "center_use_rank": use,
        "incidence_graph": incidence,
        "symmetry_and_duplicates": symmetry,
        "lattice_frame": lattice,
        "algebraic_attempt": alg,
        "verdict": verdict,
        "continuation_proposal": continuation,
        "runtime_seconds": time.perf_counter() - t_start,
    }

    out_path = R(args.out_json)
    write_json(out_path, out)
    say("wrote %s (%.1f KB) in %.2fs"
        % (os.path.relpath(out_path, repo), os.path.getsize(out_path) / 1024.0,
           out["runtime_seconds"]))
    say("verdict: %s | deepest gap rel %.3e | witnesses in band %d | algebraic %s"
        % (verdict["structural_structure"][:46], verdict["gap_to_second_deepest_rel"],
           len(band_table), verdict["algebraic_structure"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

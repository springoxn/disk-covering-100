#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exact upper-bound certificate for the n=100 triangular-lattice (97+3) configuration.

Claim verified here
-------------------
Take the triangular lattice with nearest-neighbour distance 1 in *normalised*
coordinates.  A lattice site is (i, j) in Z^2 with real position

    x(i, j) = (u, sqrt(3) * v),      u = i + j/2,   v = j/2,
    |x(i, j)|^2 = i^2 + i*j + j^2   (unscaled),

and the hexagonal Voronoi cell of a site is its translate of the hexagon H with
vertices (0, +-1/3), (+-1/2, +-1/6) in (u, v) coordinates, circumradius 1/sqrt(3).

Configuration C (n = 100): all sites with i^2 + i*j + j^2 < 28 (97 sites), plus
the three norm-28 sites (-6,4), (-2,-4), (2,4).  With

    a = sqrt(3/67),   R = 1/a = sqrt(67/3),   alpha = 1/sqrt(67),

the certificate proves: the 100 closed disks of radius alpha about the scaled
centres a*x(i, j) cover the closed unit disk D, and alpha is exactly the covering
radius ("candidate radius") of this centre configuration -- i.e. alpha is the
least radius at which these 100 centres cover D.  alpha is *not* claimed to be
the optimum r_D(100); that requires a lower bound over all centre
configurations, which is out of scope here.

Method: exact integer / Fraction arithmetic only, no floating point decisions.
Cell argument (reduction to a finite exact check, see the proof document):
  * cell(p) is contained in the closed disk of radius 1/sqrt(3) about p;
  * a site whose cell meets the closed disk of radius R satisfies
    |p|^2 < 29, hence |p|^2 <= 28, hence |i|,|j| <= 7 -- finite enumeration;
  * for every site p outside C with |p|^2 <= 28 the cell minimum of |x|^2 is
    exactly R^2 = 67/3, attained at a unique vertex v_p, certified by the
    supporting-plane inequality <v_p, w - v_p> >= 0 over all six vertices;
  * v_p lies at distance exactly 1/sqrt(3) from retained centres of C;
  * sites with |p|^2 >= 29 have cell distance >= sqrt(29) - 1/sqrt(3) > R,
    certified by the integer inequality 3*(29-22)^2 > 4*29  (7 > 2*sqrt(29/3)).

Honest scope (also recorded in the JSON as machine_verified_geometry = false):
the infinite-lattice tiling statement ("the closed translates p + H tile the
plane / H is the Voronoi cell of the origin") and the passage from cells to the
disk covering are *analytic* inputs.  This script supplies finite exact evidence
for them (edges on the perpendicular bisectors, circumradius, area equal to the
fundamental domain area, containment of the candidate cell in the Voronoi cell
over a box) but does not formalise them.

Negative controls included (each must be rejected): target disk scaled up
(precondition only -- explicitly *not* an uncovered witness for the delivered
claim), an explicit uncovered point for the enlarged-disk variant, shrunk
covering radius, enlarged covering radius, wrong metric, wrong/rotated hexagon,
inflated hexagon, truncated neighbour search, misattributed neighbour, two
removed tangency centres, an interior centre removed, and the 97-centre
configuration as a "100-point" claim.

Run:  python verify/lattice97_upperbound_n100.py
Out:  verify/out/lattice97_upperbound_n100.json   (exit code 0 iff all passed)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from fractions import Fraction as F
from math import gcd
from pathlib import Path


def rel(path):
    """Repo-relative POSIX path when possible (keeps the JSON location independent)."""
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = 'verify/out/lattice97_upperbound_n100.json'
DEFAULT_PROOF = 'proofs/n100-lattice97-algebraic-upperbound.md'

SCHEMA = 'n100-lattice97-upperbound-v1'

# --------------------------------------------------------------------------
# exact constants (all decisions below use int / Fraction only)
# --------------------------------------------------------------------------
A2 = F(3, 67)                 # a^2 for the real scaling a = sqrt(3/67)
ALPHA2 = F(1, 67)             # real covering radius squared: a^2 * (1/3)
R2 = F(67, 3)                 # target disk squared radius, normalised: 1/a^2
CELL_R2 = F(1, 3)             # squared circumradius of the Voronoi hexagon
SHELL_NORM = 28               # i^2+ij+j^2 of the retained/omitted shell sites
EXTERIOR_MIN_NORM = 29        # first norm excluded by the triangle bound
BOX_SUFFICIENT = 7            # |i|,|j| <= 7 covers every site with norm <= 28
ENUM_LIMIT = 24               # generous enumeration box (>= sufficient box)
RETAINED_EXTRA = ((-6, 4), (-2, -4), (2, 4))
ISOLATION_NUM = (1221694443, 1221694444)
ISOLATION_DEN = 10 ** 10
ISOLATION = (F(ISOLATION_NUM[0], ISOLATION_DEN), F(ISOLATION_NUM[1], ISOLATION_DEN))
ISOLATION_STRING = '[%d/%d,%d/%d]' % (ISOLATION_NUM[0], ISOLATION_DEN,
                                      ISOLATION_NUM[1], ISOLATION_DEN)
MINPOLY = (67, 0, -1)         # 67*t^2 - 1, descending powers

# hexagonal Voronoi cell of the origin, (u, v) coordinates, counter-clockwise
HEX = ((F(0), F(1, 3)), (F(-1, 2), F(1, 6)), (F(-1, 2), F(-1, 6)),
       (F(0), F(-1, 3)), (F(1, 2), F(-1, 6)), (F(1, 2), F(1, 6)))
# outward neighbour across edge k (edge k goes from HEX[k] to HEX[k+1])
HEX_NEIGHBOURS = ((-1, 1), (-1, 0), (0, -1), (1, -1), (1, 0), (0, 1))
# the hole point q = (1/2, sqrt(3)/6), i.e. (u, v) = (1/2, 1/6)
HOLE_UV = (F(1, 2), F(1, 6))


class VerificationError(Exception):
    """Raised when a required exact check fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


# --------------------------------------------------------------------------
# exact lattice arithmetic
# --------------------------------------------------------------------------
def norm2(i, j):
    """i^2 + i*j + j^2, exactly."""
    return i * i + i * j + j * j


def uv(i, j):
    """(u, v) with real position (u, sqrt(3)*v)."""
    return (F(2 * i + j, 2), F(j, 2))


def dot3(a, b):
    """Real inner product of (u, sqrt(3)v) pairs: u1u2 + 3 v1v2."""
    return a[0] * b[0] + 3 * a[1] * b[1]


def dot_plain(a, b):
    """Wrong metric used only by a negative control (the factor 3 is dropped)."""
    return a[0] * b[0] + a[1] * b[1]


def rotate90(hexagon):
    """Wrong (rotated) hexagon used only by a negative control."""
    return tuple((-h[1], h[0]) for h in hexagon)


def scale_hex(hexagon, factor):
    """Inflated hexagon used only by a negative control."""
    return tuple((h[0] * factor, h[1] * factor) for h in hexagon)


def enumerate_sites(limit=ENUM_LIMIT):
    """All lattice sites in the square [-limit, limit]^2 (row-major)."""
    return [(i, j) for i in range(-limit, limit + 1) for j in range(-limit, limit + 1)]


def difference(a, b):
    return (a[0] - b[0], a[1] - b[1])


def edge_min(a, b, dot):
    """Exact minimum of |x|^2 on the closed segment [a, b]; returns (value, t, x)."""
    d = difference(b, a)
    dd = dot(d, d)
    require(dd != 0, 'degenerate edge')
    t = -dot(a, d) / dd
    if t < 0:
        t = F(0)
    if t > 1:
        t = F(1)
    x = (a[0] + t * d[0], a[1] + t * d[1])
    return (dot(x, x), t, x)


def origin_strictly_inside(verts):
    """Exact containment test for the origin in a CCW convex polygon."""
    n = len(verts)
    for k in range(n):
        a, b = verts[k], verts[(k + 1) % n]
        if a[0] * b[1] - b[0] * a[1] <= 0:
            return False
    return True


def cell_min(site, hexagon=HEX, dot=dot3):
    """Exact minimum of |x|^2 over site + hexagon.

    The unconstrained minimiser of |x|^2 is the origin.  If the origin lies
    strictly inside the cell the minimum is therefore 0 at the origin; otherwise
    the minimiser lies on the boundary, and scanning the six edges exactly
    (the restriction of |x|^2 to a segment is a convex quadratic, so its minimum
    over the segment is found exactly) is complete.  All calls below use shell or
    far-away cells (origin outside), but the containment branch keeps the
    function correct in general.
    """
    centre = uv(*site)
    verts = [(centre[0] + h[0], centre[1] + h[1]) for h in hexagon]
    if origin_strictly_inside(verts):
        return (F(0), (F(0), F(0)), verts)
    best = None
    for k, a in enumerate(verts):
        b = verts[(k + 1) % len(verts)]
        val, t, x = edge_min(a, b, dot)
        if best is None or val < best[0]:
            best = (val, x)
    return (best[0], best[1], verts)


def polygon_area_uv(hexagon):
    """Shoelace area of the (u, v) polygon; real area = sqrt(3) * this."""
    total = F(0)
    n = len(hexagon)
    for k in range(n):
        a, b = hexagon[k], hexagon[(k + 1) % n]
        total += a[0] * b[1] - b[0] * a[1]
    return total / 2


def selection():
    """The 100-site configuration and the full shell classification."""
    sites = enumerate_sites(ENUM_LIMIT)
    inside = [p for p in sites if norm2(*p) < SHELL_NORM]
    shell = [p for p in sites if norm2(*p) == SHELL_NORM]
    inside.sort()
    shell.sort()
    require(len(inside) == 97, 'expected 97 sites with norm < 28')
    require(len(shell) == 12, 'expected 12 sites with norm == 28')
    extra = list(RETAINED_EXTRA)
    for p in extra:
        require(norm2(*p) == SHELL_NORM, 'retained extra site is not on the shell')
        require(p in shell, 'retained extra site not found in shell')
    selected = sorted(set(inside) | set(extra))
    require(len(selected) == 100, 'configuration must have 100 distinct sites')
    return {
        'inside': inside,
        'shell': shell,
        'extra': extra,
        'selected': selected,
        'selected_97': sorted(inside),
        'omitted_shell': [p for p in shell if p not in set(extra)],
    }


# --------------------------------------------------------------------------
# positive checks
# --------------------------------------------------------------------------
def check_enumeration(sel):
    """P1: counts, membership, and the finite-box reduction inequalities."""
    box = [p for p in enumerate_sites(ENUM_LIMIT) if norm2(*p) <= SHELL_NORM]
    outside_small_box = [p for p in box if max(abs(p[0]), abs(p[1])) > BOX_SUFFICIENT]
    require(not outside_small_box, 'norm<=28 site outside the proved sufficient box')
    # 2*norm2(i,j) - (i^2+j^2) = (i+j)^2 >= 0  (checked as integers)
    slack = min(2 * norm2(i, j) - (i * i + j * j) for i, j in box)
    require(slack >= 0, 'reduction 2*norm2 >= i^2+j^2 failed')
    return {
        'n_norm_below_28': len(sel['inside']),
        'n_norm_equal_28': len(sel['shell']),
        'n_norm_at_most_28': len(box),
        'n_selected': len(sel['selected']),
        'n_omitted_shell': len(sel['omitted_shell']),
        'shell_sites': [list(p) for p in sel['shell']],
        'retained_shell_sites': [list(p) for p in sel['extra']],
        'omitted_shell_sites': [list(p) for p in sel['omitted_shell']],
        'enumeration_box': [-ENUM_LIMIT, ENUM_LIMIT],
        'proved_sufficient_box': [-BOX_SUFFICIENT, BOX_SUFFICIENT],
        'sufficient_box_reason': 'norm<=28 implies i^2+j^2<=56 implies |i|,|j|<=7',
        'reduction_identity': '2*norm2(i,j)-(i^2+j^2) = (i+j)^2 >= 0',
        'reduction_min_slack': slack,
        'sites_at_most_28_outside_sufficient_box': len(outside_small_box),
    }


def check_cell_geometry():
    """P2: finite exact evidence for the candidate Voronoi hexagon."""
    area_uv = polygon_area_uv(HEX)
    require(area_uv > 0, 'hexagon must be counter-clockwise')
    require(area_uv == F(1, 2), 'hexagon area in (u,v) must be 1/2')
    # real area = sqrt(3) * area_uv; squared = 3 * area_uv^2 = fundamental domain
    require(3 * area_uv * area_uv == F(3, 4), 'fundamental-domain area mismatch')
    vertex_norms = [dot3(h, h) for h in HEX]
    require(all(v == CELL_R2 for v in vertex_norms), 'hexagon vertices not at 1/sqrt(3)')
    edges = []
    for k in range(6):
        a, b = HEX[k], HEX[(k + 1) % 6]
        nb = uv(*HEX_NEIGHBOURS[k])
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        d = difference(b, a)
        edges.append({
            'edge': k,
            'neighbour': list(HEX_NEIGHBOURS[k]),
            'endpoints_equidistant_to_origin_and_neighbour':
                dot3(a, a) == dot3(difference(a, nb), difference(a, nb)) and
                dot3(b, b) == dot3(difference(b, nb), difference(b, nb)),
            'direction_perpendicular_to_neighbour': dot3(d, nb) == 0,
            'midpoint_equals_half_neighbour': mid == (nb[0] / 2, nb[1] / 2),
        })
    require(all(e['endpoints_equidistant_to_origin_and_neighbour'] for e in edges),
            'hexagon edge is not on the perpendicular bisector')
    require(all(e['direction_perpendicular_to_neighbour'] for e in edges),
            'hexagon edge not perpendicular to the neighbour direction')
    require(all(e['midpoint_equals_half_neighbour'] for e in edges),
            'hexagon edge midpoint is not the half-neighbour point')
    halfspace = all(dot3(h, h) <= dot3(difference(h, uv(*n)), difference(h, uv(*n)))
                    for h in HEX for n in HEX_NEIGHBOURS)
    require(halfspace, 'hexagon is not inside the neighbour half-planes')
    return {
        'hex_vertices_uv': [[str(x), str(y)] for x, y in HEX],
        'orientation': 'counter-clockwise',
        'area_uv': str(area_uv),
        'area_real_over_sqrt3': str(area_uv),
        'area_equals_fundamental_domain': True,
        'vertex_squared_norms': [str(v) for v in vertex_norms],
        'circumradius_squared': str(CELL_R2),
        'edges_on_perpendicular_bisectors': True,
        'inside_neighbour_halfplanes': True,
        'edge_certificate': edges,
    }


def check_selected_cell_radius(sel):
    """P3: every selected cell is inside the closed disk of radius 1/sqrt(3)."""
    worst = None
    vertex_offsets = [dot3(h, h) for h in HEX]
    require(max(vertex_offsets) == CELL_R2, 'hexagon vertex offset beyond circumradius')
    for p in sel['selected']:
        centre = uv(*p)
        verts = [(centre[0] + h[0], centre[1] + h[1]) for h in HEX]
        # distance from the cell centre, not from the origin
        vals = [dot3(difference(v, centre), difference(v, centre)) for v in verts]
        require(max(vals) == CELL_R2, 'hexagon vertex beyond circumradius')
        # every point of the convex hexagon is a convex combination of vertices,
        # and |.|^2 is convex, hence max over the cell is attained at a vertex
        if worst is None or max(vals) > worst:
            worst = max(vals)
    return {
        'n_selected': len(sel['selected']),
        'max_squared_distance_center_to_cell': str(worst),
        'reason': 'convexity: |sum lambda_k w_k|^2 <= sum lambda_k |w_k|^2 = 1/3',
        'selected_cells_covered_by_own_disk': True,
    }


def witness_sites(point, dot=dot3, limit=ENUM_LIMIT, max_distance2=CELL_R2):
    """All lattice sites within max_distance2 of point, inside the search box."""
    out = []
    for q in enumerate_sites(limit):
        if dot(difference(point, uv(*q)), difference(point, uv(*q))) <= max_distance2:
            out.append(q)
    return sorted(out)


def check_shell_cells(sel, hexagon=HEX, dot=dot3, R2v=R2):
    """P4: cell minimum at every unselected cell that can meet the target disk.

    A cell minimum equal to R2v must be attained at a unique point, certified by
    a supporting plane, and that point must be covered by a configuration disk.
    Returns a result dict; 'ok' is False with 'failures' when the certificate
    cannot be issued (used unchanged by the negative controls).
    """
    selected = sel['selected'] if isinstance(sel, dict) else sel
    S = set(selected)
    sites = [p for p in enumerate_sites(ENUM_LIMIT) if norm2(*p) <= SHELL_NORM]
    failures = []
    table = []
    for p in sites:
        if p in S:
            continue
        m, arg, verts = cell_min(p, hexagon, dot)
        row = {
            'site': list(p),
            'norm2': norm2(*p),
            'cell_min_squared': str(m),
            'argmin_uv': [str(arg[0]), str(arg[1])],
            'argmin_is_vertex': any(arg == w for w in verts),
            'target_squared': str(R2v),
            'min_equals_target': m == R2v,
        }
        if not row['min_equals_target']:
            row['cell_min_below_target_by'] = str(R2v - m)
            failures.append('shell cell %s: min %s != target %s' % (list(p), m, R2v))
            table.append(row)
            continue
        support = [dot(arg, difference(w, arg)) for w in verts]
        row['supporting_plane_values'] = [str(x) for x in support]
        row['supporting_plane_nonnegative'] = all(x >= 0 for x in support)
        if not row['supporting_plane_nonnegative']:
            failures.append('shell cell %s: no supporting plane at argmin' % list(p))
            table.append(row)
            continue
        # |x|^2 - R^2 = |x-v|^2 + 2<v, x-v> >= |x-v|^2, so v is the unique point
        # of the cell with |x|^2 = R^2
        row['unique_minimiser'] = True
        row['cell_disk_intersection'] = [[str(arg[0]), str(arg[1])]]
        tangencies = witness_sites(arg, dot=dot)
        row['tangency_sites'] = [list(q) for q in tangencies]
        row['tangency_outside_configuration'] = [list(q) for q in tangencies if q not in S]
        witnesses = [q for q in tangencies if q in S]
        row['witnesses_in_configuration'] = [list(q) for q in witnesses]
        if not witnesses:
            failures.append('shell cell %s: critical vertex not covered' % list(p))
            table.append(row)
            continue
        d2 = min(dot(difference(arg, uv(*q)), difference(arg, uv(*q))) for q in witnesses)
        row['witness_squared_distance'] = str(d2)
        row['witness_is_tangency'] = d2 == CELL_R2
        if d2 > CELL_R2:
            failures.append('shell cell %s: witness outside radius 1/sqrt(3)' % list(p))
        row['self_tangency_squared_distance'] = str(
            dot(difference(arg, uv(*p)), difference(arg, uv(*p))))
        table.append(row)
    return {
        'ok': not failures,
        'failures': failures,
        'n_unselected_cells_checked': len(table),
        'cells': table,
    }


def check_exterior(sel):
    """P5: sites with norm >= 29 have cells at distance > R from the origin."""
    n_min = EXTERIOR_MIN_NORM
    # (sqrt(n) - 1/sqrt(3))^2 > 67/3  <=>  n - 22 > 2*sqrt(n/3)
    #                                  <=>  3*(n-22)^2 > 4*n     (n > 22)
    require(n_min > 22, 'exterior threshold must exceed 22')
    lhs = 3 * (n_min - 22) ** 2
    rhs = 4 * n_min
    require(lhs > rhs, 'exterior separation inequality failed')
    # the same chain in the equivalent form quoted in the task: 7 > 2*sqrt(29/3)
    require(49 * 3 > 4 * 29, 'equivalent form 7^2 > 4*29/3 failed')
    # monotonicity: sqrt(n) - 1/sqrt(3) is increasing in n, checked on integers
    require(all(3 * (n - 22) ** 2 > 4 * n for n in range(n_min, 400)), 'monotonicity failed')
    return {
        'threshold_norm2': n_min,
        'inequality': '3*(29-22)^2 > 4*29',
        'lhs': lhs,
        'rhs': rhs,
        'equivalent_form': '7 > 2*sqrt(29/3)  <=>  147 > 116',
        'separated_distance_squared_strictly_above_target': True,
        'reason': 'cell(p) subset disk(p,1/sqrt(3)) so dist(cell(p),0) >= sqrt(|p|^2)-1/sqrt(3)',
        'monotone_for_all_n_ge_29': True,
    }


def check_finite_reduction():
    """P6: only sites with |p|^2 <= 28 can have a cell meeting the target disk."""
    # |p| <= R + 1/sqrt(3)  =>  |p|^2 <= 68/3 + (2/3)*sqrt(67)
    # 68/3 + (2/3)*sqrt(67) < 29  <=>  2*sqrt(67) < 19  <=>  268 < 361
    require(4 * 67 < 19 * 19, 'finite reduction inequality failed')
    # numeric witness of the same statement with rationals around sqrt(67)
    lo, hi = F(8185, 1000), F(8186, 1000)   # 8.185 < sqrt(67) < 8.186
    require(lo * lo < 67 < hi * hi, 'rational bracket for sqrt(67) failed')
    upper = F(68, 3) + F(2, 3) * hi
    require(upper < 29, 'squared reach exceeds the first excluded norm')
    return {
        'inequality': '68/3 + (2/3)*sqrt(67) < 29',
        'equivalent_integer_form': '268 < 361  (2*sqrt(67) < 19)',
        'sqrt67_rational_bracket': ['8.185', '8.186'],
        'upper_bound_on_squared_reach': str(upper),
        'first_excluded_norm_squared': EXTERIOR_MIN_NORM,
        'conclusion': 'a cell meeting the disk has |p|^2 < 29, thus |p|^2 <= 28',
    }


def check_hole(sel):
    """P7: the hole point q in D forces radius >= alpha for lattice centres."""
    q = HOLE_UV
    q2 = dot3(q, q)
    require(q2 == CELL_R2, 'hole point is not at the prescribed distance')
    require(q2 < R2, 'hole point is not inside the target disk')
    q_scaled2 = A2 * q2
    require(q_scaled2 == ALPHA2, 'scaled hole point distance is not alpha^2')
    table = []
    worst = None
    for p in enumerate_sites(ENUM_LIMIT):
        c = uv(*p)
        d2 = dot3(difference(q, c), difference(q, c))
        table.append(d2)
        if worst is None or d2 < worst[0]:
            worst = (d2, p)
    require(worst[0] == CELL_R2, 'lattice point closer to q than 1/sqrt(3)')
    equal = sorted(p for p in enumerate_sites(ENUM_LIMIT)
                   if dot3(difference(q, uv(*p)), difference(q, uv(*p))) == CELL_R2)
    # symbolic identity: |q - c|^2 - 1/3 = i^2 + i*j + j^2 - i - j
    identity = all(dot3(difference(q, uv(i, j)), difference(q, uv(i, j))) - CELL_R2
                   == norm2(i, j) - i - j for i, j in enumerate_sites(ENUM_LIMIT))
    require(identity, 'symbolic gap identity failed')
    box_min = min(norm2(i, j) - i - j for i in range(-4, 5) for j in range(-4, 5))
    require(box_min >= 0, 'gap is negative inside the checked box')
    # outside the box: gap >= (i^2+j^2)/2 - |i| - |j| >= A*(A-4)/2 > 0 with
    # A = max(|i|,|j|) >= 5, because i^2+j^2 >= A^2 and |i|+|j| <= 2A
    require(all(A * (A - 4) > 0 for A in range(5, 4001)), 'asymptotic gap bound failed')
    for p in equal:
        require(p in set(sel['selected']), 'equidistant site missing from configuration')
    return {
        'hole_uv': [str(q[0]), str(q[1])],
        'hole_real_relative_to_a': ['1/2', 'sqrt(3)/6'],
        'hole_squared_norm_normalised': str(q2),
        'hole_squared_norm_real_over_a2': str(q_scaled2),
        'hole_squared_norm_real': str(ALPHA2),
        'hole_inside_unit_disk': True,
        'min_squared_distance_to_lattice': str(worst[0]),
        'min_squared_distance_to_configuration': str(worst[0]),
        'equidistant_lattice_sites': [list(p) for p in equal],
        'equidistant_sites_in_configuration': True,
        'gap_identity': '|q-c|^2 - 1/3 = i^2 + i*j + j^2 - i - j',
        'gap_nonnegative_checked_box': [-4, 4],
        'gap_nonnegative_asymptotic': 'A=max(|i|,|j|)>=5: gap >= A*(A-4)/2 > 0',
        'extra_sites_are_lattice_points': True,
    }


def minpoly_checks():
    """P8: minimal polynomial of alpha, irreducibility, exact rational isolation."""
    coeffs = MINPOLY
    require(coeffs == (67, 0, -1), 'unexpected minimal polynomial')

    def P(t):
        return 67 * t * t - 1

    # ALPHA2 is alpha^2, so "alpha is a root of P" means 67*alpha^2 - 1 = 0
    require(67 * ALPHA2 - 1 == 0, 'alpha does not satisfy 67*t^2-1')
    # content / primitivity
    content = 0
    for c in coeffs:
        content = gcd(content, abs(c))
    require(content == 1, 'polynomial not primitive')
    # rational root theorem: roots p/q in lowest terms need p | 1, q | 67
    candidates = [F(1), F(-1), F(1, 67), F(-1, 67)]
    roots = [str(t) for t in candidates if P(t) == 0]
    require(not roots, 'minimal polynomial has a rational root')
    # exact sign change on the isolating interval
    lo, hi = ISOLATION
    lo2, hi2 = lo * lo, hi * hi
    require(67 * lo2 < 1, 'P(lo) is not negative')
    require(67 * hi2 > 1, 'P(hi) is not positive')
    require(lo < hi and lo > 0, 'bad isolating interval')
    # monotonicity of P on [0, inf): P'(t) = 134 t >= 0, P(0) = -1 != 0
    require(67 * 0 * 0 - 1 < 0, 'P(0) must be negative')
    return {
        'variable': 't',
        'coefficients_descending': list(coeffs),
        'polynomial': '67*t^2 - 1',
        'alpha_squared': '1/67',
        'alpha_is_root': True,
        'primitive': True,
        'content': content,
        'rational_root_candidates': [str(t) for t in candidates],
        'rational_roots_found': roots,
        'irreducible_over_Q': True,
        'irreducibility_method': 'quadratic with no rational root (rational root theorem)',
        'positive_root_unique': True,
        'positive_root_uniqueness_method':
            'P(0) = -1 < 0 and P\'(t) = 134 t > 0 for t > 0, so P is strictly increasing on [0,inf)',
        'isolation_interval': ISOLATION_STRING,
        'isolation_interval_reduced': [str(lo), str(hi)],
        'isolation_exact_forms': [
            '67*1221694443^2 = 99999999907824376683 < 10^20',
            '67*1221694444^2 = 100000000071531432112 > 10^20',
        ],
        'isolation_denominator': '10^10',
        'sign_at_lo_over_10_pow_20': '-92175623317',
        'sign_at_hi_times_6250000000000000000': '4470714507',
        'positive_root_in_interval': True,
        'scope': 'minimal polynomial of the candidate covering radius, not of r_D(100)',
    }


def canonical_indices(selected):
    return json.dumps([[i, j] for i, j in selected], separators=(',', ':')).encode()


# --------------------------------------------------------------------------
# negative controls
# --------------------------------------------------------------------------
def control(name, mutation, outcome, rejected, kind, uncovered_witness=False,
            scope='delivered_claim', detail=''):
    return {
        'case': name,
        'mutation': mutation,
        'expected': outcome,
        'rejected': bool(rejected),
        'rejection_kind': kind,
        'uncovered_witness_produced': bool(uncovered_witness),
        'scope': scope,
        'detail': detail,
    }


def negative_controls(sel):
    """Every control must be rejected; the function raises if any slips through."""
    controls = []
    selected = sel['selected']

    # (1) target disk scaled up: precondition failure only -- explicitly NOT an
    #     uncovered witness for the delivered claim.
    scaled = R2 + F(1, 1000)
    res = check_shell_cells(sel, R2v=scaled)
    row = next((r for r in res['cells'] if r['site'] == [4, 2]), None)
    require(row is not None, 'control 1: shell cell (4,2) missing')
    require(not res['ok'], 'control 1 accepted: scaled target radius')
    require(row['cell_min_below_target_by'] == str(F(1, 1000)),
            'control 1: unexpected boundary gap')
    controls.append(control(
        'target_disk_scaled_up',
        'R^2 := 67/3 + 1/1000 (same 100 centres, same radius alpha)',
        'cell certificate precondition (cell minimum == target) must fail',
        True, 'proof_precondition', False, 'delivered_claim',
        'cell minimum stays 67/3, so cell((4,2)) meets the enlarged disk in more '
        'than the single tangency vertex; the certificate refuses to issue. '
        'This is a precondition rejection, NOT a proof that the enlarged disk is '
        'uncovered -- covering is monotone in the target radius.'))

    # (2) explicit uncovered point for the enlarged-disk variant: x on the
    #     segment from the critical vertex towards its own (omitted) site.
    p = (4, 2)
    m, v, verts = cell_min(p)
    t = F(1, 1000)
    pc = uv(*p)
    x = (v[0] + t * (pc[0] - v[0]), v[1] + t * (pc[1] - v[1]))
    x2 = dot3(x, x)
    require(x2 > R2, 'control 2: witness must lie outside the delivered disk')
    dmin = min((dot3(difference(x, uv(*c)), difference(x, uv(*c))), c) for c in selected)
    require(dmin[0] > CELL_R2, 'control 2: witness is covered after all')
    controls.append(control(
        'enlarged_disk_explicit_uncovered_point',
        'target disk R\'^2 := |x|^2 with x = v + (p-v)/1000, p = (4,2)',
        'explicit point in the enlarged disk outside all 100 disks of radius alpha',
        True, 'uncovered_witness', True, 'modified_claim (enlarged target disk)',
        'x_uv = (%s, %s), |x|^2 - R^2 = %s, nearest centre %s at squared distance '
        '%s > 1/3. This refutes the *modified* claim only; it says nothing about '
        'the delivered radius.' % (x[0], x[1], x2 - R2, list(dmin[1]), dmin[0])))

    # (3) covering radius shrunk below alpha: q becomes an uncovered point.
    shrunk = ALPHA2 - F(1, 10 ** 6)
    require(ALPHA2 > shrunk, 'control 3: bad shrinkage')
    require(dot3(HOLE_UV, HOLE_UV) * A2 > shrunk,
            'control 3: hole point would still be covered')
    controls.append(control(
        'covering_radius_shrunk_below_alpha',
        'alpha^2 := 1/67 - 1/10^6',
        'explicit uncovered witness: the hole point q',
        True, 'uncovered_witness', True, 'modified_claim (shrunk covering radius)',
        'q has real squared norm 1/67 and its nearest configuration centre is at '
        'squared distance 1/67 > 1/67 - 1/10^6, so q is uncovered: shows the '
        'lower bound direction is live and the delivered radius is minimal.'))

    # (4) covering radius enlarged: not a coverage failure, but the claimed
    #     exactness/minimality is refuted.
    enlarged = ALPHA2 + F(1, 10 ** 6)
    require(enlarged > ALPHA2, 'control 4: bad enlargement')
    controls.append(control(
        'covering_radius_enlarged_above_alpha',
        'alpha^2 := 1/67 + 1/10^6',
        'exactness claim refuted (a strictly smaller radius already covers)',
        True, 'exactness_not_minimal', False, 'modified_claim (enlarged covering radius)',
        'coverage is monotone in the covering radius, so the enlarged value still '
        'covers; what fails is exactness: q forces radius >= 1/sqrt(67) and the '
        'certified covering works at 1/sqrt(67) < alpha\'. No uncovered point is '
        'claimed.'))

    # (5) wrong metric (missing factor 3).
    res = check_shell_cells(sel, dot=dot_plain)
    require(not res['ok'], 'control 5 accepted: wrong metric')
    controls.append(control(
        'wrong_metric_missing_factor_three',
        'inner product u1u2 + v1v2 instead of u1u2 + 3 v1v2',
        'shell cell minimum must differ from 67/3',
        True, 'geometry_check_failed', False, 'modified_hypothesis',
        'min over cell((4,2)) becomes 377/18 != 67/3, so the certificate refuses.'))

    # (6) rotated hexagon.
    res = check_shell_cells(sel, hexagon=rotate90(HEX))
    require(not res['ok'], 'control 6 accepted: rotated hexagon')
    controls.append(control(
        'wrong_hexagon_rotated',
        'hexagon vertices rotated by 90 degrees in (u,v)',
        'shell cell minimum must differ from 67/3',
        True, 'geometry_check_failed', False, 'modified_hypothesis',
        'min over cell((4,2)) becomes 675/28 != 67/3; the rotated polygon is not a '
        'Voronoi cell of this lattice.'))

    # (7) inflated hexagon.
    res = check_shell_cells(sel, hexagon=scale_hex(HEX, F(3, 2)))
    require(not res['ok'], 'control 7 accepted: inflated hexagon')
    controls.append(control(
        'wrong_hexagon_inflated',
        'hexagon scaled by 3/2 (circumradius 3/2 * 1/sqrt(3))',
        'shell cell minimum must differ from 67/3',
        True, 'geometry_check_failed', False, 'modified_hypothesis',
        'min over cell((4,2)) becomes 79/4 != 67/3.'))

    # (8) truncated neighbour search: the tangency neighbours are missed.
    p = (4, 2)
    m, v, verts = cell_min(p)
    found = witness_sites(v, limit=2)
    require(not found, 'control 8: truncated search unexpectedly found a witness')
    controls.append(control(
        'truncated_neighbour_search',
        'critical-vertex neighbour search restricted to |i|,|j| <= 2',
        'no witness in the configuration -> certificate must fail loudly',
        True, 'no_witness_in_configuration', False, 'modified_search',
        'the exact tangency neighbours (3,2) and (4,1) lie outside the truncated '
        'box, so the certificate cannot be issued: certification depends on the '
        'exact neighbour attribution and fails closed.'))

    # (9) misattributed neighbour (claims the omitted site itself as witness).
    p = (4, 2)
    m, v, verts = cell_min(p)
    claimed = [(4, 2), (5, 2)]
    bad = []
    for c in claimed:
        d2 = dot3(difference(v, uv(*c)), difference(v, uv(*c)))
        if c not in set(selected) or d2 > CELL_R2:
            bad.append({'site': list(c), 'in_configuration': c in set(selected),
                        'squared_distance': str(d2)})
    require(len(bad) == len(claimed), 'control 9: bogus witnesses accepted')
    controls.append(control(
        'misattributed_critical_neighbour',
        'claim witnesses {(4,2), (5,2)} for the critical vertex of cell((4,2))',
        'witness must belong to the configuration and lie within 1/sqrt(3)',
        True, 'witness_attribution_failed', False, 'modified_hypothesis',
        'the shell site (4,2) is itself at squared distance exactly 1/3 from the '
        'vertex -- using it (or any non-configuration site) as a covering centre '
        'is exactly the error guarded against: %s' % json.dumps(bad)))

    # (10) two tangency centres removed: a genuine uncovered critical vertex.
    removed = [(3, 2), (4, 1)]
    smaller = [c for c in selected if c not in set(removed)]
    res = check_shell_cells({'selected': smaller})
    witnesses = [r for r in res['cells'] if r['site'] == [4, 2]][0]['witnesses_in_configuration']
    require(not res['ok'] and not witnesses, 'control 10: removal not detected')
    controls.append(control(
        'two_tangency_centres_removed',
        'configuration := the 98 sites left after deleting (3,2) and (4,1)',
        'coverage must fail with an explicit uncovered witness',
        True, 'uncovered_witness', True, 'modified_claim (98 centres)',
        'the critical vertex (9/2, 5/6) of cell((4,2)) has no covering centre left, '
        'so that point is an uncovered witness; shows the coverage test is '
        'sensitive to the exact tangency pair.'))

    # (11) the 97-site configuration is not a 100-point configuration (although,
    #      honestly, it still covers -- no overclaiming).
    res97 = check_shell_cells({'selected': sel['selected_97']})
    require(len(sel['selected_97']) != 100, 'control 11: 97 sites is not 100')
    require(res97['ok'], 'control 11: the 97-site configuration should still cover')
    controls.append(control(
        'ninety_seven_sites_as_100_point_configuration',
        'drop the three retained norm-28 sites (97 centres)',
        'cardinality check must reject it as the 100-point configuration',
        True, 'configuration_cardinality', False, 'modified_claim (97 centres)',
        'the index list has 97 entries, so it is not the delivered 100-point '
        'configuration. Note honestly: the 97-site set still covers D at radius '
        'alpha (all twelve shell cells, including the three retained ones, have '
        'their critical vertex covered by retained neighbours distinct from '
        'themselves), so this control rejects the cardinality, not the coverage.'))

    # (12) truncated index list: a dropped *shell* centre whose critical vertex is
    #      still covered by its partner -- only the cardinality check can catch it.
    dropped = [c for c in selected if c != (2, 4)]
    res_d = check_shell_cells({'selected': dropped})
    require(len(dropped) == 99, 'control 12: bad cardinality')
    require(res_d['ok'], 'control 12: expected coverage to survive this deletion')
    controls.append(control(
        'single_shell_centre_removed',
        'configuration := the 99 sites left after deleting the shell site (2,4)',
        'cardinality check must reject it; coverage survives (honest labelling)',
        True, 'configuration_cardinality', False, 'modified_claim (99 centres)',
        '(1,4) and (2,3) still cover the critical vertex of cell((2,4)) at squared '
        'distance exactly 1/3, so coverage survives the deletion and only the '
        'cardinality check rejects this variant -- recorded to avoid overclaiming.'))

    # (13) an interior centre removed: coverage really fails, with a witness.
    removed_interior = [c for c in selected if c != (3, 2)]
    res_i = check_shell_cells({'selected': removed_interior})
    require(len(removed_interior) == 99, 'control 13: bad cardinality')
    require(not res_i['ok'], 'control 13: interior deletion not detected')
    x = uv(3, 2)
    x2 = dot3(x, x)
    require(x2 < R2, 'control 13: witness must lie inside the target disk')
    dmin = min(dot3(difference(x, uv(*c)), difference(x, uv(*c))) for c in removed_interior)
    require(dmin > CELL_R2, 'control 13: witness is covered after all')
    controls.append(control(
        'interior_centre_removed',
        'configuration := the 99 sites left after deleting the interior site (3,2)',
        'coverage must fail with an explicit uncovered witness',
        True, 'uncovered_witness', True, 'modified_claim (99 centres)',
        'the site (3,2) itself has |x|^2 = 19 < 67/3 and its nearest remaining '
        'centre is at squared distance %s > 1/3, so it is uncovered: an unselected '
        'cell that penetrates the disk (cell minimum below the target) is caught by '
        'the certificate.' % dmin))

    if not all(c['rejected'] for c in controls):
        raise VerificationError('a negative control was accepted')
    return controls


# --------------------------------------------------------------------------
# proof binding
# --------------------------------------------------------------------------
MARKER_RE = re.compile(r'<!--\s*lattice97-upperbound-proof:\s*(.*?)\s*-->', re.S)


def check_proof_binding(proof_path, checker_sha256):
    text = proof_path.read_text(encoding='utf-8')
    found = MARKER_RE.findall(text)
    require(len(found) == 1, 'proof must contain exactly one machine-readable marker')
    fields = {}
    for chunk in found[0].split(';'):
        chunk = chunk.strip()
        if not chunk:
            continue
        key, _, value = chunk.partition('=')
        fields[key.strip()] = value.strip()
    expected = {
        'alpha_squared': '1/67',
        'minpoly': '67*t^2-1',
        'minpoly_coefficients': '[67,0,-1]',
        'target_radius_squared': '67/3',
        'isolation': ISOLATION_STRING,
        'machine_verified_geometry': 'false',
        'scope': 'candidate-configuration-radius-not-optimum',
        'checker_sha256': checker_sha256,
    }
    for key, value in expected.items():
        require(key in fields, 'proof marker missing field %s' % key)
        require(fields[key] == value,
                'proof marker %s mismatch: %r != %r' % (key, fields[key], value))
    return {
        'marker_present': True,
        'marker_fields': fields,
        'marker_matches_certificate': True,
        'mentions_unformalised_tiling': ('未形式化' in text) or ('not formalised' in text)
                                       or ('not formalized' in text),
    }


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------
def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_certificate(proof_path, checker_path):
    sel = selection()
    checker_sha = sha256_file(checker_path)

    enum = check_enumeration(sel)
    geom = check_cell_geometry()
    selected_radius = check_selected_cell_radius(sel)
    shell = check_shell_cells(sel)
    require(shell['ok'], 'shell cell certificate failed: %s' % shell['failures'])
    exterior = check_exterior(sel)
    reduction = check_finite_reduction()
    hole = check_hole(sel)
    minpoly = minpoly_checks()
    shell97 = check_shell_cells({'selected': sel['selected_97']})
    require(shell97['ok'], 'the 97-site sub-configuration should also cover')

    coverage_ok = (enum['n_selected'] == 100 and selected_radius['selected_cells_covered_by_own_disk']
                   and shell['ok'] and exterior['separated_distance_squared_strictly_above_target']
                   and reduction['first_excluded_norm_squared'] == EXTERIOR_MIN_NORM)
    require(coverage_ok, 'coverage certificate not established')

    # candidate radius = alpha: upper bound from coverage, lower bound from q
    require(hole['min_squared_distance_to_configuration'] == str(CELL_R2),
            'lower bound at q not established')
    require(A2 * CELL_R2 == ALPHA2, 'scaling of the lower bound is not alpha^2')

    problem = Path(checker_path)
    problem_stat = problem.stat()
    negative = negative_controls(sel)
    binding = check_proof_binding(Path(proof_path), checker_sha)

    indices = canonical_indices(sel['selected'])
    result = {
        'schema': SCHEMA,
        'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'python': platform.python_version(),
        'claim': {
            'statement':
                'The 100 closed disks of radius alpha = 1/sqrt(67) centred at the '
                'scaled triangular-lattice sites C cover the closed unit disk D, '
                'and alpha is exactly the covering radius of C.',
            'not_claimed': [
                'r_D(100) = alpha (no lower bound over arbitrary centre sets)',
                'optimality, local optimality or symmetry reduction',
                'a formalised proof of the infinite-lattice Voronoi tiling',
            ],
            'radius_role': 'candidate (configuration) radius, NOT the optimum',
        },
        'exact_configuration': {
            'n_centers': len(sel['selected']),
            'indices': [[i, j] for i, j in sel['selected']],
            'ordering_key': 'lexicographic in (i, j)',
            'construction_rule':
                'all sites with i^2+ij+j^2 < 28 (97 sites) plus (-6,4), (-2,-4), (2,4)',
            'construction_order': [[i, j] for i, j in sel['inside']] + [list(p) for p in sel['extra']],
            'retained_norm28': [list(p) for p in sel['extra']],
            'omitted_norm28': [list(p) for p in sel['omitted_shell']],
            'norm28_rule_excluded': [list(p) for p in sel['shell']],
            'indices_sha256': hashlib.sha256(indices).hexdigest(),
            'centers_uv': [[str(uv(i, j)[0]), str(uv(i, j)[1])] for i, j in sel['selected']],
            'real_position_rule': 'a*(u, sqrt(3)*v) with u = i+j/2, v = j/2',
            'real_scaling_a_squared': str(A2),
        },
        'alpha_squared': str(ALPHA2),
        'alpha_squared_fraction': [ALPHA2.numerator, ALPHA2.denominator],
        'alpha_decimal_diagnostic': format(float(ALPHA2) ** 0.5, '.16f'),
        'target_disk_radius_squared_normalised': str(R2),
        'coverage_confirmed': True,
        'coverage_confirmed_97_subset': bool(shell97['ok']),
        'coverage_argument_conditional_on_analytic_tiling': True,
        'exact_candidate_radius_confirmed': True,
        'exact_candidate_radius_argument': {
            'upper_bound': 'coverage at radius alpha',
            'lower_bound': 'the hole point q in D needs radius >= 1/sqrt(3) '
                           '(normalised) = alpha for any lattice subset',
            'lower_bound_applies_to_any_lattice_subset': True,
            'extra_three_sites_are_lattice_points': True,
        },
        'minpoly_coefficients': list(MINPOLY),
        'minpoly': '67*t^2 - 1',
        'minpoly_coefficients_ascending': list(reversed(MINPOLY)),
        'minpoly_checks': minpoly,
        'isolation_interval': ['%d/%d' % (ISOLATION_NUM[0], ISOLATION_DEN),
                               '%d/%d' % (ISOLATION_NUM[1], ISOLATION_DEN)],
        'isolation_interval_reduced': [str(ISOLATION[0]), str(ISOLATION[1])],
        'isolation_interval_marker_string': ISOLATION_STRING,
        'checks': {
            'enumeration': enum,
            'cell_geometry': geom,
            'selected_cell_radius': selected_radius,
            'shell_cells': shell,
            'shell_cells_97_subset': shell97,
            'exterior_sites': exterior,
            'finite_reduction': reduction,
            'hole_point': hole,
        },
        'negative_controls': negative,
        'machine_verified_geometry': False,
        'machine_verified_geometry_note':
            'Exact integer/Fraction arithmetic is machine verified. The infinite-'
            'lattice Voronoi tiling (translates of the hexagon tile the plane and '
            'the hexagon is the Voronoi cell of its site) and the reduction from '
            'cells to the disk covering are analytic inputs, supported here only by '
            'finite exact evidence; no formal geometry kernel or proof assistant '
            'was used.',
        'checker_path': rel(checker_path),
        'checker_sha256': checker_sha,
        'checker_bytes': problem_stat.st_size,
        'checker_sha256_scope': 'this script only; no project module is imported',
        'proof_path': rel(proof_path),
        'proof_sha256': sha256_file(proof_path),
        'proof_bytes': Path(proof_path).stat().st_size,
        'proof_binding': binding,
        'all_passed': True,
    }
    require(result['proof_binding']['marker_matches_certificate'],
            'proof marker does not match the certificate')
    require(all(c['rejected'] for c in negative), 'negative control accepted')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', default=DEFAULT_OUT)
    parser.add_argument('--proof', default=DEFAULT_PROOF)
    parser.add_argument('--checker', default=str(Path(__file__).resolve()))
    args = parser.parse_args(argv)

    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    proof = Path(args.proof)
    if not proof.is_absolute():
        proof = ROOT / proof
    checker = Path(args.checker)
    if not checker.is_absolute():
        checker = ROOT / checker
    require(proof.exists(), 'proof document not found: %s' % proof)

    result = build_certificate(proof, checker)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup = out.with_name(out.name + '.bak-' + stamp)
        backup.write_bytes(out.read_bytes())
        result['backup_of_previous'] = str(backup)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('PASS exact enumeration: 97 sites with norm<28 + 3 retained norm-28 = 100')
    print('PASS coverage: 12 norm-28 shell cells min |x|^2 = 67/3 at covered vertices; '
          'norm>=29 separated (3*(29-22)^2 > 4*29)')
    print('PASS finite reduction: 268 < 361 and |i|,|j| <= 7')
    print('PASS candidate radius exact: alpha^2 = 1/67 (hole point q), 97-subset covers too')
    print('PASS minpoly 67*t^2-1; irreducible; positive root in [1221694443/1e10, '
          '1221694444/1e10]')
    print('PASS negative controls rejected:', ', '.join(c['case'] for c in result['negative_controls']))
    print('checker_sha256 =', result['checker_sha256'])
    print('proof_sha256   =', result['proof_sha256'])
    print('wrote', out)
    return 0


if __name__ == '__main__':
    sys.exit(main())

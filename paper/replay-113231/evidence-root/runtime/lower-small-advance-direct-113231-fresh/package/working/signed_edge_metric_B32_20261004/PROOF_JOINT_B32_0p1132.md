# Sixteen B32 graph exclusions through .1132

Run verify_all_joint_0p1132.py with assertions enabled. Its sixteen
rational certificates are in joint_certificates_0p1132. Acceptance uses
only standard Python and the already audited outward integer backends.

This result concerns the sixteen explicitly supplied B32_P26_F108
graphs with arbitrary actual covering-center coordinates. Catalog
completeness at a new radius is a separate premise. In particular,
this document does not extend the .11318 reduced-cost theorem to .1132.

## 1. A noncircular pure-dual bootstrap

Each validated graph has 68 interior and 32 boundary vertices, 134 q0
faces and 32 ordinary q1 faces, no ears and no q0 boundary edge.
All oriented edge incidences, vertex links and marks are checked by
the complete B32 graph validator. The graph bytes are SHA-bound.

The checker first sets every boundary angle potential to zero.
It verifies every q0 scalar support over its complete actual domain
using the signed-edge backend, and every marked support by its full
conjugate. Opposite signs on each shared q0 edge cancel exactly.
The resulting radius-independent normalized center bound C satisfies

    C <= 114898227593394424275095997 / (5*10^23) < 230.

Every marked-apex potential is explicitly checked in [-.3,-.2].
Deep unmarked potentials need no such restriction. These are precisely
the premises of the separate uniform B32 window lemma

    lower_bounds_extension_20261004/UNIFORM_B32_BOUNDARY_WINDOW_0p1132.md.

Its checker is freshly called. At every radius at most .1132 the
hypothetical graph-cover consequently has every full assigned arc
greater than .08 and every marked base greater than .9R. The initial
dual uses no boundary-angle weights, so the bootstrap does not assume
the weighted comparison it later enables.

## 2. The joint dual

The second pass retains the proposed boundary weights. Every neighbor
difference is at most 1/40. The proved radial-corner absorption and
consistent angle-lift identity give the outer-area-plus-weighted-angle
bound in the audited BOUNDARY_METRIC_PROOF.md. This compares a scalar
functional and never moves the centers or assumes a changed graph.

For an ordinary marked face, the unequal-base support is

    G(u_apex-mean_base)-pi*mean_base
       +(25/16)*(u_left-u_right)^2.

The .9R base window just proved supplies its hypothesis. The boundary
loss is spent once in the radial-corner weighted comparison. The
unequal-base square charge comes from the marked triangle's own
area asymmetry and is retained explicitly.

Shared-edge terms cancel on the original graph, as in the initial
dual. All 134 complete q0 supports, 32 marked supports and 32 scalar
arc supports are recomputed. The arc backend checks endpoints and
every real in-domain quadratic stationary candidate, including
extraneous roots from squaring; retaining extra candidates is safe.
The single arc-sum multiplier compensates sum(half-arcs)=pi.

## 3. Exact result

All sixteen final area upper bounds are strictly below pi. The
smallest gap, for B32_P26_F108_001, is

    557138251266709032477 / 10^24 > .000557138251266.

The saved joint_0p1132_result.json is diagnostic; fresh arithmetic,
not saved PASS status or floating optimization, determines acceptance.
These coefficients were obtained from the earlier .11316 numerical
proposals, then rounded to exact rationals of denominator 10^12.
No numerical optimization is invoked by the verifier.

The new files are separate from every frozen .11316 and .11318 source.
A complete B32 theorem at .1132 still needs a new same-radius reduction
showing that every hypothetical cover belongs to these sixteen graphs.

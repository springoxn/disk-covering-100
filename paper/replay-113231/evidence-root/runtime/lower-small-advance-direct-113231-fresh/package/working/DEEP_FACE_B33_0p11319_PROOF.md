# B33 exclusion at .11319 using deep curvature labels

Set R=11319/100000. Normalize ALL centers of a hypothetical cover by
the proved norm reflection before forming and counting its diagram.
This component concerns B33 in that normalized diagram. It is not an
exclusion of an arbitrary original B33 count preserved through reflection,
and it is not an all-count radius theorem.

## 1. Two independent non-radial arc domains

The fresh global checker
`lower_bounds_extension_20261004/verify_B33_arc_bootstrap_0p11319.py`
replays the unpenalized cap229.203, the same-radius m100/count bridge,
the no-bad-q0/q1 geometry, and marked incidence at most3. It forces
full assigned arc>.0748 and normalized half-sine>.33. The K5 comparison
has a smaller positive margin than at previous radii and is explicitly
rechecked with threshold1/20000.

For M=U-2e<=25, the separate one-row checker
`verify_B33_small_core_arc_bootstrap_0p11319.py` proves a stronger
unpenalized center cap228.99. A positive M slope and negative shifted-
ear coefficient cover every M<=25 and arbitrary ears. Constrained H
concavity then gives full arc>.107 and normalized half-sine>.4724.
Neither bootstrap spends a radial or variance penalty.

The old total face-loss budget is freshly checked below1, giving M>=22.
Core block isoperimetry forces one deep low-degree vertex for M<=25
and two weighted units of deep positive curvature for M<=23.

## 2. A topological distinction in the face labels

DEEP_CORE_CURVATURE_WITNESSES.md proves that these witnesses can be
chosen among interior vertices with NO boundary-center neighbor.
Assign potentials to four graph-theoretic classes:

* A: interior degree at least7;
* B: boundary vertices;
* O: ordinary interior vertices;
* P: deep interior vertices of degree at most5.

P vertices have marked incidence0. Other unmarked low-degree vertices
receive O, and the vertex verifier checks both possibilities separately.
A triangle containing both P and B would contain an edge from a deep
vertex to a boundary vertex, so it is impossible. Exactly16 of the20
unordered four-label triples remain. All16 are checked, including
repeated P labels; no uniqueness or pairwise separation is assumed.

The flag is applied only to class P. For M<=23 its local weight is
max(6-d,0), with final required total2. For M24/25 the required number
of P vertices is at least1. The nondeep duplicate types receive no flag.

## 3. Complete-simplex support with range below one

The four potential values can have range larger than1/2, so the old
acute-only localization is not reused. FULL_FACE_RANGE_ONE_SUPPORT.md
proves that for range strictly below1, a global support maximizer is
either in the closed acute simplex or a degenerate simplex vertex.
The checker therefore takes the maximum of

    pi*nu+sum H(nu-l_i)-(pi/3)sum l_i,
    pi*(max l_i-(sum l_i)/3).

The exact helper verifies the strict range guard and retains the
mandatory degenerate cap on every face triple. This is a statement
about a support maximizer, not about actual triangle angles.

Each row reserves a nonnegative BI credit separately for class A and
class O. Every marked vertex of either class has at least two terminal
BI incidences bordering q0 faces, so2tau of its class is paid from the
face inequalities. P has no such incidence and no BI credit.

## 4. Two compatible, case-specific radial supports

For M<=25 use
`verify_radial_B33_lowM_bootstrapped_0p11319.py` on x>=.4724:

    lambda=.056, gamma=1.5,
    Q_low=33*(.01053086)+2pi*(-.012340219).

Its909-box replay uses the original pure radial-tip node guard. No
reflection or positive-residual correction is needed by that inequality,
although it is applied to the already normalized common diagram.

For M>=26 use
`verify_reflected_radial_B33_stronger_0p11319.py` on x>=.33:

    lambda=.095, gamma=.25,
    Q_high=33*(.00894643)+2pi*(.002439839).

Its1063-box replay uses the reflected-center residual correction.
The two inequalities are never added. Each row uses exactly one support
and that support's one variance budget.

Every marked face uses the global two-endpoint conjugate for its own
lambda, with a cache keyed by penalty and multiplier. The joint ear
cap uses the same lambda, so marked-edge squares cancel exactly.

## 5. Exact vertex and integer-range checks

Use freshly verified spans L3=.4568 and L4=.69295. For e0, the row's
gamma pays the existing multiple-p3 variance charge. For e>=1, ignore
fan charges and use only one ear's footprint. The shifted-ear coefficient
is negative in both ear rows, so e1 bounds every larger ear count.

All p=0,...,3 and d=max(3,p+1),...,99 types are checked, with the three
deep/nondeep p0,d3/4/5 duplicates. Thus each row checks390 vertex types.
The five ranges are:

* e0,M22..23: low support, weighted deep flag2, positive slope, U23;
* e0,M24..25: low support, one deep flag, negative slope, U24;
* e0,M>=26: high support, no flag, negative slope, U26;
* e>=1,M22..25: low support, one deep flag, e1,U24;
* e>=1,M>=26: high support, no flag, e1,U28.

`verify_deep_face_B33_0p11319.py` verifies80 full-face supports,1950
vertex supports, all flag/slope/ear signs, and five final area bounds.
The least strict area gap is

    132833605620796209261/(5*10^23) >.0002656672112,

in the no-ear high-M range. The M24/25 gap exceeds.0011068487.
The rational data and actual exact result are saved beside the entry.

## 6. Scope and closure

The independent global and small-core arc bootstraps must both be
replayed, along with both radial entries, the complete-simplex theorem,
and the deep-witness lemma. The complete covering diagram is classified
only after whole-cover norm normalization. Fixed finite-type limits
handle degeneracies and preserve the strict area contradiction.

Other boundary counts at .11319 remain separate requirements. The
stronger isolated-five M24 lemma and future graph refinements are not
dependencies of this certificate.

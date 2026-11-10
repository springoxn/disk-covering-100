# B33 exclusion at .11318 with two case-specific radial supports

Set R=5659/50000. First normalize the whole hypothetical cover by the
reflection in section2, and only then form its diagram and count B.
This component treats B=33 in that normalized diagram, not necessarily
the boundary count of the original unnormalized centers. It is not a
universal radius theorem. The new entries preserve earlier completed files.

## 1. Independent domain and core premises

`lower_bounds_extension_20261004/verify_B33_arc_bootstrap_0p11318.py`
rechecks m100, the complete surviving count list[31,...,38], absence of
all-boundary q0/q1 faces, and marked incidence at most3. It uses only
unpenalized full-face bounds to prove normalized center/anchor cap229.203.
Concavity then gives full assigned arc>.08, hence normalized half-sine
>.353. Its strict short-arc contradiction gap is greater than .0001508.
The five-arc footprint guard is freshly checked with its smaller positive
margin; no earlier-radius threshold is reused. The bootstrap makes no
claim of marked-apex acuteness and permits arbitrary ears.

The old nonnegative face-loss budget is freshly checked below1. The core
cut gives M=U-2e>=22. The general unmarked low-degree obstruction supplies
one degree-at-most-five unmarked vertex for M<=25. The independently
proved one-positive-curvature disk theorem strengthens this to

    sum_(unmarked vertices) max(6-d,0)>=2

for M<=23. These are weighted/count constraints, with no flat-core or
equal-spacing assumption.

## 2. Reflection normalization and the smaller radial residual

Before taking the covering diagram, all centers are normalized
to norm at most C=sqrt(1-R^2). If a center is d*u with d>C, replace it by
d'*u, where d'=(1-R^2)/d. For every point z in the unit disk,

    |z-d'u|^2-R^2
      =(d'/d)(|z-du|^2-R^2)+(1-d'/d)(|z|^2-1).

Thus the replacement preserves every covered point of the target. Apply
the ordinary diagram and finite-type reduction after this normalization.

For a boundary lens corner rho*u and displacement Delta*u+t*v, the norm
constraint implies Delta<=C-rho. Consequently the soft radial residual
uses

    P(a)=(C-rho(a))*max(F_K(a),0),

instead of the older2h factor. The stable identity is
C-rho=2h*rho/(C+rho). The separately proved reflection/weak-neighbor
backend verifies the complete combined cyclic inequality; no pointwise
radial-tip optimality is assumed.

## 3. Two independently valid pair inequalities

Both pair certificates use the same complete arc domain [.353,1] and
cone factor3.60225. They differ only in the penalty and variance weight.

For low M use `verify_reflected_radial_B33_lowM_0p11318.py`:

    lambda=.056, gamma=1.5,
    Q_low=33*(.0105348)+2pi*(-.012369677).

Its1137-box replay proves outer+lambda*sum edge^2<=Q_low-gamma*V.
The exact Q upper is269927427219042734286867/10^24.

For high M use `verify_reflected_radial_B33_0p11318.py`:

    lambda=.08, gamma=.75,
    Q_high=33*(.00955965)+2pi*(-.003273547).

Its1007-box replay proves the analogous bound; its exact Q upper is
294900147587238186227221/10^24.

These are alternative bounds for disjoint M ranges. They are never
added together, and their variance budgets are not combined.

## 4. Full-face and marked support

The complete three-label face, terminal BI credit, centered-angle
cancellation, and affine vertex formulas are those proved in
RADIAL_FACE_B33_0p11316_PROOF.md. Each row rechecks all ten q0 label
triples and every p=0,...,3, d=max(3,p+1),...,99 type.

The marked score is the exact global two-branch conjugate in
QUADRATIC_MARKED_CONJUGATE.md, valid for0<=lambda<=1/8. Its cache is
keyed by both penalty and multiplier, so the two pair instances cannot
reuse an incompatible scalar value. The joint Jensen/slab ear cap uses
the same row's penalty, ensuring exact edge cancellation.

Use freshly checked spans L3=.4568 and L4=.6929. In the no-ear ranges,
the row's gamma multiplies the multiple-p3 footprint charge. In every
ear range, use only one ear and its single global variance charge.
Each ear row has a negative shifted-ear coefficient E+2c_U and hence
covers every e>=1 by evaluation at e1.

## 5. Five exact integer ranges

`verify_radial_face_B33_0p11318.py` uses:

* e0,22<=M<=23: low support, weighted curvature flag2, positive M slope,
  endpoint U23;
* e0,24<=M<=25: low support, one-low-vertex flag, endpoint U24;
* e0,M>=26: high support, no flag, endpoint U26;
* e>=1,22<=M<=25: low support, one-low-vertex flag, endpoint e1,U24;
* e>=1,M>=26: high support, no flag, endpoint e1,U28.

The last four slopes are negative. All50 full-face and1935 vertex
supports pass. The least strict target-area gap is

    9418539365562120227 / 40000000000000000000000
      > .0002354634841,

in the no-ear M24/25 range. The high-M no-ear gap exceeds .0004086372.
The rational proposal file and actual exact output are supplied beside
the verifier; numerical optimization does not participate in acceptance.

## 6. Replay and scope

Run the independent arc bootstrap, both reflected pair entries, and the
face entry in fresh processes. The face entry calls the two core flags,
the direct conjugate checks, and the integer fan lemma. Reflection is
performed before classification; continuity and the inherited constant
finite-type subsequence argument include closed/degenerate endpoints.

The optional stronger small-M arc bootstrap and its separate .06 pair
are research improvements, not dependencies of this certificate.
Other boundary counts at .11318 require their own complete exclusions
before this can become a universal lower-bound checkpoint.

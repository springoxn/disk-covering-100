# Normalized B34 exclusion at R=.1132

This component treats B34 after ALL centers of a hypothetical cover have
been reflected to norm at most sqrt(1-R^2), before constructing its new
diagram. It does not preserve the original B label and is not an all-count
radius theorem. Set R=283/2500, A=3sqrt(3)/4 and M=U-2e.

## 1. Independent domain allowing all-boundary faces

`verify_B34_arc_bootstrap_0p1132.py` replays the count bridge, giving m100
and B31,...,38. The six-arc footprint excludes more than four ordinary
marked faces at any interior apex. The old K4 exclusion is NOT assumed:
all-boundary q0 faces, bad q1 faces and q2 ears are allowed.

The three radius-independent angular proposal rows from .11319 are
rechecked at the new radius. They use full-simplex q0 supports and the
unpenalized true marked conjugate C0. Let b count bad all-boundary q1
faces. There are130+e q0 faces and34-2e-b ordinary q1 faces, while the
interior degree excess is28+e-b-U. The q0 boundary-angle sum is
Gamma+(e-2)pi, unchanged by b. Consequently a bad face contributes the
coefficient

    T_bad = M_bad - C0 - beta - eta.

Every all-boundary center triangle has normalized area at most
w=2/(1+sqrt(1-2R)); its one anchor is at most1/2. Hence M_bad=w+1/2
in this unpenalized stage. All three T_bad and shifted-ear coefficients
are strictly negative. All-boundary q0 triangles are already included
among the full-face label triples.

The same cap228.352 therefore holds for arbitrary b and e. Constrained
H concavity gives full assigned arc>.0416 and sin(half arc)/R>.1837.
The short-arc contradiction margin is100966685910149861/10^23>0.
This cap has no radial, minimum-arc or actual-angle premise.

The old normalized loss d is slightly above1 and is recomputed exactly;
the obsolete assertion d<1 is not used. If M<=21, the core has at least
109 q0 triangles, area at least R^2(109A-d), and total frontier perimeter
at most42R. Summed Euclidean isoperimetry requires
pi(109A-d)<=21^2, contradicted by the exact checked positive gap. Thus
M>=22, including disconnected or non-simple core frontiers.

## 2. Two boundary supports

`verify_general_reflected_B34_0p1132.py` replays both generalized reflected
supports on x>=.1837. Their shared cone factor is12167/3125. Tangential
residuals are retained explicitly. Both have variance coefficient0.

* low: lambda=.07,841 boxes,Q<=1468540792392406031731/(5*10^21)
* high: lambda=.08,935 boxes,Q<=60745143312187720030403/(2*10^23)

The low support is used for M<=25; high is used for M>=26. They are
alternatives, not simultaneous deductions. The node derivation and
pointwise pair support impose no ear or bad-face restriction.

## 3. Full-face rows and complete integer ranges

The general core-block theorems force two weighted deep-curvature units
for M<=23, and one deep low-degree vertex for M<=25. A deep vertex has
no boundary-center neighbor, even when bad faces are allowed. Use the
four labels and16 permitted unordered triples from
DEEP_CORE_CURVATURE_WITNESSES.md and FULL_FACE_RANGE_ONE_SUPPORT.md.
Every triple containing both deep and boundary labels is impossible;
every other triple is checked, including the degenerate-vertex cap.

Each of three rows checks485 vertex types, including both deep and
nondeep versions of unmarked degree3/4/5. Nonnegative BI credits are
reserved on q0 faces; every ordinary marked apex still has two terminal
BI transitions to q0, because a bad q1 face has only boundary vertices.

For penalty lambda the bad-face cap is

    M_bad = w + (sqrt(1+16lambda^2)-4lambda)/2.

Indeed its area is at most w, and maximizing x*sqrt(1-x^2)-4lambda*x^2
over the marked half-side x in[0,1] gives the displayed remainder.
The exact checker verifies T_bad=M_bad-C_lambda(0)-beta-eta<0 in every
row. The joint Jensen/slab q2 cap separately gives a negative shifted-ear
coefficient. Thus no count restriction on b or e is needed.

All M slopes are negative. Evaluate the weighted-flag row at M22, the
one-flag row at M24, and the flag-free row at M26. These cover every
M>=22. The complete checker `verify_deep_face_B34_0p1132.py` replays
the domain and both boundary supports, then48 face supports and1455
vertex inequalities. The smallest area margin is

    8060281986132165481/25000000000000000000000 > .00032241127.

The strict inequalities extend to the closed endpoint by the inherited
whole-cover normalization, generic perturbation and finite-type limit
argument. Other B branches must be independently combined before any
universal radius conclusion.

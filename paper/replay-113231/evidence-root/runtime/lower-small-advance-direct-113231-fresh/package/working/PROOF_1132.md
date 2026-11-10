# A certified lower bound r_D(100) > 0.1132

The problem is coverage of the closed unit disk by100 equal-radius disks
with freely chosen centers. Set R=283/2500. This is a strict lower-bound
certificate, not a determination of the exact optimum. Numerical
optimization proposes coefficients; all acceptance comparisons are exact
rational or outward integer-interval calculations.

## 1. Normalize the entire cover, then classify

Put C=sqrt(1-R^2). For every center d*u with d>C, replace it by d'*u,
where d'=(1-R^2)/d. The identity

    |z-d'u|^2-R^2
      =(d'/d)(|z-du|^2-R^2)+(1-d'/d)(|z|^2-1)

preserves every covered point z of the unit disk. Apply this to ALL
centers before forming a new clipped Voronoi/Delaunay diagram. Reflection
can change redundancy and boundary ownership, so no original B label is
preserved or used. All counts below refer to the normalized diagram.

The same-radius bridges in the B33 and B34 components recheck the old
marked constants and concavity, exclude every m<=99 case, and leave only

    m100, B=31,32,33,34,35,36,37,38.

Both reflected branches use the norm bound established before counting.
The remaining branches are valid for unrestricted centers.

## 2. B31 and the complete B32 graph reduction

The unrestricted B31 curvature theorem is valid through .11322. The
loss budget forces all interior degrees at least6, contradicting
F<=B^2/6 for F167,B31. Apply its inequalities to the same diagram with a
larger bounding radius, without reflecting or classifying again.

`lower_bounds_extension_20261004/verify_B32_complete_0p1132.py` runs the
complete new-radius reduction and finite metric chain. Low-core cases
use a unique deep degree-five witness: M24 isolates its five faces, and
M25 allows at most four incidences between its positive label and high
degree vertices. The remaining case has the same P26/F108 flat core.

The checker rebuilds41 deletion masks and16 canonical graphs, matches
each complete generated graph to its metric file by exact data equality
and SHA, and checks all16 joint boundary/metric certificates at R.
The reduction margin exceeds .000111 and the metric margin exceeds
.000557. The combinatorial lattice classification places no lattice
restriction on the actual covering centers.

## 3. B33 with an independent variance-to-arc bootstrap

`verify_complete_B33_0p1132.py` is a complete five-subprocess chain.
Initially a six-arc footprint gives only q<=4. Exact q4 vertex checks
cost at most8*.02 normalized area, giving the preliminary center cap
229.363. Constrained H concavity then excludes five boundary-center
neighbors at one apex. This restores q<=3 before the original uncharged
cap229.203 is used. It implies every full arc>.0685.

For M=U-2e<=25, an independent unpenalized cap228.99 gives full arc>.1004.
For M>=26, an initial reflected lambda=.09,gamma=.25 support is combined
with one full-face row while reserving its ENTIRE variance coefficient.
The resulting small total surplus and Cauchy on one arc and its32
complements imply full arc>.092.

Only after those actual domains are proved are the final supports used:
lambda=.056,gamma=1.5 for low M, and lambda=.11,gamma=0 for high M.
The initial and final high-M inequalities are alternatives; their
budgets are never added. The final four-label rows use deep curvature
witnesses, full-simplex supports with degenerate caps and paid terminal
BI credits. All64 faces,1560 vertices and four integer ranges pass.
Arbitrary ears are covered by checked shifted-ear coefficients.

The smallest final area gap is
1062118256560764921/31250000000000000000000, greater than .00003398.
See DEEP_FACE_B33_0p1132_PROOF.md and B33_ANGULAR_BOOTSTRAPS_0p1132.md.

## 4. B34 allowing all-boundary faces

`verify_deep_face_B34_0p1132.py` replays its own domain and both reflected
supports. It does not reuse the now-failed K4 exclusion. All-boundary q0
faces are included in the face table; bad all-boundary q1 faces have a
strictly negative coefficient M_bad-C_lambda(0)-beta-eta in both the
unpenalized bootstrap and final rows. Arbitrary ears are also allowed.

The independent cap228.352 gives full arc>.0416 and x>.1837. Two
generalized reflected supports at lambda=.07 and .08 retain their
tangential residuals explicitly. Deep-core flags and48 face/1455 vertex
checks exclude M22..23, M24..25 and M>=26. The old normalized loss is
slightly above1; the core-size proof uses its actual exact value rather
than the obsolete d<1 assertion.

The smallest area gap exceeds .0003224. See DEEP_FACE_B34_0p1132_PROOF.md.

## 5. B35 and all larger boundary counts

`lower_bounds_extension_20261004/check_B35_compensated_bootstrap_0p1132.py`
uses independently bounded raw deficits of the compensated boundary
functional to prove every half-arc>.074 or .075 in its critical ranges.
Five assigned full arcs would then exceed the3R footprint span, so every
apex has at most four boundary-center neighbors, q<=3, and each q3 fan
is contiguous. The strengthened boundary variance coefficients1.3/1.35
then pay the fan charges and exclude the remaining M25/26/27 ranges.
The complete130-face/3991-vertex replay has minimum gap greater than
.000015. No later short-arc or fan conclusion is used in its raw-budget
premise.

The unrestricted capped-pair theorem
`verify_capped_pair_B36plus_0p11323.py` excludes every B>=36 and m<=100
through .11323. Apply it to this same normalized diagram with the larger
bounding radius, without another normalization or irredundancy claim.

## 6. Integration and closed endpoints

The integrated entry uses fresh processes for the six complete boundary
components. The B32 and B33 entries additionally isolate their own
subcomponents. Exact radius, complete count lists, graph identities,
nested pair PASS results and reflection requirements are checked.
Assertions must remain enabled. Result metadata never replaces a
recomputed mathematical comparison, and Python large integers are
serialized without a floating-point round trip.

For a degenerate cover, slightly enlarge first, normalize ALL centers at
the enlarged radius, move norm-boundary centers inward, and perturb
generically within the uniform strict-coverage margin. Select a constant
finite type and pass the closed inequalities to the limit. Every final
gap is strict. Thus every possible normalized diagram is excluded and
r_D(100)>.1132.

# Alternative B33 high-M closure by the actual-anchor three-face theorem

This is a complete alternative for the normalized B33, M>=26 branch at
R=11321/100000. It is not an all-count theorem. It uses the unchanged old
reflected radial support and does not require the 402-graph metric route
or the new quadratic-lens radial backend.

## Existing necessary reduction

Retain the three successive independent variance-to-arc bootstraps.
They establish full assigned arcs>.136 and normalized half-sines>.6.
The unchanged final reflected support has lambda=7/50 and gamma=0;
its Q is no larger than 2234297/6250000. The retained 16-face profile
row then forces e=0, M=26, 66 degree-six interior vertices and one
degree-seven q3 apex. Its area upper bound exceeds pi by at most

    delta=255452797335856006499/10^24.

All initial stages establish domains only. Their variance budgets are
not added to the final inequality. Whole-cover norm normalization occurs
before the diagram is constructed and classified.

## The eligible fan and its exact coefficient

The initial geometry places every apex's boundary neighbors within four
consecutive boundary cells. The unique q3 apex uses three distinct
boundary-cycle edges; within that four-cell window these must be exactly
the three consecutive edges. The associated three marked faces form a
consistently oriented consecutive common-apex fan. Their actual common
unit transition points are covered by both endpoints of each base, and
every center triangle has circumradius at most R.

The high-degree and boundary labels in the rational profile row give
the same apex-angle coefficient

    t=1071883/20000000.

There is only one charged fan, so its marked-face and anchor incidences
are automatically disjoint. No q0 terminal edge credit is reassigned.

## Actual signed anchors, not independent anchor maxima

For successive boundary centers c_i,c_(i+1) with actual unit transition
z_i, use the signed anchor

    A_i=det(z_i-c_i,c_(i+1)-c_i)/2.

The old boundary Q bounds only sum Hactual_i plus lambda times the sum
of squared actual boundary-base lengths. It does not include the gap
J_R(L_i)-A_i. Start with the signed shoelace decomposition before using
A_i<=J_R(L_i). The exact accounting is detailed in
ACTUAL_ANCHOR_FEE_PROFILE_INTERFACE_0p11321.md.

The pinned local theorem in
local_actual_anchor_20261005/research/q3_actual_quadratic_support/PROOF.md
proves, at these exact R, lambda and t,

    sum over the three faces of
    [area/R^2 + actual signed A/R^2 - lambda*(L/R)^2 + t*gamma]
       < 3*C_lambda(t)-1/40.

It permits either anchor sign, arbitrary actual covered unit anchors,
and all circumradii at most R. Its paid-deficit proof includes skew,
apex-angle slack and the actual anchor slack once. It assumes neither
equal circumradii nor independently maximal anchors. Its separate
degenerate-closure addendum excludes zero-area limits before divisions.

Apply this theorem only to the unique eligible fan; retain the usual
J majorants for all other marked faces. The final boundary Q, all q0
face supports, star-angle identities and terminal BI credits stay in
their original locations. The global area bound decreases by R^2/40.

## Exact replay and strict contradiction

verify_actual_anchor_highM_B33_0p11321.py replays all three arc stages,
the old final pair, and the rational profile. It checks the exact tilt,
then hashes all 70 frozen local research files against the pinned source
manifest and imports the local guard under a non-main name in a fresh
Python process. The local guard is called once; no certificate is
rewritten, and all returned fields must equal its pinned certificate.

The local and global scalar kernels concern the same mathematical
conjugate. The adapter nevertheless subtracts three times their possible
enclosure mismatch from the fee, using the local upper and global lower,
and checks that the two rigorous conjugate intervals overlap. This
conservative adjustment is far smaller than the final strict margin.

Without that optional rounding allowance the exact gap is

    R^2/40-delta=64959805164143993501/10^24.

The verifier requires the adjusted gap to exceed .0000649. Together with
the inherited generic-limit argument and the local degenerate closure,
this excludes the whole normalized B33 high-M branch. Other counts and
the low-M branch retain their separate complete verifiers.

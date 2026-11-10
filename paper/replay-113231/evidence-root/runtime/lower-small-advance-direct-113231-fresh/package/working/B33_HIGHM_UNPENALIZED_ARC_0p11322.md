# Independent B33 high-M starting domain at R=.11322

This proves an actual arc-domain implication, not a covering exclusion.
Let R=5661/50000 and assume the normalized diagram has m100, B33 and
M=U-2e>=26. Whole-cover normalization precedes the diagram; the present
angular inequalities themselves do not need the norm constraint.

First replay lower_bounds_extension_20261004/verify_B33_arc_bootstrap_0p11322.py.
It freshly excludes m<=99, leaves counts B31,...,39, excludes bad q0/q1
faces by the four-cell span .4569, and initially allows q<=4 via the
six-cell span .6932. The original center cap is enlarged from229.203 to
229.363 by a rigorously paid .02 per q4 star, at most eight times. A
five-cell grouped-H comparison then excludes five boundary neighbors,
giving q<=3 and the four-consecutive-cell window. Only after this step
is the uncharged229.203 cap used to establish full arc>.0562. No radial,
fan-variance or actual marked-apex acuteness premise enters this chain.

The strengthened high-M checker adds two four-label rows. Their q0
supports use the full-simplex range-below-one theorem with its degenerate
vertex cap and all16 label multisets without a deep/boundary pair. The
positive label is assigned only to genuinely deep unmarked low-degree
vertices; both deep and nondeep degree-three through degree-five types
are checked. No compulsory low-degree witness is assumed here. The
global full-apex marked conjugate is used with zero squared-edge penalty.
Nonnegative terminal BI credits are reserved and paid once.

The M26 row is used at that exact integer. Its M slope is positive and
is not extrapolated. The second row has a strictly negative M slope and
is used for all M>=27. Both shifted-ear coefficients are negative, so
arbitrary ear counts are covered. Their exact center upper bounds are

    M26: 57294182175388450322604237/(250000000000000000000000),
    M>=27: 229172432381487357539725229/10^24.

Both are less than229177/1000. The checker verifies32 full-face supports
and780 vertex inequalities without an actual-angle or degree-window
restriction.

Let H(a)=a-sin(a)*(cos(a)-sqrt(R^2-sin(a)^2)) and mu=pi/33. If one full
assigned arc is at most .0597, strict concavity of H and the other32
half-arc sum give

    pi <= R^2*(229177/1000)+H(.0597/2)
                              +32H((pi-.0597/2)/32).

For a still shorter first arc the right side decreases, because its
derivative is H'(a)-H'((pi-a)/32)>0 for a<mu. Exact arithmetic proves
the displayed upper bound is below pi by

    9599858496401094353/10^24 > .00000959985.

Therefore every actual full arc is greater than597/10000=.0597, and the
exact sine comparison gives sin(a)/R>659/2500=.2636. The complete entry
verify_B33_highM_unpenalized_arc_0p11322.py invokes the original domain
checker in a fresh process, then checks both new rows and the final
Jensen comparison. Its result is only a starting domain for a later
radial support; no radial or variance budget is spent here.

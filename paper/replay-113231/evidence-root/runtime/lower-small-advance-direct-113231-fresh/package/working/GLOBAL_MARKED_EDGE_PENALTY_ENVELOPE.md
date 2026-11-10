# A global marked-apex penalty envelope

For lambda=37/1000 or1/25, the concave marked penalty envelope from
MARKED_EDGE_PENALTY_ENVELOPE.md is valid on the **full** apex interval[0,pi].
This removes its acute-apex hypothesis for these two parameters. The same
claim is false for lambda=.06; that parameter is not included.

The normalized area-plus-anchor minus lambda times the normalized marked
base square is bounded by

A z+sqrt(z(1-z)), A=cot(gamma/2)-4lambda,
0<=z<=sin(gamma)^2.

The proposed envelope remains its low-angle curve throughpi/3 and that
curve's tangent thereafter. Its low-curve concavity and active endpoint
maximum through6/5 are checked as before.

On[6/5,13/5], discard the upper constraint on z. The unrestricted maximum
U_lambda=(A+sqrt(1+A^2))/2 is convex in gamma: cot(gamma/2) is convex on
this interval, and the displayed function of A is increasing and convex.
The proposed line exceeds U_lambda at both endpoints by exact positive
margins, so it exceeds it throughout.

For gamma>=13/5, sine decreases and is less than1/sqrt(2). The derivative
of the z-score at its upper endpoint is at least

-4lambda+(1-2sin(13/5)^2)/(2sin(13/5)),

because A>=-4lambda and sqrt(1-sin(gamma)^2)<=1. The exact checker makes
this lower bound positive. The z-score is concave and its derivative
decreases in z, so its maximum is at z=sin(gamma)^2. Since gamma is obtuse,
that endpoint score simplifies to sin(gamma)-4lambda*sin(gamma)^2. It is
at most sin(gamma)<=pi-gamma. The proposed line exceeds pi-gamma at both
13/5 andpi, hence on their full interval.

These arguments cover the closed angle simplex by continuity. The envelope
is globally concave because its low curve is concave and joins its tangent
with equal value and derivative atpi/3. All non-symbolic guards are replayed
by verify_global_marked_edge_penalty.py. This is a local tool for future
star or fixed-graph certificates, not a new covering-radius lower bound.

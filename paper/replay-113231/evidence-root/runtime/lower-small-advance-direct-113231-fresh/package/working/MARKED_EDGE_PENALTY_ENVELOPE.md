# Acute marked-apex score with a squared-base penalty

This local lemma has an explicit acute-apex hypothesis. It must not be used
as an all-angle envelope: for lambda=.06 its line fails near gamma=2.6852.
It is intended to combine exact star/face angle supports with a separately
certified bound for the sum of squared marked edge lengths and the circular
outer-fan contribution.

Let a marked center triangle have circumradius at most R and acute apex
gamma, marked side length L=2Rx, and its boundary anchor area at most
R^2*x*sqrt(1-x^2). Its normalized area-plus-anchor minus lambda*L^2/R^2 is
at most

(cot(gamma/2)-4lambda)z+sqrt(z(1-z)), 0<=z=x^2<=sin(gamma)^2.

For lambda=1/25 or3/50, a concave majorant on the entire interval[0,pi/2] is

G_lambda(gamma)=sin(gamma)*(1+2cos(gamma))-4lambda*sin(gamma)^2,
  for gamma<=pi/3;

sqrt(3)-3lambda-(1/2+2sqrt(3)lambda)*(gamma-pi/3),
  for gamma>=pi/3.

## Proof

On gamma<=6/5 the derivative of the z-score at z=sin(gamma)^2 is
cot(gamma/2)+cot(2gamma)-4lambda. Its unpenalized portion is strictly
decreasing and its value at6/5 is greater than4lambda, as the exact checker
verifies. Hence the maximum occurs at the circumradius endpoint and equals
the first displayed curve. This curve is concave through6/5: its second
derivative is -sin(gamma)(1+8cos(gamma))-8lambda*cos(2gamma). On[0,pi/4]
both terms are nonpositive. On[pi/4,6/5], use sin(gamma)>=sqrt(2)/2 and
cos(gamma)>.36 to obtain a strictly negative upper bound.

Its tangent atpi/3 therefore dominates it through6/5. Beyond6/5, discard
the upper constraint on z. The unrestricted score is

U_lambda(gamma)=(A+sqrt(1+A^2))/2, A=cot(gamma/2)-4lambda.

The cotangent is convex on this interval, and the displayed function of A
is increasing and convex, so U_lambda is convex. The proposed line exceeds
it at both6/5 andpi/2 by exact positive margins. Their difference is
concave, so the line dominates throughout. The line meets the low curve
with its tangent derivative atpi/3, giving a globally concave majorant on
the acute domain, including both closed endpoints by continuity.

`verify_marked_edge_penalty_envelope.py` replays every non-symbolic comparison
using the immutable rational interval arithmetic. It also exposes the
one-variable conjugate for use in future exact angle certificates. No
covering-radius improvement is claimed from this local lemma alone.

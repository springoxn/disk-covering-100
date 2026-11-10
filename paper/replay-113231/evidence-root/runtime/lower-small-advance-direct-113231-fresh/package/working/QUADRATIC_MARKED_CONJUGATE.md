# Full-apex conjugate for a squared marked-base penalty

Let a center triangle have circumradius at most1, marked base length2x,
apex angle gamma, and ordinary anchor x*sqrt(1-x^2). For any real s and
0<=lambda<=1/8, the sharp supremum of

    area + anchor - 4lambda*x^2 + s*gamma

is the maximum of the two one-dimensional suprema, for a in[0,pi/2],

    F_acute(a)=sin(a)[1+2cos(a)]-4lambda*sin(a)^2+s*a,
    F_obtuse(a)=sin(a)-4lambda*sin(a)^2+s*(pi-a).

Both scalar functions are concave on the entire interval. In particular
this conjugate does not require a globally valid concave envelope as a
function of the actual apex angle, or any actual-apex acuteness premise.

## Proof of the two endpoint reduction

For fixed x and gamma, elementary triangle geometry gives

    area <= x^2*cot(gamma/2).

Equality holds for an isosceles triangle. For example, write the two
base angles as beta and pi-gamma-beta. The sine rule shows that area is
proportional to their sine product, maximized when they are equal.
The circumradius constraint is x<=sin(gamma), so

    asin(x) <= gamma <= pi-asin(x).

For x>0 the upper score

    x^2*cot(gamma/2)+x*sqrt(1-x^2)-4lambda*x^2+s*gamma

is convex as a function of gamma: the second derivative of cot(gamma/2)
is positive on(0,pi). Its maximum on the displayed interval is at an
endpoint. With x=sin(a), the first endpoint's area is
x(1+sqrt(1-x^2)); adding the anchor gives x(1+2sqrt(1-x^2)). The second
endpoint's area is x(1-sqrt(1-x^2)); adding the anchor gives x. This
proves the two formulas. Their endpoint configurations have circumradius
one and are attained by isosceles triangles; zero-base limiting cases
follow by continuity. Thus the support bound is sharp.

## Concavity

The second derivatives are

    F_obtuse''=-sin(a)-8lambda*cos(2a),
    F_acute''=F_obtuse''-4sin(2a).

If cos(2a)>=0 they are nonpositive. Otherwise put y=sin(a) in[0,1].
Then |cos(2a)|=2y^2-1<=y, since

    2y^2-y-1=(2y+1)(y-1)<=0.

Together with8lambda<=1 this again makes both derivatives nonpositive.
No trigonometric numerical approximation is used in this argument.

## Exact implementation and endpoint hardening

`exact_quadratic_marked_conjugate.conjugate(lambda,s)` evaluates the two
concave suprema by outward integer-interval root bisection, including
both endpoint maxima. The uncertain pi/2 endpoint is handled by an
explicit tangent continuation:

    acute: (s-2)*a + pi + 1-4lambda,
    obtuse: -s*a + s*pi + 1-4lambda.

The values and derivatives match at pi/2. Each continuation preserves
concavity, and interval hulls cover the uncertain join. When its slope
is positive (acute s>2 or obtuse s<0), the routine obtains the lower
endpoint from the feasible exact pi/2 value rather than from the
slightly extended domain; the upper remains safe. Therefore the
routine never relies on the original acute formula's behavior just
beyond the exact endpoint. The larger of the two enclosing intervals
is the desired conjugate. All multipliers supplied to acceptance are
rational; proposal optimization is separate.

The module's30 sample checks exercise five penalty values, including0
and1/8, and six multipliers with both interior and endpoint regimes.
These tests supplement the analytic proof rather than replacing it.

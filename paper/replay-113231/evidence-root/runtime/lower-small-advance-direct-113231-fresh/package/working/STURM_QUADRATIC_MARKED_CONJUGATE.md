# Complete scalar marked support for arbitrary nonnegative base penalties

The module sturm_quadratic_marked_conjugate.py extends the squared-base marked
conjugate to every rational lambda>=0. It changes no completed radius source.
The geometry is the same fixed-base endpoint reduction used by the audited
exact_quadratic_marked_conjugate.py; only the one-dimensional maximization
method changes. No concavity is asserted for lambda>1/8.

## 1. Fixed-base endpoint reduction

Normalize the radius to1 and write x=L/2 in[0,1]. For a center triangle with
marked base L and opposite angle gamma, its circumradius at most1 forces

    asin(x)<=gamma<=pi-asin(x).

At fixed gamma and L its area is at most x^2*cot(gamma/2): put the base
endpoints at(-x,0),(x,0), and maximize apex height on the constant-angle arc.
Adding the external anchor and a squared-base penalty gives

    x^2*cot(gamma/2)+x*sqrt(1-x^2)-4lambda*x^2+t*gamma.

This function is convex in gamma on(0,pi), since cot(gamma/2) has positive
second derivative there. Therefore its maximum on the permitted interval
is at an endpoint. With a=asin(x), the two endpoint functions are

    F(a)=sin(a)*(1+2cos(a))-4lambda*sin(a)^2+t*a,
    H(a)=sin(a)-4lambda*sin(a)^2+t*(pi-a),

for a in[0,pi/2]. Their maximum is the desired scalar support. Degenerate
bases/triangles are covered by endpoint limits. This reduction is valid
for all lambda>=0 and every real t; large lambda changes neither convexity
in gamma nor the angle domain.

## 2. All stationary candidates are algebraic cosines

Put c=cos(a), s=sqrt(1-c^2). At an interior stationary point,

    F': 4c^2+c-2+t=8lambda*c*s,
    H': c-t=8lambda*c*s.

Squaring gives quartic polynomials

    P_F(c)=(4c^2+c-2+t)^2-64lambda^2*c^2*(1-c^2),
    P_H(c)=(c-t)^2-64lambda^2*c^2*(1-c^2).

For rational lambda,t these have rational coefficients; denominators may
be cleared to obtain integer polynomials. Every actual stationary cosine
belongs to their roots in[0,1]. The implementation deliberately retains
all real roots in that interval, including those violating the unsquared
sign condition. Such extra roots are feasible values of a and cannot
invalidate an upper bound or a feasible lower bound.

## 3. Exact complete root isolation

The module uses rational polynomial long division, gcd and squarefree
reduction. Endpoint roots0 and1 are recorded and deflated. For the remaining
polynomial the rational Sturm chain is p,p', followed by negative Euclidean
remainders; only positive rescalings are used within that chain. Its sign
variation drop between two nonroot rational endpoints counts exactly the
distinct roots in their open interval.

The initial interval[0,1] is split until every retained bracket has one
root. A subdivision coinciding with a polynomial root is avoided while
isolating multiple roots; there are only finitely many such trial points.
When refining a one-root bracket, an exact rational midpoint root is
recorded directly. Otherwise the Sturm counts select the unique subinterval
containing the root. Repeated roots are covered by squarefree reduction,
not discarded. Five root-count fixtures check repeated/endpoint/interior
root cases.

The reusable root-isolation entry rejects the identically zero polynomial,
which has infinitely many roots rather than an empty finite root list.

## 4. Radical, inverse-trigonometric and score enclosures

For a cosine bracket, outward fixed-point intervals bound c and sqrt(1-c^2).
The decreasing acos function is evaluated at its rational interval
endpoints. For0<=c<=1, write

    z=sqrt((1-c)/(1+c)),
    acos(c)=4atan(z/(1+sqrt(1+z^2))).

The atan argument is at most sqrt(2)-1<1/2. Forty alternating-series terms
give a lower sum and a positive omitted-term upper remainder. The exact
cases c=0 and c=1 use pi/2 and0. The pi enclosure, integer square root and
all outward arithmetic are the unchanged checkpoint interval routines.

Both feasible endpoint scores and every isolated cosine-root score are
enclosed. The maximum of their upper endpoints bounds the true global
maximum: a smooth function on a compact interval achieves it at an endpoint
or an interior stationary point. The maximum of their lower endpoints is
a legitimate feasible lower bound, since each root itself lies in[0,1].

Refinement stops at the requested score width or the exact fixed-point
resolution. An exact-grid rational root can sit strictly between all dyadic
bracket endpoints; the module tests the at most three enclosed grid points
algebraically and records the exact root if found. Otherwise an unchanged
two-unit cosine plateau is retained as a safe outward enclosure. A
wider-than-requested interval at that resolution remains a
safe bound and is not reported as a sharper certificate. The sample replay
checks a width below10^-11 for its inputs. No floating result, numerical
optimizer or presumed root count is accepted.

## 5. Interface and limits of this result

conjugate(lambda,t) returns an outward interval of the scalar support and
uses exact rational lambda,t. Its sample verifier checks30 pairs including
lambda=0,1/25,1/8,3/20,1/2,2, compares with the existing concave backend on
their shared domain, and separately checks feasible endpoint/equilateral
scores. It establishes a scalar kernel only. Any covering theorem still
needs its geometric preprocessing, arc-domain certificate, squared-edge
cancellation, count duals, other boundary counts and limiting closure.

# Exact full-shape support for a PPZ triangle

Normalize the target radius to1. Let two P-corners have equal corner potential
lambda_P and opposite half-edge coefficient -tau, where tau>=0. The Z-corner
has potential lambda_Z and opposite half-edge coefficient0. Put
delta=lambda_Z-lambda_P. Allow a nonnegative center-area weight A. The exact
closed full-shape support is

    max{-pi*delta/3,2pi*delta/3,
        max_[0<=s<=1] [4A*s*(1-s^2)^(3/2)-2tau*sqrt(1-s^2)
                       +2delta*asin(s)-pi*delta/3]}.

No acute-angle or potential-range/edge-size localization premise is needed.
This is a local face theorem, not a complete covering proof.

## 1. Symmetrization is a convex-endpoint reduction

Write alpha,beta for the P-angles, gamma for the Z-angle, and rho<=1 for
the circumradius. The equal P-potential gauge cancels because the angles
sum to pi, leaving delta*(gamma-pi/3). Put

    s=sin(gamma/2), y=cos(gamma/2), x=cos((alpha-beta)/2) in[s,1].

The score is

    2A*rho^2*sin(gamma)*(x^2-s^2)-2tau*rho*y*x
        +delta*(gamma-pi/3).

For fixed gamma,rho it is convex in x, so only x=s or x=1 can maximize it.
The first is degenerate: its area is0 and its edge term is nonpositive.
Its score is at most the maximum of the two displayed corner caps. The
second makes alpha=beta. Its remaining dependence on rho is convex, since
A>=0 and the area is nonnegative. Thus rho=0 or1 suffices. The rho=0 branch
again gives the corner caps; rho=1 gives the displayed one-variable score.

All these branches are feasible closed local limits. This proves equality
of the full-shape supremum and the stated maximum, rather than merely an
upper obtained by assuming reflection symmetry. Positive tau is required;
a signed coefficient of the opposite sign needs a different degenerate cap.

## 2. Every interior stationary point is a quartic root

The derivative of the one-variable score is

    2[8A*s^4-10A*s^2+tau*s+2A+delta]/sqrt(1-s^2).

For A>0, every interior stationary s is therefore a root of this nonzero
quartic in(0,1). The endpoints and both corner caps are retained. The
implementation uses the independently audited rational squarefree/Sturm
isolation functions to cover all roots in[0,1]. This polynomial is unsquared,
so there are no squaring-sign extraneous candidates. Multiple roots and
rational/grid roots are covered by the same audited isolation logic.

For A=0, the score is at most its corner caps because the edge penalty is
nonpositive, so the implementation returns those caps directly and never
passes a zero polynomial to root isolation.

## 3. Outward score evaluation

Every root bracket is evaluated using exact integer outward intervals,
radicals and asin(s)=pi/2-acos(s), with the audited transformed-atan acos
routine. The maximum of upper endpoints bounds the full-shape support;
lower endpoints are feasible lower bounds because the actual bracketed
root corresponds to an isosceles local shape. Fixed-grid plateaus retain
safe broader intervals if requested precision is below kernel resolution.
No floating optimizer or numerical root participates in acceptance.

exact_pp_face_support.py exposes pp_support(tau,delta,area_weight=1). Its
60 sample checks include tau up to1.3, either sign of delta, zero area weight,
equilateral and degenerate lower fixtures, and an exact-grid half-angle root
at requested precision10^-40. These tests supplement the analytic proof.

Global use must retain the actual sign and gauge convention stated here,
the two equal P-potentials and edge coefficients, the chosen area weights,
and all neighboring face/edge cancellation and incidence constraints.

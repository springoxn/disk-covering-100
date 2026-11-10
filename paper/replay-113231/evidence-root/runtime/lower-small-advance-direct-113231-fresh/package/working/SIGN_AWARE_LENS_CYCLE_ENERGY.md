# A stronger sign-aware endpoint-lens cycle energy bound

Let0<R<1/2. Boundary assigned half-arcs a_i are in[a0,asin R], where
x0=sin(a0)/R. Endpoint-lens displacements have radial component Delta_i>=0
and tangential component t_i, and their direction differs from the radial
midpoint by at most beta_i=acos(sin(a_i)/R). Set

    eta0=asin(x0)-a0, xi0=asin(x0)+a0.

If x0>=2R*sqrt(1-R^2), then

    sum_i|delta_i-delta_next|^2<=K*sum_i|delta_i|^2,
    K=2+max(0,cos(2eta0))+max(0,cos(2xi0)).

This improves the prior factor2+2max(0,cos(2eta0)) by distinguishing the two
opposite-sign orientations. It is not an assumption of equal arcs or equal
displacements. Reflection normalization is unnecessary for this energy
lemma itself; it remains necessary for the subsequent reflected-node cap.

## Direction cones and sign classification

The endpoint lens gives s_i|t_i|<=h_i*Delta_i. Thus every nonzero delta_i
has direction theta_i+sigma_i*phi_i, with sigma_i the sign of t_i and
0<=phi_i<=beta_i. Zero tangential components can receive either sign;
zero displacements are harmless. Consecutive radial midpoint directions
differ by a_i+a_next in[0,2asin R].

For equal signs the absolute displacement-direction difference is at most
acos(x0)+2asin R<=pi/2, by the stated cutoff guard. Their dot product is
nonnegative and creates no positive energy contribution.

For a negative-to-positive edge, its direction difference is at most

    a_i+a_next+beta_i+beta_next=pi-eta_i-eta_next,
    eta_i=asin(sin(a_i)/R)-a_i>=eta0.

The negative part of its normalized dot product is therefore bounded by
cA=max(0,cos(2eta0)). For a positive-to-negative edge, the absolute difference
is at most the larger of a_i+a_next and beta_i+beta_next-a_i-a_next. The
first is at most pi/2. The second is pi-xi_i-xi_next, where

    xi_i=asin(sin(a_i)/R)+a_i>=xi0.

It can yield a negative dot product only when xi_i+xi_next<pi/2; its negative
part is bounded by cB=max(0,cos(2xi0)). Since R<1/2, xi0<3pi/4, so this
positive-part expression has no spurious second positive cosine branch.
The monotonicity of eta and xi follows from derivatives c/h-1>0 and c/h+1>0.

## Every vertex has one slot of each orientation

A positive vertex can have at most one incoming negative-to-positive edge
and one outgoing positive-to-negative edge; for a negative vertex the roles
reverse. Consequently each vertex is incident to at most one cA edge and
one cB edge. Put d_i=|delta_i|. Dropping nonnegative dot products and using
2d_i*d_next<=d_i^2+d_next^2 gives

    sum|delta_i-delta_next|^2
      <=2sum d_i^2+2sum c_edge*d_i*d_next
      <=[2+cA+cB]sum d_i^2.

This argument applies to odd or even cycles, arbitrary magnitudes and
arbitrary arc sizes. It does not assume that all neighboring pairs can
simultaneously attain their individual worst directions.

## Exact radical and rational forms

Write s0=R*x0,c0=sqrt(1-s0^2),h0=R*sqrt(1-x0^2),rho0=c0-h0. Then

    cos(2eta0)=1-2(x0*rho0)^2,
    cos(2xi0)=1-2[x0*(c0+h0)]^2.

Both can be checked without inverse trigonometry. When both are positive,
their sum simplifies exactly to

    2(1-2x0^2)(1-2R^2*x0^2).

At R=.11321,x0=.6, K is less than2.55484, compared with the old2.81507
rounded factor. The checker supplies the cutoff guard and outward scalar
factor; any radial backend must explicitly use this new energy proof rather
than passing the old larger-factor guard unchanged. No new radius theorem
is asserted by this lemma alone.

# Exact lens compensation using only unit-disk center projection

This lemma does not require the stronger radius-dependent center bound
sqrt(1-R^2). Centers may first be projected into the closed unit disk:
for d>1 and |x|<=1,

    |x-u|^2-|x-d*u|^2=(1-d)(1+d-2x.u)<=0.

This projection preserves the covered part of the unit disk. As usual,
the resulting diagram is classified afterward.

For a boundary half-arc use s,c,h,rho,u,a and the displacement(Delta,b)
from EXACT_NORMALIZED_LENS_PENALTY.md. More generally impose a fixed norm
bound C with C>=rho. The far endpoint-lens circle has parametrization

    Delta=R[cos a-cos theta], b=R[sin theta-sin a], theta=a+2z.

Its upper-half branch has a<=theta<=pi-a. The actual center's norm
squared is1+R^2-2R*cos(theta-t), increasing along that branch. If its norm
circle cuts the branch, the intersection is

    theta_C=acos((1+R^2-C^2)/(2R))+t.

The exact support is the same objective

    max 2R^2 sin z[k-u sin(z+a)]

over zero<=z<=[min(theta_C,pi-a)-a]/2. If the cap circle contains the
entire lens branch, simply use the endpoint pi-a. Beyond a cap-circle
intersection, d^2=C^2-rho^2-2rho*Delta decreases with Delta, so no point
of that cap-circle boundary improves the objective.

For C=1 the relevant intersection is theta_C=acos(R/2)+t. In the bad
interval u^2<=k, the accompanying checker verifies theta_C<pi-a, so this
intersection formula applies without a branch ambiguity. The zero
displacement remains included, and the endpoint-lens inequality alone
still proves the support is zero for u^2>=k.

The scalar second derivative is

    g''/(2R^2)=-k*sin z-2u*cos(2z+a).

When2z+a<=pi/2 it is nonpositive immediately. Otherwise
z>=(pi/2-a)/2. A sufficient explicit guard is

    k*sin((pi/2-a)/2)>2u*max(0,-cos(theta_C)).

The checker verifies this guard on every outward-rounded t box. It is
valid because sine is increasing on the relevant z interval and cosine
is decreasing up to the tested theta_C<pi. Thus the same tangent support
method remains rigorous even when theta_C is slightly beyond pi/2.

At R=.11322,B35,k=.42 the exact1000-box check passes with variance.03 and
minimum bad-box margin greater than.00040915. At t=0 the exact penalty
is k*R^2*sqrt(2-R), also enclosed independently by the half-angle formula.
The global reference-edge/half-side accounting and good-arc curvature
argument are unchanged from the normalized-lens proof.

This is a conditional boundary envelope, not a complete radius branch.
It replaces one displacement estimate rather than adding a second copy
of its loss. Its only center-norm prerequisite is1, independent of the
target radius, which avoids the stronger normalization's radius-transfer
issue in future assembled arguments.

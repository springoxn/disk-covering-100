# A sharper radial node guard below the sine cutoff1/3

This extends the simultaneous center support from the earlier checkpoints.
It does not change their constants. Let half-arcs lie in[a0,asin(R)], with
0<R<1/2, and define s0=R*x0=sin(a0), c0=cos(a0),
h0=sqrt(R^2-s0^2), rho0=c0-h0. The endpoint-lens displacement expansion
gives the same radial and tangential node coefficients w_r,w_t as before.

Four exact guards suffice:

1. 1+R*c0/s0-2rho0*c0 <4;
2. x0/sqrt(1-x0^2) >2R*sqrt(1-R^2)/(1-2R^2);
3. 4lambda*rho0*s0 <1;
4. 8lambda*rho0*s0^2+8lambda*h0-s0 <0.

The auxiliary quantities1-rho0*c0 and R-rho0*s0 are positive. They can be
proved algebraically from rho0<=c0<1 and s0<R; the code rechecks their
signs. The source radial_sharp_node_backend.py verifies every guard by
outward-rounded exact intervals.

## Tangential charge

For fixed middle half-arc b, rho(a)*sin(a+b) is increasing in a: rho'>=0,
and both sin(a+b) and cos(a+b) are positive since a+b<pi/2. Its minimum
is rho0*sin(a0+b), and its maximum is at most sin(asin(R)+b). Thus the
difference of two such neighbor terms has absolute value at most their
range, not their sum. Dividing this range by sin(b) and using
cot(b)<=cot(a0) gives an upper bound

1+R*c0/s0-2rho0*c0.

Guard1 proves |w_t|<=8lambda*sin(b), so the residual tangential charge k
is zero, even when x0<1/3.

## Neighbor radial products

The derivative rho'(a)=sin(a)*rho(a)/h(a) gives

d/da [rho(a)cos(a+b)]
=rho(a)cos(a+b)[sin(a)/h(a)-tan(a+b)].

Its first ratio is at least x0/sqrt(1-x0^2), and the tangent is at most
tan(2asin(R))=2R*sqrt(1-R^2)/(1-2R^2). Guard2 makes the derivative positive,
including the endpoint by continuity. Both neighbor radial products are
therefore minimized at a0, rather than by combining unrelated worst-case
radial and angular values.

Consequently w_r at the middle arc b is at most

F(b)=4lambda[cos(b)(1-rho0*c0)+h(b)+rho0*s0*sin(b)]-sin(b).

Differentiating, its negative terms can be dropped to obtain
F'(b)<=cos(b)[4lambda*rho0*s0-1]<0 by guard3. Its maximum is therefore at
b=a0, where it equals the left side of guard4. Thus w_r<0 everywhere.

Combining k0 and w_r<0 with the endpoint-lens inequality makes every node
residual nonpositive. Hence the actual outer-fan contribution plus the
global squared marked-edge penalty is bounded by its radial-tip version.
The h=0 endpoint is handled by the continuous limit; no derivative at that
endpoint is divided by zero in the proof or code.

At R=.11312,lambda=.039,x0=.307 all guards pass with comfortable strict
margins, and the necessary full-arc cutoff.0695 places every actual half-arc
inside this closed parameter domain. The accompanying stable pair bound
and complete star/count arguments are separate components.

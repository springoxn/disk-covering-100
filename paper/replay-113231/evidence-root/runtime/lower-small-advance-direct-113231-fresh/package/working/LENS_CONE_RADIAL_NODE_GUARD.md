# A lens-cone improvement of the cyclic displacement bound

This is a local support theorem for the simultaneous radial-center reduction. It improves the crude quadratic factor four without assuming symmetry or compatibility of independent maximizing centers. It does not establish a new covering radius by itself.

Fix 0<R<1/2, a nonnegative squared-edge penalty lambda>=0, and a normalized half-sine cutoff 0<x0<1. Every assigned half-arc a_i lies in [asin(R*x0),asin(R)]. Define

s_i=sin(a_i), h_i=sqrt(R^2-s_i^2), rho_i=cos(a_i)-h_i,
eta_i=asin(s_i/R)-a_i.

Let p_i=rho_i*u_i be the inward endpoint-lens corner, and write the actual center as p_i+delta_i. In radial/tangential components delta_i=Delta_i*u_i+t_i*v_i, endpoint coverage gives

2h_i*Delta_i >= |delta_i|^2+2s_i*|t_i|.

Thus Delta_i>=0 and |t_i|<=h_i*Delta_i/s_i. Every nonzero displacement direction is within beta_i=arccos(s_i/R) of its radial direction.

## 1. A stronger global quadratic bound

Adjacent radial midpoint directions differ by a_i+a_(i+1). Their displacement directions therefore differ by at most

beta_i+beta_(i+1)+a_i+a_(i+1)=pi-eta_i-eta_(i+1).

This lies strictly below pi. Since eta'(a)=cos(a)/h_i-1>0, one has eta_i>=eta0=asin(x0)-asin(R*x0)>0. Consequently

delta_i dot delta_(i+1) >= -cos(2eta0)*|delta_i|*|delta_(i+1)|.

Assume eta0<=pi/4, so q=cos(2eta0)>=0. Young's inequality then gives

|delta_i-delta_(i+1)|^2 <= (1+q)(|delta_i|^2+|delta_(i+1)|^2).

Summing the cycle proves

sum |delta_i-delta_(i+1)|^2 <= K_cone*sum |delta_i|^2,
K_cone=2(1+q)=4cos(eta0)^2.

Zero displacements and h_i=0 are included by continuity. The proof applies to any boundary-cycle length; it does not require odd parity. If eta0 exceeds pi/4, the simpler factor two follows by discarding the positive scalar products, but that case is not needed by the supplied certificates.

The constant has a radical-only expression. Put s0=R*x0, c0=sqrt(1-s0^2), h0=R*sqrt(1-x0^2), rho0=c0-h0. Then sin(eta0)=x0*rho0 and

K_cone=4[1-x0^2*rho0^2].

At R=.11312 and x0=.307 this is less than3.700214, substantially below both four and the C33 spectral factor2+2cos(pi/33).

## 2. The resulting node guard

Choose any exact upper K>=K_cone with K>=2. In the established cyclic edge-square expansion, substituting the cone bound and the endpoint-lens inequality changes the residual node coefficients to

wr=2lambda[2rho_b-rho_a*cos(a+b)-rho_c*cos(b+c)]+2K*lambda*h_b-s_b,
wt=2lambda[rho_a*sin(a+b)-rho_c*sin(b+c)],

with tangential subtraction 2K*lambda*s_b*|t_b|.

The independently proved endpoint argument in RADIAL_NODE_ENDPOINT_GUARD.md remains valid with these replacements. Sufficient exact guards are

1. x0^2>4R^2(1-R^2)
2. 4lambda*rho0*s0<1
3. sqrt(1-R^2)*(s0*sqrt(1-R^2)+c0*R)-2rho0*s0*c0 <= K*s0
4. 8lambda*rho0*s0^2+2K*lambda*h0 <= s0.

The neighbor radial products increase, so

wr <= 4lambda[(1-rho0*c0)*cos(b)+rho0*s0*sin(b)]
       +(2K-4)*lambda*h_b-s_b.

Its derivative is negative under guards1-2 and K>=2, and its maximum is the left side of guard4 minus s0. The tangential neighbor range divided by sin(b) decreases; guard3 makes |wt|<=2K*lambda*s_b. Therefore every remaining node objective is nonpositive, and the actual outer-area plus squared-edge functional is bounded by its simultaneous radial-tip version.

## 3. Exact instances and scope

`verify_lens_cone_radial_node_guard.py` checks the cone and node comparisons with outward integer intervals. It passes:

- R=.11312, x0=.307, lambda=.04 and K=3.700214;
- the same domain with lambda=.043;
- R=.113129, x0=.29, lambda=.04 and K=3.732822.

The .043 first-domain node margin exceeds .00009932. The last instance's margin exceeds .00016900. The current all-angle marked backend also validates the two relevant penalties; that does not replace its separate triangle/star accounting.

The actual full-arc lower domain, stable radial-pair support and complete star/count proof must still be established at every desired radius. This lemma spends the same outer displacement loss as its cyclic squared-edge reduction, and cannot be added to another reduction spending that loss without a joint allocation proof. Earlier frozen checkpoints are unchanged.

# A sharper analytic radial-node guard

This strengthens the previously audited simultaneous cyclic radial-center reduction. It is a local support theorem, not a covering-radius exclusion by itself.

Fix 0<R<1/2, lambda>=0 and 0<x0<1. Put

s0=R*x0, c0=sqrt(1-s0^2), h0=R*sqrt(1-x0^2), rho0=c0-h0, C=sqrt(1-R^2).

For half-arcs a,b,c in [asin(s0),asin(R)], write s_a=sin(a), h_a=sqrt(R^2-s_a^2) and rho_a=cos(a)-h_a. The node coefficients of the established cyclic expansion are

wr=2lambda[2rho_b-rho_a*cos(a+b)-rho_c*cos(b+c)]+8lambda*h_b-s_b,
wt=2lambda[rho_a*sin(a+b)-rho_c*sin(b+c)].

If the following exact comparisons hold, every node residual is nonpositive:

1. x0^2>4R^2(1-R^2)
2. 4lambda*rho0*s0<1
3. C*(s0*C+c0*R)-2rho0*s0*c0<=4s0
4. 8lambda*(h0+rho0*s0^2)<=s0

Strict final inequalities are convenient for exact certificates. At h=0 the result is interpreted continuously; the corresponding endpoint lens contains only its corner.

## Proof

For fixed b, the neighbor function rho_a*cos(a+b) is increasing in a. Its derivative has the sign of

sin(a)*cos(a+b)-h_a*sin(a+b).

Indeed rho'_a=s_a*rho_a/h_a. All cosines are positive because a+b<=2asin(R)<pi/2. The inequality follows from

sin(a)/h_a >= x0/sqrt(1-x0^2) > tan(2asin(R)),

where the strict comparison is equivalent, after squaring positive quantities, to condition 1. Continuity includes the singular endpoint. Therefore

wr <= W(b) = 4lambda[(1-rho0*c0)*cos(b)+h_b+rho0*s0*sin(b)]-sin(b).

The coefficient 1-rho0*c0 is positive. Under condition 2,

W'(b)=-4lambda*(1-rho0*c0)*sin(b)-4lambda*sin(b)*cos(b)/h_b
       +(4lambda*rho0*s0-1)*cos(b) <0.

Thus W is largest at b=asin(s0), where it equals

8lambda*(h0+rho0*s0^2)-s0 <=0.

Next, rho_a*sin(a+b) is increasing in a because rho'_a, sine and cosine are nonnegative. Its range is therefore at most the endpoint spread

E(b)=C*sin(asin(R)+b)-rho0*sin(asin(s0)+b).

Writing E(b)=A*sin(b)+B*cos(b), one has A=h0*rho0>=0 and B=R*C-rho0*s0>=0. For the latter, x*sqrt(1-R^2*x^2) is increasing on [0,1] when R<1/2; hence rho0*x0<=c0*x0<=C. Consequently E(b)/sin(b)=A+B*cot(b) decreases in b. Condition 3 is exactly E(asin(s0))<=4s0, so E(b)<=4sin(b) throughout the domain. It follows that |wt|<=8lambda*s_b.

The full endpoint-lens inequality gives Delta>=0 and

2h_b*Delta >= |delta|^2+2s_b*|t|.

In the already established global cyclic expansion the remaining node objective is wr*Delta+wt*t-8lambda*s_b*|t|. Both parts are now nonpositive. Summing proves the simultaneous radial-tip upper bound without independent favorable neighboring displacements.

## Certified parameters

`verify_radial_node_endpoint_guard.py` checks the radical comparisons with the previously audited outward integer interval kernel. In particular they pass at R=.11312, x0=.307, lambda=.039, and also lambda=.037. This extends the older loose analytic guard that required x0>1/3. The genuine coverage lower-arc domain must still be established separately at every radius.

This theorem spends the same outer-area displacement loss as the cyclic squared-edge reduction. It cannot be superposed with another reduction that already spends that loss without a joint allocation proof.

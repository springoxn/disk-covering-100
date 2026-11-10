# A safe small-arc correction when radial-tip optimality fails

This is a local extension of the independently reviewed lens-cone cyclic reduction. It gives an upper support, not a claim that actual centers can be moved to radial tips.

Use the notation of LENS_CONE_RADIAL_NODE_GUARD.md with lambda>=0, 0<R<1/2, a positive cutoff x0, and a certified K>=K_cone with K>=2. Assume neighboring radial products are increasing and the tangential endpoint spread is at most K*sin(b), as in that theorem. The radial-normal nonpositivity guard is deliberately not required here.

For every middle half-arc a define

F_K(a)=4lambda[(1-rho0*c0)*cos(a)+rho0*s0*sin(a)]
       +(2K-4)*lambda*sqrt(R^2-sin(a)^2)-sin(a),

P(a)=2sqrt(R^2-sin(a)^2)*max(F_K(a),0).

Then the actual simultaneous outer-area and squared-edge objective obeys

sum outer_actual + lambda*sum actual_boundary_edge^2
<= sum H_R(2a_i)+lambda*sum radial_boundary_edge^2+sum P(a_i).

## Proof and allocation

After the global cone bound and full endpoint-lens substitution, the residual node objective is

wr*Delta+wt*t-2K*lambda*sin(a)*|t|.

The tangential guard makes the last two terms nonpositive. Neighbor radial monotonicity gives wr<=F_K(a). The lens inequality gives Delta>=0 and Delta<=2h, because |delta|^2>=Delta^2 and 2h*Delta>=|delta|^2. Therefore the entire residual is at most2h*max(F_K(a),0)=P(a). At h=0 the displacement and P are zero. Summing yields the stated bound.

This is a bound on one already combined cyclic functional. P is not an independent second deduction from the outer loss budget. The corresponding two-variable pair support must include exactly[P(a)+P(b)]/2, so every node correction is counted once around the cycle. The negative marked-edge penalties then cancel the same positive edge-square terms as before.

## Exact derivative handling

Write s=sin(a),c=cos(a),h=sqrt(R^2-s^2),A=1-rho0*c0. For h>0,

h'=-s*c/h,
F_K'=-4lambda*A*s+(4lambda*rho0*s0-1)*c-(2K-4)*lambda*s*c/h.

On F_K>0, P'=2h'*F_K+2h*F_K'; on F_K<0, P'=0. At a crossing of F_K=0 the derivative need not exist. An interval proof may retain its natural enclosure there, or use a rigorously justified derivative hull containing both branches. It must not silently apply only one smooth derivative across the crossing. Similarly, endpoint boxes with h=0 may use the natural value enclosure instead of division by h.

If4lambda*rho0*s0<1, then F_K is decreasing; this can simplify identifying the corrected small-arc region, but is unnecessary for the basic pointwise upper bound.

The actual cutoff, cone constant, monotonic/tangential comparisons, corrected pair bound, one global variance charge and complete star/count inequalities must all be reverified at the desired radius. This note alone establishes no new covering-radius exclusion.

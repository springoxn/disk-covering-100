# Necessary B33 high-M reduction at R=.11321

This document concerns normalized m100/B33 diagrams with M=U-2e>=26.
It reduces such a hypothetical covering to402 combinatorial graphs.
Metric exclusion of those graphs and all lower-M cases are separate.

Normalize ALL centers at R before constructing the diagram, so every
center has norm at most sqrt(1-R^2). No center is moved between any of
the following domain or support steps.

The independent angular bootstrap first pays at most8 q4 vertices at
.02 normalized area each. Its preliminary cap229.363 excludes any five
assigned cells in a3R footprint, restoring q<=3 and a four-consecutive-
boundary-neighbor window. The uncharged cap229.203 gives full arc>.0624.
At R the complete count bridge leaves m100,B31,...,38; the B33 four-arc
2R check excludes all-boundary q0/q1 faces.

Three successive high-M supports reserve their ENTIRE variance budget.
Each pairs one reflected radial inequality with16 full-face supports
and390 vertex inequalities. Negative M and shifted-ear coefficients
allow evaluation at M26,e0. No fan or ear variance charge is spent.

1. lambda=.04,gamma1.5 onx>.2755 gives full arc>.0896,x>.3955
2. lambda=.08,gamma1 on that domain gives full arc>.1133,x>.5
3. lambda=.10,gamma9/8 on that domain gives full arc>.136,x>.6

For each step, a half-arc a<=h<pi/33 would force
V=sum(a_i-pi/33)^2 >=(33/32)(pi/33-h)^2. The exact total surplus is
smaller than gamma times this quantity. The resulting actual domain is
proved before the next inequality is used. Budgets from different steps
are never added. Earlier rejected stage-three gamma1.25/1.2 proposals
are not part of this chain.

The final lambda=.14,gamma0 reflected support onx>.6 gives

    outer + .14*sum(marked base lengths squared)
      <=22342969807217685203019/(625*10^20)
      <2234297/6250000.

The separate retained rational profile row uses the global stationary-
quartic marked conjugate and range-below-one full-face supports. Its
exact comparisons exclude M>=27, every positive ear count, and every
interior type except degree6 or(q3,d7). Euler then forces e0,M26,
precisely66 degree-six interior vertices and one degree-seven q3 apex.

N26_Q3_PROFILE_CATALOG_BRIDGE.md supplies the planar/topological step.
It proves original and core chordlessness, one P26/F106 core, flat strict
interior, and the one-fan relation d=h+q+2. The unique degree-seven q3
apex is a convex core corner. The existing exhaustive57-core catalog
and442 raw corner placements give402 symmetry representatives.

`verify_B33_highM_profile_0p11321.py` runs the domain chain, final radial
support, exact profile row and complete graph-index generator in fresh
processes. It checks the Q inequality, complete generated index equality,
counts and source catalog identity. This is a necessary-reduction theorem,
not a claim that402 graphs have already been excluded.

The sources were reconstructed after an execution-workspace replacement.
Fresh exact replays, rather than earlier logs, establish recovered results.

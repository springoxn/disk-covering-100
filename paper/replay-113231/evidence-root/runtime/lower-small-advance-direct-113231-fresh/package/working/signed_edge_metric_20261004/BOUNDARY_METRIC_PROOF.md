# Joint shared-edge and boundary-angle support for a specified graph

## Result and scope

The exact replay `verify_boundary_metric.py graph_N27_0009.json certificate_boundary_N27_0009.json` excludes this specific no-ear graph at R=1131/10000. Its actual center coordinates are unrestricted. The exact area contradiction is

`2791854194766835369179 / 10^24 > .00279185`.

This is an additional graph-conditional certificate and reusable metric method. It is not an enumeration of all possible covering graphs or a new universal lower bound. The baseline certificate uses the universal .1131 metric-window premises. Section 6 gives the independently rechecked graph-specific extension through .1132.

## 1. Incidence and signed edges

The graph replay checks an oriented triangulated disk, all vertex links, 100 vertices, 33 boundary vertices, 67 interior vertices, 132 unmarked q0 faces and 33 ordinary q1 faces. Every outer boundary edge is the base of exactly one q1 face with one interior apex. The actual embedding need not resemble the lattice labels used to name this graph.

Use a real angle potential u_v at every vertex. In a q0 face f, assign signed coefficients tau_fj to its three opposite halfedges. The two incidences of each q0--q0 edge receive opposite coefficients; every q0--q1 interface gets zero. For face circumradius ratio rho<=1 and angles alpha_j, its normalized area plus metric score minus angle score is

`rho^2 * 2 product sin(alpha_j) + rho sum tau_fj sin(alpha_j) - sum u_j alpha_j`.

The opposite halfedge term is tau times edge length/(2R), so every shared metric term cancels exactly in the full sum even when neighboring circumradii differ. Convexity in rho reduces the maximum to rho=0 or 1. At a simplex vertex all sine terms vanish, and the rho=1 score realizes the largest pure linear rho=0 score. Thus the complete-angle-simplex support in PROOF.md and WIDE_LOCALIZATION_PROOF.md remains valid. The new certificate keeps every face's potential range below .3 and every signed edge coefficient at most .2, inside the independently verified first wide localization domain.

## 2. Unequal-base marked support

Use the independently audited geometric lemma in `lower_bounds_extension_20261004/BOUNDARY_ANGLE_RADIAL_REDUCTION.md`. Its premises are rechecked by `check_boundary_angle_reduction.verify()`, including the same-radius unrestricted old area budget, full assigned arc >.08 and every ordinary marked base L>.9R.

For one q1 face let a,b be its boundary vertices, c its interior apex, m=(u_a+u_b)/2 and d=u_a-u_b. Its normalized face-plus-anchor score minus all three weighted angles is at most

`G(u_c-m) - pi*m + (25/16)*d^2`,

where G(v)=sup_gamma[Gbar(gamma)-v*gamma]. The majorant Gbar covers the entire apex domain [0,pi], as proved in GLOBAL_MARKED_APEX_SUPPORT.md. The exact conjugate implementation requires -1/2<v<3; every supplied v is checked. The quadratic base-asymmetry loss is paid inside that face, not from the outer-area budget.

## 3. Boundary-angle compensation

Summing the negative corner-angle terms yields -2*pi*sum(interior u_v) minus sum(boundary u_i P_i), where P_i is the actual center polygon's interior angle. Restore the first term explicitly. Combine the second term with the actual signed outer area using the audited radial-corner inequality. It applies because adjacent boundary weights differ by at most 1/40; the actual maximum in this certificate is 1/50.

For t_i equal to half of the assigned circle arc, let

`H(t)=sin(t)*sqrt(R^2-sin(t)^2)+t-sin(t)*cos(t)`

and `eta(t)=asin(sin(t)/R)-t`. The actual boundary contribution plus R^2*sum u_i P_i is at most

`pi*R^2*sum u_i + sum [H(t_i)-2R^2*u_i*t_i+(R^2/2)*(u_(i-1)-2u_i+u_(i+1))*eta(t_i)]`.

This comparison bounds one scalar functional; it never moves the actual centers or assumes reference corners preserve the covering or its graph. The outer displacement loss is spent exactly once here. There is no separate boundary length-penalty term.

Because sum t_i=pi, any rational common multiplier zeta gives the upper bound

`pi*zeta + pi*R^2*sum u_i + sum sup_{.04<=t<=asin(R)} [H(t)+b_i*eta(t)-a_i*t]`,

with a_i=2R^2*u_i+zeta and b_i=(R^2/2)*(u_(i-1)-2u_i+u_(i+1)). In particular b_i<R^2, as verified.

## 4. Exact scalar arc acceptance

Put T=R^2 and U=sin(t)^2. In the open scalar domain the derivative of H+b*eta-a*t, multiplied by the positive sqrt(T-U), is

`D=(2U-b-a)*sqrt(T-U)+sqrt(1-U)*(T-2U+b)`.

Every interior stationary point therefore satisfies the exact quadratic

`4(a-1)U^2 + [-4T(a+b)-(a+b)^2+4(T+b)+(T+b)^2]U + T(a+b)^2-(T+b)^2=0`.

The polynomial identity was independently checked in the inherited geometry verifier. `exact_boundary_conjugates.arc_support` evaluates both domain endpoints and retains every real quadratic root whose outward interval meets the domain. The linear coefficient case is handled separately. Roots introduced by squaring are deliberately retained: extra domain evaluations cannot omit the true maximum. The verifier does not infer derivative signs from the squared equation. Continuity includes the singular upper endpoint, whose value is evaluated by its explicit formula with h=0. The score is strictly concave for b<T, but exhaustive endpoint/stationary enumeration is sufficient by itself.

All arithmetic is outward-rounded integer intervals at scale 10^24. Discriminant signs and rational polynomial coefficients are computed exactly before interval radicals. Intersections, square roots and inverse-sine inputs are clipped only to domains already known for the exact candidate. Inverse sine uses the audited full-domain inverse cosine backend. The returned lower bound uses only endpoint values; acceptance uses the upper bound. Assertions and parameter checks reject unsupported domains and optimized Python.

## 5. Final area sum

Add all 132 q0 supports and 33 q1 supports, restore 2*pi times the 67 interior weights, multiply that total by R^2, and add the boundary scalar bound above. Signed shared edges and all actual vertex-angle terms cancel. The resulting bound is strictly below pi by the displayed exact rational margin. Therefore no covering with this specific original diagram and radius at most R exists. The unchanged graph validator and inherited closed limiting argument handle the stated diagram convention; no graph-catalog completeness is claimed.

The numerical optimizer only proposed rational coefficients. The final replay recomputes geometry, graph incidence, complete-simplex support domains, all 33 scalar arc maxima and the final strict sign using standard-library exact arithmetic.

## 6. Graph-specific larger-radius window and application

For N27_0009, `check_graph_boundary_window_N27_0009_0p1132.py` separately replays the pure signed-edge certificate with zero boundary weights and proves that the required full-arc and marked-length restrictions hold for every hypothetical covering at radius at most .1132. Its proof is GRAPH_BOUNDARY_WINDOW_N27_0009_0p1132.md. The complete nonnegative slack decomposition includes each signed metric term before global cancellation. The old pure certificate is used only as a dimensionless support bound and is not numerically extrapolated. All radius-dependent quantities and absorption constants are rechecked at the larger radius.

For any accepted radius between .1131 and .1132, the new replay checks the family and exact graph hash against that premise, then evaluates every face and arc support at its requested radius. At .1131 it can instead use the original generic no-ear geometric premise. The .11316 proposal uses face ranges below .3, edge coefficients at most .25, and adjacent boundary-weight differences below .025, hence the second audited wide localization table. The positive exact area margin and final certificate identities are recorded in result_boundary_N27_0009_11316.json. This excludes only this specified graph at the stated radius.

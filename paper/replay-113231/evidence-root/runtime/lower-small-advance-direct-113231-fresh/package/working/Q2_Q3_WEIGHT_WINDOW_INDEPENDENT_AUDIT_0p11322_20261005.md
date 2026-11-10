# Independent conditional q2/q3 metric-window audit at R=.11322

2026-10-05 UTC. PASS for the stated same-radius conditional geometry only.

## Scope and fresh replay

I read the supplement and its checker, the imported exact arithmetic/support sources, the prior conditional profile receipt, and the inherited radial-corner metric proof. Fresh read-only execution of `python -B -S verify_q2q3_weight_window_0p11322.py` exited zero with PASS. It freshly recomputed the conditional profile's 16 full-face and 390 vertex supports. A separate standard-library stdin calculation independently reconstructed both endpoint caps, both true-conjugate gaps, the sine/reference/angle/absorption comparisons, and the unequal-base variance coefficient. No cached result artifact was used for acceptance. Reviewed sources were unchanged; this is a new receipt.

All premises stay conditional: a whole-cover-normalized m100/B33 diagram at R=5661/50000, M>=26, no bad all-boundary q0/q1 faces, ordinary marked incidence<=3, the four-consecutive-cell neighbor window, and actual Q=sum Hactual+(7/50)sum Lactual^2<=17877/50000. Separately, every actual full assigned arc must exceed 147/1000 in that same diagram. This receipt does not establish Q or the full-arc premise. It uses the previous profile reduction only within its audited scope: e0/M26, 66 degree-six interior sites and one degree-seven site of marked incidence 2 or 3.

## Correct tilts and short-base contradiction

A marked q1 face has a degree-six zero-potential or degree-seven high-potential apex. Both boundary endpoints use the common profile potential -40712065/10^8; the high potential is -35352650/10^8. Thus the plus-angle marked score uses s=apex potential minus boundary potential, exactly 8142413/20000000 or 1071883/20000000, respectively. These positive tilts must not be replaced by the unweighted conjugate or by their negatives. The degree-six case applies for every permitted marked incidence. The unique degree-seven site's q2/q3 choice changes incidence count, not this individual-face tilt.

At fixed x=L/(2R), circumradius<=R gives asin(x)<=gamma<=pi-asin(x). Area/R^2<=x^2 cot(gamma/2). Adding the fixed ordinary anchor, -4lambda x^2 and s gamma remains convex in gamma throughout (0,pi). The endpoint reduction therefore covers acute, obtuse and limiting degenerate cases for lambda=7/50; it does not extend the old lambda<=1/8 concavity claim. The hardened arbitrary-penalty Sturm kernel encloses both complete scalar branches.

For 0<=x<=9/20 the acute derivative is bounded below by 1+2h-2x^2/h-8lambda x, because the omitted s/h is positive. This lower bound decreases: its derivative is -6x/h-2x^3/h^3-8lambda. The obtuse derivative 1-8lambda x-s/h also decreases. Their endpoint lower bounds are positive: the acute lower bound exceeds 1.82854 for both tilts; the obtuse lower bounds exceed .0401123 and .435986. Thus evaluating both scores at x=9/20 bounds every short marked base.

The recomputed whole-profile surplus upper bound is 799847568053744389853/10^24. Subtracting this entire surplus from R^2 times the true-conjugate-minus-short-cap loss gives strictly positive lower bounds:

- zero-potential apex: 1872101154324980846851/(5*10^23) > .00374420
- high-potential apex: 393796473355296549083/(125000000000000000000000) > .00315037

Both are individual local slacks within the original profile decomposition. All other retained slacks remain nonnegative, so one short face contradicts that same whole-cover area budget. Hence ALL ordinary marked bases exceed .9R, regardless of whether the unique defect is q2 or q3. As an independent cross-check requiring no Sturm maximization, the feasible equilateral score sqrt(3)-3lambda+s*pi/3 already gives positive contradiction margins greater than .00320998 and .00180022.

## Arc domain, reference lengths and angle lifts

The separate actual-arc premise and endpoint-lens domain give 147/2000<t_i<=asin(R). Sine is increasing on this domain. The outward lower bound of sin(147/2000)-R*(1297/2000) is 5335155293900826279/(5*10^23)>0. Therefore sin(t_i)/R>1297/2000=.6485.

Each inner radial lens reference tip has radius >=1-R. Consecutive midpoint directions have gap t_i+t_(i+1)<pi; their half-gap is <=asin(R), so the minimum reference edge is strictly larger than 2(1-R)R*.6485. Its exact coefficient is 57507683/50000000=1.15015366, exceeding 23/20 by 7683/50000000. Thus every reference edge exceeds 1.15R.

The inherited lift proof remains radius-independent in its topology. At a strict actual Voronoi transition, alpha_i=phi_i+pi/2+epsilon_i has -pi/2<epsilon_i<pi/2. Ordered transition lifts, positive full arcs and the simple counterclockwise actual center cycle ensure the polygon interior angle is P_i=pi-alpha_i+alpha_(i-1), without discarded 2pi jumps. The reference radial polygon is simple and star-shaped because its radii are positive and successive midpoint gaps are below pi. With eta(t)=asin(sin(t)/R)-t, its edge offset is [eta(t_i)-eta(t_(i+1))]/2 in (-pi/4,pi/4); hence e_i=alpha_i-alpha_i* lies in (-3pi/4,3pi/4) and is the principal angle. Its reference turn is 2t_i+eta(t_i)-[eta(t_(i-1))+eta(t_(i+1))]/2.

For edge lengths L>.9R and L*>1.15R, |a-b|^2>=4LL* sin^2(e/2), |e|<=pi|sin(e/2)|, and endpoint displacement triangle inequalities yield |e_i|<=13/(8R)*(d_i+d_(i+1)). The exact test pi^2<4*(9/10)*(23/20)*(13/8)^2 has positive outward margin. Strict-transition/simple-cycle premises are the inherited generic diagram premises; this receipt does not supply a new nongeneric limiting theorem.

## Once-only absorption and unequal-base charge

Summation by parts has the sign sum w_i(P_i-P_i*)=sum(w_(i+1)-w_i)e_i. For max neighboring difference<=1/8 its absolute angular cost is <=2*(13/8)*(1/8)*R*sum d_i. Endpoint-lens geometry gives Delta_i>=0 and sin(t_i)d_i<=R Delta_i, so the genuine outer-area loss sum sin(t_i)Delta_i is >(.6485)^2 R sum d_i when displacement is nonzero. The exact unspent residual is (.6485)^2-2*(13/8)*(1/8)=57209/4000000>0. Zero displacement gives equality and requires no strict loss.

Adding circular segments gives the same scalar arc functional, with b_i=(R^2/2)*(w_(i-1)-2w_i+w_(i+1)) and a_i=2R^2 w_i+zeta. The neighboring difference cap implies |b_i|<=R^2/8<R^2. Downstream scalar supports must use the corresponding same-radius closed safe domain [147/2000,asin(R)], check their own coefficients/roots and include the upper endpoint h=0. The supplement itself supplies no final arc-conjugate acceptance or graph metric contradiction.

The marked face's independent asymmetry gap is 2z^2 R^2 sin(gamma) sin^2(delta), with delta=(beta_a-beta_b)/2 and z sin(gamma)=L/(2R)>.45. Since |delta|<=pi/2, it exceeds (81/(50*pi^2))R^2 delta^2>(4/25)R^2 delta^2. The checker safely verifies pi^2<81/8. Completing the square against the boundary-potential difference therefore retains the positive 25/16 times difference-squared allowance, with the same physical half-edge units and either angle-sign convention. The fixed-base anchor and any fixed-base-square penalty do not spend this asymmetry loss.

The outer displacement loss is spent ONCE in the joint outer-area-plus-angle comparison. Neither the conditional Q bootstrap nor the new short-base contradiction is an additional loss in a final metric sum. The supplement does not prove a simultaneous penalized length-plus-angle reference replacement. It moves no physical covering centers, asserts no preservation of the graph under a move, and adds no fan fee or final variance to the graph dual.

## Boundaries of acceptance

This receipt certifies conditional geometry at the stated same radius, not an all-count result, complete graph catalog, global covering lower bound, complete Q proof, or exact endpoint/limiting closure. The independent arc ladder may establish the arc premise elsewhere; that result is not inferred from this supplement. Each actual graph certificate still needs its weights, actual arc domain, signed-halfedge cancellation, all local face supports and final strict area comparison independently assembled and checked.

## SHA-256 source bindings

- `verify_q2q3_weight_window_0p11322.py`: `c3b220abb2ebe697bc25444c69da4fe425c7995a0dbe5ce26389abfe0a4681c2`
- `Q2Q3_WEIGHT_WINDOW_0p11322.md`: `84377f8fa5cf7cb6d9de73750ca5c02b24099d078adbde129b0d24f7bae1a6c1`
- `verify_B33_q2q3_profile_0p11322.py`: `44912fe9b46a35251ba34319962e51090d440f10889f0b17b54b90550b69ee8f`
- `B33_Q2_Q3_PROFILE_0p11322.md`: `618093d99f4130a46240e1b71d9035c9ec58211007e6436c8ecf6558912e1b05`
- `B33_q2q3_profile_0p11322_proposal.json`: `4cfcdc535d4ad2e0dc6aadffa92709dc564db5bff34a80a9c91e3277209362ad`
- `B33_Q2_Q3_PROFILE_INDEPENDENT_AUDIT_0p11322_20261005.md`: `db1be37a46720f7a1c77085f60f5f4b9a8e98c3347b63170adc376e539c3e616`
- `sturm_quadratic_marked_conjugate.py`: `e85c5fb42eabb12c17e05d62ff484e757dc7fa019dd32d9eb6ecd1804116fb6d`
- `STURM_QUADRATIC_MARKED_CONJUGATE.md`: `3db58ff7a9caa119450d5e3fa2f9ad62ea32f56c0fae79ca603956a85fca2547`
- `STURM_QUADRATIC_MARKED_CONJUGATE_INDEPENDENT_AUDIT.md`: `4739484b804b0487a070c36fc7c27924cbe51a1080a6e1a5bf65fc9bedd0d8cb`
- `verify_star_lp_duals.py`: `23568fed518e451d3d6b7f11603e080546bb74afa020ef0fd8fbb1a3b02be6d7`
- `verify_potential_star_duals.py`: `d4609b4441dae93c105966dd28f72b2e9d84342f012dd519dca25f2515e3e2c3`
- `exact_angle_conjugates.py`: `cee5e03352e7b6c94ecbe5dbf0cd43f97342c9c23492b6820e7fc935fc8d1cb9`
- `exact_range_one_face_support.py`: `a33023537a5f20e406e2fac79dc16f6ce79ac152798e08563a7097e48a1414ef`
- `verify_jensen_slab_ear_support.py`: `1c8d46f5e08714519e1545199fdd6edebe7b1defec0df3b693649be0ad6c4e4b`
- `exact_quadratic_marked_conjugate.py`: `a54af21d3b405b468e74f93ec53cab24714c5bb0fb4c66a61bd16987edfdfb6d`
- `QUADRATIC_MARKED_CONJUGATE.md`: `c03b881d967d4c4dcf547ab05466621fd9e15fe09c349f00f519e52f4cdb77fa`
- `lower_bounds_extension_20261004/BOUNDARY_ANGLE_RADIAL_REDUCTION.md`: `56ab1c340ba36cf046a4aa24c2425042969bf69cb42e1b1958a653eadb1941eb`
- `Q3_CORNER_BOUNDARY_WEIGHT_WINDOW_0p11321.md`: `528115a8d3c9b2893a0ad74636476e6b16c01fe3130ee5cd535750c22dbe4cdb`
- `signed_edge_metric_20261004/BOUNDARY_METRIC_PROOF.md`: `3edb99cb07ef86c2fea29775bb16359a7e7bc8d65495ccc8b69055265cf2070e`

# Exact B33 exclusion at 0.11311 by footprint-aware radial stability

This is a graph-independent B33 branch, to be integrated with the separately
verified remaining boundary counts. It is not an exact-optimality result.
The complete .11309 and .1131 checkpoints are unchanged.

## Same-radius geometric domain

The exact starting checker is
lower_bounds_extension_20261004/check_one_ear_structure_0p11311.py, with
proof ONE_EAR_STRUCTURE_0p11311.md. At R=11311/100000 it gives m100,I67,F165;
unmarked angles in(.42,pi/2+.205); good marked apex angles in(.42,pi/2);
interior degrees5 through14; at most3 good marked incidences per apex; and
every full assigned arc greater than.0755. Its K4 footprint test excludes
all-boundary q0/q1 faces, and its two-ear test leaves e0 or1. Boundary chords
and unmarked faces with two boundary centers remain allowed.

The arc cutoff implies sin(a_i)/R>16683/50000, where a_i is a half-arc.
The radial checker includes the slightly larger closed domain
sin(a_i)/R in[417/1250,1]. Its lower endpoint is .3336>1/3.

## Radial stability support

Use lambda=37/1000. The simultaneous displacement expansion, full endpoint-
lens tangent charge, and analytic k=0/radial-normal guard are exactly the
geometry proved in ONE_EAR_RADIAL_STAR_0p1131_PROOF.md, now checked at the
new radius and lower endpoint. The analytic radial margin remains strictly
positive. Therefore the actual circular outer contribution plus lambda
times every squared marked-edge length is bounded by the corresponding
radial-tip pair sum.

The instance-based backend never changes earlier checkpoint constants. Its
exact pair inequality is

[H_R(2a)+H_R(2b)]/2+lambda L0(a,b)^2
+(5/6)[(a-pi/33)^2+(b-pi/33)^2]
<=2267/200000-(19781457/10^9)(a+b).

The exhaustive closed-domain replay uses the same proven natural and
derivative mean-value interval upper bounds. It visits1107 boxes, with508
accepted leaves and46 symmetry skips. Hence, writing

L=2267/200000, mu=-19781457/10^9, gamma=5/3,

the complete radial outer/edge score is at most

33L+2pi*mu-gamma*sum(a_i-pi/33)^2.

No equal-gap assumption is used to establish this inequality.

## Three exhaustive structural branches

1. No ears, and at least one apex has p3. Three distinct marked boundary
   edges use at least four distinct boundary sites, since B33. Each site
   center is within2R of that apex, so its covering disk is contained in
   the apex-centered radius3R disk. This contains four complete assigned
   arcs, whose sum is at most L4=1733/2500=.6932. The exact checker proves
   sin(L4/2)>3R. The chosen four arcs need not be consecutive: their
   disjoint union lies in the same short footprint, so their total angle
   is still bounded.
2. No ears, and every apex has p<=2. There is no extra mandatory footprint,
   but the scalar star type set is restricted accordingly.
3. Exactly one ear. Its three consecutive assigned arcs have total at most
   L3=2283/5000=.4566, since sin(L3/2)>2R. The three-arc footprint is the
   same consequence of the ear's common Voronoi point used previously.

These branches cover every configuration in the starting domain. The p3
branch's LP is allowed to contain p<=2 stars as a relaxation; the extra
variance charge is applied because the actual branch has a p3 apex, not
because a floating-point optimizer chooses one.

For a chosen group of k arcs with total at most Lk, Cauchy and the total
half-arc sum pi imply

sum(a_i-pi/33)^2
>=(k*pi/33-Lk/2)^2*(1/k+1/(33-k)).

Both deficits are positive and the exact lower bounds are checked. Use k4
in branch1, zero in branch2, and k3 in branch3.

## A sharper ear cap with both edge penalties retained

The ear center triangle lies in the radial slab and has area at most
R*(1-sqrt(1-2R)). For either marked base put x=L_edge/(2R). Its anchor
minus the squared-edge penalty is bounded, after normalization, by

x*sqrt(1-x^2)-4lambda*x^2
<=(sqrt(1+16lambda^2)-4lambda)/2.

For example set u=2x^2-1 and apply Cauchy to the unit vector
(sqrt(1-u^2),u). Thus the penalized ear score is at most

E=(1-sqrt(1-2R))/R+sqrt(1+16lambda^2)-4lambda.

Both negative ear-edge penalties cancel the same two positive boundary-edge
terms already included in the radial support. No extra edge charge is
introduced. The ear apex is not assumed acute; this slab/anchor cap handles
it independently.

## Star potential, counts and exact duals

Good marked triangles use the already exactly checked acute G_lambda
envelope. Unmarked triangles use the concave angle potential with coefficient
9/20, rational splice2201/2000 and endpoint pi/2+41/200. Every numerical
endpoint comparison is repeated at these parameters. As before the face
potential is a zero-sum compatibility majorant, not a universal quadratic
area deficit.

For e0/1, let M=33-2e and U=132+e. Star multiplicities satisfy
sum x67,sum p*xM,sum j*x3U-N and sum_(p>0)x<=N. The unmarked boundary-angle
sum is Gamma+(e-2)pi. Thus each row gives normalized center/anchor upper
bound

67u0+M u1+(3U-N)u2+Nv+N C(eta)+(e-2)pi*eta+eE.

Branch1 checks all40 types p0 through3, degrees5 through14, and N11-94.
Branch2 checks30 types p0 through2 and N17-94: its lower endpoint follows
from ceil(33/2)<=number of distinct apices<=N. Branch3 checks the full40
types and N11-95. These are247 integer cases and9100 scalar inequalities.

The final area bound is R^2 times the displayed normalized score plus
33L+2pi*mu minus the branch's forced gamma-weighted variance. Every case
is strictly below pi. The smallest exact margin is

16726610263154651319/(5*10^23),

in branch1,N23. Proposals come from numerical LPs, but acceptance uses only
outward-rounded integer intervals, exact integer radicals and bounded
rational series. Optimizer output never determines a sign.

The verifier additionally checks u0+6u2>=0 in every row. This records a
useful monotonicity guard for future fewer-center generalizations; the
present proof still uses the independently checked m100 count bridge.

## Files and logical scope

The actual scalar receipts are radial_stability_support_0p11311_result.json
and footprint_star_0p11311_result.json. Replay
verify_radial_stability_support_0p11311.py and verify_footprint_star_0p11311.py
with assertions enabled, and the separate starting geometry checker.
The radial backend's natural/mean-value derivatives are documented in the
.1131 proof and independently exact-replayable here. No optional mode can
skip an entire component.

The same compactness/genericity closure applies: approximate a hypothetical
radius<=R cover by generic slightly enlarged covers, choose a fixed finite
topology and pass the closed coordinate, endpoint, area and angle
inequalities to a limit. Strict starting and final margins contradict the
limiting cover. This is not a claim that generic perturbation preserves R.

Completing the universal .11311 lower bound requires all other surviving B
branches at the same or a stronger radius. The exact optimum and a global
optimal covering remain unresolved.

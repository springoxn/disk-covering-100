# Exact star-model premises at radius 11307/100000

This document supplies geometry and incidence premises for the separate B32 ordinary-star and B33 potential-star scalar certificates. It does not by itself exclude the other boundary counts or identify the exact optimum.

The two runnable checkers are `check_B32_star_0p11307.py` and `check_star_premises_0p11307.py`. They use the immutable rational interval backend `verify_extension.py`. Each exports `verify()` and supports `--json`. Both were executed successfully. Their result files record the output.

## Common count reduction

The previous all-radius concavity proof for H and the marked-triangle inequality give the necessary E criterion. Exact evaluation excludes every cover with at most 99 disks. For 100 disks only B=32,33,34,35,36,37 remain. Thus m=100. The generic clipped-Voronoi triangulation and continuous limiting argument are as in the earlier proof extension; strict interval margins persist under sufficiently small perturbations. Neither checker assumes that a perturbation leaves a cover's radius unchanged.

Write A=3sqrt(3)/4, kappa=461134488/10^9, and let d be the old total area surplus divided by r^2. Every individual nonnegative loss is at most d. Center-face counts are F=198-B.

## B32: ordinary variance stars

Here d<.074. The loss for a nonacute q0 face is at least A-1; for a nonacute q1 face it is at least A+kappa-3/2. Both exceed d, so every center triangle is acute. The previously proved logarithmic sine modulus gives area/r^2 <= A exp(-.59 V), where V is the sum of squared deviations from pi/3. The exact fourth-order exponential bound proves V<.37. Then the quadratic exponential estimate gives area/r^2 <= A-.68V.

Every q0 angle exceeds pi/3-sqrt(2*.37/3)>.55. The fixed-apex marked-face bound excludes q1 apex angles <=.55. Therefore interior degrees are 5 through 11.

The three-arc cluster check with L=.45623 and containing radius 2r proves chordlessness. The five-arc check with L=.69216 and containing radius 3r proves that an interior apex is incident to at most three marked faces. The exact margins exceed .001 in both checks.

There are I=68 interior vertices, 32 q1 faces and 134 q0 faces. For types (p,j), p=0,...,3 and 5<=p+j<=11, the incidence constraints are sum x=68, sum p x=32, sum j x=402-N. The number of stars with p>0 is at most N. Here N counts q0 boundary-angle occurrences. The fan-terminal argument gives N>=ceil(32/3)=11; the minimum degree gives N<=94.

## B33: potential stars allowing slightly obtuse q0 faces

Here d<.336. For a q0 angle alpha, the normalized area is at most Q(alpha)=sin(alpha)(1+cos(alpha)). The exact endpoint comparisons give .54<alpha<pi/2+.04. For a q1 apex gamma, the small-angle marked-face bound excludes gamma<=.54. A nonacute apex has joint face-plus-anchor score at most (1+sqrt(2))/2, which also contradicts its individual loss budget. Thus .54<gamma<pi/2.

These windows imply degrees at least four and at most eleven. In fact degree four is impossible. Set epsilon=.04 and consider p marked and j=4-p unmarked incidences. Their angles sum to 2pi. Since marked apices are acute, the mean q0 angle is at least pi/2. Q is concave through pi/2+epsilon because its second derivative has the sign of -(1+4cos alpha). Consequently the q0 areas sum to at most j. The q0 upper angle bound forces the mean marked angle to be at least pi/2-j epsilon/p, above pi/3 when p>0. Concavity and the linear branch of the majorant Gbar then bound the marked score by p(sqrt(3)-pi/12)+j epsilon/2. For p=0 the q0 bound alone suffices. Relative to the allowance 4A+p kappa, the resulting deficit exceeds d by more than .75 for every p=0,1,2,3. Thus the actual degree range is 5 through 11.

For an all-boundary center face, each center has norm between 1-r and 1. If u is its circumcenter and rho<=r its circumradius, projection onto u/|u| gives every vertex coordinate at least sqrt((1-r)^2-rho^2)>=sqrt(1-2r). The triangle lies in a strip of width w=1-sqrt(1-2r) and has diameter at most 2r, so its area is at most rw. Every anchor has area at most r^2/2. Relative to the old q-marked-face allowance, the weakest saving for q=0,1,2 is therefore (A+2kappa-1)r^2-rw, since kappa<1/2. A q3 face is impossible when the triangulation has interior vertices. The face's three boundary cells have footprints in the same radius-2r disk; the contained short boundary arc includes at least three consecutive assigned arcs. Applying the three-arc Jensen bound with L=.45623 and subtracting this face saving contradicts coverage with margin greater than .001. Hence no center face has three boundary vertices. This does not assert chordlessness.

The five-arc cluster check with L=.69216 has margin greater than .005 and proves p<=3. There are I=67, q1=33 and q0=132. Count q0 boundary-angle occurrences with multiplicity, so a face with two boundary vertices contributes two. The incidence constraints are sum x=67, sum p x=33, sum j x=396-N. Each marked fan has two terminal boundary-to-interior edges; a q0 boundary-angle occurrence meets at most two such edges. Therefore the number of distinct marked apices is at most the number of fans, which is at most N. The same degree count gives 11<=N<=94.

The separately generated potential-star certificate uses a weaker valid relaxation allowing degree four, at most one degree-four star, and N<=95. Its validity follows either from the stronger facts above or from d<2(A-1), which allows at most one nonacute q0 triangle. No assumption that all q0 faces are acute is made in the B33 potential-star argument.

## Scope

The receipts verify these premises only. The final .11307 exclusion also requires the independent scalar star duals and B34-37 effective-interface/pair cases. Even a complete lower-radius exclusion is not an exact global-optimality proof for the 100-disk problem.

# All boundary counts B>=36 are excluded at .11323

For a unit-disk cover by at most 100 equal disks of radius R=11323/100000, the center-triangulation reduction cannot have B>=36 boundary cells. This is a complete family of boundary-count exclusions, not a global .11323 lower bound: smaller B remain separate.

Run `python verify_capped_pair_B36plus_0p11323.py` in a fresh process with assertions enabled. The exact acceptance path uses only the standard library and the inherited integer-interval pair backend.

## A second pointwise bound for each boundary pair

Let two adjacent boundary centers C_i,C_(i+1) correspond to half-arcs a,b. They both cover their common unit-circle endpoint, hence

`|C_i-C_(i+1)|<=2R`.

The signed outer-fan and circular-segment contribution of each cell is bounded above by H_R of its full arc. Consequently the actual pair objective, containing half of each outer contribution and the squared-edge penalty, obeys

`Phi_actual(a,b)<=4lambda R^2+[H_R(2a)+H_R(2b)]/2`.

Independently, the already proved endpoint-lens/Young support provides its existing pair upper bound. Both bounds hold for every actual pair with the same a,b. Taking their pointwise minimum is therefore valid. It does not require their separate maximizing centers to agree.

The distance cap is particularly useful for tiny arcs, where the older independent-displacement relaxation can be loose. No positive arc cutoff, radial-tip optimality, ear restriction, fan bound or actual-angle acuteness is imposed.

## Exact scalar certificate

Use

`lambda=3/50`, `K=3892/12500`,

`mu=92531/10^7`, `L=751/100000`.

The inherited q=1,2,3 marked-triangle caps are rechecked at lambda=.06. They give

`area+sum marked anchors-lambda*sum marked_edge^2 <= R^2*(A_up+qK)`,

where `A_up=129903810568/10^11>3sqrt(3)/4`. The q=0 case is the ordinary maximum triangle area. These checks make no assumption about how many marked sides a face actually has.

The new pair verifier subdivides the full normalized sine square [0,1]^2 and proves

`min(old_pair_upper, distance_cap_upper)-mu*(a+b)/2 <= L`.

Its successful exhaustive replay visits 3,371,339 boxes and accepts 1,681,223 leaves; symmetry skips cover only the redundant half of the square. Every retained box is accepted by a rigorous outward interval upper bound. When the elementary cap already proves a box, the more expensive lens support is not evaluated. This changes performance, not the inequality being proved.

Summing actual pair objectives around the boundary yields at most `B*L+mu*pi`, because the half-arcs sum to pi. The positive squared-edge penalties cancel the marked-triangle negative terms exactly, once per boundary edge.

## All larger boundary counts and fewer centers

For m<=100, the number of center triangles is `2m-B-2<=198-B`. Since A_up is positive, replacing it by this upper count is conservative. The necessary total-area inequality is therefore

`pi <=[(198-B)A_up+BK]R^2+B L+mu*pi`.

At B=36, its exact contradiction margin is

`34107048521050938382469778967931605940457120574226219/10^56`,

approximately .0003410704852105.

Increasing B by one increases this contradiction margin by

`(A_up-K)R^2-L > .00515305`.

The verifier checks this sign exactly. Thus B36 is the weakest case and every larger admissible B is excluded by the same pointwise scalar certificate. No separate finite list of higher-B geometries is needed.

The positive exact margin and the inherited fixed-finite-type limiting argument include degenerate covers. At any smaller radius the same stronger-radius exclusion applies to the hypothetical cover's fixed clipped Voronoi/straight-disk diagram. The exact optimum remains unresolved.

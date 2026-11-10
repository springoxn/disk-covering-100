# Boundary pair lower bound for the 100 disk covering problem

## Result and scope

This extension establishes r_D(100) > 113/1000 = 0.113. It improves a lower bound; it does not identify the exact optimum or close the gap to a constructive upper bound.

Run `python verify_pair_bound.py all` with Python 3 and its standard library. The script exhausts explicitly stated compact scalar domains with outward-rounded integer intervals. The continuous geometric reduction below is a written mathematical argument, not a formalization in a proof assistant.

The earlier proof, `previous/GLOBAL_LOWER_PROOF.md` in the retrieved `disk100_continued_proof` archive, supplies the irredundant Voronoi reduction, the simple disk triangulation, its signed area identity, and the original marked-triangle estimates. We retain the signed outer fan areas and strengthen the marked-side estimate to preserve boundary edge lengths.

## Counts left by the earlier inequality

Let m ≤ 100 disks form a generic irredundant covering and B be its number of boundary Voronoi cells. The earlier reduction proves 3 ≤ B ≤ m−1 and F = 2m−B−2 center triangles, each of circumradius at most r. Thus F ≤ 198−B. Each boundary side belongs to exactly one center triangle.

Put A = 3√3/4 and κ = 461134488/10^9. The earlier necessary conditions are sin(π/B) ≤ r and

E_B(r) = [((198/B)−1)A+κ]r² + sin(π/B)√(r²−sin²(π/B)) − sin(π/B)cos(π/B) ≥ 0.

At r = 113/1000, `remaining_counts()` exhausts all B = 3,…,99 using exact rational trigonometric enclosures. Exactly B = 33,34,35 remain. The independent check in `lower_bounds_extension_20261004/verify_extension.py` reaches the same conclusion and rechecks the original κ estimates.

## A side length penalty

Choose the exact rational constants

λ = 1/25, Ā = 129903810568/10^11, K = 17999/50000.

The checker proves Ā > A by Ā² > 27/16. If q sides of a center triangle T are marked, with lengths ℓ_j, then

|T| + Σ_j J_r(ℓ_j) − λΣ_j ℓ_j² ≤ r²(Ā+qK),

where J_r(ℓ) = (ℓ/2)√(r²−ℓ²/4). The q = 0 case is the classical triangle area bound. Scale to r = 1 for the other cases. The earlier proof's fixed-base, Heron and circumradius arguments give these scalar majorants:

- q = 1: x(1+2√(1−x²))−4λx² for 0 ≤ x ≤ 1
- q = 2: t+√(2t−t²)−4λt for 0 ≤ t ≤ 1, and (t+1)√(2t−t²)−4λt for 1 ≤ t ≤ 2
- q = 3: (1/√3−4λ)s+√(3s−s²) for 0 ≤ s ≤ 3

Here x is a marked half-side length, t is the sum of the two marked squared half-side lengths, and s is the sum of all three squared half-side lengths. Subtracting the exact penalty from the corresponding old scalar majorant preserves each inequality. The checker replaces 1/√3 by its upper bound 4Ā/9 in the last expression. Exhaustive one-dimensional interval checks prove the qth majorant is at most Ā+qK. Actual box totals are 3503,112,45 for q = 1,2,3.

Adding the center faces and their attached anchor triangles therefore gives an upper bound

FĀr² + BK r² + λΣ_i |c_i−c_(i+1)|².

## Exact signed outer contribution

Write the boundary arc assigned to c_i as angle 2a_i, where 0 ≤ a_i ≤ asin(r) and Σ_i a_i = π. Let u_i be its midpoint unit direction. The two endpoints are cos(a_i)u_i ± sin(a_i)v_i for a perpendicular unit vector v_i.

The signed triangle from these endpoints to c_i, plus the outside circular segment, is exactly

Hactual_i = a_i−sin(a_i)u_i·c_i.

The signed edge cancellation identity in the earlier proof is valid even if the straight center cycle is nonconvex or overlapping. It yields

π ≤ FĀr² + BK r² + Σ_i Φ_i,

where Φ_i = λ|c_i−c_(i+1)|² + (Hactual_i+Hactual_(i+1))/2.

## A two variable upper bound for each pair

Consider two consecutive arc half-angles a,b and rotate their shared endpoint to (1,0). Their midpoint directions are u=(cos a,−sin a) and U=(cos b,sin b). Set

s=sin a, h=√(r²−s²), ρ=cos a−h, c0=ρu,

S=sin b, H=√(r²−S²), P=cos b−H, C0=PU, d=c0−C0.

The first center lies in the intersection of the two radius-r disks about its assigned arc endpoints. In radial and tangential coordinates about cos(a)u, this lens is

x²+(|z|+s)² ≤ r².

If c=c0+δ, its weaker containing-disk inequality gives |δ|² ≤ 2h u·δ. Similarly, writing C=C0+Δ gives |Δ|² ≤ 2H U·Δ. Thus

λ|δ−Δ|² ≤ 2λ(|δ|²+|Δ|²) ≤ 4λ(h u·δ+H U·Δ).

Expanding the pair objective proves

Φ ≤ λ|d|² + (a−sρ+b−SP)/2 + σ_a(w)+σ_b(W),

w=2λd+(4λh−s/2)u,
W=−2λd+(4λH−S/2)U,

where σ_a(w) is the maximum of w·δ over the shifted first lens.

For radial and tangential components w_r,w_t, the exact support problem is

σ_a(w)=w_r h−|w_t|s + max_(s≤y≤r)[|w_r|√(r²−y²)+|w_t|y].

If w_r≤0 and |w_t|h≤−w_r s, the unconstrained maximizing y lies at or below s. The constrained maximum is then at y=s, and the support equals zero. Otherwise, dropping the restriction y≥s gives the always-safe bound

σ_a(w) ≤ w_r h−|w_t|s+r√(w_r²+w_t²).

Cauchy's inequality makes this right side nonnegative. The cases a=0, h=0 and w=0 are included directly or by continuity. The script encloses this pair upper bound, using zero only when its interval normal-cone test proves the zero-support condition throughout the box.

## Three supporting inequalities

For every a,b in [0,asin(113/1000)], the checker proves

Φ ≤ L_B+μ_B(a+b)/2

using the following exact constants:

| B | μ_B | L_B |
|---:|---:|---:|
|33|−37951627/10^9|1127/100000|
|34|−19173670/10^9|953/100000|
|35|−4281108/10^9|41/5000|

This is a pointwise inequality for all adjacent arc lengths and all feasible centers. It does not impose equal arc lengths or rotational symmetry.

The interval domain uses x=sin(a)/r and y=sin(b)/r in [0,1]². All trigonometric quantities except asin become radicals. Integer endpoints represent multiples of 10^−15, with outward rounding for each multiplication, square, halving and square root. Square roots use `isqrt` and integer comparisons. Asin uses its positive Taylor series through degree 19 and the rigorous tail bound z^21/(1−z²); every coefficient is at most 1. Exact fractions are used before the final outward rounding.

Each run begins with the entire unit square. Every unaccepted box is bisected along its longer side. Symmetry under exchanging a,b allows boxes wholly above the diagonal to be omitted; all boxes intersecting the diagonal are checked in full. Every retained leaf must have its upper bound at most the rational target. The interval operation tree always encloses all actual values, including at degenerate endpoints. Finishing with an empty queue proves exhaustive acceptance. Actual visited-node counts were 247707,107933,72157. A timeout reports PENDING, not success.

## Area contradiction

Summing pair inequalities uses Σ_i(a_i+a_(i+1))/2=π. Since F≤198−B, a hypothetical covering would satisfy

(1−μ_B)π ≤ [(198−B)Ā+BK]r²+BL_B.

The final exact Fraction computations, using a Machin lower bound for π, prove the opposite strict inequality for all three cases. Positive margins are approximately 0.0003000144, 0.0011881556 and 0.0034126252. The decimal descriptions are not used for acceptance.

Together with the earlier exclusions, every B is impossible at r=113/1000.

## Limits and strictness

An arbitrary hypothetical covering is projected into the unit disk, enlarged by ε and perturbed into general position, then made irredundant. Along a sequence ε→0, pass to a fixed combinatorial type and a convergent subsequence of the finitely many labeled centers, anchors and face witnesses. The marked-triangle and signed area bounds pass to the limit. Zero arcs and collapsed faces are included in the closed scalar domains above. Thus the same strict contradictions exclude arbitrary degenerate coverings at r=113/1000.

The covering-radius function is continuous on the compact projected center space D^100, so its minimum is attained. Excluding all covers of radius 113/1000 proves the strict bound r_D(100)>113/1000.

The global optimum and the exclusion of all intermediate radii remain unresolved by this certificate.

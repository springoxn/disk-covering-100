# Concave face potentials: the B33 branch at radius 0.11307

## Verified result and scope

This supplement excludes B=33 at r=11307/100000=.11307. All85 integers N=11,...,95 and all2720 scalar dual inequalities passed `verify_potential_star_duals.py`. The weakest area deficit is

\[
\frac{2961696501414281057}{40000000000000000000000}
>0.0000740424125353.
\]

This is one branch of the full lower-bound proof. The other B branches and the radius-specific geometric premises must accompany it. It does not determine the exact optimum. Earlier audited proof packages are unchanged.

## 1. Required radius-specific premises

The separate .11307 certificate gives m=100,F=165,I=67 for B33, excludes every face with three boundary vertices, and bounds each interior apex's marked-face count by3. Consequently each marked face has one boundary edge and an interior apex. Every other face has at most two boundary vertices; N below counts boundary-angle occurrences, not faces.

Marked apex angles are acute by the area-plus-anchor cap (1+sqrt2)r^2/2 for an obtuse apex. Unmarked angles obey

\[
.54<\alpha<\alpha_{\max}=\pi/2+1/25.
\]

These endpoint restrictions follow from the old per-face area budget and the fixed-angle upper function sin(alpha)(1+cos(alpha)). Marked apices also exceed .54. Thus all interior degrees are at most11. Every interior angle is less than alpha_max<2pi/3, so degrees are at least4.

The old area slack permits at most one nonacute unmarked triangle. Any degree4 interior star needs a nonacute unmarked corner, since all marked apices are acute. A triangle has at most one such corner, so the number of degree4 interior stars is at most1. A stronger independent lemma actually excludes them entirely, but the present certificate safely allows one.

## 2. A face-level potential valid even for obtuse triangles

For any triangle with angles alpha_i and circumradius R<=r,

\[
\Delta/r^2\le\frac12\sum_i\sin(2\alpha_i).
\tag{2.1}
\]

The sum is positive for a nondegenerate triangle; hence this follows from the area identity even when one sine term is negative.

Put delta_i=alpha_i-pi/3, so sum delta_i=0. As proved in the asymmetric-star supplement, the squared positive deviations sum to at least half the squared negative deviations. Therefore, with k=1/2,

\[
\Delta/r^2\le\sum_i F(\alpha_i),
\]

\[
F(a)=\frac12\sin(2a)
+\frac12(a-\pi/3)_+^2-\frac14(a-\pi/3)_-^2.
\tag{2.2}
\]

The negative part here is min(a-pi/3,0), and the positive part is max(a-pi/3,0). The added potential sums to a nonnegative quantity separately on each face. There is no global variance coefficient or acute-unmarked-face assumption.

## 3. A simple exact concave majorant

Choose the rational splice

\[
a_0=11483/10000=1.1483.
\]

Define

\[
\phi(a)=
\begin{cases}F(a),&0\le a\le a_0,\\
F(a_0)+F'(a_0)(a-a_0),&a\ge a_0.
\end{cases}
\tag{3.1}
\]

It is globally concave on its nonnegative extended domain and dominates F on [0,alpha_max]. On [0,pi/3], F''=-2sin(2a)-1/2<=0. On [pi/3,a0], F''=-2sin(2a)+1<0, as the exact check sin(2a0)>1/2 confirms.

For the tail, F'''=-4cos(2a)>0 throughout [a0,alpha_max]. Thus F'' is increasing, with at most one sign change. The tangent-minus-F function starts with value and derivative zero, and its second derivative changes from positive to negative at most once. It is nonnegative on the entire tail whenever its endpoint is nonnegative. The verifier checks the endpoint with strict margin

\[
F(a_0)+F'(a_0)(\alpha_{\max}-a_0)-F(\alpha_{\max})
>0.0000132173984301.
\]

No transcendental contact point is solved or assumed. The extended straight line after alpha_max is used only to safely enlarge scalar maximization domains.

## 4. Complete star types and corner counts

The32 allowed types are p=0,...,3 and4<=p+j<=11. Their counts x_(p,j)>=0 satisfy

\[
\sum x=67,\quad\sum p x=33,\quad\sum j x=396-N,
\quad\sum_{p>0}x\le N,\quad\sum_{p+j=4}x\le1.
\tag{4.1}
\]

The apex-count inequality uses distinct boundary-fan transitions and unmarked corner witnesses; it remains valid when one unmarked face has two boundary vertices, because it then supplies two counted angle occurrences.

At most3 marked faces per apex and (4.1) give N>=11. Minimum degree5 except at most one degree4 gives total interior degree>=334, hence N<=95. All85 integers are checked, including zero-unmarked-fan boundary vertices.

Let Gamma be the marked apex-angle sum. Actual complete Delaunay interior stars sum to2pi. Counting unmarked angles gives the boundary unmarked angle sum

\[
\sum\alpha=\Gamma-2\pi.
\tag{4.2}
\]

This does not assume a convex boundary-center polygon.

## 5. Concave scalar supports

Use the previously proved concave acute-apex score Gbar from `STAR_LP_PROOF.md`, which bounds the marked center triangle plus its anchor. At an interior star let g be the mean of its p marked apex angles. The j unmarked angles have mean (2pi-pg)/j. Jensen therefore bounds its joint score by

\[
p\overline G(g)+j\phi((2\pi-pg)/j).
\]

For arbitrary eta, define the concave scalar maximum

\[
s_{p,j}(\eta)=\max_g
\{p\overline G(g)+j\phi((2\pi-pg)/j)+\eta pg\}.
\tag{5.1}
\]

For p=0 it is the explicit constant j phi(2pi/j). For p>0 the allowed closed domain is

\[
\max\{0,(2\pi-j\alpha_{\max})/p\}\le g\le\pi/2.
\]

For the boundary angles, define the concave conjugate

\[
C(\eta)=\max_{0\le a\le\alpha_{\max}}[\phi(a)-\eta a].
\tag{5.2}
\]

Their total contribution is at most eta Gamma-2pi eta+N C(eta). The same linear apex term has already been included in (5.1).

Both maxima are verified by endpoint tests and derivative-sign bisection. The functions are concave and continuously differentiable at their piece boundaries. Flat or unresolved-derivative cases use a global tangent with a conservative rounded-domain distance. The interval bisection does not presume a numerical optimum.

## 6. Rational dual inequalities and the final area contradiction

For each N the supplied rational data eta,u0,u1,u2,v,w, with v,w>=0, satisfy every scalar inequality

\[
s_{p,j}(\eta)<u_0+u_1p+u_2j
+v\mathbf1_{p>0}+w\mathbf1_{p+j=4}.
\]

Summing with (4.1) gives the normalized upper bound

\[
67u_0+33u_1+(396-N)u_2+Nv+w+NC(\eta)-2\pi\eta.
\]

The boundary circular contribution is at most33H_r(2pi/33) by the original H concavity theorem. Thus full coverage would require

\[
\pi\le r^2[67u_0+33u_1+(396-N)u_2+Nv+w+NC(\eta)-2\pi\eta]
+33H_r(2\pi/33).
\tag{6.1}
\]

Exact arithmetic shows the right side is strictly smaller than pi for all85 integers N. This excludes B33 at the working radius.

## 7. Files, exactness, and unfinished work

The input coefficients are `potential_star_dual_proposals.json`; the standard-library replay is `verify_potential_star_duals.py`, with its unchanged exact helper `verify_star_lp_duals.py`. The saved output is `potential_star_verification_result.json`.

All acceptance uses integers, Fraction, isqrt, degree49/48 Taylor enclosures, and Machin pi bounds. The sine/cosine interval routines include interior extrema explicitly. Numerical LP code only proposes coefficients and is unnecessary for replay.

Strict margins permit the established generic-cover limiting argument. A universal lower-bound assertion additionally requires all remaining B branches and their count bridge. The exact optimum, optimal algebraic centers, and exclusion of every smaller radius remain unproved.

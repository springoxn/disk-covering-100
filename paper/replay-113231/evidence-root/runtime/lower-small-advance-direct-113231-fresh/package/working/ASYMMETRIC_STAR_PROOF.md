# Local face-angle compatibility: B33 at radius 0.11306

## Verified result and scope

At r=5653/50000=.11306, the B=33 branch is excluded by this exact finite certificate. All84 integers N=11,...,94 and all2352 scalar dual inequalities passed `verify_asymmetric_star_duals.py`. The weakest final margin is

\[
\frac{78915378264433360217}{10^{24}}>0.0000789153782644.
\]

This supplement must be combined with the separate geometric-premise checks and the exclusions for other surviving B. It does not determine the exact optimum. The previously audited .11305 files are unchanged.

## 1. Geometric premises at the new radius

The required B33 structural certificate gives m=100,F=165,I=67, no face with three boundary vertices, at most three marked faces per interior apex, and the exact interior-star angle sums. Every unmarked triangle is acute and has

\[
|T|/r^2\le A-cV_T,\quad A=3\sqrt3/4,\quad c=73/100.
\]

Every marked apex is acute. This is stronger than assuming the whole marked triangle acute: an obtuse boundary base angle is harmless to the present interior-star method. For an obtuse marked apex, the fixed-base area bound plus its anchor gives at most (1+sqrt2)r^2/2, which is excluded by the old total-area slack. Unmarked triangles have area>r^2, excluding a right or obtuse angle.

The sharp fixed-variance lemma bootstraps the unmarked variance below .39828, verifies coefficient c=.73, and forces every unmarked angle above .53. Marked apex angles exceed .55. Thus interior degrees remain5,...,11 even though some marked boundary base angles need not be acute.

Chordlessness is **not** required by this new supplement. An unmarked face may have two boundary vertices. Accordingly, N means the number of unmarked **boundary-angle occurrences**, rather than the number of boundary-touching faces. The corner-incidence counts and the angle partitions below still hold.

## 2. The new local compatibility inequality

For the three angle deviations of any unmarked triangle, write delta_1+delta_2+delta_3=0 and

\[
V_-=\sum_{\delta_i<0}\delta_i^2,\qquad
V_+=\sum_{\delta_i>0}\delta_i^2.
\]

Then

\[
V_+\ge V_-/2,\qquad V=V_-+V_+\ge\frac32V_-.
\tag{2.1}
\]

Proof: if there is one negative deviation of magnitude a+b, the two positive deviations a,b have a^2+b^2>=(a+b)^2/2. If there are two negative deviations a,b, the single positive magnitude a+b has square at least a^2+b^2. Zero and degenerate sign cases follow continuously.

This condition is imposed separately on every triangle. It was absent from the earlier symmetric star relaxation, which retained only angle sums at vertices and a global boundary sum.

## 3. An asymmetric variance allocation

At an interior star of type(p,j), let the p marked apex angles have mean g. The sum of the j unmarked deviations is

\[
D_{p,j}(g)=2\pi-pg-j\pi/3.
\]

Their total variance is at least D^2/j. Their negative-part variance is at least (D_-)^2/j, where D_-=min(D,0). Indeed, the total magnitude of negative deviations is at least -D whenever D<0, and Cauchy applies to at most j corners.

Let Gamma be the sum of all marked apex angles. The N unmarked boundary-angle deviations have sum

\[
D_b=\Gamma-(N+6)\pi/3,
\]

so the corresponding ordinary and negative-part variance bounds are D_b^2/N and (D_b^-)^2/N.

All unmarked corners are partitioned into the interior stars and this boundary group. Combining one-third of the ordinary Cauchy bound with two-thirds of (2.1) yields

\[
\sum_TV_T\ge
\sum_{\rm stars}\frac{f(D_{p,j})}{j}+\frac{f(D_b)}N,
\tag{3.1}
\]

where the convex function is

\[
f(D)=D^2/3+(D_-)^2
=\begin{cases}D^2/3,&D\ge0,\\4D^2/3,&D\le0.\end{cases}
\tag{3.2}
\]

The two one-sided coefficients are exactly1/3 and4/3. This allocation reserves each triangle's variance only once and does not add an interface penalty from another proof.

## 4. Counts and boundary conjugate

The same28 integer types satisfy p=0,...,3 and5<=p+j<=11. Their counts x_(p,j) obey

\[
\sum x=67,\quad\sum p x=33,\quad\sum j x=396-N,
\quad\sum_{p>0}x\le N.
\tag{4.1}
\]

The last inequality counts distinct marked apices. Each transition between common-apex boundary fans requires an unmarked corner at the transition vertex. If one unmarked face supplies two different transitions, it also supplies two distinct boundary-angle occurrences, both counted in N. Thus the proof does not require chordlessness.

The p<=3 bound gives N>=11; minimum interior degree5 gives N<=94. These84 integers are all checked.

For every real eta,

\[
-\frac cNf(D_b)\le\eta D_b+
\frac{N\eta^2}{4c\,a_\eta},
\tag{4.2}
\]

where a_eta=4/3 if eta>=0, and a_eta=1/3 if eta<0. To prove this, maximize -c f(D)/N-eta D: its maximizer has the sign opposite eta, and completing the corresponding square gives (4.2).

## 5. Scalar star supports and exact rational duals

Use the globally concave acute-apex marked-face majorant from `STAR_LP_PROOF.md`:

\[
\overline G(g)=
\begin{cases}\sin g(1+2\cos g),&0\le g\le\pi/3,\\
\sqrt3-(g-\pi/3)/2,&\pi/3\le g\le\pi/2.
\end{cases}
\]

The new scalar coefficients are

\[
s_{p,j}(\eta)=\max_{0\le g\le\pi/2}
\left[p\overline G(g)-\frac c j f(2\pi-pg-j\pi/3)+\eta pg\right].
\tag{5.1}
\]

For p=0 this is an explicit constant. For p>0 the maximand is concave: Gbar is concave and f is convex. Its derivative remains continuous both at g=pi/3 and at the residual sign change. The verifier checks endpoints and bisects derivative signs using outward-rounded integer intervals. If a derivative sign is unresolved, a concave-function tangent with a conservative rounded-bracket distance gives a valid upper bound. There is no floating-point maximum acceptance.

For every N the coefficient file gives rational eta,u0,u1,u2,v, with v>=0. All28 inequalities

\[
s_{p,j}(\eta)<u_0+u_1p+u_2j+v\mathbf1_{p>0}
\tag{5.2}
\]

are independently verified. Equations(4.1)-(4.2) then give the full area upper bound

\[
r^2\left[132A+67u_0+33u_1+(396-N)u_2+Nv
-\eta(N+6)\pi/3+\frac{N\eta^2}{4c\,a_\eta}\right]
+33H_r(2\pi/33).
\tag{5.3}
\]

It is strictly smaller than pi for every N=11,...,94. Hence the B33 branch cannot cover the closed unit disk at the working radius.

## 6. Files and acceptance

- `asymmetric_star_dual_proposals.json`: exact rational candidate dual coefficients with denominator10^8
- `verify_asymmetric_star_duals.py`: all2352 scalar inequalities and84 area contradictions
- `verify_star_lp_duals.py`: immutable standard-library exact interval and trigonometric helpers
- `asymmetric_star_verification_result.json`: actual replay results
- the separate .11306 premise certificate: necessary geometry, corner counts, and c=.73

The proposal-generating SciPy code is unnecessary for acceptance. It only discovers candidate coefficients. Accepted computations use integers, Fraction, isqrt, Taylor bounds, and Machin pi bounds. Positive margins support the standard generic-cover limiting argument; a complete universal radius statement must also include the other B branches.

# Acute interior-star compatibility at radius 0.11305

## Status and scope

This supplement excludes the **B=33 branch** at

\[
r=2261/20000=0.11305.
\]

It does not alone exclude the other surviving boundary counts or determine the exact optimum. The separate geometric-premise certificate is required. The arithmetic replay is `verify_star_lp_duals.py`, using the rational coefficients in `star_dual_proposals.json`. All 84 integer cases and 2352 scalar inequalities have actually passed. The weakest case is N=25, with area deficit at least

\[
\frac{47175064172473171313}{500000000000000000000000}
>0.000094350128344.
\]

Numerical optimization was used only to propose rational coefficients. No numerical solver output is accepted as proof.

## 1. Precisely required geometric premises

For a generic irreducible covering at the working radius, previous exact checks give:

1. m=100, B=33 in the branch under consideration, F=165 center faces, I=67 interior centers
2. The boundary cycle is chordless. Thus every boundary face has exactly one boundary edge and an interior apex; every other face has at most one boundary vertex
3. Each interior apex belongs to at most three boundary faces
4. All center triangles are acute
5. Every unmarked triangle obeys
   \[
   |T|/r^2\le A-cV_T,\quad A=3\sqrt3/4,\quad c=17/25,
   \]
   where V is the sum of its three squared angular deviations from pi/3
6. Every angle incident to an interior center exceeds 11/20, so each interior degree is between 5 and 11
7. The center faces are a straight Delaunay subcomplex; all selected incident angles at an interior center sum to 2pi

These are independently checked by the geometric-premise worker. This supplement explains the variance mechanism and the remaining reduction rather than silently treating the premises as arbitrary assumptions.

### 1.1 Why the stronger variance coefficient is valid here

Let delta_1+delta_2+delta_3=0, V=sum delta_i^2, and T=sum delta_i^3. The elementary identities

\[
\sum\delta_i^4=V^2/2,\qquad T^2\le V^3/6
\]

give, along the radial angle segment alpha_i(t)=pi/3+t delta_i,

\[
\frac{\sum\delta_i^2\csc^2\alpha_i(t)}V
\ge1+\frac{t^2V}{2}-\frac{t\pi\sqrt V}{3\sqrt6}+\frac{\pi^2}{36}
\ge1+\frac{\pi^2}{54}>59/50.
\]

Here csc^2 x=1+tan^2(x-pi/2)>=1+(x-pi/2)^2. Integrating the second derivative of sum log sin alpha_i(t) yields

\[
|T|/r^2\le A\exp(-59V/100).
\]

The original area budget at r=.11305 has normalized surplus d<245643/10^6. Consequently every unmarked face has area/r^2>=A-d. Exact exponential-Taylor arithmetic excludes V>=37/100. On the remaining range,

\[
A(1-e^{-(59/100)V})
\ge A\left(\frac{59}{100}-\frac{(59/100)^2}{2}\frac{37}{100}\right)V
>\frac{17}{25}V.
\]

Thus premise 5 is a consequence of the small total area slack, not a global claim for arbitrary acute triangles. Also V<.37 and the zero-sum deviations imply every unmarked angle exceeds

\[
\pi/3-\sqrt{37/150}>.55.
\]

For a marked-face apex gamma<=.55, its area plus anchor is at most sin(.55)(1+2cos(.55))r^2, already too small for the same original slack. Hence marked apex angles also exceed .55. Acute interior stars have at least five faces, and 12*.55>2pi gives the upper degree 11.

## 2. Integer star types and face-angle accounting

At an interior center let p be its number of boundary faces and j its number of unmarked faces. The only necessary types are

\[
p=0,1,2,3,\qquad5\le p+j\le11.
\]

There are 28 types. Write x_(p,j) for their nonnegative counts. Let N be the number of unmarked faces having one boundary vertex. Chordlessness makes N also the number of unmarked boundary-angle occurrences. Counting gives

\[
\sum x=67,\qquad\sum p x=33,\qquad\sum j x=396-N.
\tag{2.1}
\]

The number of distinct boundary apices is at most N:

\[
\sum_{p>0}x\le N.
\tag{2.2}
\]

Indeed, decompose boundary faces into common-apex fans. Each transition between fans occurs at a distinct boundary vertex and has at least one unmarked face in the intervening link. Such witnesses are distinct because no unmarked face has two boundary vertices. The number of distinct apices is at most the number of fans.

Since each apex receives at most three boundary faces, (2.2) gives N>=11. The minimum interior degree 5 and (2.1) give 429-N>=335, hence N<=94. We exhaust all 84 integers in this range.

Let Gamma denote the sum of all marked-face apex angles. Interior stars sum to 2pi. Counting unmarked face angles directly gives the unmarked boundary-angle sum

\[
\sum\alpha=\Gamma-2\pi.
\tag{2.3}
\]

This identity uses actual Delaunay angles: an interior center's entire ordinary Voronoi cell lies inside D, so all its ordinary Delaunay incident faces are selected. Abstract topology alone would not justify it.

## 3. A globally concave upper score for an acute marked face

For acute apex gamma and circumradius R<=r, set z=(R/r)^2 sin^2 gamma. Its maximum triangle area plus marked anchor, divided by r^2, is bounded by

\[
\cot(\gamma/2)z+\sqrt{z(1-z)},\qquad0\le z\le\sin^2\gamma.
\]

The unconstrained maximum occurs at z=cos^2(gamma/4). Thus the exact optimized upper function is

\[
U(\gamma)=
\begin{cases}
\sin\gamma(1+2\cos\gamma),&0\le\gamma\le2\pi/5,\\
\tfrac12\cot(\gamma/4),&2\pi/5\le\gamma\le\pi/2.
\end{cases}
\]

The convenient concave majorant used by the verifier is

\[
\overline G(\gamma)=
\begin{cases}
\sin\gamma(1+2\cos\gamma),&0\le\gamma\le\pi/3,\\
\sqrt3-(\gamma-\pi/3)/2,&\pi/3\le\gamma\le\pi/2.
\end{cases}
\tag{3.1}
\]

The first branch is concave; its value and derivative at pi/3 match the line. This tangent dominates U through 2pi/5. Beyond that point U is convex, and the line dominates at both endpoints, as certified by

\[
\sqrt3-\pi/30>\tfrac12\sqrt{5+2\sqrt5},\qquad
\sqrt3-\pi/12>\tfrac12(1+\sqrt2).
\]

Hence (3.1) bounds all acute marked-face shapes, not only radius-r or isosceles triangles.

## 4. Star closure and boundary variance

For an interior star with p>0, write g for the average of its p marked apex angles. Concavity gives a marked-face sum at most p Gbar(g). Its j unmarked angles sum to 2pi-pg, so their squared deviations sum to at least

\[
\frac{(2\pi-pg-j\pi/3)^2}{j}.
\]

For p=0 the same expression is independent of g. The remaining unmarked boundary-angle variance is at least

\[
\frac{(\Gamma-(N+6)\pi/3)^2}{N}.
\]

For any real rational eta, the last negative quadratic satisfies

\[
-\frac cN(\Gamma-(N+6)\pi/3)^2
\le\eta(\Gamma-(N+6)\pi/3)+\frac{N\eta^2}{4c}.
\]

Consequently the normalized star coefficient to certify is

\[
s_{p,j}(\eta)=\max_{0\le g\le\pi/2}
\left[p\overline G(g)-\frac c j(2\pi-pg-j\pi/3)^2+\eta pg\right].
\tag{4.1}
\]

For p=0 this is the explicit constant -c(2pi-jpi/3)^2/j. For p>0 the maximand is globally concave, with strictly negative second derivative from the quadratic. Its derivative is continuous through pi/3, so exact sign bisection and endpoint checks enclose its unique maximum. No floating root is accepted.

## 5. A rational dual certificate for every N

For each N the supplied file contains rational eta,u0,u1,u2,v with v>=0. The verifier independently proves all 28 inequalities

\[
s_{p,j}(\eta)<u_0+u_1p+u_2j+v\mathbf1_{p>0}.
\tag{5.1}
\]

Multiplying by the nonnegative counts and using (2.1)-(2.2) gives

\[
\sum s_{p,j}(\eta)x_{p,j}
<67u_0+33u_1+(396-N)u_2+Nv.
\]

The final area upper bound is therefore

\[
r^2\left[132A+67u_0+33u_1+(396-N)u_2+Nv
-\eta(N+6)\pi/3+\frac{N\eta^2}{4c}\right]
+33H_r(2\pi/33).
\tag{5.2}
\]

It is strictly less than pi for every N=11,...,94. This contradicts complete coverage in the B=33 branch.

The arithmetic uses denominator 10^24 integer intervals. Sine and cosine use degree49/48 Taylor sums with explicit next-degree remainder bounds; their arguments stay in the asserted monotone intervals. Square roots and rational divisions are enclosed exactly. All numerical LP duals are rounded to denominator10^8 and then checked from scratch, with strict slack. LP optimality, primal solutions, and floating-point feasibility are irrelevant to acceptance.

## 6. Remaining work

The strict margins permit the usual generic-cover limiting argument. However, this file is only the B=33 branch at .11305. Before asserting a universal lower bound at that radius, every other surviving B branch must also be excluded and the premise/audit files packaged together. The exact minimum and algebraic optimal centers remain unknown.

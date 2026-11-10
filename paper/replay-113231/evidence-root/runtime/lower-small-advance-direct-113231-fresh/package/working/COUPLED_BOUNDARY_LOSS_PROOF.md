# Nonsymmetric boundary coupling: a new strict lower bound

This supplement proves, together with the separately certified count/no-ear reduction,

\[
r_D(100)>\frac{113}{1000}.
\]

It does **not** identify the exact optimum. In particular, the current upper construction does not match this lower bound.

The acceptance program is `coupled_boundary_loss_verify.py`. It uses only integer arithmetic, exact fractions for rational division, and outward-rounded intervals. Floating-point arithmetic appears only in elapsed-time reporting.

## 1. The required count and no-ear reduction

The earlier area theorem, at radius \(r_0=113/1000\), excludes every cover with at most 99 nonredundant disks. With 100 disks it leaves only boundary-cell counts

\[
B\in\{33,34,35\}.
\]

The separate three-arc certificate excludes every triangulation face carrying two boundary edges. Indeed, such a face uses three consecutive boundary centers and a common Voronoi point within \(r_0\) of all three. Their three assigned boundary arcs lie in a disk of radius \(2r_0\), so their total angle is at most \(2\arcsin(2r_0)<456/1000\). The previously proved concavity of \(H_r\), followed by exact interval arithmetic, excludes this concentration for each of the three surviving \(B\). A face carrying three boundary edges would be the entire disk triangulation, which is impossible with 100 vertices and interior vertices.

Consequently, the \(B\) boundary edges belong to \(B\) distinct triangulation faces, each carrying exactly one boundary edge. The other faces carry none. The total face count is

\[
F=198-B.
\]

The present supplement supplies the missing additional loss, without assuming equal arcs, symmetric centers, rings, or a fixed triangulation.

## 2. The inner vertex of a boundary lens

Write the angle of boundary arc \(i\) as \(\theta_i\), with

\[
0<\theta_i\le 2\arcsin r,
\qquad \sum_i\theta_i=2\pi.
\]

Let \(u_i\) be the radial unit vector to its midpoint and \(v_i\) a perpendicular unit vector. Put

\[
s_i=\sin(\theta_i/2),\quad
c_i=\cos(\theta_i/2),\quad
h_i=\sqrt{r^2-s_i^2}.
\]

The two unit-circle endpoints are \(c_i u_i\pm s_i v_i\). Their innermost common radius-\(r\) lens vertex is

\[
p_i=(c_i-h_i)u_i.
\]

Use \(z_i\) for the actual covering center, so it is not confused with the scalar \(c_i\). Write

\[
z_i=p_i+d_i u_i+t_i v_i.
\]

Both endpoint distances are at most \(r\), so

\[
2h_i d_i\ge d_i^2+t_i^2+2s_i|t_i|.
\tag{2.1}
\]

Thus \(d_i\ge0\), and for \(s_i>0\),

\[
|z_i-p_i|\le\frac r{s_i}d_i.
\tag{2.2}
\]

To check (2.2), use \(|t_i|\le(h_i/s_i)d_i\) and \(s_i^2+h_i^2=r^2\). If \(h_i=0\), (2.1) forces both displacement coordinates to vanish.

The signed triangle joining \(z_i\) to its two boundary anchors has area exactly

\[
s_i(h_i-d_i).
\]

Hence its loss from the radial lens maximum is exactly \(s_i d_i\). This is a signed identity and does not require the center to be on the inward side of the anchor chord.

## 3. The marked-face functional

Set

\[
A=\frac{3\sqrt3}{4},\qquad
\kappa=\frac{461134488}{10^9}.
\]

For \(0\le L\le2r\), the maximum area of a triangle of circumradius at most \(r\) with a distinguished side of length \(L\) is bounded by

\[
f_r(L)=\frac L2\left(r+\sqrt{r^2-L^2/4}\right).
\]

The anchor triangle above the same side has area at most

\[
J_r(L)=\frac L2\sqrt{r^2-L^2/4}.
\]

Their sum is

\[
g_r(L)=f_r(L)+J_r(L)
=r^2 x(1+2\sqrt{1-x^2}),\qquad x=L/(2r).
\]

It is concave in \(L\), with maximum

\[
G_1r^2,
\qquad G_1=\sqrt{\frac{207+33\sqrt{33}}{128}}<A+\kappa.
\]

For \(0<x<1\),

\[
g_r'(L)=r\left(\frac12+\sqrt{1-x^2}-\frac{x^2}{\sqrt{1-x^2}}\right),
\]

\[
g_r''(L)=-\frac{3x}{2\sqrt{1-x^2}}
-\frac{x^3}{2(1-x^2)^{3/2}}<0.
\]

The endpoint values are obtained by continuity.

## 4. A loss for every neighboring pair of arcs

For the edge joining centers \(z_i,z_{i+1}\), let

\[
L_i=|z_i-z_{i+1}|,\qquad
L_i^0=|p_i-p_{i+1}|,
\qquad
k_i=\frac{\min(s_i^2,s_{i+1}^2)}{2r}.
\]

The triangle inequality and (2.2) give

\[
\frac12(s_i d_i+s_{i+1}d_{i+1})
\ge k_i|L_i-L_i^0|.
\]

Define the nonnegative continuous function

\[
D_r(\alpha,\beta)
=\min_{0\le L\le2r}
\left\{G_1r^2-g_r(L)+k(\alpha,\beta)|L-L^0(\alpha,\beta)|\right\}.
\tag{4.1}
\]

Here \(s_\alpha=\sin(\alpha/2)\), \(a_\alpha=\cos(\alpha/2)-\sqrt{r^2-s_\alpha^2}\), and a stable formula is

\[
(L^0)^2=(a_\alpha-a_\beta)^2
+4a_\alpha a_\beta\sin^2((\alpha+\beta)/4).
\tag{4.2}
\]

The usual directed-area identity, now applied to the \(B\) distinct one-marked faces, yields

\[
\pi\le [(198-B)A+B\kappa]r^2
+\sum_i H_r(\theta_i)-\sum_iD_r(\theta_i,\theta_{i+1}),
\tag{4.3}
\]

where

\[
H_r(\theta)=\sin(\theta/2)\sqrt{r^2-\sin^2(\theta/2)}
+\frac{\theta-\sin\theta}{2}.
\]

For completeness: the unmarked faces contribute at most \((F-B)Ar^2\); each marked face and its anchor triangle contribute at most \(g_r(L_i)\); each center-to-two-anchors triangle plus circular segment contributes \(H_r(\theta_i)-s_i d_i\). Summing the neighboring half-losses, using (4.1), and then using \(G_1<A+\kappa\), proves (4.3).

## 5. A finite nonsymmetric interval certificate

Fix \(r=r_0=113/1000\), and \(\mu_B=2\pi/B\). Define the concave-function tangent deficit

\[
Q_B(\theta)=H_{r_0}(\mu_B)
+H_{r_0}'(\mu_B)(\theta-\mu_B)-H_{r_0}(\theta)\ge0.
\]

The program proves, over **every** allowable pair of angles,

\[
D_{r_0}(\alpha,\beta)
+\frac12(Q_B(\alpha)+Q_B(\beta))>\delta_B,
\tag{5.1}
\]

with

\[
\delta_{33}=\frac9{10^6},\qquad
\delta_{34}=\frac1{20000},\qquad
\delta_{35}=\frac1{10000}.
\]

Outside the following respective angle intervals, convexity of \(Q_B\) and its exact endpoint checks already give \(Q_B>2\delta_B\):

- \(B=33\): \([186/1000,195/1000]\)
- \(B=34\): \([173/1000,196/1000]\)
- \(B=35\): \([161/1000,196/1000]\)

Inside their squares, a complete recursive rectangular partition is verified. There are respectively 73, 138, and 71 accepted leaves, of maximum binary depth 10, 12, and 10. Splits retain both closed children, so there are no gaps.

No minimizer in (4.1) is accepted numerically. On every rectangle the program chooses a rational support length \(z\), verifies strictly

\[
|g_{r_0}'(z)|<k_{\rm lower},
\]

and uses concavity to obtain

\[
D_{r_0}(\alpha,\beta)
\ge G_1r_0^2-g_{r_0}(z)-g_{r_0}'(z)(L^0-z).
\tag{5.2}
\]

This follows directly from the tangent upper bound on \(g\), because the remaining expression
\(k|L-L^0|-g'(z)(L-L^0)\) is nonnegative. A negative right side in (5.2) may be replaced by zero.

All intervals have denominator \(10^{24}\). Sine is enclosed by its degree-13 alternating Taylor sum plus the next-term bound; cosine uses degree 12 and its next-term bound. Their arguments lie in \([0,1/3]\). Square roots are bounded by integer square-root calculations. All divisions and products round outwards. The \(\pi\) enclosure is inherited from the exact Machin-series routine in the original package.

## 6. The final contradiction and strictness

Summing (5.1) around the boundary cycle cancels every linear tangent term, because \(\sum\theta_i=B\mu_B=2\pi\). Equation (4.3) therefore gives

\[
\pi<[(198-B)A+B\kappa]r_0^2
+BH_{r_0}(2\pi/B)-B\delta_B.
\]

But exact interval checks show the right side is strictly **less** than \(\pi\), with gaps exceeding respectively

\[
0.0000421067980742,\qquad
0.0002566608195759,\qquad
0.0025491411764394.
\]

The decimals here summarize rational margins printed by the verifier; they are not acceptance inputs.

For arbitrary or degenerate configurations, use the original compactness and generic-perturbation argument. If a cover at \(r_0\) existed, perturb centers by arbitrarily small amounts and enlarge its radius to \(r_0+\varepsilon\), then delete redundant disks. The count and no-ear exclusions have strict margins, so for all sufficiently small \(\varepsilon\) the auxiliary covers still have \(m=100\), \(B\in\{33,34,35\}\), and no two-marked faces. Pass to a subsequence with constant \(B\). All final angle-only functions in (4.3)–(5.1) extend continuously to zero-length arcs. Equivalently, the finitely many strict interval inequalities persist for sufficiently small changes in radius. Taking \(\varepsilon\downarrow0\) contradicts the displayed positive margins.

Thus no radius-\(r_0\) cover exists. Since the covering-radius minimum is attained on the compact projected center space, the new bound is strict:

\[
\boxed{\frac{113}{1000}<r_D(100).}
\]

# Nonsymmetric common-apex bounds for two boundary triangles

These lemmas apply to two actual adjacent q1 boundary faces with a common apex. They do not assert that such a fan exists in every covering. No equal-arc, equal-radius-position, or symmetry assumption is made. The formulas have been independently audited; their use to exclude all fans still requires a complete scalar interval certificate.

Write J(x,y)=(-y,x), so det(u,v)=Ju dot v.

## 1. Orientation is a consequence of the Voronoi transition

Let boundary sites a,b occur in this order around the unit circle, with transition point q. The squared-distance difference changes from favoring a to favoring b as the circle is traversed counterclockwise. Thus (b-a) dot Jq>0. Put e=b-a and m=(a+b)/2. Since q-m is perpendicular to e and q dot(q-m)>0, q lies on the right side of the directed edge a to b.

The clipped bisector runs inward from q to its first interior Voronoi vertex v. If p is the third site there, it is co-nearest at v but is no nearer than a,b on the segment back to q. Subtracting the two affine squared-distance differences shows that p lies to the left of a to b. Equivalently, in coordinates with a=(-x,0), b=(x,0), q=(0,t), t<0, and v=(0,s), s>t, the difference at q is 2(s-t)p_y>=0. Genericity excludes collinearity, so p_y>0.

Therefore the center triangle adjacent to each directed boundary edge has positive signed area in the boundary ordering. This argument does not require the center boundary polygon to be convex.

## 2. Feasible apex disk for a fixed base

Let a directed base have length ell<=2r, midpoint m, and inward unit normal n=J(b-a)/ell. Put h=sqrt(r^2-ell^2/4) and K=m+h*n.

Every third vertex p on the inward side whose triangle has circumradius at most r belongs to the disk B(K,r). To prove this, take base coordinates (-ell/2,0),(ell/2,0). Its circumcenter is (0,k), where |k|<=h. A third vertex (X,Y), Y>=0, satisfies

\[
X^2+Y^2-2kY=\ell^2/4.
\]

Hence

\[
X^2+(Y-h)^2=\ell^2/4+h^2+2(k-h)Y\le r^2.
\]

The disk B(K,r) can contain positions that fail the original circumradius or side condition. Enlarging the feasible set is harmless for an upper bound.

## 3. Joint support for two actual center triangles

Suppose the consecutive boundary centers are a,b,c and both triangles abp and bcp have the same apex p. Construct the two apex disks B(K1,r), B(K2,r) from Section 2. Their intersection contains p. Averaging their squared-distance inequalities gives

\[
\left|p-\frac{K_1+K_2}{2}\right|^2
\le r^2-\frac{|K_1-K_2|^2}{4}.
\]

If the right side is negative, the fan is impossible. Otherwise define

\[
w=\frac{J(c-a)}2,\qquad C=\frac{\det(a,b)+\det(b,c)}2.
\]

The sum of the two positive center-triangle areas is exactly C+w dot p, and consequently is at most

\[
C+w\cdot\frac{K_1+K_2}{2}
+|w|\sqrt{r^2-|K_1-K_2|^2/4}.
\tag{1}
\]

The two anchor upper bounds J_r(|b-a|)+J_r(|c-b|) can be added separately.

At the specifically certified threshold r=.11302, B=33, the companion exact checker `verify_boundary_edge_window.py` proves that all q1 faces are acute and 1.3r<ell_j<1.85r. These imply a useful nondegeneracy bound for an actual two-face fan. Its middle polygon angle is the sum of two acute base angles, so the directed turn tau between the two boundary edges belongs to (0,pi). Set a_j=asin(ell_j/(2r)). The vectors K1-b and K2-b both have length r, and their angular difference is tau-a1-a2. Consequently

\[
\frac{|K_1-K_2|}{2r}
=\left|\sin\frac{\tau-a_1-a_2}{2}\right|
\le\max\{.925,\sqrt{1-.65^2}\}=.925.
\]

Thus |K1-K2|<=1.85r and the smaller containing-ball radius in (1) is at least r*sqrt(231)/40. The normal denominators ell_j and the radicals h_j also have strictly positive certified lower bounds. This is a conditional restriction on real fans, useful for interval pruning; it should not be assumed for arbitrary boxes or other radii without its premises.

For numerically stable evaluation translate b to zero, set A=a-b and Cvec=c-b, and use

\[
K_1=A/2-(h_1/|A|)JA,\quad
K_2=Cvec/2+(h_2/|Cvec|)JCvec,\quad
w=J(Cvec-A)/2.
\]

Then the additive determinant constant vanishes, so the bound is simply w dot Kmid plus the support-radius term. Generic distinct centers give nonzero denominators. A limiting proof must retain limiting directions or establish a positive edge-length bound before dividing.

## 4. Exact fan-patch cancellation removes the middle center

Let q0,q1,q2,q3 be the consecutive target-circle transition points, with a owning the arc q0 to q1, b owning q1 to q2, and c owning q2 to q3. Denote their total angular length by Theta.

Combine the following signed areas without replacing them by independent absolute-value bounds:

- Center triangles abp and bcp
- Anchor triangles baq1 and cbq2
- Outer triangles q0q1a, q1q2b, q2q3c
- The three target-circle segments

All internal edges cancel. In particular the middle center b disappears entirely. The combined patch area is exactly

\[
\frac{\Theta}{2}
+\frac{\det(a,q_0)+\det(q_3,c)}2
+\frac{J(c-a)}2\cdot p.
\tag{2}
\]

Both edges ap and cp belong to center triangles of circumradius at most r, so |p-a|,|p-c|<=2r. For d=|c-a|<=4r, the support of this equal-radius lens in the direction perpendicular to c-a is exact. Equation (2) is therefore bounded by

\[
U(a,c)=\frac{\Theta}{2}
+\frac{\det(a,q_0)+\det(q_3,c)-\det(a,c)}2
+\frac d2\sqrt{4r^2-d^2/4}.
\tag{3}
\]

If d>4r the fan is impossible. Formula (3) drops the middle-center constraints and the detailed circumradius constraints, so it is a relaxation; nevertheless it often retains a substantial shared-apex loss. It has only three arc variables and the two outer-center lens positions, instead of three center positions plus an apex.

Signed cancellation is important. Formula (2) remains valid if an outer triangle has negative signed area. For the remaining portions of the full covering one may still use the earlier absolute-area upper bounds. No extra assumption that all patch pieces have disjoint interiors is needed.

## 5. A sufficient condition to eliminate the two remaining center positions

For an assigned arc of angle theta, let u be its radial midpoint direction, v=Ju, s=sin(theta/2), h=sqrt(r^2-s^2), and let the inner radial lens corner be c0=(cos(theta/2)-h)u. Write any feasible center as c0+z*u+t*v.

The two endpoint distance inequalities imply

\[
z^2+t^2-2hz+2s|t|\le0.
\]

In particular z>=0 and |t|<=(h/s)z. The exact tangent extent is |t|<=sqrt(r^2-(z-h)^2)-s, but the simpler cone bound is often sufficient.

Let Q(d)=d*sqrt(4r^2-d^2/4)/2. For 0<d<4r, the gradients of (3) are

\[
\nabla_a U=\tfrac12J(c-q_0)+Q'(d)(a-c)/d,
\]

\[
\nabla_c U=\tfrac12J(q_3-a)+Q'(d)(c-a)/d.
\]

If throughout a convex-lens parameter region

\[
\nabla_aU\cdot u_a+|\nabla_aU\cdot v_a|h_a/s_a\le0
\]

and the analogous inequality holds for c, then U is maximized by taking both centers at their inner radial corners. Indeed, along the segment from an inner corner to any point in its convex endpoint lens, the displacement satisfies the displayed cone inequality, so the directional derivative is nonpositive. Apply this to a with c fixed, then to c.

This is a sufficient criterion, not an already-certified universal fact. At r=.11302, B=33, numerical exploration over a coarse old-area-budget domain found negative cone coefficients, suggesting an exact certificate may reduce the remaining fan problem to only three arc variables. That numerical exploration is not used to accept a theorem in this bundle.

## 6. Combining losses without double counting

A shared-apex pair need not occur: all boundary faces might be singleton fans. If maximum fan length is three and there are Nf fans, there are D=2Nf interface edges and at least ceil((B-Nf)/2) non-singleton fans from which disjoint two-face pairs can be selected.

However, a raw common-apex loss and an independently proved interface loss cannot simply be added if both spend the same triangle-area deficit. Either include the same interface stress terms in the pair objective, split the deficit budget with explicit weights, or combine the valid bounds by a maximum/linear-programming allocation. This qualification is essential for a sound stronger global inequality.

There is a second allocation issue: even two-face pairs having disjoint center triangles can share an endpoint boundary center. Their full three-arc patch formulas would then count that center's outer contribution twice. For a complete partition into fans, assign full outer contributions to a fan's internal boundary centers and half to each of its two endpoints. For the two-face patch, subtract half of each endpoint contribution Hactual_i=theta_i/2-s_i*u_i dot c_i from (2). The resulting weighted patch is

\[
\frac{\theta_b}{2}+\frac{\theta_a+\theta_c}{4}
+\frac{\det(a,q_0)+\det(q_3,c)}2+w\cdot p
+\frac{s_a u_a\cdot a+s_c u_c\cdot c}{2}.
\]

The middle center still cancels. Across complete fans these endpoint/internal weights sum to exactly one for every boundary outer contribution. A proof using only one selected fan does not require this division, because it can reserve all three outer contributions for that one patch, but a sum over multiple fans must account for overlaps explicitly.

# New necessary graph conditions and a limitation of finite target certificates

## 0. Scope

Let D be the closed unit disk and let r_D(n) be its minimum covering radius using at most n congruent closed disks with arbitrary centers. Put

\[
U=11563027143/10^{11},\qquad R=113/1000.
\]

This extension does **not** establish r_D(100)=U, r_D(100)>R, or any exact optimal radius. It provides additional necessary conditions on hypothetical improvements and rules out one proposed form of exact-optimality certificate.

The foundation is the supplied earlier proof `disk100_continued_proof/previous/GLOBAL_LOWER_PROOF.md`, independently inspected in this investigation. The following established ingredients are used:

1. Centers may be projected into D. The covering radius is continuous and attains its minimum on D^n
2. A strict counterexample can be perturbed, with a sufficiently small increase of radius, to a generic cover; redundant disks can then be deleted
3. In a generic irredundant cover, each clipped Voronoi cell meets the boundary in at most one connected arc. The dual center graph is a disk triangulation with m vertices and B boundary edges, with F=2m-B-2 center triangles
4. Every center triangle has circumradius at most r; in particular every graph edge has length at most 2r
5. With A=3sqrt(3)/4 and kappa=461134488/10^9, joint center-triangle and anchor-triangle area is at most [(2m-B-2)A+B kappa]r^2

For r<1/2, a cell containing the origin cannot reach the boundary because its diameter is at most 2r<1. Thus B<=m-1. Generic and irredundant are auxiliary conditions, not restrictions imposed on the original optimization problem. Statements below about a specific graph refer to such an auxiliary graph.

## 1. The boundary function is concave for all 0<r<1

Define

\[
H_r(\theta)=\sin(\theta/2)\sqrt{r^2-\sin^2(\theta/2)}
                +(\theta-\sin\theta)/2,
\quad 0\le\theta\le2\arcsin r.
\]

The previous proof established concavity only for r<=1/5. In fact it is strictly concave throughout the open interval whenever 0<r<1.

Set x=sin(theta/2), t=r^2, u=x^2, and

\[
N=t^2+3t-(2+6t)u+4u^2.
\]

Direct differentiation gives

\[
H_r''(\theta)=x\left(\sqrt{1-u}-\frac{N}{4(t-u)^{3/2}}\right).
\]

For 0<=u<=t<1, the derivative of N with respect to u is at most 2t-2<0. Hence N>=t(1-t)>0. With v=u/t, the exact identity is

\[
N^2-16(t-u)^3(1-u)
=t^2(1-t)\{4(t+1)v^2-4(t+3)v+9-t\}.
\]

The expression in braces decreases on 0<=v<=1: its derivative at 1 is 4(t-1)<0 and its derivative is increasing. Its minimum on that interval is therefore its value at 1, namely 1-t>0. Both sides compared before squaring are nonnegative, so

\[
N>4(t-u)^{3/2}\sqrt{1-u}.
\]

Consequently H_r''<0 for 0<theta<2asin r. Continuity supplies concavity at the endpoints. The verifier independently expands the factorization using sparse integer polynomials and checks every coefficient.

## 2. The inherited area condition in the larger radius range

Let the B assigned boundary arcs have angles theta_i, summing to 2pi. Each theta_i<=2asin r. The established oriented-area argument gives

\[
\pi\le[(2m-B-2)A+B\kappa]r^2+\sum_{i=1}^B H_r(\theta_i).
\tag{1}
\]

By the new concavity lemma, this argument applies to every 0<r<1/2 while retaining B<=m-1. For at most n disks, let

\[
s_B=\sin(\pi/B),\quad c_B=\cos(\pi/B),\quad
\lambda_{nB}=\left(\frac{2n-2}{B}-1\right)A+\kappa.
\]

Every cover must satisfy, for some B in {3,...,n-1},

\[
s_B\le r,\qquad
E_{nB}(r)=\lambda_{nB}r^2+s_B\sqrt{r^2-s_B^2}-s_Bc_B\ge0.
\tag{2}
\]

This remains only a necessary condition. The verifier uses exact rational intervals to test all B. It never treats a positive value of E as evidence that a covering exists.

## 3. Graph-distance tails

Let d(v) be graph distance from a center vertex v to the boundary cycle. A boundary center has norm at least 1-r. Along a path of d edges, each edge has length at most 2r, so

\[
\|c_v\|\ge1-(2d+1)r.
\]

For d<k, the disk at c_v misses the open concentric disk of radius 1-2kr. Thus vertices with d>=k must cover that core. Since a finite union of closed disks is closed, they also cover its closure. Whenever 1-2kr>0, scaling yields

\[
r_D(N_k)\le\frac{r}{1-2kr},\qquad
N_k=\#\{v:d(v)\ge k\}.
\tag{3}
\]

The quotient on the right is increasing in r. At U, exact arithmetic verifies:

- 57 disks cannot cover D at U/(1-2U); all 54 boundary-count cases are excluded
- 29 disks cannot cover D at U/(1-4U)=11563027143/53747891428; all 26 cases are excluded, with tight B=18 and area margin greater than 687/10^6
- 10 disks cannot cover D at U/(1-6U)=11563027143/30621837142; all 7 cases are excluded, with tight B=9 and area margin greater than 49/3125
- 1-8U>0, so at least one vertex is needed beyond graph distance 3

Therefore a generic irredundant cover at radius at most U must obey

\[
\boxed{N_1\ge58,\quad N_2\ge30,\quad N_3\ge11,\quad N_4\ge1.}
\tag{4}
\]

These statements constrain actual graph layers, beyond the old pair (m,B). They do not enumerate those graphs or exclude every graph.

## 4. Concentrated boundary arcs have a certified area cost

Work now at r<=R=113/1000. Exact tests of (2) show that n=99 is impossible and that, for n=100, the only boundary counts not excluded are B=33,34,35. Thus m=100 for a generic irredundant cover at this radius.

Suppose some K consecutive assigned arcs have total angle S<=L, where L<2Kpi/B. Concavity gives

\[
\sum_i H_R(\theta_i)
\le K H_R(S/K)+(B-K)H_R((2\pi-S)/(B-K)).
\]

The right-hand side increases with S below 2Kpi/B: its derivative is H_R'(S/K)-H_R'((2pi-S)/(B-K))>=0. Provided both arguments remain in H's domain, it is therefore at most

\[
K H_R(L/K)+(B-K)H_R((2\pi-L)/(B-K)).
\tag{5}
\]

If a proposed smaller S makes the second argument leave the domain, that S is already impossible because the remaining arcs could not total 2pi-S. Thus no feasible case is lost by this domain qualification.

The exact verifier checks all stated domain conditions and the following strict inequalities after adding the center/anchor term in (1):

- K=3, L=456/1000, for each B=33,34,35: the resulting total area is below pi by more than 1/2000
- B=33, K=4, L=692/1000: the resulting total area is below pi by more than 9/10000
- B=34 or 35, K=5, L=692/1000: the resulting total area is below pi by more than 9/10000

The first family means that no three consecutive assigned arcs can total at most .456. The second family similarly prohibits the indicated four- or five-arc concentration.

These are exact interval calculations, not floating-point sign tests. For example, sin(.228)>.226 and sin(.346)>.339 are established using rational Taylor lower bounds. Hence

\[
2\arcsin(2R)<.456,\qquad2\arcsin(3R)<.692.
\tag{6}
\]

## 5. Chordless boundary cycle and short boundary fans

If two graph vertices have graph distance d, their centers are at distance at most 2dr. Their two radius-r disks fit inside the disk centered at their midpoint with radius (d+1)r. Consequently both of their complete assigned boundary arcs fit in that larger disk.

A disk of radius a<1 meets the unit circle in an arc of angular length at most 2asin a. Its footprint is connected and shorter than pi. If the two chosen boundary vertices have cyclic boundary distance p, the containing footprint includes a consecutive block of at least p+1 whole assigned arcs, where p is the smaller of the two cyclic distances.

### 5.1 No boundary chords

For a graph edge d=1. If its endpoints were nonconsecutive boundary vertices, the containing footprint would include at least three consecutive assigned arcs with total angle at most 2asin(2r)<.456. Section 4 excludes this. Therefore the boundary cycle has no chords.

In particular, every triangle incident to a boundary edge has exactly one boundary edge and an interior third vertex. A triangle with two boundary edges is an ear and is excluded. A non-boundary triangle has at most one boundary vertex, because two such vertices would either form a forbidden chord or a boundary edge.

### 5.2 Boundary neighbors of one interior vertex

Two boundary vertices adjacent to the same interior vertex have graph distance at most 2. Their containing radius-3r disk has boundary footprint shorter than .692.

For B=33, Section 4 excludes four consecutive arcs in such a footprint. The two boundary vertices must therefore have cyclic distance at most 2. For B=34 or 35, their cyclic distance is at most 3.

When B>4q, a collection of boundary indices with pairwise cyclic distance at most q lies in one cyclic interval of q edges. To see this, fix one index: all others lie within q steps on either side. If both sides occur, the sum of the two extreme distances is at most 2q<B/2, so their pairwise cyclic distance is that sum and must be at most q. Thus the full set lies in a single interval of q edges. The required hypothesis holds here because B>=33 and q<=3.

Accordingly every interior vertex has at most 3 boundary neighbors for B=33, or at most 4 for B=34,35.

### 5.3 Fan and interface counts

Join two boundary triangles when they share a non-boundary edge. Every boundary triangle has two such edges, so each component is a path or cycle. Adjacent boundary triangles have the same interior apex, because their shared edge joins that apex to a boundary vertex. Thus an entire component has a common apex.

A cycle component would run around that apex and use the entire boundary cycle; this is impossible with at most 3 or 4 boundary neighbors. Hence the components are paths, or fans. Their lengths are at most 2 for B=33, or at most 3 for B=34,35.

There are exactly B boundary triangles. Hence the numbers of fan components are at least 17,12,12 respectively. Each fan has exactly two terminal non-boundary edges. The adjacent face across each is not a boundary triangle, since otherwise it would belong to the same component. These edges are distinct across fans, giving

\[
\boxed{\text{boundary/non-boundary interface edges}\ge34,24,24
\quad\text{for }B=33,34,35.}
\tag{7}
\]

Every non-boundary triangle has at most one boundary vertex, and therefore at most two such interface edges. These observations can support a future shared-edge area-deficit argument, but that argument is not supplied here.

## 6. Generic perturbations and the endpoint caveat

The graph statements above hold directly for generic irredundant covers at the stated thresholds. If an arbitrary cover has radius strictly below a threshold, the original small-perturbation argument produces a generic cover that remains below the threshold, to which the restrictions apply.

For a cover exactly at a threshold, perturbation may increase the radius. The finite numerical exclusions in this file have strict margins, so they continue to hold in some neighborhood above that threshold; a finite-type subsequence or an explicitly certified slightly larger rational threshold can be used when an endpoint argument is needed. This document does not silently identify the graph of a degenerate original cover with the graph of its perturbation.

Most importantly, these necessary conditions still leave possible graphs and continuous realizations. No conclusion r_D(100)>R follows merely from Sections 4 and 5.

## 7. No fixed finite target set certifies the exact optimum

**Proposition.** Suppose 0<r_D(n)<1. For every finite S contained in D, its minimum covering radius by n disks is strictly less than r_D(n).

**Proof.** Choose an optimal full-disk configuration C and write r*=r_D(n). Its worst-point set

\[
W=\{x\in D:\min_i\|x-c_i\|=r_*\}
\]

is finite. An interior worst point cannot have only one nearest distinct center, since the squared distance is locally strictly convex. If it has exactly two nearest centers, restrict to their perpendicular bisector: the squared distance is again strictly convex. Thus every interior worst point is a circumcenter of three distinct noncollinear centers; there are finitely many such candidates. Every boundary worst point lies in the intersection of the unit circle with one radius-r* covering circle. Each such intersection has at most two points, because r*<1 rules out coincident circles. Hence W is finite.

Rotate C about the origin. The full disk and its covering radius are unchanged, while W rotates with C. Avoid the finitely many rotations that send a nonzero point of W to a point of S. All nonzero points of S then have strictly positive covering slack.

If the origin is absent from S, or is already strictly covered, finiteness of S permits a strict decrease of the radius. Otherwise choose a center at distance r*>0 from the origin and move it a sufficiently small positive distance epsilon toward the origin. The origin then has distance at most r*-epsilon to that center. The minimum positive slack at the other finitely many sample points is preserved by choosing epsilon smaller than half of it, using the Lipschitz bound for moving a center. Again the common radius can be strictly decreased while covering S. The one-point set consisting only of the origin is immediate. This proves the proposition.

The consequence is specific: one fixed finite spatial sample, even with an exact set-cover infeasibility solver, cannot establish the exact full-disk optimum. It can establish rational lower bounds below that optimum. An infinite parameterized family, geometric inequalities, or symbolic elimination can still support an exact proof.

This does not conflict with the finite critical-point theorem for certifying one given configuration. That critical set depends on the configuration; it is not one target set that constrains all possible configurations.

## 8. Verification and remaining gap

`verify_extension.py` contains a standalone rational backend: Machin's identity and alternating arctangent series for pi, Taylor remainders for sine and cosine, and integer-square-root checks for radicals. Every acceptance comparison is exact. It rechecks the joint-triangle constants, the concavity factorization, every claimed boundary-count exclusion, and the concentrated-arc margins.

The script was run successfully in this investigation. No earlier proof artifact was modified.

Still missing are an exact optimal-radius integer polynomial and isolating interval, algebraic coordinates of a globally optimal construction, and a proof excluding every smaller radius. The old certified upper construction and all new restrictions remain compatible with a nonzero optimality gap.

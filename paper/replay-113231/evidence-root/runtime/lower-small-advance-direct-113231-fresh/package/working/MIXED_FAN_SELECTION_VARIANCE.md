# Selecting q3/q4 footprint cells with controlled overlap

Assume the boundary cycle has B cells, every ordinary marked edge belongs to one interior apex, and the boundary-neighbor window of each apex has at most five consecutive cells. Select n3 apices with three ordinary marked incidences and n4 apices with four. Put N=n3+n4 and W=4n3+5n4.

For each selected q3 apex one can choose exactly four of its endpoint cells, and for each q4 apex all five, so that no cell is selected more than twice and at most N cells are selected twice. If w_i is the resulting membership count,

`sum w_i=W`, `w_i in {0,1,2}`, `sum w_i^2<=W+2N`.

This does not assume different footprints are disjoint.

## Boundary runs and the selection

A q4 apex occupies all four edges of its five-cell window, so it is one four-edge fan. A q3 apex either is one three-edge fan on four cells, or occupies three of four consecutive edges on five cells. In the latter case it has two runs separated by one internal gap edge. Call it split, and let s count split selected q3 apices.

Color each marked edge of a selected apex by that apex, and color all other boundary edges unselected. There are N+s colored runs. If c counts unselected-edge components, the initial number of cells shared by two different selected apices is `T0=N+s-c`; for full selected coverage use c=0. This follows by counting the two endpoints of every colored run. Initial membership count is W+s. Each boundary cell belongs to at most two selected apices, the colors of its incident cycle edges.

A split apex whose gap edge is unselected has a singleton unselected component. Distinct such gaps are distinct components, because the two neighboring edges determine the apex. Thus their number s_bad is at most c. For each such split, omit one of its two unshared gap-endpoint cells.

Every other split has a gap edge colored by another selected apex. Its two gap-endpoint cells are shared and give two choices for omission. In the bipartite incidence graph between these split apices and their candidate cells, each left vertex has degree two and every right vertex degree at most two. For any set of left vertices, counting incidences gives at least as many neighboring cells. Hall's theorem therefore supplies a matching to distinct shared cells. Omit the matched cell from each corresponding split apex's group.

All split groups now have four cells, and all other groups keep their required sizes. Each matched shared cell ceases to be double-counted; unmatched deletions cannot increase overlap. The final number of double-counted cells is at most

`T0-(s-s_bad)=N+s_bad-c<=N`.

This proves the selection statement. Every chosen set remains a subset of its original apex footprint.

## A single global variance inequality

Suppose each selected apex's complete footprint has full-arc span at most L. Let a_i be half-arcs, sum a_i=pi, and mu=pi/B. Each chosen group has half-arc sum at most L/2. Thus

`sum w_i*(a_i-mu)<=NL/2-W*mu`.

When `D=W*mu-NL/2>0`, centered Cauchy gives

`D^2 <= [sum w_i^2-W^2/B]*sum(a_i-mu)^2`.

If `W+2N-W^2/B>0`, the controlled-overlap bound yields

`sum(a_i-mu)^2 >= D^2/[W+2N-W^2/B]`.

If that denominator is nonpositive while D>0, the hypotheses themselves are impossible. N=0 has the trivial zero variance bound.

This is one global variance budget. It may be combined with another independently valid variance lower bound by taking their maximum, not by adding them. For example, an existing q4 endpoint-union bound and a single q3 group/complement bound can strengthen individual count cases without double charging.

The radius-specific footprint, no-bad-marked-apex, q<=4 and q4-count restrictions are separate geometric prerequisites. The selection theorem itself is purely combinatorial. It also permits boundary ears among the unselected edges.

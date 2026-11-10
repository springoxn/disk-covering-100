# Charging every p3 fan through one global arc variance

Assume B33, every interior apex has at most three good marked faces, and
no interior vertex has five boundary neighbors. The latter follows from
the exact K5 radius3r footprint test in the current covering reductions.
Let k be the number of p3 interior apices. A radius3r footprint gives each
such apex four complete assigned arcs with half-angle total at most L/2.
Put D=4pi/33-L/2>0 and a0=pi/33.

Then the complete half-arc variance satisfies

sum_i(a_i-a0)^2 >= (33/133)*D^2*k.

This is a **single global variance charge**. It may be assigned linearly
to the p3 star count, but must not be added to an independent full variance
charge using the same budget.

## Contiguous fan blocks

Three distinct boundary-cycle edges have at least five distinct vertices
unless they form one contiguous three-edge path (B33 rules out a cycle of
three edges). All neighbors of a p3 apex have their covering disks in its
radius3r disk. Five sites would contradict the K5 footprint restriction.
Thus every p3 apex has one contiguous three-edge marked fan, with four
consecutive boundary sites. Distinct apices have disjoint marked edges.
Their four-site blocks can overlap only at a shared endpoint when the two
three-edge blocks are adjacent.

Assign each site a weight w_i equal to the number of these four-site blocks
containing it. Then w_i is0,1 or2, sum w_i=4k and sum w_i^2=4k+2c, where
c is the number of adjacent pairs of fan blocks. There are at most k-1
such adjacencies if their edges do not cover the whole boundary cycle.
For k<=10 this gives sum w_i^2<=6k-2. The exceptional k11 case uses all33
edges, has c11 and sum w_i^2=66. An ear creates extra gaps, so it cannot
increase this overlap bound; with an ear k<=10.

## Weighted Cauchy

Let d_i=a_i-a0. Since sum d_i=0, and every fan block has deviation sum at
most-D,

sum_i(w_i-4k/33)d_i <= -kD.

Cauchy yields

sum d_i^2 >= k^2 D^2/(sum w_i^2-16k^2/33).

For k1 through10 the right side per fan is at least

D^2/[6-2/k-16k/33].

The denominator is at most133/33 for every integer k. Equivalently
16k^2-65k+66=(16k-33)(k-2)>=0 for integer k; its only negative interval
lies strictly between2 and33/16 and contains no integer. Equality occurs
at k2. For k11 the per-fan coefficient is3/2, also above33/133. The k0
case is trivial. All integer comparisons and denominator signs are
replayed by verify_multiple_p3_footprint_variance.py.

An actual configuration has integer k. After deriving this bound, subtracting
a constant per p3 type in a continuous LP remains safe: the LP merely
relaxes the actual integer star multiplicities. No geometric claim about
fractional fans is made.

## General form

If a maximal p=q fan is forced to be a contiguous q-edge block, its q+1
site weights satisfy sum w=(q+1)k and sum w^2<=(q+3)k-2 while a gap remains.
The analogous per-fan coefficient is the reciprocal of the largest integer
value of(q+3)-2/k-(q+1)^2*k/B, with the whole-cycle case checked separately.
Applying this generalization requires the corresponding geometry and
contiguity proof; it is not automatically inherited at a new radius.

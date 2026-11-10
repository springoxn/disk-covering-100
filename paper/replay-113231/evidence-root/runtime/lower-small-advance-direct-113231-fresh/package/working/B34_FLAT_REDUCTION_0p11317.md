# Conditional B34 profile reduction at radius 0.11317

This is a necessary-profile theorem, not a new universal lower bound and not
an exclusion of the surviving graphs. The executable is
`verify_B34_flat_reduction_0p11317.py`. All acceptance arithmetic is exact.

Assume 100 congruent radius-r disks cover the closed unit disk, where
r <= 11317/100000, and the limiting generic diagram has B=34 boundary cells.
The fresh 99-center exclusion forces m=100. The same-radius four-arc cluster
test, with span 0.4567 and containing-radius factor 2, excludes every q0 or
q1 center triangle with three boundary vertices. A six-arc test with span
0.693 and factor 3 gives marked incidence q<=4. The endpoint-union bound
gives at most five q4 vertices. Ears, boundary chords, and split fans are
allowed in this argument.

Write e for the number of q2 ears, U for the number of q0 boundary-angle
occurrences, and M=U-2e. There are 66 interior vertices. The full-domain
face supports, terminal BI credits, and mixed-fan Hall selection theorem
are precisely the independently audited .11315 components. Their complete
exact replay is part of this verifier. Only their radius-independent
rational coefficients are reused. The boundary baseline, one global
half-arc variance coefficient .29, Jensen-slab ear cap, and integer fan
budget are checked again at the new radius.

## 1. The complete remaining M list

For each proposal row, let c be its U coefficient and E its ear
coefficient. Direct substitution gives

    G(U) + e E = G(M) + e(E+2c).

Every E+2c is strictly negative. The general core-obstruction theorem in
`UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md` says that M<=25 forces an
unmarked interior vertex of degree 3, 4, or 5. Subtract the minimum exact
reduced cost of those three types once. The three rows exclude M<=23,
M=24, and M=25 respectively. The last row has negative M slope and
excludes all M>=28 without using that obstruction. Therefore M is 26 or27.

For each of those two values, the cost of a single ear, namely -(E+2c),
is larger than the entire remaining normalized area surplus. Hence e=0,
and U=M. These deductions do not assume an ear-free graph in advance.

## 2. Interior degrees and marked incidences

For every admissible vertex type q=0,...,4 and d=max(3,q+1),...,99,
the verifier recomputes the exact nonnegative slack between the affine
vertex majorant and its local score. At either remaining M value, each
of the following minimum slacks exceeds the total area surplus:

* every type with degree at most 5;
* every type with degree at least 8;
* the unmarked type (q,d)=(0,7).

Thus every interior degree is 6 or7, and every degree-seven vertex is
marked. The Euler/angle-incidence identity gives

    sum(d-6) = B-6+e-U = 28-M.

There are exactly two degree-seven vertices when M=26, and exactly one
when M=27. The marked-edge identity is sum q =34. The number of vertices
with positive q is at most U, by the terminal-edge incidence argument.

## 3. Finite integer profile refinement

Let the sorted list Q record the marked incidences of the degree-seven
vertices, and let c_q count degree-six vertices with marked incidence q.
The checker exhausts all nonnegative integer solutions of

    sum c_q = 66 - len(Q),
    sum q c_q + sum Q =34,
    66-c_0 <= M,
    n3=c_3+count_Q(3),  n4=c_4+count_Q(4),
    n4<=5,  3 n3+4 n4<=34.

For each profile it subtracts the sum of its individual vertex slacks
and uses its own exact mixed-fan variance budget, instead of the maximum
over all fan counts. The .29 variance term is used exactly once.

The surviving degree-seven marked-incidence lists are:

* M=26: (2,3), (3,3), (3,4), or (4,4), with 182 integer profiles in total.
  No degree-six vertex has q=4;
* M=27: (3), with 57 integer profiles in total. Every surviving profile
  has c_4=0, so no q4 vertex occurs in this branch.

The result JSON lists every profile. This is exhaustive for the necessary
integer relaxation; it does not say each listed profile has a geometric
realization.

## 4. What remains

The core identities now give useful candidates for a further geometric
reduction: perimeter26 with104 triangular faces, or perimeter27 with103
faces. Turning these into a complete metric exclusion requires the
separate planar block, development, enumeration, and geometric-support
arguments. They are not asserted by this executable. In particular the
status PASS means the stated reduction passed, not that radius .11317
has been globally excluded.

As in the earlier certificates, nongeneric diagrams are handled by the
constant finite-type limiting argument. All strict exclusion margins are
preserved by continuity.

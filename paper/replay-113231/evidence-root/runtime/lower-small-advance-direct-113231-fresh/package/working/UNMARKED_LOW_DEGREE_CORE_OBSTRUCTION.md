# A compulsory low-degree unmarked star in small-U branches

Let a simple straight center triangulation have m>B vertices, B>=4 outer
boundary vertices, e q2 ears, and U q0 boundary-angle occurrences. Here q0
means an unmarked face, and an interior vertex has p marked incidences if
it is the interior apex of p ordinary q1 faces. All-boundary q0 or q1 faces,
boundary chords, disconnected induced cores, and bridges are allowed.

If every interior vertex with p=0 has degree at least six, then

    2m-2B-2+e-U <= U^2/6.                 (1)

For m=100 and B=32,33 or34, (1) excludes every U<=25. Thus such a branch
must contain an interior vertex with p=0 and degree at most five. In a
simple triangulation the possible low degrees are3,4,5. If an independent
minimum-degree-five theorem is available, this is exactly the necessary
integer constraint `x_(p=0,d=5)>=1`.

## 1. Removing the outer vertices

The center triangulation has 2m-B-2 faces. Since each marked boundary edge
belongs to one face, the total q1 count is B-2e and the q0 count is

    F_q0=2m-2B-2+e.

This identity includes bad all-boundary q1 faces; they do not alter it.
There is no q3 face when B>=4.

Let n_j count q0 faces with j boundary vertices, j=0,1,2,3. Then

    U=n1+2n2+3n3,
    F_core=n0=2m-2B-2+e-U+n2+2n3.

Delete all outer boundary vertices and incident edges. Every bounded face
of the induced interior graph is one of the original n0 triangles. Indeed
an original outer boundary vertex cannot lie inside a cycle of interior
vertices in the planar disk, and any bounded region inside such a cycle
was already completely triangulated. Thus no untriangulated bounded hole
is created.

The total length of the outer facial walks, counting a bridge twice, is
exactly n1. To see this, each q0 face with one boundary vertex has one II
edge opposite it. An II edge with one core incident face contributes once
to the exterior walk; an II edge with no core incident face is a bridge
and contributes twice. The neighboring removed faces in those cases are
respectively one or two q0-B1 faces. Faces with two or three boundary
vertices and marked faces have no II edge. Hence the total walk length is

    b=n1<=U.                               (2)

Isolated interior vertices contribute zero to both b and the core face
count and cause no exception.

## 2. Face-bearing blocks retain the needed degrees

Split the induced interior graph at cut vertices and bridges. Every
face-bearing block is a triangulated disk with a simple outer boundary.
A vertex strictly inside that block cannot have an edge to an original
boundary vertex: such an edge would cross the block's outer cycle. Nor
can it have an edge to an interior vertex outside the block. Consequently
its degree in the block is its complete original degree, and it has p=0.
Under the hypothesis, all strict block-interior degrees are at least six.

Apply the independently proved GENERAL_DISK_ISOPERIMETRY.md to every
face-bearing block. If its boundary length is b_j, it has at most b_j^2/6
triangles. The block boundaries use at most the total exterior walk length
b; bridges consume walk length without supplying any faces. Therefore

    F_core<=sum b_j^2/6 <= b^2/6 <= U^2/6.

Combining this with the exact face count proves (1). This is combinatorial
isoperimetry, independent of actual Euclidean triangle shapes or areas.

## 3. Integer consequences and exact reduced costs

At m=100, B32/33/34 and U<=25, even the e=0 lower bound gives

    6*(2m-2B-2-U)-U^2 >= 29,17,5,

respectively. The expression decreases with U>=0, so these endpoint
checks exclude every smaller U as well. For B35 through B38, the same
argument excludes U<=24, with respective integer margins48,36,24,12.

An angular or face-label LP may exploit this necessary low-degree star by
adding the constraint that at least one (p=0,d=3,4,5) type occurs. Equivalently,
an exact dual may subtract the minimum positive reduced-cost slack over
those types once. This is legitimate only if the corresponding support
inequalities and the remaining total surplus are checked exactly. It does
not authorize subtracting a face deficit again outside that dual's own
nonnegative slack decomposition.

## 4. The shifted form also permits all-boundary faces

Write I=m-B>0, and let c>=1 be the number of components of the induced
interior graph, including isolated vertices. Let E be its number of edges.
Because all its bounded faces are the actual core triangles, Euler and
face-edge incidence give

    F_core=E-I+c,  2E=3F_core+n1.

Substitute the exact expressions from section1 for F_core and n1. The
resulting identity is

    n2+n3=e+2(c-1).

Therefore with M=U-2e,

    b=n1=M-4(c-1)-n3<=M,
    F_core=2I-2-M+2(c-1)+n3>=2I-2-M.

The assumption I>0 is essential for c>=1. No all-boundary face exclusion
is needed. Consequently (1) strengthens to

    2m-2B-2-M <= M^2/6.

For m=100 and B32/33/34, M<=25 therefore forces a p=0 vertex of degree
at most five. In particular, at B33 with the established minimum degree
five, every U<=25+2e branch must contain a (p=0,d=5) star. Both the
unshifted and shifted forms permit all-boundary q0 and q1 faces, boundary
chords, disconnected cores and bridges. The special n3=0 case agrees
with the previously audited identities in CORE_CUT_ISOPERIMETRY.md.

`verify_unmarked_low_degree_core_obstruction.py` checks the exact integer
consequences. Neither this lemma nor its checker is a new covering-radius
exclusion without the companion metric/angular score certificates.

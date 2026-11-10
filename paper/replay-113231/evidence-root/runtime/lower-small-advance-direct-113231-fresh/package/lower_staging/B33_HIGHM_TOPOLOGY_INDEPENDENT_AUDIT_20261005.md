# Independent audit: B33 high-M topology and complete face counts

## Verdict and scope

PASS. The radius-independent combinatorial arguments in
B33_HIGHM_METRIC_0p11323.md and
N27_METRIC_CHORD_CASES_0p11322.md are valid under their stated global
degree premises. This audit checks topology, face-pattern completeness,
incidences, and the centered-angle bookkeeping. It does not duplicate
the independently accepted local metric support calculations or establish
a standalone covering-radius exclusion.

The /6 disk theorem and induced-core identities used here are the files
in ../working/lower_bounds_extension_20261004/GENERAL_DISK_ISOPERIMETRY.md
and ../working/UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md.

## 1. Four high-M profiles

Once the preceding metric argument excludes every global interior
degree-five vertex and the established degree window excludes smaller
degrees, all 67 global interior degrees are at least six. The identity

    sum(d-6) = 27-M-e-bad

with M>=26 leaves exactly four possibilities:

    M26,e0,bad0: one degree seven, all others six;
    M26,e1,bad0: all degrees six;
    M26,e0,bad1: all degrees six;
    M27,e0,bad0: all degrees six.

The minimum-degree argument is a separate dependency, not an assumption
silently recovered from the present topology.

## 2. Connected interior plus no original ear forbids a BC chord

Here BC means an original outer-boundary vertex. Any BC chord separates
the disk into two subdisks whose boundary is that chord and one original
boundary arc. Its endpoints are not in the induced interior graph. A
path in that induced graph cannot cross the chord, so connectedness puts
every interior vertex on the same side. The other side has no interior
vertices and is a triangulated polygon.

Such a polygon has an ear away from the two endpoints of the distinguished
base chord. A precise proof is to root its triangle-dual tree at the face
incident to the base: if the polygon has more than one triangle, a leaf
other than the root is an ear face using two polygon boundary edges,
neither being the base. If it has one triangle, its third vertex is the
required ear. In both cases the ear tip is a non-endpoint of the base.

The two ear edges are original boundary edges. Its tip has no edge to
the other side of the base and has degree two in the whole triangulated
disk. Thus this is an original q2 ear. Therefore connected induced
interior graph and e=0 imply no BC chord.

For M26,e0, the general identities and /6 bound force one component and
n2=n3=0: if there were q>=2 components, the total frontier would be at
most22 and the core would have at least108 faces, contradicting
108>22^2/6. With q=1, n2+n3=e+2(q-1)=0. A bad q1 triangle has all three
vertices BC and exactly one original boundary edge, so it has BC chords.
Consequently the M26,e0,bad1 profile is impossible. This argument is
purely topological and spends no area or hinge charge.

## 3. The all-six M26,e1 profile

For q induced-interior components, the exact identities are

    frontier=26-4(q-1)-n3,
    Fcore=106+2(q-1)+n3,
    n2+n3=1+2(q-1).

As above q>=2 is impossible, so q=1 and n2+n3=1. If n3=1, then
frontier25 and Fcore107 contradict 107>25^2/6. Hence

    n2=1, n3=0, frontier26, Fcore106.

Every strict face-block interior vertex retains its global degree six.
A bridge consumes two units of frontier and implies Fcore<=24^2/6<106.
At least two cyclic blocks give Fcore<=(3^2+23^2)/6<106. Thus the core is
one simple disk. A core boundary chord would split it into perimeters
at least three summing28, giving

    Fcore<=(3^2+25^2)/6=317/3<106.

The core is chordless and has 67-26=41 strict deep vertices, each of
degree six. No flat development or graph catalog is needed.

### The exact five q0 patterns

Write D for a deep vertex, R for a core-boundary vertex, and B for an
original BC vertex. Each of the26 core-boundary edges has a core triangle
DRR. Its third vertex cannot be R because that would require a chord
(or make the entire disk a triangle). A single DRR triangle contains
exactly one core-boundary edge, so these26 triangles are distinct.
Every other core triangle is DDD or DDR. If their counts are x,y, then

    x+y=106-26=80,
    3x+2y+26=41*6=246.

Therefore x=60 and y=20. Exactly n1=26 outer q0 triangles have one B
vertex and one exposed core edge, so all are BRR. Exactly n2=1 q0
triangle has two B vertices; its third vertex must be R, since a deep
vertex has no original boundary neighbor. It is BBR. Since n3=0, there
are no other q0 patterns. The full count is

    DDD60, DDR20, DRR26, BRR26, BBR1,
    total133=2*100-2*33-2+e.

There are33-2e-bad=31 ordinary q1 triangles and one q2 ear. In the full
triangulation the count of triangles with exactly two B vertices is
T2=31+1=32, and the count with three B vertices is T3=1. If C counts
original BC chords, boundary-edge incidence gives

    33+2C=T2+3T3=35,

so C=1. This is the edge opposite the unique ear tip. The unique BBR
q0 triangle contains a BC chord and is therefore exactly the triangle
across that ear chord. This proves the adjacency claim, not just its
numerical face count.

There are precisely26 core/outer shared edges. The opposite signed
edge terms pair the26 DRR triangles with the26 BRR triangles. BBR has
no II edge, so requires no missing signed partner. The marked-edge
count is31+2=33, matching the boundary envelope's33 terms.
The q0 B-incidence count is26+2=28=U. As an additional degree check,
the ring has72 core corners,52 BRR corners, one BBR corner, and31
ordinary marked apex corners, totaling156=26*6.

## 4. The all-six M27 core has at most two chords

The identities and /6 inequalities in N27_METRIC_CHORD_CASES_0p11322.md
correctly give one simple P27/F105 core with40 strict deep vertices and
no bridges. Specifically q>=2 gives107>23^2/6; a bridge gives105>25^2/6;
and two cyclic blocks give105>(3^2+24^2)/6. With q=1,e=0,
n2=n3=0. The BC-chord lemma in section2 also applies.

Consider a chord in the current core after t ear deletions. The current
parameters are P=27-t,F=105-t, and the same40 deep vertices retain their
full degree-six stars. If the chord had deep vertices on both sides,
each side would have perimeter at least six. This follows from the
small-boundary case of the /6 disk theorem: a disk with all strict
interior degrees at least six and perimeter at most five has no strict
interior vertex. The two side perimeters sum29-t. Therefore

    F <= [6^2+(23-t)^2]/6 < 105-t,

for each t=0,1,2. Thus each current chord has an empty side with no deep
vertices. The distinguished-base polygon lemma in section2 supplies
an ear at a non-endpoint of that chord.

Its tip is a current boundary vertex of degree two in the whole current
disk; its two neighbors are boundary vertices. Deleting it removes one
vertex and one triangle, and turns its opposite chord into a boundary
edge. No other chord is removed or changes boundary status: no chord
is incident to the degree-two tip, and the only new consecutive pair
on the boundary is its two neighbors. Thus the chord count decreases
by exactly one. No deep vertex becomes boundary, and no deep degree
changes because the deleted tip has only boundary neighbors.

If the starting core had at least three chords, this procedure could
be applied for t=0,1,2. It would leave P24/F102 with all40 strict deep
vertices still degree six, contradicting102>24^2/6=96. Hence the original
core has at most two chords. This reasoning does not assume all chords
were initially disjoint ear chords; nested empty-side triangulations
are handled by the successive deletion argument.

### Exhaustive patterns and incidences

A core triangle with j ring vertices has exactly binomial(j,2)
ring-ring edges. Its k core-boundary edges are among them; the others
are core chords, so h=binomial(j,2)-k. At most two distinct core chords
exclude (j,k)=(3,0). The case(3,3) would make the entire outer boundary
a triangle, impossible for P27. The exhaustive core patterns are

    (j,k)=(0,0),(1,0),(2,1),(2,0),(3,2),(3,1).

There are105 core faces, 40*6=240 deep incidences, and therefore
315-240=75 ring incidences. Core-boundary incidences total27 and core-
chord incidences total twice the number of chords. The27 remaining
outer q0 triangles are BRR, with one positive shared-edge term each.
Every one of the33 ordinary marked apices is R. Thus the seven local
metric patterns and all aggregate multipliers are complete.

## 5. Centered-angle bookkeeping in the two all-six profiles

Every global interior degree is six, so its full centered-angle sum is
2pi-6*pi/3=0. The global triangulation has165 faces, hence495 corners.
The67 interior vertices contribute402 corners, leaving93 B corners.
Their angles sum(33-2)pi=31pi, so their centered-angle sum also vanishes.
Accordingly the full global centered potential is zero for the constant
labels D0,R=L,B=Blabel.

An ordinary q1 triangle with apex angle alpha has centered potential
(L-Blabel)*(alpha-pi/3). An all-B ear has centered potential zero.
Combining the q0 potential with the q1 conjugates therefore leaves
-Q1*(L-Blabel)*pi/3. For the one-ear case Q1=31 this is

    -31*L*pi/3 + Blabel*(pi+28*pi/3).

For M27, Q1=33 and the same identity gives

    -33*L*pi/3 + Blabel*(2*pi+27*pi/3).

Both stated corrections are exact. Neither suppresses a potential
contribution from the one BBR face or adds a second ear/edge charge.

## Independent finite receipt

verify_B33_highM_topology_independent_20261005.py uses only exact Python
integers and fractions. It checks the profile list, induced-core integer
possibilities, all isoperimetric comparisons, one-ear face counts, the
six-pattern list, centered-angle coefficients, and the rooted polygon
ear/deletion statement on all polygon triangulations through size nine.
For the latter test, each polygon is glued along every possible base
edge to a six-wheel; the checked ear deletions preserve the wheel's
strict degree-six vertex and reduce the full disk's chord count by one.
These finite tests support the general proofs above rather than replace
them. No numerical metric support is replayed by this audit.

The exact checker passed. Its polygon test covered625 triangulations,
5,331 choices of distinguished base edge, and10,983 valid full-disk ear
deletions. The narrowest structural inequalities have strict margins
1/3 (the P26 chord exclusion) and5/6 (the P27 bridge exclusion).

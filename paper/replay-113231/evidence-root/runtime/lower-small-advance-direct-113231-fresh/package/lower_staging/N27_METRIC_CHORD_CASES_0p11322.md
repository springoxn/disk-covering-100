# The all-six M27 profile has at most two core chords

Assume the normalized B33 high-M reduction: m100, no ears or bad q1,
M27, and all67 original interior vertices have degree6. The induced-core
identities give

 b=27-4(c-1)-n3, F=105+2(c-1)+n3, n2+n3=2(c-1).

For c>=2, the blockwise /6 inequality gives107<=23²/6, impossible. Thus
c1,n2=n3=0. A bridge would leave at most25 face-block perimeter, but
105>25²/6. Multiple cyclic blocks give at most(3²+24²)/6 faces. Therefore
the core is one simple P27/F105 disk, containing exactly40 strict deep
vertices, each of degree6. The original outer boundary is chordless for
the same reason as in the M26 proof: no adjacent face type with a boundary
chord remains.

## Chord bound by deleting empty-side ears

In a triangulated disk whose strict interior degrees are at least6, a
subdisk with at least one strict interior vertex has boundary length at
least6. If a core chord had strict interior vertices on both sides, the
two side perimeters would both be at least6 and sum P+2. After t previous
ear deletions, P=27-t and F=105-t. For t=0,1,2, the maximum /6 bound over
such splits is [6²+(23-t)²]/6, always smaller than105-t.

Consequently every remaining chord has a side with no deep vertices.
That side is a triangulated polygon, which has an ear at a vertex other
than the two chord endpoints. Deleting such an ear removes exactly one
boundary vertex and one face, and turns its opposite chord into a boundary
edge. It preserves every one of the40 deep vertices and their degrees.
Every deletion reduces the number of core chords by exactly one. If there
were at least three chords, three deletions would leave a disk with
P24,F102, contradicting102<=24²/6. Hence the original core has c=0,1,or2
chords. No flat development or enumeration is used.

## Seven exact local metric supports

Give deep vertices label0, all27 ring vertices label L=-13/100, and
original BC vertices label B=-14/25. Put -tau*rho*sin(alpha), tau=49/100,
opposite every core-boundary edge in its core triangle, and the positive
matching term opposite that edge in the outer ring triangle. These27
pairs cancel as signed edge lengths divided by2R.

For a core triangle let j be its number of ring vertices and k its number
of core-boundary edges. Its number of core-chord incidences is
h=binomial(j,2)-k. With at most two chords, the exhaustive possibilities
are (j,k)=(0,0),(1,0),(2,1),(2,0),(3,2),(3,1). The case(3,0) would need
three distinct core chords; (3,3) would make the entire core one triangle.
The outer ring has the seventh pattern BLL with one positive edge term.

The exact full-simplex support checks all angle-boundary caps and the
range-plus-negative-edge localization guard; its minimum guard is51/100.
Each core face is bounded by A+u+j*r+k*b+h*c. Their exact aggregate counts
are105 faces,75 ring incidences,27 boundary-edge incidences, and2c chord
incidences. The40 deep degree-six vertices contribute240 incidences,
so75=315-240 does not assume any particular arrangement of ring degrees.

All33 marked apices lie on the core boundary and share label L. Summing
centered corner potentials gives the correction

    -33*L*pi/3 + B*(2pi+27pi/3).

The marked contribution is33*C_k(L-B), with linear halfside multiplier
k=11/25. Add the independently verified normalized boundary envelope at
this same k. No hinge deficit is spent in this final metric inequality.

verify_N27_metric_chord_cases_0p11322.py checks the six core patterns, the
outer-ring pattern, and all c=0,1,2 cases. Its minimum area margin is
675506006906614092373/(125000000000000000000000)>.00540404. Thus this
last high-M profile is impossible at R=5661/50000.

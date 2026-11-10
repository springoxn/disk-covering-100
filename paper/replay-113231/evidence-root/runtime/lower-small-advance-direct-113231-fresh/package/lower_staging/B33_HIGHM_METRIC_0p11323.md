# B33 high-M structure and metric exclusions at R=.11323

## A stronger minimum-degree contradiction

verify_B33_highM_any_five_0p11323.py first rechecks m100 and the original
global interior degree window5..8. Assume at least one degree5 vertex.
Every degree5 vertex, marked or unmarked and whether deep or adjacent to
the original boundary, receives one common positive corner label. All20
three-label multisets are accepted, including positive/boundary faces.
The26 vertex types d=5..8,p<d have a negative multiplier on every degree5
type. Summing it uses only the assumed count>=1. This differs from a deep
curvature witness and does not impose any location on the selected low
vertex. The exact row has negative M, shifted-ear, and bad-face coefficients
and gives area contradiction margin146810961635931078341/10^24 for M>=26.
Thus every original interior degree is at least6.

The Euler identity sum(d-6)=27-M-e-b leaves four possibilities: M26 with
one7 and e=b0; M26 with all6 and e1,b0; M26 with all6 and e0,b1; or M27
with all6 and e=b0. The metric methods below keep these cases explicit.

## The bad-face case is topologically impossible

For M26,e0, blockwise /6 isoperimetry and the general induced-core identities
force one connected induced interior graph, n2=n3=0, core frontier26 and
faces106. Any original BC chord separates the triangulated disk. Since
the induced interior graph is connected, all interior sites lie on one
side of that chord. The other side is a polygon triangulation without
interior sites, so it contains an original boundary ear at a non-endpoint
of the chord. This contradicts e0. A bad q1 face necessarily has a BC
chord. Therefore the e0,b1 case cannot occur, without a new area charge.

## The one-ear case has a five-pattern metric cap

For M26,e1 and all67 interior degrees6, the identities force c1 and
n2+n3=1. The alternative n3=1 would give frontier25 and faces107,
contradicting107<=25²/6. Hence n2=1,n3=0. Bridges, multiple face blocks,
and core chords are excluded by the same P26/F106 /6 comparisons as in
the no-ear proof. The core is simple and chordless with41 deep vertices.

There are60 DDD,20 DDR,26 DRR core triangles;26 BRR outer ring triangles;
and one BBR q0 triangle adjacent to the unique original ear chord. The
marked faces are31 ordinary q1 and one q2 ear. Give labels D0,R=-1/5,
B=-7/10 and a signed shared-edge multiplier16/25 on the26 ring/core edges.
Five complete-simplex supports bound the q0 score, with exact opposite
edge cancellation. The ear uses the audited normalized slab/Jensen cap
M2(R,k), k=11/25, including its two anchors and both halfside penalties.

The centered-angle correction is

    -31*Rlabel*pi/3 + Blabel*(pi+28pi/3).

This is the e1,U28 specialization of the full angle identity. The final
boundary inequality is the same independently verified normalized linear
halfside envelope. No additional hinge charge is used in this metric cap.
The executable verify_B33_one_ear_metric_0p11323.py checks every local
support at the new radius.

## No-ear metric cases

The M26/one7 and M27/all6 topology and metric proofs from the .11322
checkpoint are radius-independent except their boundary/area evaluations.
A same-radius wrapper sets their radius to11323/100000 in memory and
freshly replays every support and normalized boundary scalar. It does not
transfer a stronger-radius norm assumption onto a different diagram.

This document addresses M>=26 only. M<=24 and the unique deep degree5
premise for M25 are separately verified in the low-M prerequisite checker.

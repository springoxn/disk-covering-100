# Catalog-free normalized B32 high-M closure at R=.11323

This proves the B32, M=U-2e>=26 branch at exact radius 11323/100000.
It assumes the established generic irredundant clipped-Voronoi center
triangulation and oriented-area framework. Normalize the whole cover
before its diagram is classified, so every center has squared norm at
most 9871789671/10000000000. Reflection is never claimed to preserve an
already classified graph. Other boundary counts, low M, a universal
radius theorem and exact optimality remain separate obligations.

Run `python -B -S verify_B32_highM_complete_0p11323.py` with assertions
enabled. No optimizer, graph catalog, flat development, center lattice,
actual-face acuteness or saturated circumradius assumption is used.
Historical source and proposal hashes are checked, but all target-radius
inequalities are freshly recomputed. Earlier checkpoints are unchanged.

## 1. A slightly weaker scalar reduction is sufficient

The exact count bridge excludes 99 effective disks and gives m=100,
68 original interior sites. The same-radius four-cell/2R grouped-arc
comparison excludes all-boundary q0 and bad q1 faces; the five-cell/3R
comparison gives ordinary marked incidence p<=3. The verifier also
retains the bad-face coefficient, so the scalar accounting permits it.

Reuse the unchanged rational four-label row from
`reduce_B32_high_core_0p11322.py`. Its normalized k=.3 boundary envelope,
all20 complete face multisets and all387 types
0<=p<=3, max(3,p+1)<=d<=99 are checked at the new radius. Labels are
positive on every d<=5 site, zero on d6 and negative on d>=7, with a
separate original-boundary label. Low sites may have original boundary
neighbors. No narrower degree window is needed.

At M26/e0/b0 the raw area margin is about -.003847176. The minimum
reduced cost per unit of positive interior curvature is about .264611.
The margin after one such unit is still about -.000454593. This negative
diagnostic is preserved: the old row alone does not prove minimum degree6
at the new radius.

Two positive-curvature units give a strict contradiction. Consequently
any low-degree survivor has exactly one d5 vertex; d3/d4 are excluded.
The compulsory cost of a marked low vertex also gives contradiction,
so this unique5 has p=0. This is not a claim that it has no boundary
neighbor.

The row's M slope, shifted-ear and bad-q1 coefficients are respectively
about -.152550244, -.187019093 and -.291844880. Adding any one M unit,
ear or bad face to the one-low endpoint gives a strict contradiction.
Thus a low survivor has M26/e0/b0. Euler's exact identity

    sum_original_interior(d-6)=26-M-e-b

then forces exactly one compensating degree7 and all other66 sites degree6.
Without any low site, the same identity directly forces all68 sites degree6
and M26/e0/b0. This leaves precisely two profiles, which are closed below.

## 2. The unique5 needs a genuine boundary-neighbor case split

If the unique5 has no original boundary neighbor, its five neighbors are
interior sites forming its simple vertex-link cycle. All five central
faces and every face on the other side of a cycle edge are q0. Reuse the
immutable historical `direct_M25_metric_20261004/exact_proposals.json`
local supports, at R=.11323 and the new exact profile M26, e0, one7.

Reserve3/5 of the five actual central areas for the polygon/perimeter
support with tau=13/10; retain their full original angle potentials on
the complementary2/5 area. Give the physical cycle half-lengths opposite
signs in the central and outside faces. They cancel on each unchanged
edge. Every outside face meets at most two selected edges. The9 ordinary,
18 outside and8 residual-central complete-simplex supports include their
mandatory degenerate edge caps. There is at most one high neighbor, so
only central patterns (5,0,0) and (3,2,0) are needed in the final sum.

For the degree7 marked count p=0,1,2,3, put n=66, P=32-p and U=26.
The normalized center baseline is

    134A+32C0+P*(C(b)-C0)
    +p*(C(b-a)-C0)+a*(p-1)*pi/3
    +(7-p)*charge_H+(396-P+5)*charge_O+26*charge_B
    -b*(2pi+26pi/3).

For each k=0 or1 high neighbor, replace the entire central allowance
5A+2k*charge_H+(15-2k)*charge_O by its coherent star cap plus the
outside allowance J. Add only the ordinary concave boundary cap32H(pi/32).
All8 cases pass, with minimum strict area margin

    739858192019342675093 / 10^24 > .000739858.

The historical1/50 fan charge is discarded entirely. There is no hinge,
variance or half-side budget in this local closure, and no overlapping
face loss is appended to a completed dual.

The packaged entry uses the current generic signed complete-simplex
backend and the exact linear-halfside conjugate specialized to k=0.
Their valid conservative interval expressions differ slightly from the
older positive-only/quadratic-specialization diagnostic replay. The
displayed numerator is the freshly recomputed packaged result; historical
result JSONs and the immutable local support proposal are not changed.

If instead the unique5 has an original boundary neighbor, it cannot lie
strictly inside any face-bearing induced-core block: a boundary edge to
it would cross that block's simple enclosing cycle. Thus every strict
block interior has degree at least6, including the possible degree7.
Apply the catalog-free topology below. The5 is a ring vertex; the7 may
be a ring vertex or a deep vertex. Both possibilities are included.

## 3. The general induced core is simple and chordless

This step applies to the all-six profile and the preceding ring5 profile.
After removing original boundary sites, every bounded face is an original
triangle; an original outer-boundary vertex cannot be enclosed by a cycle
of original interior vertices. There are no missing bounded holes.

Let c count core components, including isolated vertices. The no-ear,
no-all-boundary-q0 identities give n2=2(c-1), core face count
108+2(c-1), and total frontier walk length26-4(c-1), with bridges counted
twice. For c>=2 the /6 disk isoperimetric theorem applied blockwise would
give at least110 faces with total perimeter at most22, impossible.
Hence c=1 and n2=0. There are no original boundary chords.

The connected core has108 faces and frontier26. A bridge would leave
face-block perimeters totaling at most24, but6*108>24^2. Two or more
face-bearing blocks would give6*108<=3^2+23^2, also false. Therefore it is
one simple disk with68 vertices,108 triangular faces and a26-cycle boundary.
A boundary chord splits it into two disks with total perimeter28, so
6*108<=3^2+25^2 would follow, again false. It is chordless.

All strict block-interior vertices retain their entire original stars,
which is the only degree premise used by the /6 theorem. No equilateral
development or enumeration is needed.

## 4. Four metric patterns cover ring defects and one deep excess

There are42 deep vertices. In the all-six case their degree excess is h=0.
In the ring5 case the sole7 can be on the ring (h0) or deep (h1).
Chordlessness makes every core-boundary edge incident to a distinct DRR
triangle, with one deep and two ring sites. Thus there are26 DRR triangles.
Every other core face has at least two deep sites. Deep incidence is
252+h and ring incidence72-h, forcing

    DDD=62+h, DDR=20-h, DRR=26, h in {0,1}.

Every exposed core edge has one q0 BRR face on the deleted side, so there
are26 BRR faces. Every marked interior apex is on the ring. Ring vertices
appear in two BRR faces apiece. Their q0 centered-angle sum is therefore
(32+h)*pi/3-Gamma; the original-boundary centered sum is
Gamma-2pi-26*pi/3. These angle identities do not require ring degree6.

Use deep potential0, ring potential LR=-.20663069056, original-boundary
potential LB=-.72993038978 and shared-edge multiplier tau=.6623191134.
Assign -tau opposite the RR edge in each DRR face and +tau opposite that
same physical edge in its BRR neighbor. All26 actual half-side pairs cancel
exactly, regardless of circumradius ratios. The four signed full-simplex
supports verify the localization guard and all3 degenerate edge caps.

The remaining center correction is

    32*C_.44(LR-LB) -(32+h)*LR*pi/3
      +LB*(2pi+26*pi/3).

Add one freshly verified same-radius normalized exact-lens k=.44 boundary
envelope with zero variance coefficient. The exact margins are

    h0: 3688487681599945871237 / 10^24
    h1: 1018177408390856135123 / 10^24.

Both are positive. The metric premise is deep degree excess0 or1,
not all original interior degrees6. The ring5/ring7 case is included,
as is a ring5/deep7 case. Together with the direct-star case split,
this excludes every normalized B32 high-M profile at the stated radius.

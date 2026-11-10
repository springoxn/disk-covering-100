# Complete normalized B35 exclusion at R=.11323

## Outcome and exact scope

Set R=11323/100000, B=35, m=100 and I=m-B=65. No cover in the
normalized B35 branch is possible at this radius. The exact standard-library
entry is `check_B35_complete_0p11323_v2.py`; assertions must remain enabled.
It checks 80 full-face supports and 2382 vertex supports. Every final branch
has a positive outward lower margin; the smallest is

    10083273211437482109/125000000000000000000000
    > .00008066618.

This is a complete B35 branch certificate, conditional on the established
clipped-Voronoi/straight-center triangulation and oriented-area foundations.
It is not an all-B theorem and makes no exact-optimum claim. Historical
.11322 artifacts are unchanged. `check_B35_complete_0p11323.py` is a
superseded initial packaging version missing one import search path; use v2.

## 1. Fresh whole-cover normalization and boundary envelope

Before choosing boundary ownership, an effective-center count or graph,
normalize every radius-R center to norm at most C=sqrt(1-R^2). Replace d*u
with d'*u when d>C, where d'=(1-R^2)/d. The exact identity

    |x-d'u|^2-R^2
      =(d'/d)(|x-du|^2-R^2)+(1-d'/d)(|x|^2-1)

preserves the old disk's entire intersection with the target unit disk.
Both coefficients are nonnegative. The norm-squared cap is freshly checked as

    1-R^2 = 9871789671/10000000000.

Classify only after the whole cover is normalized. Reflection is not a
fixed-graph transformation and no former B or irredundancy is retained.

The fresh specialization `verify_normalized_boundary_penalty_0p11323.py`
checks the same norm-aware complete half-arc envelope at k=33/100 with
variance coefficient v=1/20. It verifies the reflection polynomial identity,
all 14 bad-arc subintervals and 28 endpoint comparisons, the increasing
concavity-numerator guard and its strictly negative endpoint, and the good-arc
curvature. Its minimum bad-arc margin is

    10952494364811146157/10^24 > .00001095249.

For completeness, if q=sin(t)^2/R^2, c=cos(t), h=sqrt(R^2-sin(t)^2),
rho=c-h, and a normalized center differs from rho*u by delta with length D
and radial component Delta, the endpoint and norm constraints give

    D^2<=2h*Delta,
    sin(t)*D<=R*Delta,
    D^2+2rho*Delta<=2h*rho.

Thus D<=beta_k*h on q<=k, where

    beta_k=sqrt(2(1-R*sqrt(1-k)/sqrt(1-R^2*k))).

The required displacement compensation is bounded by

    R*k*D-sin(t)*Delta
      <=beta_k*R^2*sqrt(1-q)*(k-q)_+.

The collapsed h=0 lens has delta=0. On q>=k the left side is nonpositive.
For the bad-arc penalty, its second derivative has numerator

    A(q)=-6q^2+9q-k-2
           +R^2*q*(9q^2-(14+k)q+2k+4).

The checked guards A'(q)>=9-12k-2R^2(14+k)k>0 and
A(k)=2(1-k)(3k-1+2R^2*k(1-2k))<0 prove concavity. Midpoint tangent bounds
therefore cover each whole bad interval; the quadratic support minus the
midpoint tangent is concave, so both endpoint tests suffice. The good-arc
curvature covers [asin(R*sqrt(k)),asin(R)], with endpoint continuity.
This yields one global variance budget, not two independent displacement
savings. The complete derivation is the preserved
`NORMALIZED_CENTER_DISPLACEMENT_PENALTY.md` and its historical audit.

## 2. Counts, footprint, and one paid q4 allowance

The current-radius original count/area and concavity checks exclude 99
effective disks, and leave B=31,...,39 for 100 disks. This proof addresses 35.
The fresh six-cell footprint comparison at L=1733/2500=.6932 and radius 3R
has margin >.001. Every original boundary neighbor of an interior apex has
its full assigned boundary cell inside that footprint. It therefore has at
most five such neighbors, at most p=4 ordinary marked edges, and a p=4 edge
set must be one contiguous four-edge path. A split four-edge set would have
at least six distinct endpoints. This is independent of ears and bad faces.

Distinct p=4 apices own disjoint marked edges. With n of them, 1<=n<=8,
their proper edge union contains at least 4n+1 endpoint cells, whose half-arc
sum is at most nL/2. The full cycle is excluded by nL/2<pi. Global Cauchy
on that union and its complement gives

    V=sum(t_i-pi/B)^2
      >= B*((4n+1)*pi/B-nL/2)^2/((4n+1)*(B-4n-1)).

Using the exact lower endpoint of pi is conservative. All eight current-
radius checks prove v*V>n*R^2/500. Hence a local normalized allowance
CHARGE=1/500 for each p=4 vertex is paid by this single variance budget.
This payment is not counted again in any later margin or topology argument.

## 3. Coherent full-face and vertex bookkeeping

Write e for original two-marked-side ears, b for bad all-boundary one-marked-
side faces, U for q0 boundary-angle occurrences, and M=U-2e. The exact counts
are

    ordinary q1 faces = B-2e-b,
    q0 faces = 198-2B+e = 128+e,
    sum_interior(d-6) = B-6+e-b-U = 29-M-e-b.

The total q0 boundary angle is Gamma+(e-2)pi, where Gamma is the ordinary
marked-apex angle sum. All-boundary q0 faces, arbitrary original ears and
boundary chords are initially admitted. The marked and actual-ear supports
retain the full permitted apex-angle domains.

Each row uses one common boundary corner potential -lb, one common high-
degree potential -a, a neutral degree-six potential 0, and when needed one
low-degree potential c. For every unordered face-label triple, the checker
takes the maximum of the acute sine-conjugate support and the mandatory
closed-simplex degenerate-vertex cap. All ranges are strictly below one.
Thus actual triangles need not be acute. Every actual q0 face sees the same
potential at each shared vertex, so the corner-angle identities are coherent.

Let A=3*sqrt(3)/4, C0=conjugate(k,0), and C_k(s) be the full-apex linear
half-side conjugate. For a vertex type (p,d), select its label lambda and
corresponding corner charge ch. Its checked normalized local score is

    p*(C_k(lambda+lb)-C0)
      -lambda*(6-d+p)*pi/3+(d-p)*ch.

It is at most u0+p*beta+(d-6)*eta+CHARGE*[p=4], with an additional
sigma*[d-p=3] only in the new restricted M26 row below. The corresponding
face scores are at most A+sum of their corner charges.

With no sigma the global normalized gain over the common boundary/face
baseline is

    G(M)=65*u0+35*beta+eta*(29-M)+M*ch_B
           -lb*(2pi+M*pi/3).

The M coefficient is c_M=-eta+ch_B-lb*pi/3. The shifted original-ear and
bad-q1 coefficients are respectively

    E=A-2C0+ear_cap-2beta+eta+lb*pi+2*c_M,
    T=bad_cap-C0-beta-eta.

Every checked E and T has a negative outward upper endpoint. The full bound
is baseline+R^2*(G+eE+bT), less any retained nonnegative vertex slack.
This identity admits arbitrary ears and bad faces before their exclusion.

## 4. Exact source-row replay at the new radius

The historical rational ROWS and RESTRICTED are copied unchanged. The replay
script compares those assignments by exact parsed equality and checks the
historical source hashes. Their envelope, geometry and cap inputs are all
fresh R=.11323 specializations. The outcomes are:

- M<=24: the shifted induced-core obstruction forces a p=0 degree<=5
  vertex. The positive-slope M24 row, keeping one minimum reduced-cost slack,
  gives a margin >.00050001463 for every M<=24
- M25 with any degree<=5: the second row gives >.00120832106
- M>=27: the source M26 row has c_M<0; at M27 its margin is >.00086919701,
  and it improves for every larger M
- Source unrestricted M26: its ordinary margin is
  -218243214146605345303/(5*10^23), about -.00043648643. This failed direct
  row is reported honestly and is not accepted as a branch exclusion

That last row nevertheless gives three independent necessary conditions
for the remaining M26 case. Keeping one low-degree slack gives margin
>.00230584163. Keeping one original ear gives >.00164626427, and keeping
one bad q1 face gives >.00258826083. Thus M26 has e=b=0 and all original
interior degrees at least six. These are alternative branch contradictions,
not additional savings added to the final row.

## 5. Remaining M25: the unchanged restricted row still closes

The induced graph on all 65 original interior vertices has c components.
Let n_j count q0 faces with j original boundary vertices. Every bounded
induced-core face is an original triangle: a retained cycle cannot enclose
an original boundary vertex. Euler and exposed-II-edge incidence give

    n2+n3=e+2(c-1),
    F_core=128-M+2(c-1)+n3,
    P_walk=M-4(c-1)-n3.

A face-bearing block has a simple boundary; all its strict interior vertices
retain their full original degree. The preserved general-disk isoperimetry
therefore gives F_core<=sum(P_block^2)/6. Bridges consume walk perimeter
without contributing faces.

At M25, c>=2 would imply F>=105/P<=21; n3>=1 after c=1 gives
F>=104/P<=24. Both violate 6F<=P^2. Hence F103/P25. A bridge leaves face-
block perimeter at most23, and multiple face blocks have squared-perimeter
sum at most3^2+22^2; both contradict 6*103. Thus there is one simple disk.
A chord would split it into two disks with perimeters summing27 and give
6*103<=3^2+24^2, also false. The core is chordless and has core degree at
least three. This argument permits original e>0 and b>0: M is shifted,
and n2=e is allowed after c1,n3=0.

A proper p-edge subset of the original 35-cycle has at least p+1 distinct
boundary endpoints, all neighbors of its interior apex. Thus d>=p+1+3,
or p<=d-4. The unchanged three-label source row checks all 467 allowed
vertex types and gives the minimum final margin stated at the top,
>.00008066618. Its negative ear and bad-face terms remain valid.

## 6. Remaining M26: one simple P26/F102 core and at most one core ear

We now use the already proved M26 premises e=b=0 and original d>=6.
The same induced-core identities give

    F_core=102+2(c-1)+n3,
    P_walk=26-4(c-1)-n3.

If c>=2, F>=104 and P<=22, contradicting 6*104>22^2. Therefore c1;
n2+n3=e+2(c-1)=0 implies n2=n3=0, hence exactly F102/P26.
A bridge would leave face-bearing perimeter at most24, contradicting
6*102>24^2. Multiple face-bearing blocks would give
6*102<=3^2+23^2, also false. Connectedness and absence of bridges leave
no additional acyclic vertices. The core is one 2-connected triangulated
disk, with simple 26-cycle boundary and minimum core degree two.

Every proper p-edge marked set has at least p+1 original boundary endpoints,
so every marked apex satisfies d-p>=3. If equality holds, it has exactly
two core neighbors and exactly p+1 original boundary neighbors. It is
therefore a degree-two vertex on the simple core boundary. With p<=4 and
d>=6, equality types are precisely (p,d)=(3,6),(4,7).

There cannot be two degree-two vertices on that core boundary. First, two
such vertices cannot be adjacent unless the entire boundary is a triangle:
if v and w are adjacent and their other boundary neighbors are a and b,
w's ear requires edge v-b, whereas v has only neighbors a,w, so b=a.
This would give a 3-cycle boundary, contrary to P26. For two nonadjacent
such vertices, remove both ear triangles. Removing a degree-two boundary
vertex deletes one face and reduces the simple boundary length by one;
the other nonadjacent ear remains. The remaining triangulated disk has
P24/F100. Strict interior vertices keep their degrees, since both removed
vertices were on the boundary. General disk isoperimetry would require
6*100<=24^2, but 600>576. Thus at most one equality type occurs.

The exact integer checker records contradiction margins 140 (components),
36 (bridge), 74 (multiple blocks), and 24 (two core ears). These integer
checks accompany the topology proof; they do not replace it.

## 7. New exact rational support for that M26 core

All inputs below have denominator 10^9:

    a=308167941, lb=168977954,
    charges=(17937717,5433731,25),
    u0=5000, beta=153867006, eta=-110119657,
    sigma=27009838,
    nus=(-808167941,-760239879,-697242295,-714021974,
         -653553203,-596512829,-668977954,-610361366,
         -554356250,-500000000).

The labels are (-a,-lb,0), and nus follow lexicographic combinations-with-
replacement of their indices. All ten full-simplex face inequalities pass
with minimum slack >.00000007498913. The 469 allowed local types satisfy
0<=p<=4 and max(6,p+3)<=d<=99; each checked vertex inequality includes
sigma exactly for d-p=3. All vertex gaps are nonnegative, with minimum
>.00000485.

The preceding combinatorial theorem gives sum[d-p=3]<=1, so the global
gain is G(26)+sigma. The nonnegative sigma is charged once, not once for
every vertex. The p4 allowance is still canceled by the same one global
variance budget from section 2. No combinatorial step spends extra metric
loss. This final row gives the strictly positive outward margin

    16042062609909122661/62500000000000000000000
    > .00025667299.

A numerical optimizer helped find the rational input. Optimizer output is
not evidence: the acceptance entry imports only standard-library exact and
outward-interval support code, checks every listed face and local type, and
asserts every final covering margin. No optimizer is called during replay.

## 8. Endpoint covers and integration boundary

The proof uses the inherited generic disk-triangulation foundations, exact
circumradius<=R faces, actual boundary ownership, and annular-slab caps.
For nongeneric endpoint covers, use the established finite-type limiting
argument: slightly enlarge the radius, normalize ALL centers at that
radius, move norm-boundary centers inward within the strict covering margin,
and perturb generically. Choose a constant finite combinatorial subsequence
and let the radius decrease to R. The normalization cap is updated at each
radius. The closed-domain support inequalities and uniformly strict finite
margins persist sufficiently close to R, including the new exact row.
The topology restrictions are combinatorial and are established on each
generic member. No same-radius arbitrary perturbation or fixed-graph
reflection is asserted.

This closes the normalized B35 branch for that limiting proof. Integration
into a global radius theorem still requires every other surviving B branch
at the same radius and the common normalization/count foundations. It does
not determine the exact optimal 100-disk covering radius.

## Reproduction

From the working root:

    python -B lower_staging/B35_0p11323/check_B35_complete_0p11323_v2.py
    python -B lower_staging/B35_0p11323/replay_B35_0p11323.py

The result and audit receipts are saved beside this proof. All historical
sources are checked against `source_manifest.json`; additions are confined
to this staging directory. Different existing files are never overwritten.

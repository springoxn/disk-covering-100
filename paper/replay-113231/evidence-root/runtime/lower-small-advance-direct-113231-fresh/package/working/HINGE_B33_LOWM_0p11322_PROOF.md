# Complete B33 low-M exclusion at R=.11322

This proves only the B33,M<=25 branch after whole-cover normalization.
It does not exclude M>=26 or other boundary counts and does not identify
the exact covering optimum. The entry is verify_hinge_B33_lowM_0p11322.py;
all acceptance uses exact outward rational intervals. Numerical proposal
fields are informational only.

## Independent geometric premises

Normalize before classifying the diagram, using center norm at most
sqrt(1-R^2), where R=5661/50000. The old exact99-disk bound forces m=100.
Here B=33,I=67. Write e for ears, b for all-boundary singly marked faces,
U for q0 boundary-angle occurrences and M=U-2e.

The old area upper bound gives a normalized total deficit d. The verifier
recomputes d and checks it is strictly below the universal degree-four
star threshold from GLOBAL_STAR_ANCHOR_DEGREE_WINDOW.md. That theorem
then places every original interior degree in[5,8], with no acute-angle
assumption. A marked apex owns fewer incident marked faces than its
degree; otherwise its full fan would fill the boundary disk and leave
only one interior vertex, contradicting I=67.

The induced core has at least132-M triangular faces and total frontier
walk length at most M. Its area is at least
R^2*((132-M)*A-d), with A=3sqrt(3)/4, since its q0 area losses are a
subset of the nonnegative old deficit. Its perimeter is at most2RM.
Planar isoperimetry therefore requires

    pi*((132-M)*A-d)<=M^2.

The exact endpoint comparison at M=21 is strictly reversed. The left
minus right decreases for M>=0, so all M<=21 are impossible.

The blockwise core-curvature theorem gives at least two units of positive
deep curvature for M22/23 and at least one for M24/25. A strict block
interior vertex retains its entire original star and has no original
boundary neighbor. Since all original interior degrees are at least5,
the witnesses are respectively two distinct deep degree-five vertices
or one. These premises are independent deductions, not extra deficits
subtracted again in the final area functional.

## Boundary hinge allocation, without a qmax footprint assumption

At this radius and boundary count, the exact lens checker proves

    delta(t)>=.03*(.092-t)_+,

as well as delta(t)>=0 globally, for half-side multiplier k=.44. The
assigned half-arcs sum to pi. MARKED_APEX_HINGE_CHARGE.md proves that an
apex owning p marked edges may be charged

    gamma_p=.03*((p+1)*.092-.6934/2)_+/(2R^2).

The proof selects p+1 endpoint cells of its proper boundary-edge subset.
Their arcs lie in one radius3R footprint, and each boundary cell is an
endpoint for at most two distinct owner apices. This permits split fans,
ears and bad faces. All counts p<33 are covered. The actual degree window
restricts the finite vertex table to p<d<=8; no separate qmax or
contiguous-fan hypothesis is imposed. No simultaneous variance charge is
taken from these same scalar deficits.

Put mu=pi/33,rho=cos(mu)-sqrt(R^2-sin(mu)^2). The remaining boundary
constant is

    Q=33*(mu-sin(mu)*rho+k*R*sin(mu)*rho).

## Exact face and vertex inequalities

Use labels H=-a on degrees7/8, B=-lb on original boundary vertices,
O=0 on the other interior vertices, and P=c on selected deep5 witnesses.
Every selected P vertex has no original boundary neighbor. The general
face list therefore consists of the sixteen three-label multisets not
containing both P and B. Every face support checks its acute conjugate
and degenerate-simplex cap through the range<1 theorem.

For a q0 face the checked inequality has the form

    area/R^2+sum labels*(angle-pi/3)
       <= A+sum corner_charges-sum BI_edge_credits.

At every marked apex, at least two terminal BI occurrences lie in q0
faces. Thus a nonnegative credit tau_H or tau_O can contribute2tau at
that vertex. This terminal count remains valid with split fans and bad
faces. The resulting per-vertex score, for label l, degree d and marked
count p, is

    V=p*(C_k(l+lb)-C_k(0))-l*(6-d+p)*pi/3
        +(d-p)*charge_l-2tau_l*[p>0]-gamma_p.

The exact finite tables prove

    V<=u0+beta*p+eta*(d-6)+apex*[p>0]-flag*[selected deep5].

The number of marked apices is at most U: their terminal q0 boundary-angle
occurrences supply the usual double-counting witnesses. All selected
deep witnesses are explicitly colored P; other degree5 vertices may be
colored O even if they too are deep.

The exact incidence identities are

    q0=132+e, ordinary q1=33-2e-b,
    sum p=33-2e-b, sum(d-6)=27-M-e-b,
    q0 boundary-angle sum=Gamma+(e-2)*pi, U=M+2e.

For N selected deep witnesses, the e=b=0 center upper bound is

    C(M)=132A+33C_k(0)+67u0+33beta+(27-M)eta
         +M*apex-N*flag+M*charge_B-lb*(2pi+M*pi/3).

Its M slope is s=-eta+apex+charge_B-lb*pi/3. The shifted ear coefficient
is A-2C_k(0)+M2-2beta+eta+lb*pi+2s. The bad-face coefficient is
M1-C_k(0)-beta-eta. The replay verifies both are negative for every row,
so arbitrary ears and bad faces are safely retained and then discarded
only as nonpositive contributions. Every reported final comparison is
pi>R^2*C(M)+Q.

## Exhaustive low-M cases

1. For M22/23 choose two deep5 witnesses. The M22 row has negative M
   slope and a positive exact margin, so it excludes both cases.
2. At M24 choose exactly one guaranteed deep5 for P and color all other
   degree5 vertices O. The initial row need not exclude this case alone.
   However every extra O degree5 has a certified vertex slack; adding
   that slack exceeds the entire remaining area surplus. Therefore there
   is exactly one original degree5 vertex.
3. With this unique-five premise, ISOLATED_FIVE_CORE_M24.md applies. The
   core is a simple chordless P24/F108 disk; the five has no high-degree
   or core-boundary neighbor. Its five faces have only the pattern(P,O,O).
   The eleven-face isolated row then excludes M24. This is a fresh
   functional after a structural deduction, not a sum of two area losses.
4. The general M25 row, with one selected deep5, directly has positive
   margin and needs no uniqueness premise.

The replay checks59 face supports and103 vertex supports. Its least final
area margin is134763746755812455711/(5*10^23), greater than.000269527.
The M24 unique-five reduction has its own positive margin, and all
geometric/count premises are recomputed at the same radius. Independent
review and a separate high-M branch remain necessary before global use.

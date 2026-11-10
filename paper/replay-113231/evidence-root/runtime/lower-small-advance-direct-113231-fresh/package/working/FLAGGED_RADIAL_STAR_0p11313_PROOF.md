# B33 exclusion at .11313 using compulsory low-degree core curvature

This branch concerns R=11313/100000 and does not identify the exact optimum.
It must be combined with the inherited Voronoi/Delaunay reduction and every
other surviving boundary count. Earlier completed checkpoints are unchanged.

## 1. Same-radius geometry and core incidence

The .11313 case in
lower_bounds_extension_20261004/check_two_ear_structure_next_radii.py proves
m100, B33, I67, F165, no all-boundary q0 or q1 faces, p<=3, and e=0,1,2 q2
ears. Every interior angle in an unmarked face is in(.35,pi/2+.285), every
ordinary marked apex is in(.4,pi), and interior degrees are5 through17.
Every full assigned boundary arc exceeds.063, hence its normalized half-
chord sine exceeds.2783. The degree-five premise uses the all-angle global
degree lemma, not an acute-angle assumption.

Let N count q0 boundary-angle occurrences, not q0 faces. The separate
CORE_CUT_ISOPERIMETRY.md and exact checker establish N>=22+2e. To recall
the allocation, if F2 counts q0 faces with two boundary vertices and a
counts ring/ring II edges, the core cut has h=N-2F2-2a and F2>=e. With
M=N-2e its perimeter is at most2RM and it has at least132-M q0 faces.
The old nonnegative face-loss budget is less than R^2. Euclidean
isoperimetry contradicts M<=21. The original degree count gives N<=94+e.

UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md supplies a stronger, purely
combinatorial constraint on all rows with N-2e<=25. If every unmarked
interior star had degree at least six, every strict interior vertex of
every face-bearing induced-core block would retain that degree. The
audited disk isoperimetric theorem F<=b^2/6 then yields

    132-M <= M^2/6.

This fails for M<=25. Therefore at least one p0, degree-at-most-five star
exists. The independent minimum-degree-five premise makes it exactly the
type(p,j)=(0,5). This deduction permits disconnected cores, bridges and
boundary chords; it assumes no flat lattice development or symmetric cover.

## 2. A corrected simultaneous radial support

Use lambda=1/25 and the normalized half-sine domain[.2783,1]. The endpoint
lens notation is s=sin a, h=sqrt(R^2-s^2), rho=cos a-h. A displacement from
the inner radial lens corner has components Delta,t and obeys

    2h Delta >= Delta^2+t^2+2s|t|.

The independently audited lens-cone theorem gives the global quadratic
factor K=187707/50000=3.75414, larger than4[1-x0^2*rho0^2]. The exact
radical guards prove neighbor radial monotonicity and the tangential
spread bound. Radial-normal nonpositivity is deliberately not assumed.

RADIAL_NODE_SOFT_CORRECTION.md proves that the residual node is bounded by

    P(a)=2h*max(F_K(a),0),
    F_K(a)=4lambda[(1-rho0*c0)cos a+rho0*s0 sin a]
           +(2K-4)lambda*h-sin a.

Indeed the tangential terms are nonpositive, the residual normal is at
most F_K(a), and0<=Delta<=2h. Thus the combined actual outer-area and
positive squared-edge functional is bounded by the radial score plus
sum P(a_i). This is one combined support, not a second use of displacement
or variance loss.

The exact two-variable checker proves on the complete closed domain:

    [H_R(2a)+H_R(2b)+P(a)+P(b)]/2 + lambda*L0(a,b)^2
    +(3/4)[(a-pi/33)^2+(b-pi/33)^2]
    <=112049/10^7-(9291853/500000000)(a+b).

Here L0 is the actual distance between the two radial lens corners. Its
stable radical identity is retained from the earlier checkpoint. The
mean-value interval derivative includes both branches at F_K=0; endpoint
boxes with h=0 use the natural value bound. No differentiability is
silently assumed at the positive-part kink. The replay visits1173 boxes.

After summing, with L=112049/10^7, mu=-9291853/500000000 and gamma=3/2,

    outer_actual+lambda*sum marked_edge^2
    <=33L+2pi*mu-gamma*V,
    V=sum(a_i-pi/33)^2.

## 3. Marked scores, ears and one variance allocation

The all-apex global G_lambda envelope is revalidated at lambda=.04. It
bounds each ordinary marked face plus anchor minus lambda times its
marked base square. It uses the same concave low curve and its pi/3
tangent on the full apex interval[0,pi]; no acute-only envelope is reused.

Each ear uses the sharper independently audited Jensen/slab cap

    E=w+sqrt(2w-w^2)-4lambda*w,
    w=2/[1+sqrt(1-2R)].

This retains both ear base penalties, which cancel the same two edges
already counted in the positive cyclic edge-square sum.

For e0, the multiple-p3 weighted footprint theorem gives

    V >= (33/133)*(4pi/33-.6926/2)^2 * number_of_p3_stars.

Its integer-overlap proof, including the whole-cycle exception, is
rechecked. Subtract the corresponding normalized constant from every p3
star. For e1 instead subtract one global variance charge

    V >= (11/30)*(3pi/33-.4566/2)^2.

For e2, the two three-cell ear blocks have disjoint marked edges and share
at most one endpoint cell. Their weights have sum6 and square sum at most8.
Weighted Cauchy gives

    V >= (11/19)*(3pi/33-.4566/2)^2.

The exact sine checks prove the two footprint spans contain their2R/3R
circle intersections. Each ear-count branch spends exactly one variance
budget. Fan and ear charges are not added to each other.

## 4. Concave star supports and the compulsory-type flag

The q0 face compatibility majorant uses coefficient21/50, splice433/400
and endpoint pi/2+57/200. The rational tangent endpoint guard is rechecked.
Actual q0 and marked lower angle bounds restrict the closed star domain.
For each of52 types p0 through3, degree5 through17, maximize

    pG_lambda(g)+j*phi((2pi-pg)/j)+eta*p*g.

The boundary conjugate C(eta) uses the same actual q0 angle interval. In
the no-ear branch the scalar score already includes its p3 charge.

Every rational dual row proves

    score_(p,j) <= u0+p*u1+j*u2+v*1_(p>0)-f*1_((p,j)=(0,5)),
    v>=0, f>=0.

On N-2e<=25 rows the compulsory-type theorem permits subtracting f once
in the total. On all other rows the exact checker requires f=0. This sign
is important: it is a negative indicator allowance derived from a lower
bound on that type's multiplicity, not a free extra geometric deficit.

With Mq=33-2e and Uq=132+e, the counts are

    sum x=67, sum p*x=Mq, sum j*x=3Uq-N,
    sum_(p>0)x<=N.

The boundary q0-angle sum is Gamma+(e-2)pi. Thus every row bounds the
center/anchor part by

    R^2[67u0+Mq*u1+(3Uq-N)u2+Nv-f
         +N*C(eta)+(e-2)pi*eta+eE].

Add33L+2pi*mu and subtract the appropriate single global variance charge.
The exact checker requires a strict area upper bound below pi for every
row. Numerical optimization only proposes the rational coefficients;
no floating-point result accepts any inequality.

## 5. Replay and logical scope

Run verify_radial_corrected_support_0p11313.py and
verify_flagged_star_0p11313.py with assertions enabled. The latter calls
the exact global marked guards, fan integer lemma, low-type obstruction,
core-cut constants and sharper ear helper. The same-radius structural
case remains an explicit dependency of the integrated proof.

The star ranges are e0:N22..94, e1:N24..95 and e2:N26..96:216 cases and
11232 scalar inequalities. Actual replay output, rather than the numerical
proposal generator, is the evidence of acceptance.

The completed scalar replay has minimum strict area margin
22790518191106752471/10^23, at e0,N26. The old tight N24 relaxed pattern
is excluded by the compulsory unmarked degree-five star.

Generic covers and endpoint degeneracies are handled by the inherited
compactness-limit argument with fixed finite topology. Strict area margins
exclude the limit as well. This branch alone excludes B33 at R=.11313;
a universal lower-bound checkpoint additionally requires every other
surviving B branch. The exact minimum is still unresolved.

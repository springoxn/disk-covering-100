# B33 exclusion at .11316 with arbitrary ears

Set R=2829/25000, B=33, and lambda=13/200. This is a complete B33
component. It must still be combined with every other surviving boundary
count for a universal radius theorem.

## 1. Independent domain bootstrap

`lower_bounds_extension_20261004/verify_B33_angular_bootstrap_0p11316.py`
starts from the original area reduction, with no radial, squared-edge,
halfside, or fan penalty. It rechecks m100, the complete all-count bridge,
absence of all-boundary q0/q1 faces, and marked incidence at most3.
Its two full-face rows prove an unpenalized normalized center/anchor cap
229.203. Concavity of H then forces every full assigned boundary arc
to exceed .094, hence its normalized half-sine exceeds .415. This is
an independent necessary-domain bootstrap, not a consequence of the
radial inequality it later enables. It permits arbitrary q2 ears.

The old normalized nonnegative face-loss budget at this exact radius is
freshly checked below1 in the present verifier. The audited Euclidean
core cut therefore gives M=U-2e>=22, where U counts q0 boundary-angle
occurrences. The stronger combinatorial block theorem says that M<=25
forces an unmarked interior vertex of degree3,4,or5. Actual triangle
acuteness and an interior maximum-degree estimate are unnecessary here.

## 2. Corrected radial support

`verify_radial_corrected_support_0p11316.py` uses the proved weak
neighbor-product guard and lens-cone residual correction. On the entire
closed sine domain [.415,1], its1137-box exact replay proves

    outer_actual + lambda sum(marked base length)^2 <= Q - (3/2)V,
    Q = 33*(101769/10^7) + 2pi*(-9017068/10^9),
    V = sum(a_i-pi/33)^2.

The cone factor is172351/50000. The exact Q upper endpoint is
55836358165712156105137/(2*10^23). The soft positive radial correction
is retained; no individual-center radial optimality is assumed.

## 3. A full-apex marked conjugate at the larger penalty

The older tangent G_lambda envelope is not used at lambda=.065.
`QUADRATIC_MARKED_CONJUGATE.md` proves the direct support

    C_lambda(s)=max over 0<=a<=pi/2 of
       sin(a)(1+2cos(a))-4lambda sin(a)^2+s*a,
       sin(a)-4lambda sin(a)^2+s*(pi-a).

For a fixed half-base x, area is at most x^2*cot(gamma/2), and
asin(x)<=gamma<=pi-asin(x). The area/anchor/penalty score plus s*gamma
is convex in gamma, so one of those endpoint branches is maximal.
Both branches are concave in a for0<=lambda<=1/8. The exact implementation
uses a tangent continuation across the uncertain pi/2 endpoint.
This is a conjugate for a complete marked face, not an assertion of
pointwise concavity in the actual apex angle.

An ear is bounded by the independently proved joint Jensen/slab cap

    E_lambda=w+sqrt(2w-w^2)-4lambda*w,
    w=2/[1+sqrt(1-2R)].

The negative marked-base penalties cancel the positive edge-square sum
in the radial support exactly.

## 4. Finite complete q0 face supports and interface reservation

For each rational row, label high-degree interior vertices (d>=7) by
-a, the other interior vertices by0, and boundary vertices by-b. The
range is below1/2. Full-simplex localization and the exact sine conjugate
bound each of the ten possible unordered label triples by

    A + sum corner charges - tau*(number of high/boundary BI edges),
    A=3sqrt(3)/4,  tau>=0.

Every marked high-degree interior vertex has at least two distinct fan
terminal BI edges incident to q0 faces. Thus the reserved credit pays
2tau for each such vertex. This uses the same audited face/terminal
incidence theorem as the .11315 B34 and B33 methods and does not spend
any boundary variance.

For a vertex of marked incidence p, degree d, and label l, the exact
centered score is bounded by

    p[C_lambda(l+b)-C_lambda(0)]
      -l(6-d+p)pi/3+(d-p)*corner_charge(l)
      -2tau*1_(p>0,d>=7),

with the additional p3 charge below only when e=0. Each row checks every
p=0,...,3 and d=max(3,p+1),...,99. These are full-angle face supports.

## 5. Two disjoint uses of the single variance budget

Use L3=.4566 and L4=.69275. Both footprint sine inequalities are freshly
verified at R. For e=0, the multiple-p3 theorem yields

    V >= (33/133)*(4pi/33-L4/2)^2 * number of p3 vertices.

Multiply by3/2, divide by R^2, and subtract the resulting per-p3 constant
from the vertex score. For every e>=1, ignore all fan charges and use
just one existing ear:

    V >= (11/30)*(3pi/33-L3/2)^2.

Only one global variance budget is spent in either branch. No upper
bound of one or two ears is required by this proof.

## 6. Four rational rows cover every U and every ear count

The vertex majorant has the form

    u0+beta*p+eta*(d-6)+v*1_(p>0)-f*1_(p=0,d<=5),
    v>=0, f>=0.

The exact counts are67 interior vertices, sum p=33-2e,
sum(d-6)=27+e-U, and at most U marked interior vertices. On M<=25 the
compulsory low-type theorem permits subtracting f once. Otherwise f=0.
The normalized total is

    (132+e)A+(33-2e)C0+eE_lambda
      +67u0+(33-2e)beta+(27+e-U)eta+Uv-f+U p_b
      -b[(2-e)pi+U*pi/3],
    C0=C_lambda(0).

Its U coefficient is c=-eta+v+p_b-b*pi/3. At fixed M=U-2e the per-ear
coefficient is

    E_shift=A-2C0+E_lambda-2beta+eta+b*pi+2c.

The two e>=1 rows certify E_shift<0. Consequently their total is largest
at e=1; larger ear counts only strengthen the exclusion. All four rows
have negative M slope, so it suffices to check:

* e0, 22<=M<=25: U22;
* e0, M>=26: U26;
* e>=1, 22<=M<=25: e1,U24;
* e>=1, M>=26: e1,U28.

The executable `verify_radial_face_B33_0p11316.py` checks40 full-face
supports,1548 vertex supports, all slope/ear signs, and the four final
area comparisons. The minimum strict gap is

    83559252134969281147 / 125000000000000000000000
      > .0006684740170.

The no-ear M>=26 gap is separately greater than .0009410711060.
The saved result is `radial_face_B33_0p11316_result.json`. Rational
proposals are never accepted by floating-point numerical optimization.

## 7. Logical scope and replay

Run the independent angular bootstrap in a fresh process, then the
radial support entry and this face verifier. The original topology and
generic limiting reduction remain inherited dependencies. A fixed
finite-type subsequence and continuity extend all closed inequalities
to nongeneric endpoint covers; the strict area gaps exclude the limit.

The three steps are noncircular: unpenalized full-face area gives the
arc domain; that domain gives the larger-penalty radial support; the
new penalized face scores then exclude every B33 cover at R. Other B
values must be excluded separately before announcing a global bound.

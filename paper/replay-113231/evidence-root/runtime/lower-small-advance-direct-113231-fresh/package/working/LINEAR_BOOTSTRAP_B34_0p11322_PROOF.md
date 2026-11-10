# Complete normalized B34 exclusion at R=.11322

This is a single boundary-count branch, not an all-count lower bound. Set
R=5661/50000. Normalize every center to norm at most sqrt(1-R^2) before
constructing and classifying the diagram. The normalization, subsequent
generic reduction and finite-type limit are the inherited whole-cover
construction; no center is moved during the argument below.

## 1. Same-radius starting geometry

The exact original count inequalities exclude m<=99 and leave precisely
B31,...,39 for m100. This branch has B34, I66 and F164. The freshly checked
six-cell radius-3R footprint excludes six consecutive boundary cells in
a span .6932, so ordinary marked incidence is at most four. Ears, bad
all-boundary q1 faces and all-boundary q0 faces are initially allowed.

Let e count q2 ears, b count bad q1 faces, U be the number of boundary
angle occurrences in q0 faces, and M=U-2e. The exact old area-loss budget
and core-cut inequality prove M>=22. In particular the checker uses the
actual loss value, which exceeds one, rather than an obsolete loss<1
shortcut. There are 130+e q0 faces and 34-2e-b ordinary q1 faces.

The general deep-core curvature obstruction gives two weighted deep
positive-curvature units when M<=23, and one deep low-degree vertex when
M<=25. Deep means that the vertex has no original boundary neighbor.
Both deep and nondeep unmarked degree-three through degree-five types
are included in the local inequalities; no witness is assigned to a
boundary-adjacent vertex by assumption.

## 2. One complete compensated boundary inequality

Use linear half-side multiplier k=1/2 throughout. For assigned half-arc
a let s=sin(a), c=cos(a), h=sqrt(R^2-s^2), rho=c-h, and mu=pi/34.
The normalized exact endpoint-lens support gives the already derived
compensated boundary function F(a) and its displacement penalty P(a).
Writing

    delta(a)=F(mu)+F'(mu)(a-mu)-F(a)-P(a),

the same-radius scalar replay proves delta(a)>=.03*(a-mu)^2>=0 on the
entire allowed arc domain. Its bad-arc part has 1000 exhaustive exact
interval boxes; the good-arc part uses the proved curvature bound.
The resulting total boundary constant is

    Q=34*[mu-sin(mu)*rho(mu)+k*R*sin(mu)*rho(mu)].

The global half-side accounting is that of EXACT_NORMALIZED_LENS_PENALTY.md.
In particular delta is a lower bound on the loss in this same boundary
inequality. Neither its variance nor its pointwise loss is paid as a fan
charge in the initial rows below.

## 3. Three initial full-face rows

Each row has four corner labels: high-degree interior, boundary, zero,
and positive deep. Their ranges are strictly below one. The exact
full-simplex support includes both the acute sine-conjugate bound and
the degenerate-vertex cap. Precisely the 16 label multisets with no
deep/boundary pair are checked; that pair cannot be an actual face edge.
Nonnegative terminal boundary/interior edge credits are reserved in the
q0 face allowances and paid at most twice per marked apex.

The global marked conjugate treats the entire apex-angle domain, with
the exact linear half-side penalty. Every permitted total degree from
three through 99 is checked, including duplicate deep/nondeep low types.
Thus these rows do not require acuteness or an unproved degree window.

Three initial rows cover M22..23, M24..25 and M>=26. Their M slopes are
negative, as are their shifted-ear coefficients and bad-q1 coefficients.
Consequently arbitrary e and b are covered by their values at e=b=0.
The first row directly excludes M23, the second directly excludes M25,
and the third directly excludes every M>=26. The remaining raw surpluses
at M22 and M24 are, respectively,

    68462325846092381861/(250000000000000000000000),
    366308813550757665903/1000000000000000000000000.

Both are less than 1/2500=.0004. Keeping all nonnegative boundary losses
unspent therefore proves sum(delta(a_i))<=.0004 separately in each of
these two still-hypothetical ranges.

## 4. An independent actual-domain improvement

verify_B34_exact_lens_short_arc_bootstrap_0p11322.py replays the global
nonnegative-loss inequality and a separate 1000-box pointwise proof:

    delta(a)>=209009010821514964381/(5*10^23)>.000418018
    whenever 0<=a<=39/500=.078.

This contradicts the raw budget if any such short arc exists. Hence every
actual assigned full arc exceeds .156. Three cells belonging to a common
center face lie in a radius-2R disk about its circumcenter, but their
total assigned arc would exceed .468>2asin(2R). The exact sine comparison
therefore excludes every all-boundary center face, including ears.

Likewise five boundary cells adjacent to an apex would have total arc
greater than .78>2asin(3R). Its neighbors lie in a window of at most four
consecutive boundary cells, so ordinary marked incidence is at most
three. These conclusions establish actual geometry. They do not subtract
the initial deficit a second time from a later inequality.

## 5. Two final rows and exact closure

Two new rows apply to the now established e=b=0, q<=3 domains at M22 and
M24. They use the same k=.5 global boundary support, with all its losses
available anew; no stronger multiplier or isolated-five classification
is needed. They preserve the appropriate weighted or single deep flag.

verify_linear_bootstrap_B34_0p11322.py checks all 80 full-face supports,
2235 vertex inequalities and five count ranges, and directly invokes the
independent short-arc checker before accepting either final row. The
minimum of the five final area margins is

    136785503193493452653/(5*10^23) > .000273571006.

The final M22 and M24 margins exceed .00265107 and .00145166. Every
integer M>=22 is excluded. The positive strict margins pass through the
inherited generic-limit argument. Other boundary counts and any global
radius theorem are separate obligations.

The numerical proposal generator does not accept any inequality. The
replay uses integer/rational outward interval arithmetic and must run
without Python's -O flag.

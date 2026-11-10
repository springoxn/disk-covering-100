# Exact B33 exclusion at .11312 with full marked-apex angles

This is a B33 branch for R=707/6250=.11312, not a theorem identifying the
exact optimum. Its completion with other boundary counts is separate.
The earlier completed checkpoints are unchanged.

## 1. Exact starting domain

The separate checker check_one_ear_structure_0p11312.py and its proof in
lower_bounds_extension_20261004 establish m100,I67,F165, q0 angles in
(.39,pi/2+.25), good marked apex angles in(.4,pi), interior degrees5 through16,
and no interior vertex with five boundary neighbors. The K4 test excludes
all-boundary q0/q1 faces and the two-ear test leaves e0 or1. Every full
assigned arc is greater than.0695, so its normalized half-chord sine is
greater than.307. Boundary chords and q0 faces with two boundary centers
remain allowed.

The degree-five lemma does not assume acuteness. The global single-angle
triangle support Q(alpha)=sin(alpha)(1+cos(alpha)) is bounded on[0,pi] by
its slope-1/2 tangent at2pi/5. The global unpenalized marked envelope is
also bounded by its slope-1/2 line. Summing these supports over a degree3
or4 complete star gives a deficit greater than.84467, while the current
old normalized area-loss budget is less than.562. The degree upper bound
uses every interior angle greater than.39. No obsolete acute-apex premise
is carried into this proof.

## 2. Sharp simultaneous radial center support

Use lambda=39/1000 and normalized sine domain[.307,1]. The endpoint-lens
displacement expansion and cyclic squared-edge summation are inherited
from the earlier exact proofs. Their tangential loss is retained, rather
than discarding favorable but incompatible neighbor movements.

SHARP_RADIAL_NODE_GUARD.md proves the new analytic guard. For s0=R*.307,
c0=sqrt(1-s0^2), h0=R*sqrt(1-.307^2), rho0=c0-h0, the exact checker proves:

- the neighbor tangential spread divided by the middle sine is below4;
- rho(a)*cos(a+b) increases with the neighbor half-arc;
- the resulting radial residual decreases with the middle half-arc;
- its endpoint maximum8lambda(rho0*s0^2+h0)-s0 is negative.

Hence every residual node support is nonpositive. The actual circular outer
contribution plus lambda times all squared marked-edge lengths is bounded
by the corresponding radial-tip score. This proof works below the old
sine cutoff1/3 and does not need a three-variable numerical maximization.
The independent endpoint proof in the audit uses equivalent radical guards.

## 3. Exact stable radial-pair bound

The instance-based radial backend proves on the complete closed domain:

[H_R(2a)+H_R(2b)]/2+lambda*L0(a,b)^2
+(3/4)[(a-pi/33)^2+(b-pi/33)^2]
<=112497/10^7-(2374117/125000000)(a+b).

The stable length identity and derivative mean-value interval enclosure
are those proved in the .1131 checkpoint. The new replay visits1015 boxes,
accepts467 leaves and discards41 boxes only by exact exchange symmetry.
Consequently, with L=112497/10^7, mu=-2374117/125000000, gamma=3/2,

outer_actual+lambda*sum marked_edge^2
<=33L+2pi*mu-gamma*V,
V=sum(a_i-pi/33)^2.

All angular variables are genuine unequal assigned half-arcs. The diagnostic
uniform point is not an assumption or an acceptance criterion.

## 4. A global marked penalty envelope

GLOBAL_MARKED_EDGE_PENALTY_ENVELOPE.md gives a conditional endpoint proof
which is repeated directly for lambda=.039 in global_marked_penalty_backend.py.
The normalized good marked triangle-plus-anchor minus lambda times its base
square is bounded on the full apex interval[0,pi] by the concave function:

G_lambda(g)=sin(g)(1+2cos(g))-4lambda*sin(g)^2, g<=pi/3;
G_lambda(g)=sqrt(3)-3lambda-(1/2+2sqrt(3)lambda)(g-pi/3), g>=pi/3.

The proof checks the active circumradius endpoint through6/5, then the
unrestricted convex z-score at6/5 and13/5, then the constrained high-angle
endpoint and its bound by pi-g. Every guard passes for.039. The high-angle
line is evaluated before the low-angle derivative expression, so a full
apex interval never accidentally calls a trigonometric routine at2pi.
This is a genuinely global envelope, unlike the acute-only.06 version.

## 5. Counting every p3 footprint without double charging

In the e0 branch, let k be the number of p3 apices. The K5 neighbor bound
forces each into one contiguous three-edge marked fan: three disconnected
cycle edges would use at least five boundary sites. Their four-site blocks
overlap only at adjacent endpoints. MULTIPLE_P3_FOOTPRINT_VARIANCE.md proves
by weighted Cauchy and exact integer overlap counts that

V >= (33/133)*(4pi/33-L4/2)^2*k,
L4=3463/5000=.6926.

The exact checker verifies sin(L4/2)>3R and the11 integer cases, including
the k11 whole-cycle exception. This allows one constant charge per p3 star.
The geometric inequality is derived for actual integer multiplicities;
the subsequent continuous LP merely relaxes those multiplicities.

In the e1 branch, instead use the ear's three-arc footprint
L3=2283/5000=.4566, with sin(L3/2)>2R. Cauchy gives

V >= (3pi/33-L3/2)^2*(1/3+1/30).

The no-ear branch uses the multiple-fan charge, and the one-ear branch uses
the ear charge. They are never added against the same variance budget.

The normalized penalized ear cap remains

E=(1-sqrt(1-2R))/R+sqrt(1+16lambda^2)-4lambda.

It retains both negative marked-edge penalties. The radial slab controls
the center triangle, while each anchor-minus-edge term is bounded by half
of the displayed radical term. Those penalties cancel exactly the same two
edges in the positive radial sum.

## 6. Full-apex star domains and exact duals

Unmarked faces use the concave compatibility potential with coefficient
21/50, splice11027/10000 and endpoint pi/2+1/4. Its exact tangent endpoint
guard is repeated. The underlying face potential dominates normalized
triangle area by the zero-sum positive/negative deviation identity.

Every star type has p0 through3 and degree5 through16:48 types. For p>0,
the marked mean g is maximized over

max(.4,(2pi-j*(pi/2+.25))/p)
<=g<=min(pi,(2pi-j*.39)/p).

These are full-apex bounds from the current geometry and star closure, not
the old pi/2 cutoff. The mean q0 angle is(2pi-pg)/j. The boundary conjugate
also uses the actual q0 interval[.39,pi/2+.25]. Concavity gives the scalar
raw star score pG_lambda(g)+jphi((2pi-pg)/j)+eta*p*g.

For e0 subtract gamma*(33/133)*(4pi/33-L4/2)^2/R^2 from every p3 type.
For e1 do not subtract that type charge; its ear variance is subtracted
once from the global radial boundary bound instead.

The counts remain M=33-2e,U=132+e,sum x67,sum p*xM,sum j*x3U-N and
sum_(p>0)x<=N. The boundary q0-angle sum is Gamma+(e-2)pi. Therefore every
rational dual row gives center/anchor bound

R^2[67u0+M u1+(3U-N)u2+Nv+N C(eta)+(e-2)pi*eta+eE],

with the p3 type charge already included in its scalar inequalities when
e0. Add33L+2pi*mu, and for e1 subtract the single ear variance charge.

All84 no-ear and85 one-ear N cases pass, N11 through94+e. There are8112
checked scalar inequalities. The smallest strict area margin is

52113330775123282437/(5*10^23),

at e0,N24. Numerical optimization only proposes rational coefficients;
every sign is rechecked using outward-rounded integer arithmetic and
bounded rational series. The extra nonnegative m-slope guard is recorded
for later work but does not replace the present exact count bridge.

## 7. Replay and logical scope

Replay verify_radial_stability_support_0p11312.py and
verify_multiple_fan_star_0p11312.py with assertions enabled, together with
the separate same-radius structure checker. Actual results are saved in
radial_stability_support_0p11312_result.json and
multiple_fan_star_0p11312_result.json. The multiple-fan integer lemma and
global marked guards are called directly by the star verifier.

Genericity is handled by a compactness limit of slightly enlarged generic
covers with a fixed finite topology, not by claiming same-radius
perturbations preserve coverage. Closed coordinate, arc, angle and area
inequalities pass to that limit; the strict final margin contradicts it.

This completes the B33 branch conditional on the inherited Voronoi/Delaunay
reduction and explicitly replayed same-radius structural premises. A
universal .11312 lower bound additionally needs the remaining B branches.
The exact optimum is still unresolved.

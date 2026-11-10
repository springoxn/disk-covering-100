# Complete-star area/perimeter support: recovered proof

This is a fresh equivalent reconstruction of the already independently
audited polygon-star theorem. It is not represented as the lost byte-identical
proof. The recovered scalar helper polygon_star_perimeter_support.py has
SHA256426c5eb338326931ce581d24697e1463815ed826ebfd24e926a1b12f9fa01a94.
Its582 sample checks supplement the derivation below; sampling is not the
proof of the geometric statement.

Let a complete interior center star in a simple straight triangulation have
d>=3 neighbors, with every incident circumradius at most R. Define

    theta=2pi/d, S_d=d*sin(theta)*(1+cos(theta)), T_d=d*sin(theta).

For its total area A_star and neighbor-cycle perimeter P_star, every a>=0
and real b satisfy the sharp local support

    a*A_star/R^2+b*P_star/(2R)<=max(0,a*S_d+b*T_d).

## 1. The polygonal isoperimetric inequality

Any simple d-gon of area A and perimeter P satisfies

    A<=P^2/[4d*tan(pi/d)].

A primary geometric reference is Beniamin Bogosel, A Geometric proof for
the Polygonal Isoperimetric Inequality,
https://arxiv.org/pdf/2309.05802 . The following argument is self-contained.

Convexification does not decrease area and does not increase perimeter.
Rescaling the hull to the fixed perimeter P, then inserting edge midpoints
if necessary, gives a convex polygon with at most d noncollinear vertices
and d labeled vertices. Up to translation, fixed-perimeter vertex tuples
lie in a compact set, so a maximal-area convex limiting polygon exists.
The supremum over all simple polygons equals this convex supremum, because
every simple polygon can be convexified and padded in this fashion.

A positive-area maximizer cannot have fewer than d effective vertices.
Pad such a polygon with distinct collinear edge points. At one padded point
displace the vertex outward by epsilon. The oriented area increases to first
order by half the sum of the adjacent edge lengths times epsilon, whereas
the perimeter changes only by O(epsilon^2). The perturbation remains simple
for sufficiently small epsilon; it need not remain convex. Rescaling to P
therefore increases area, contradicting the equal simple/convex supremum.
The same argument rules out any collinear vertex. Thus the maximizer is
strictly convex, has positive edges and all turns in(0,pi).

Write e_(i-1),e_i for its incoming/outgoing unit edge vectors and l_(i-1),l_i
for their lengths. With J the counterclockwise right-angle rotation, the
area and perimeter gradients at vertex i are

    -(1/2)J(l_(i-1)*e_(i-1)+l_i*e_i),
    e_(i-1)-e_i.

Lagrange multipliers apply at the strict maximum. Homogeneity gives their
multiplier mu=2A/P>0. Dotting their equality with e_(i-1)+e_i shows the
adjacent lengths are equal, since the turn has nonzero sine. Taking norms
then gives mu=(l/2)*cot(turn_i/2). The cotangent is strictly decreasing on
(0,pi/2), so all turns are equal. Their sum is2pi, and the maximizer is
regular. Its area is the displayed bound. Degenerate limits follow by
continuity; nonconvex polygons were already handled by convexification.

## 2. The actual star perimeter bound

The link of a complete interior vertex is a simple neighbor cycle. Its
incident triangles have disjoint interiors, fill that polygon, and have
central angles alpha_i in(0,pi), summing to2pi. Each opposite side has
length L_i=2r_i*sin(alpha_i)<=2R*sin(alpha_i). Sine concavity gives

    P_star<=2R*d*sin(2pi/d)=2R*T_d.

Apply the polygon inequality to the actual neighbor coordinates:

    A_star/R^2<=T_d^2/[d*tan(pi/d)]=S_d.

This includes the sharp shared-coordinate degree-three value S3=3sqrt(3)/4.
An earlier angle-only cap2 remains valid but is weaker; it is not invalidated.

## 3. Both signs of the perimeter coefficient

Put x=A_star/R^2, p=P_star/(2R), and c=d*tan(pi/d). The polygon inequality
gives p>=sqrt(c*x), while the preceding bounds give0<=x<=S_d and p<=T_d.
If b>=0, the two terms are bounded separately. If b<0,

    a*x+b*p<=a*x+b*sqrt(c*x).

The right side is convex in x on[0,S_d], so its maximum occurs at0 or S_d.
Since c*S_d=T_d^2, these endpoints are0 and a*S_d+b*T_d. This proves the
claimed support for every a>=0 and every real b.

## 4. Sharpness and closed limits

Place the d neighbors regularly at radius2R*cos(pi/d) around their center.
Each incident triangle has circumradius R, and its neighbor polygon is
regular, attaining both preceding bounds. Scaling those coordinates toward
their center approaches the zero endpoint. These are local extremizers,
not claimed100-disk covers.

Fixed-topology degenerate limits preserve the area, lengths and inequalities
by continuity. Thus the theorem fits the inherited enlarged-cover endpoint
argument even when a limit link ceases to be strictly simple.

## 5. Scope of a global use

For a deep unmarked degree-five vertex, all neighbors are interior; its five
opposite edges are II and their outside faces are q0. Signed half-edge
potentials can cancel its perimeter penalty with those outside faces.
For a marked star, perimeter edges or outside faces may be marked, requiring
additional boundary/anchor support. A finished global face dual cannot simply
be reduced by a new constant: affected area coefficients and corner potentials
must be reserved or replaced coherently, and overlapping neighborhoods cannot
be charged twice. This proof alone establishes no new covering-radius bound.

# A global degree window from sharp star areas and anchor caps

Assume the inherited simple center triangulation has more than one
interior vertex. All complete interior center stars have angle sum2pi,
and every selected triangle has circumradius at most R. Let

    A=3sqrt(3)/4, kappa=461134488/10^9,
    h0=1/2-kappa>0.

Use the original nonnegative joint face-loss budget d: its total area
allowance minus pi, divided by R^2. This includes the original H boundary
upper bound. If an incident star has degree d_v and p ordinary marked
faces, its old allowance is d_v*A+p*kappa. The sharp complete-star cap
from COMPLETE_STAR_AREA_CAPS.md bounds its center-triangle sum by S_(d_v).
Each of its p distinct marked anchors has area at most R^2/2. Therefore
that one star incurs mandatory normalized loss at least

    d_v*A-S_(d_v)-p*h0.                         (1)

The incident faces and anchors are counted exactly once in this local
replacement. It is not an additional loss to stack on a dual which has
already spent the same faces.

## 1. Why p is at most d_v-1

If every face in an interior star were a q1 face, its cyclic neighbor
edges would all be marked outer-boundary edges. A closed cycle in the
simple outer boundary cycle must be the entire boundary cycle. The
star would therefore cone off the whole disk, leaving that center as
the only interior vertex. The assumed interior count greater than one
rules this out. q2 ears have no interior vertex, and all-boundary marked
faces likewise cannot belong to an interior star. Thus p<=d_v-1.

## 2. Minimum degree five without acute assumptions

For degree three, S3=2 and p<=2. Formula(1) gives loss at least
3A-2-2h0. For degree four, S4=4 and p<=3, giving

    D4=4A-4-3h0=3sqrt(3)-4-3*(1/2-kappa).

The three-degree loss is larger. Consequently every interior degree is
at least five whenever the old normalized budget is strictly below D4,
approximately1.07956. No actual-angle window, acute marked-apex premise,
or maximum marked-incidence hypothesis is needed.

## 3. Degree at most eight under the same budget

For a real degree parameter z>=9, put t=2pi/z and
S(z)=z*Q(t), Q(t)=sin(t)*(1+cos(t)). The worst anchor allowance uses
p=z-1, so define

    L(z)=z*A-S(z)-(z-1)*h0.

Its derivative is A-h0-[Q(t)-t*Q'(t)]. On0<t<=2pi/9, Q''(t)<0, so
Q(t)-tQ'(t) increases with t. The exact checker proves

    A-h0-[Q(2pi/9)-(2pi/9)*Q'(2pi/9)]>0.

Thus L(z) increases for z>=9. Every degree at least nine therefore
has loss at least

    D9=9A-S9-8h0.

The checker proves D9>D4. Hence the same condition budget<D4 forces
the full integer degree window5 through8. This conclusion remains valid
even if a previous p<=3 footprint condition ceases to hold.

## 4. Scope and exact checks

verify_global_star_anchor_degree_window.py rechecks the original kappa
certificate, the exact star constants, the monotonic derivative margin,
and sample B33 old budgets through R=.11323. At each radius its use must
be accompanied by the actual old-budget and complete-star hypotheses.
The statement is a necessary degree restriction; it is not a global new
covering-radius exclusion on its own.

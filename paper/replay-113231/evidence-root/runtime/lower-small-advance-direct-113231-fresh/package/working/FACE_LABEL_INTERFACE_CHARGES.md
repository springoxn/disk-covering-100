# Mandatory boundary-interface charges in a finite face-label dual

This is a conditional refinement of the full-face label method. It is not
an accepted numerical radius certificate by itself.

Assume a center triangulation has an outer boundary cycle, every q1 marked
face has an interior apex, and no marked fan runs around the whole boundary.
The last condition follows, for example, from a bound q<=3 or q<=4 that is
strictly smaller than the boundary length. Ears and boundary chords may be
present. Distinguish the boundary corner tag b from interior potential tags.

For each interior tag l choose a nonnegative interface credit delta_l.
Suppose the exact full-simplex support for every actual q0 face f proves

    area_f/R^2 + sum l_i*(alpha_i-pi/3)
      <= A + sum p(l_i) - sum_{BI edges of f} delta_(interior tag).

This is a local face inequality; its right side reserves one credit for
each boundary-to-interior edge in that face. It can be checked by the same
finite multiset conjugates as the existing face-label support. Boundary and
interior tags must remain distinguished even if their numerical potentials
happen to coincide.

Consider an interior vertex v with at least one marked incidence. Each
maximal consecutive component of its incident marked faces is a fan. Every
fan has two distinct terminal BI edges. Across such an edge lies a q0 face:
another q1 would extend the fan, while an all-boundary face cannot contain
the interior endpoint. A marked cycle would use the complete boundary and
is excluded by the premise. Thus at least two q0 face-edge incidences carry
credit delta_(tag(v)).

Terminal edges belonging to different interior vertices are distinct. A
q0 face may carry two such edges, but its displayed support has explicitly
reserved both credits. Hence summing the local inequalities gives an extra
global deficit at least

    2 * sum_{interior vertices with q_v>0} delta_(tag(v)).

It is therefore safe for the vertex dual inequality to include the extra
right-hand allowance `2*delta_(tag(v))*1_(q_v>0)`: the reserved face deficit
pays it exactly once. Nonterminal BI edges only create further unused
nonnegative deficit. No graph enumeration or disjoint-face assumption is
needed.

## Three-label specialization

If tag a is used on high-degree interior vertices, tag0 on other interior
vertices, and b on the boundary, reserve only delta_a=delta>=0. The numbers
of a-b edges in the three mixed multisets are:

- (a,b,0): one
- (a,a,b): two
- (a,b,b): two

Other multisets have none. Thus those three exact face gaps must be at
least delta,2delta,2delta. Every marked high-degree vertex then receives a
paid allowance2delta in its vertex support. This reservation is disjoint
from a separately proved outer half-arc variance deficit: one is a q0
face-support improvement and the other is an outer-area improvement.

A linear proposal solver can optimize the charges p(l), the credits
delta_l and its vertex-dual coefficients simultaneously. Final acceptance
still requires exact replay of every tagged face support, every vertex
inequality, all incidence premises, and the complete area comparison.

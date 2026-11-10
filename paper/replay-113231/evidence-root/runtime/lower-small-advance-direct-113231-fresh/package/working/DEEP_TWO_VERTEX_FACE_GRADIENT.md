# Two deep vertices:51 face signatures and shared-edge conservation

Let a simple straight triangulation of a disk have two distinguished interior
vertices P1,P2. They are deep: neither has an original boundary vertex as a
neighbor. Assume every interior vertex adjacent to P1 or P2 has degree at
least4. Global minimum interior degree5 is a sufficient stronger premise.
The other interior vertices may be partitioned into arbitrary labels H,O;
original boundary vertices receive label B, and P1,P2 receive label P.

For a q0 triangular face f and each corner i, let o_i indicate that corner i
has label P. Let e_i indicate that the third vertex of the face across the
opposite edge has label P. On a q0/q1 interface set e_i=0. Then:

1. A face containing P has no B corner, and it has at most two P corners.
2. If the opposite edge touches B then e_i=0, by depth of each P.
3. The external opposite vertices counted by e_i are distinct and are not
   vertices of f. Hence sum o_i+sum e_i<=2.

To prove the only nontrivial assertion, suppose one external P lies across
two edges of f. Those edges share a vertex A, which neighbors P and is
therefore interior. The face f and the two adjacent faces give all three
edges of a3-cycle in A's vertex link. An interior link is one simple cycle;
each of those three link vertices already has its two incident link edges,
so the entire link is that3-cycle. Thus A has degree3, contradicting the
assumption. A third vertex across an edge cannot be one of f's vertices
in a simple geometric triangulation.

## Exhaustive signatures

Use one unordered own-label triple from H,B,O,P and retain all ordered
external binary triples satisfying the displayed restrictions. There are
15 own triples and51 signatures:

- ownP0:37 signatures, split28 with no B,6 with one B,2 with two B,
  and1 with three B
- ownP1:12 signatures
- ownP2:2 signatures.

The checker regenerates these lists and verifies every restriction. It does
not claim that all51 signatures are geometrically attainable; retaining
extra signatures is safe for an upper support.

## Exact metric cancellation

Give each q0 face a scalar potential phi_f=tau*sum o_i, with tau>=0.
Across a shared q0 edge, the signed coefficient on the side opposite
corner i of f is

    phi_g-phi_f = tau*(e_i-o_i),

because the two shared endpoints cancel. Assign that coefficient to
L_edge/(2R). On the other face its coefficient is the negative, so the
physical edge-length terms cancel regardless of the two circumradii.

A q0/q1 interface is a boundary/interior edge. Its q0 face cannot contain P
since P is not adjacent to B; its q1 face likewise cannot contain P.
Both face potentials are zero, justifying the zero coefficient at that
interface. No boundary-length correction is omitted.

Each P incidence in a q0 face has exactly one opposite-edge neighbor.
That edge has two interior endpoints, so the other face is also q0.
Consequently total external-P incidences equal total own-P incidences.
If both P sites have degree5, both totals are10.

Thus for any free scalar xi, a local allowance containing

    xi*(sum e_i-sum o_i)

sums to zero globally. The full face score is its ordinary area and corner
potential score plus sum_i tau*(e_i-o_i)*sin(alpha_i) at unit circumradius,
with the usual rho endpoint reduction for actual circumradius<=R.
The generic exact signed-sine backend applies when its explicit range/
negative-coefficient guard holds, and all simplex boundary edges must
remain included.

This is only a geometric incidence/support construction. A radius exclusion
also needs valid ordinary vertex counts and angular supports, a coherent
single area budget, exact coefficient acceptance, and a proof that two such
distinguished vertices exist in the particular branch. No radius or new
global degree profile is asserted here.

# Deep witnesses for the compulsory core-curvature flags

Call an interior center deep if it has no boundary-center neighbor in
the center triangulation. This is a graph-theoretic definition; no
metric distance or equilateral realization is assumed.

Every vertex strictly inside a face-bearing block of the induced
interior graph is deep and retains its entire original star. An edge
from such a vertex to a boundary center would have to cross the block's
simple outer cycle. This is the same retained-degree argument used by
the audited block isoperimetric proofs.

Consequently the core-obstruction flags can be strengthened as follows.
With m100, B in{32,33,34}, and M=U-2e:

* M<=25 forces at least one deep interior vertex of degree at most5;
* M<=23 forces sum over deep vertices max(6-d,0)>=2.

For the first statement, otherwise every strict block interior degree
would be at least6, and summing F<=b^2/6 over blocks would contradict
Fcore>=198-2B-M>=130-M and total frontier<=M. For the second, if the total deep
positive curvature were at most1, every block would satisfy F<=b^2/5;
the same bounds contradict M<=23. The forced vertices need not be
distinct degree-five vertices; degrees3 and4 carry weights3 and2.

## Face-label consequence

Assign a distinguished potential P only to deep vertices with d<=5.
They necessarily have marked incidence p=0. Assign the ordinary zero
label to other low-degree unmarked vertices. The vertex dual must check
both classes of p0,d3/4/5 types, applying the compulsory negative flag
only to the deep class.

A q0 triangle cannot contain both the distinguished P label and a
boundary-vertex label: every pair of vertices in that triangle is an
edge, which would give the deep vertex a boundary neighbor. Therefore
all label triples containing both classes may be omitted from the
complete face-support list. With four labels (high-degree interior,
boundary, ordinary interior, distinguished deep),16 of the20 unordered
triples remain. All16 must still be checked, including repeated deep
labels; no uniqueness or separation of multiple deep witnesses is
assumed.

The distinction concerns the topological label classes even if two
numerical potential values happen to coincide. All usual centered-angle
and degree-count identities remain valid because each actual vertex
receives exactly one label and one applicable vertex inequality.

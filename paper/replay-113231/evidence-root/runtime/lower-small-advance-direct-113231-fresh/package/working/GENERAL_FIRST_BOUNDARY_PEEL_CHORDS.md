# First boundary peeling with chords

Let a simple triangulated disk have a boundary cycle of length P and at
least one strictly interior vertex. Write D=sum(deg(v)-6) over its strict
interior vertices, C for the number of boundary chords, and f_j for the
number of triangular faces with exactly j boundary vertices. Removing
the boundary vertices leaves an induced planar graph, possibly with cut
vertices, bridges, isolated vertices or several components.

Every bounded face of this induced graph is an original triangle: an
original boundary vertex cannot lie inside a cycle of interior vertices.
Its total outer facial walk length, counting bridges twice, is b=f_1.
This follows by counting the original triangles on the two sides of each
interior-interior edge. There are no missing bounded holes.

Count boundary-boundary face incidences and boundary-interior edges:

    f_2+3f_3=P+2C,     E_BI=f_1+f_2.

Consequently the boundary degree sum is 3P+4C+f_1-3f_3. The disk Euler
curvature identity then gives

    b=P-6-D-4C+3f_3.

The deleted face count is f_1+f_2+f_3=P+b+2(C-f_3). The C noncrossing
chords divide the boundary polygon into C+1 regions; at least one region
contains an interior vertex. Every all-boundary triangular face is a
distinct empty region, so f_3<=C. Set a=C-f_3>=0 and L=P-6-D. Then

    b=L-C-3a,     deleted faces=P+L-C-a.

Suppose every remaining cyclic block satisfies F_j<=P_j^2/k. Strict
interior vertices of a cyclic block retain their complete original
stars. Summing the block bounds, using sum P_j<=b, yields

    F <=P+L-C-a+(L-C-3a)^2/k <=P+L+L^2/k.

If C>=1, the sharper upper bound P+L-1+(L-1)^2/k holds. These comparisons
assume b>=0, as the exact counting identity guarantees.

When C=0 the induced interior graph is connected. To see this without
assuming a simple frontier, traverse the original boundary. Each
boundary edge has an interior third vertex. At a shared boundary vertex,
the two successive third vertices are joined by the chain of interior
neighbors in its vertex link. This gives one connected frontier walk
containing every interior vertex adjacent to the original boundary.
Every induced-interior component must contain such a vertex, since the
original disk graph is connected. Hence there is only one component.

This is a reconstructed statement of the previously independently
audited chord-aware peeling argument. Its combinatorial equalities do
not require flat development, convexity, or a chordless initial disk.

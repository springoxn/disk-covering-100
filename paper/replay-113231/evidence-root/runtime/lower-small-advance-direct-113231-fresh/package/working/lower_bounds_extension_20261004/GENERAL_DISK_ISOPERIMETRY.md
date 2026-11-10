# Combinatorial isoperimetry with nonpositive interior curvature

## Theorem

Let a finite simple plane graph triangulate a closed topological disk. Its outer boundary is a simple cycle of length B>=3. Let F be its number of triangular faces, excluding the exterior face. If every vertex strictly inside the boundary has degree at least six, then

    F <= B^2/6.

Thus F<=floor(B^2/6). No metric realization, flat lattice, convex boundary or simple first-layer frontier is required.

## Proof by induction on F

The triangle with no interior vertex is immediate. Disks of boundary length at most five have no interior vertices under the degree hypothesis: the disk curvature identity

    sum_boundary(4-degree)+sum_interior(6-degree)=6

forces a degree-two boundary vertex whenever all boundary degrees are at least three would give a sum at most five. A degree-two vertex is an ear. Removing it preserves every interior vertex and its degree and reduces the boundary length. Repeating reaches boundary length three, where an interior vertex would require all three boundary degrees at least three and contradict the same identity. The remaining face count is B-2, which is at most B^2/6 for B=3,4,5.

### Case 1: a boundary chord

Split the disk along an edge joining two nonconsecutive boundary vertices. The two resulting disks have boundary lengths b1,b2>=3, with b1+b2=B+2, and strictly fewer faces. Each vertex interior to either subdisk retains its original degree. By induction,

    F <= (b1^2+b2^2)/6.

For B>=5 the maximum at fixed sum and b1,b2>=3 is attained at 3,B-1, so

    b1^2+b2^2 <= 9+(B-1)^2 <= B^2.

The B=4 case consists of the two triangular subdisks already covered by the small-boundary argument.

### Case 2: no boundary chord

For B>3, every face incident to a boundary edge has exactly one interior vertex. There are B such faces, one per boundary edge. Every other face meeting the outer boundary has exactly one boundary vertex and two interior vertices; let U count these faces. No face has two nonconsecutive boundary vertices, since their connecting edge would be a chord.

Let h count edges joining boundary and interior vertices, and put

    D=sum_interior(degree-6)>=0.

Boundary degrees sum to 2B+h. The curvature identity gives

    h=2B-6-D.

Counting face incidences at boundary vertices gives 2B+U=B+h. Consequently

    U=B-6-D <= B-6.

Deleting every boundary vertex and its incident faces removes exactly B+U faces. Retain the induced graph H on all original interior vertices, including its isolated vertices and bridge edges.

### Why a nonsimple stripped frontier is harmless

Every bounded face of H is an original triangular face. Indeed, any simple cycle made of interior edges lies strictly within the original disk and encloses no original outer-boundary vertex. All original triangles in its interior therefore survive the deletion. A bounded hole or nontriangular bounded face of H would contradict this observation.

For each connected component of H, traverse its exterior boundary walk, counting a bridge twice. The sum of these walk lengths is U: every oriented exposed interior edge has, on its removed side, exactly one original face with one outer vertex and two interior vertices. Conversely each of the U removed faces supplies precisely that oriented edge. Isolated vertices contribute length zero.

Split H at articulation vertices into its maximal two-connected blocks and ignore bridge blocks, which have no triangular faces. Each remaining block triangulates a disk with a simple boundary of length P_a>=3. The sum of their boundary lengths is at most U; unused bridge edges account for the omitted twice-counted length. Their bounded triangular faces partition all surviving faces.

A vertex strictly interior to such a block retains its entire original star: any edge or deleted triangle leading outside the block would have to cross its simple boundary. Hence its degree is still at least six. Each block has fewer faces than the original disk, so induction gives

    F_core <= sum_a P_a^2/6 <= (sum_a P_a)^2/6 <= U^2/6.

This argument allows disconnected components, bridges and repeated vertices in the stripped exterior walks.

Finally,

    F <= B+U+U^2/6
      <= B+(B-6)+(B-6)^2/6
      = B^2/6.

The second inequality uses U>=0, B>=6 in this nontrivial chordless case, and monotonicity of U+U^2/6. This completes the induction.

## Consequences for the admitted .11309 core profiles

Assume the separately proved simple-core topology, 67 core vertices, boundary length N and all strictly interior core degrees at least six. The core has F_core=132-N faces.

- N=25 is impossible, since 107>25^2/6.
- For N=26,F_core=106, a boundary chord is impossible: splitting would give at most (3^2+25^2)/6=105+2/3 faces.
- That N26 core is therefore chordless. If its strictly interior degree excess D is at least one, U<=26-6-1=19, and the proof gives F_core<=26+19+19^2/6=105+1/6, again impossible.

Thus an admitted N26 degree-seven vertex cannot be deep; it must be on the ring. These are conditional structural exclusions, not a universal radius theorem. The .11309 coarse profile and simple-ring premises remain separate dependencies.

# A radius-independent B35 M25 core-profile obstruction

Consider a generic simple straight center triangulation for 100 effective centers, with 35 boundary centers. Let e count two-marked-side ears, b count all-boundary one-marked-side faces, and U count q0 boundary-angle occurrences with multiplicity. Suppose

- e=b=0 and U=25;
- every one of the 65 interior vertices has degree six or seven;
- every degree-seven vertex is an ordinary marked apex with four marked boundary edges.

Then this profile is impossible. No radius, arc minimum, actual-angle cap, lattice development or fan-contiguity assumption is needed. The complete boundary cycle and the previously proved general-disk isoperimetry are the inherited structural dependencies.

## 1. The induced interior graph is connected

Let c≥1 count components of the induced interior graph, and n_j count q0 triangles with j original boundary vertices. Its bounded faces are exactly the n_0 original three-interior triangles. A retained cycle cannot surround an original boundary vertex, so there are no unfilled bounded holes. The general Euler identities give

`n_2+n_3=e+2(c−1)=2(c−1)`

and, since M=U−2e=25,

`F_core=103+2(c−1)+n_3`,

`P_walk=n_1=25−4(c−1)−n_3`.

Every vertex strictly inside a face-bearing induced-core block retains its full original interior star. Its degree is at least six. Apply GENERAL_DISK_ISOPERIMETRY.md to every such block; their simple boundary lengths sum at most P_walk, with bridges counted twice in that walk. Thus `F_core≤P_walk²/6`.

If c≥2, this would imply `105≤21²/6`, impossible. Therefore c=1, n_2=n_3=0, F_core=103 and P_walk=25. In particular all-boundary q0 faces and q0 faces with two original boundary vertices have been eliminated by the argument, not assumed away.

## 2. One simple chordless core disk

A bridge consumes two occurrences in the outer facial walk, leaving total face-bearing block perimeter at most 23. This would imply `103≤23²/6`, impossible.

If two or more face-bearing blocks remained, their perimeters are at least three and sum at most 25. Their squared sum is at most `3²+22²`, giving `103≤(3²+22²)/6`, also impossible. Connectedness and the absence of bridges leave no extra acyclic vertices. The induced core is consequently one 2-connected triangulated disk with 65 vertices, 167 edges, 103 faces and simple boundary length 25.

A chord of that core boundary splits it into two triangulated disks whose boundary lengths sum 27, each at least three. Strict subdisk interior vertices retain their full core stars, so general-disk isoperimetry would give

`103≤(3²+24²)/6=97.5`,

a contradiction. Thus the core boundary is chordless.

Every core vertex has induced-core degree at least three. Strict interior vertices retain degree at least six. A boundary vertex of induced-core degree two would have only its two boundary neighbors, whose joining edge is a boundary chord when boundary length exceeds three. This is excluded.

## 3. A degree-seven/four-marked apex is impossible

The four distinct marked boundary edges assigned to such an apex form a proper subgraph of the original 35-cycle. A proper subgraph consisting of four cycle edges is a union of paths and has at least five distinct endpoint vertices. Every endpoint is an original boundary neighbor of the apex. This remains true for split fans; contiguity is unnecessary.

The apex therefore has at least five boundary neighbors. Full degree seven leaves at most two induced-core neighbors, contradicting the induced-core minimum degree three from section 2.

Finally the full triangulation incidence identity gives

`sum_interior(degree−6)=B−6+e−b−U=4`.

Under the assumed degree window there are exactly four degree-seven vertices. Each is impossible by the preceding argument. Hence the entire profile is impossible.

More generally, in this chordless-core situation a proper marked set of q boundary edges has at least q+1 boundary neighbors, giving `degree−q≥4` for any marked interior vertex. The forbidden type here is degree7/q4.

## Scope and exact checks

`verify_B35_M25_core_profile_obstruction.py` checks the integer face/frontier, block/chord and degree-endpoint comparisons. The written topology proof above is essential; the arithmetic checker is not a substitute for it. Any radius-specific covering theorem must independently prove the stated profile assumptions with its current-radius inequalities. The already audited finite-type limiting argument handles threshold degeneracies after this obstruction is applied to generic covers.

# Independent audit: one-unit positive-curvature disk isoperimetry

PASS, 2026-10-04 UTC. For a finite simple triangulated disk with boundary b≥3 and total positive strict-interior curvature `K=sum max(6−degree,0)≤1`, the stated theorem `F≤b²/5` is sound. This is a combinatorial theorem and weighted core filter, not a covering-radius exclusion.

Both an independent focused reviewer and I inspected the full induction. For b≤4, the curvature identity forces a boundary degree-two ear if interior vertices existed; ear removal preserves strict-interior vertices and degrees, and reduces to the triangular base. Chord splits inherit the positive-curvature budget. In the chordless case, the stripped frontier is `U=b−6+sum(6−degree)≤b−5`; the removed face count is b+U. Face-bearing induced-interior blocks have simple boundaries with total perimeter at most U, no unaccounted holes, and their strict interiors retain full original stars. Applying the induction blockwise gives `F≤b+U+U²/5≤b²/5`. Bridges, articulation vertices, disconnected components and isolated vertices cause no missing area term.

The general shifted induced-core identities give `F_core≥2I−2−M`, frontier≤M, with M=U−2e. Every strict core-block interior vertex is unmarked. Thus, for B33,m100,M≤23, the integer gap `5(132−M)−M²>0` forces at least two units of unmarked positive curvature. A local dual allowance with `−f max(6−degree,0)` on unmarked vertices therefore permits a final deduction 2f. This does not assert two distinct degree-five vertices.

Fresh standard-library checker replays passed. The reviewer also checked optimized-mode rejection. The earlier general-disk F≤b²/6 proof and inherited simple-plane-disk hypotheses remain dependencies; the new factor 1/5 is proved here rather than taken from an external source.

SHA-256 bindings:

- `ONE_POSITIVE_CURVATURE_ISOPERIMETRY.md`: `2f293c5ebb259b078bf47d6be8552062c6a81c0bcd2932940df322836922352d`
- `verify_one_positive_curvature_isoperimetry.py`: `f16a50aa3c9abefcf35d5c6fdc7d16a031afff1da3b1322d3fdafd8aa882a275`

No reviewed source was changed.

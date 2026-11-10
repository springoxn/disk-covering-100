# Independent audit: full-simplex supports with range below one

PASS, 2026-10-04 UTC. The new range<1 area-plus-linear-corner-potential theorem is sound. It establishes a support bound, not a covering-radius exclusion or actual-angle acuteness.

I independently derived the nonacute interior-maximizer contradiction. With alpha≥pi/2, c=−cos(alpha)≥0 and z=cos(beta−gamma)>0, the sum-preserving direction (1,−1/2,−1/2) has second area derivative `sin(alpha)(4c−z)`. Local maximality implies 4c≤z. The opposite inward derivative is `1−2c²+cz=1+c(z−2c)≥1`. Its linear-potential derivative is at least minus the label range, hence greater than −1. A positive total inward derivative contradicts maximality.

On the closed simplex boundary, the area term is identically zero, so its largest linear value occurs at a simplex vertex. Consequently the full bound must be the maximum of the acute sine-conjugate supporting expression and `pi(max(lambda)−mean(lambda))`. The degenerate cap cannot be silently omitted. The source test exercises a case where it strictly dominates.

I inspected the code and freshly replayed the exact algebraic/sample checks. The function correctly states that its returned interval encloses the chosen supporting expression, rather than the exact constrained supremum for an arbitrary nonoptimal nu. Its upper endpoint is the valid face bound. The caller must retain enabled assertions and check strict range<1 for every face multiset.

For a triangle of circumradius≤R, normalized area is at most the simplex area term, so this applies without restricting its actual angles. Additional shape-dependent signed edge-length or squared-edge penalties are outside this theorem; they need their own localization or full-shape bound.

SHA-256 bindings:

- `FULL_FACE_RANGE_ONE_SUPPORT.md`: `72680706132cc5c53996caed9081532c4912b22b16ff6e81d3c9d6a10afaceea`
- `exact_range_one_face_support.py`: `a33023537a5f20e406e2fac79dc16f6ce79ac152798e08563a7097e48a1414ef`

No reviewed source was changed. Current frozen radius checkpoints do not depend on this extension.

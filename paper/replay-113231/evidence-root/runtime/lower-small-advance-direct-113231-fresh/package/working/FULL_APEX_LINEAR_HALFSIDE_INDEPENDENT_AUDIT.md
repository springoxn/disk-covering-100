# Independent audit: full-apex linear-halfside marked conjugate

PASS, 2026-10-04 UTC. For 0≤k≤1 and any real rational apex multiplier s, the helper's complete marked-face conjugate is valid. This is a scalar support lemma, not a radius exclusion.

I independently derived the fixed-base reduction. With normalized half-base x and actual apex gamma, circumradius≤R gives `asin(x)≤gamma≤pi−asin(x)`. The score is bounded by `x²cot(gamma/2)+x sqrt(1−x²)−kx+s gamma`, convex in gamma, so its maximum is at one of the two endpoints. Setting a=asin(x) gives

- acute: `(1−k)sin(a)+sin(2a)+s a`;
- obtuse: `(1−k)sin(a)+s(pi−a)`.

Both are concave on [0,pi/2], including k=1. The exact endpoint tangent continuations match values and derivatives; increasing-continuation lower endpoints are taken from the feasible exact pi/2 value. The same previously audited outward root-bracket arithmetic then encloses each maximum.

I inspected the implementation and independently evaluated 33 parameter/multiplier cases with closed-form stationary roots and the separate exact acos backend, including negative, zero and large positive multipliers and k=0,.24,1. Every interval overlaps the bisection conjugate. For the acute branch the stationary cosine solves `4c²+(1−k)c+s−2=0`; for the obtuse branch it is `c=s/(1−k)` in its interior regime. Endpoint regimes were evaluated directly. These checks supplement, rather than replace, the complete convexity/concavity proof.

No actual-apex acuteness, actual-center radial assumption or lower-radius support bound is used. The cache key includes both k and s, and the resulting normalized support is independent of radius. The invoking certificate must retain enabled assertions and bind the intended parameter.

SHA-256 bindings:

- `exact_linear_halfside_marked_conjugate.py`: `12308a08e76ead613dc36555bc16026bfaf0ea928dda6f18d18b1f4e8ccc23e4`
- `FULL_APEX_LINEAR_HALFSIDE_CONJUGATE.md`: `185362d74fb02d89ecb07472b3f4efc71c8bbb301ce3ef49eb2617f76f7c5356`

No reviewed source was changed.

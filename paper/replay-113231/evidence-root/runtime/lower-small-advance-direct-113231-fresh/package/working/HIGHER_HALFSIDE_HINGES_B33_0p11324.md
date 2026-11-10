# Larger half-side multipliers at R=.11324

This supplement contains three conditional scalar supports for the B33
boundary functional. It does not assert a new covering-radius bound.
The geometry is EXACT_NORMALIZED_LENS_PENALTY.md, and the tighter affine
interval enclosure is TIGHT_EXACT_LENS_HINGE_0p11323.md. Whole-cover norm
normalization is required before diagram classification.

Set R=2831/25000, B=33. For each half-side multiplier k, form the theorem's
own F, P, and tangent deficit delta(t) at mu=pi/B. Its global nonnegative
deficit is checked independently for that same k and radius. The additional
exact hinge is delta(t)>=c*(T-t)_+ on the entire allowed half-arc domain.

| k | T | c | Exact minimum hinge margin |
|---:|---:|---:|---:|
| 23/50=.46 | 37/400=.0925 | 61/2000=.0305 | 109920429657721549/10^23 |
| 12/25=.48 | 93/1000=.093 | 1/40=.025 | 922530661643210449/10^24 |
| 1/2=.50 | 93/1000=.093 | 11/500=.022 | 6530493581701845763/10^24 |

Each instance uses1000 whole-envelope boxes and1000 additional hinge boxes.
No variance is reserved or spent by these supports. Increasing k improves
the negative marked-side term available to a center-face dual but decreases
the hinge available for shared endpoint ownership; the complete dual must
choose the tradeoff coherently. These different boundary inequalities must
not be added together as independent losses of the same signed outer area.

Executable: verify_higher_halfside_hinges_B33_0p11324.py. Its verify_case(i)
rejects unknown indices; verify() asserts PASS for all three fixed settings.
All floating computations only propose z tangents. Domain, derivative,
value and final acceptance checks use the outward exact interval backend.

For later joint footprint applications, the radius-dependent angle spans
must be refreshed too. At this radius .4569 is too short for a radius-2R
footprint: use a separately checked larger span such as .457. A radius-3R
span such as .6934 also needs its own exact sine guard. This scalar artifact
does not silently carry over any earlier ear, apex, degree or graph premise.

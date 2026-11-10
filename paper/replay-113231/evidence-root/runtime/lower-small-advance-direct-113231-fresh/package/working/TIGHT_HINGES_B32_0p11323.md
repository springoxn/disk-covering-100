# Exact B32 normalized boundary hinges at R=.11323

These scalar supports use EXACT_NORMALIZED_LENS_PENALTY.md and the
algebraically tightened affine enclosure in TIGHT_EXACT_LENS_HINGE_0p11323.md.
They are necessary-condition components, not covering-radius exclusions.
Normalize the entire hypothetical cover before forming its boundary cells.

Here R=11323/100000, B=32, k=11/25 and mu=pi/32. The larger B32 mean
requires its own F, compensation coefficient b0 and exact tangent deficit;
none of the B33 scalar values are carried over. Each case independently
rechecks the global nonnegative deficit and its additional positive hinge

    delta(t)>=c*(T-t)_+.

| Case | T | c | Exact minimum hinge margin |
|---:|---:|---:|---:|
| 0 | 187/2000=.0935 | 119/2000=.0595 | 930318098179779509/(2*10^23) |
| 1 | 47/500=.094 | 111/2000=.0555 | 1010557312676697267/10^24 |
| 2 | 19/200=.095 | 11/250=.044 | 145175730494202819/(2*10^23) |

Each uses1000 global-envelope boxes and1000 hinge boxes. All three
whole-domain checks have minimum bad-arc margin
1401501994384782893363/10^24. No variance is reserved or spent. The first
two settings give stronger three-marked-apex/ear ownership inputs than a
much larger cutoff with a weak slope; the full dual must choose a single
coherent setting and verify its own ownership and structural premises.

Executable: verify_tight_hinges_B32_0p11323.py. verify_case(0/1/2) rejects
unknown indices, and verify() asserts all three PASS statuses. Every
acceptance is outward exact interval arithmetic. Floating computations
only propose the local concave-penalty tangent location. Neither the
marked-apex count, effective center count nor a graph catalog is asserted
by this scalar artifact.

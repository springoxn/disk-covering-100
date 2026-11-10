# Independent local actual-anchor fee .038 and uniform-radius audit

2026-10-05 UTC. PASS for the continuous local theorem at the fixed coefficient pair and the stated positive-radius interval. This receipt does not certify an independent-J fee, a coefficient rectangle, a whole-cover budget, or a new universal radius bound.

Canonical package: `disk100_q3_shared_geometry_extensions_20261005.zip`, SHA-256 `18e02dc1e6d5c53339589bace04a5f2ecefa9e8bf94a9318b564b3d4e9a6bbb6`. I independently checked the archive hash and ZIP CRC. All 100 extracted file hashes remained unchanged during my read-only replays. Their sorted relative-path/hash JSON, with compact separators, has aggregate SHA-256 `8719ad183b7c585f2177db7ee1eab60326c09c7fc416211fb0ed1f0ad6132a5d`.

Primary SHA-256 bindings within the package:

- `research/q3_stronger_fee_19_500/PROOF.md`: `5a58cc96f916018885d39888bcd07ca77e768d3c719a695e2d619311fed1610f`
- `research/q3_stronger_fee_19_500/verify_actual_quadratic_19_500.py`: `bd042f4976fbeeb8440da66864814371f82e4fd0e380844cd153dcb7e600f46d`
- `research/q3_stronger_fee_19_500/certificate.json`: `b79cc05457486de14e8ed89a8d62bacf596581b152092a3951f9893b3dfa56bb`
- `research/q3_radius_uniform_19_500/PROOF_ADDENDUM.md`: `eacd376402698410798b1ade9373c786896519a18b7a95c589ba4cb93a480fae`
- `research/q3_radius_uniform_19_500/radius_endpoint_fraction.py`: `7f56e4f3dd808320586ed060a9eb089ec752868a479ea38780cc25cda7783d47`
- `research/q3_radius_uniform_19_500/SOURCE_PINS.json`: `c29656471c6dff992ba1f4e87e05e13d7e5408e28d4820e7233e8023de4a891b`

I read the complete stronger proof, its implementation, conjugate dependencies and radius addendum. In a fresh assertions-enabled Python process I imported the stronger module and called its `verify()` function, rather than its certificate-writing main block. Its returned JSON exactly matched the pinned certificate. I separately reran the pinned conjugate's `verify()` and matched every certificate field, then ran the standard-library radius endpoint arithmetic. No reviewed source or certificate was changed.

## Exact theorem and signed convention

Fix lambda=7/50 and t=1071883/20000000. For every real

    0<R<=794400/5378209,

consider three positive-area consecutive triangles (p,c_i,c_{i+1}) with common actual apex, consistently oriented positive apex increments and circumradii <=R. Each base has an actual unit anchor q_i covered by both endpoint disks. Define

    x_i=|c_{i+1}-c_i|/(2R),
    A_i=-det(c_{i+1}-c_i,q_i-c_i)/2.

Then, with C the true complete-apex conjugate at this same fixed lambda,t,

    sum_i[area_i/R^2+A_i/R^2-4lambda*x_i^2+t*gamma_i]
        <3C-19/500.

Negative signed A on the apex side is included. No norm bound, reflection, assigned-arc domain, ownership/tie rule or restriction on the apex position is used. The radius interval includes .11322 and extends beyond .1155. It is a local geometric theorem only.

## Continuous paid-deficit proof independently checked

The sine-rule area/skew formula and endpoint disk constraints yield the exact actual score F(theta,gamma)-sigma-tau, with sigma,tau>=0. Convexity in gamma retains both acute and obtuse endpoints before localization. The pinned full-apex conjugate covers the entire domain at lambda=.14; it does not incorrectly assume whole-interval concavity beyond pi/3.

If a triple had deficit D<=19/500, the strict endpoint guards localize theta to (.7,.96), the acute curve has -G''>4 on that complete interval, and a convex cut at gamma-theta=.1 excludes the rest of the apex domain. Integrating the strict slope and curvature bounds gives one simultaneous budget

    2 sum e_i^2+sum z_i+sum sigma_i+sum tau_i<=D.

This is one paid loss, not four independently reusable budgets. The actual apex angles become acute only as a consequence of that budget.

I independently checked the signed anchor-to-tip inequality |q_i-a_i|/R<=tau_i/x_i^2, including negative anchor heights. The exact tip formula and shared-ray phase identities agree with a positively embedded fan and the stated determinant orientation. The circumradius/apex slack and skew coefficients are valid on the localized domain. At zero skew the displacement is zero; the squared skew inequality is correctly read as non-strict there, with strict coefficient and final fit guards furnishing the needed strict margins.

The full-box Jacobian components retain both endpoint imaginary signs. Their Frobenius bounds control every segment from the unique ideal peak to the actual triple. Cauchy combines angular/skew errors against precisely their share of the one budget. The remaining z/tau errors have the stated linear coefficients. The rational conditions 4L^2 D0<alpha^2 make the joint square-root-plus-linear error maximal at zero linear spending. Thus the strict translation-free fit bounds are |B-B*|<.34 and |b-b*|<.30.

Ideal sagitta/half-chord sizes and the projection guard then give

    2|B_perp_to_b|>993/1250,
    |B|^2+|b|^2<5378209/1000000.

The proof of the unit-circle compatibility inequality is algebraic: endpoint mean a and half-chord h satisfy a dot h=0 and |a|^2+|h|^2=1; the identity (1-alpha*beta)^2-(alpha-beta)^2=(1-alpha^2)(1-beta^2)>=0 gives

    2|B_perp_to_b|<=R(|B|^2+|b|^2).

The derived |b|>1.43 justifies its perpendicular and rules out endpoint repetition without assuming it away.

## Radius extension and closure

I checked that every normalized guard preceding the unit-circle step is independent of R. In the stronger verifier its fixed R occurs only in the last compatibility upper and reporting metadata. The primitive's unrelated boundary-radius declaration is not referenced by its imported interval/trigonometric definitions. The conjugate is also radius independent.

The strict fits therefore contradict compatibility whenever R<=K/S=794400/5378209. The closed endpoint is valid because both fitted inequalities are strict: K<actual_left<=R*actual_sum<R*S<=K. The old fixed-radius reporting gap >.18 is not promoted to the entire interval. The new endpoint arithmetic is exact and gives K-Rmax*S=0, as it should.

At every fixed positive R, a zero-area limiting face has score limsup<=1/2+t*pi<.7, whereas C-19/500>1.432. It cannot occur in a hypothesized high-score triple; localization and divisions are used only afterward. Positive-area limits retain defined parameters. No statement at R=0 or a false identification of vanishing physical area with vanishing normalized area is made.

## Whole-cover interface remains separate

The physical fee is (19/500)R^2. It applies to the actual signed edge anchors before replacing A by the independent J majorant. The existing BC-lens/boundary functional, its variance, unmarked face/angle allowances and BI credits keep their original once-only allocations. One must separately prove eligible consecutive-fan incidence, coefficient matching and any conjugate-enclosure adjustment. Multiple applications need disjoint charged face/anchor sets.

This receipt validates the local .038 theorem and its uniform-radius range at the exact fixed tilt and penalty. It does not itself establish a parent global inequality or exclude any covering boundary count.

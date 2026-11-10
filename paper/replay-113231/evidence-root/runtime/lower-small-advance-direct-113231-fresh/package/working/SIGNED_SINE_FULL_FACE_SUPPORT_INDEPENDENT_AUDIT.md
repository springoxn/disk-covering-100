# Independent audit: generic signed-sine full-face support backend

Date: 2026-10-04 UTC. Result: PASS for the hardened local support implementation. A fresh standard-library replay passes all1224 exact diagnostic comparisons and five invalid-domain rejection cases, plus independent near-minus-one and near-plus-one stationary-edge regressions.

The localization proof is SIGNED_SINE_FULL_FACE_LOCALIZATION.md. Its sufficient guard is range(lambda)+sum negative sine-coefficient magnitudes/2<the positive area coefficient. The implemented scaling divides labels, sine coefficients and the chosen face multiplier by that area coefficient, then restores the area scale. The inward-derivative/Hessian proof applies to arbitrary signed coefficients under this guard; positive sine coefficients have no additional size restriction.

The acute scalar dual uses nu-lambda with the correct sign and subtracts pi times the mean label. Its imported exhaustive signed-sine conjugate includes both endpoints and every quadratic critical cosine. The complete boundary treatment checks all three simplex edges. For T=t_i+t_j<=0 the edge score is convex, so endpoints suffice; for T>0 and |d|<T it also retains sqrt(T^2-d^2)+d*acos(-d/T)+pi*(lambda_j-mean). Equality cases |d|=T are already endpoint cases. Thus no nonacute interior or boundary maximum is dropped. The radius-ratio-zero linear branch is covered by the same vertex endpoints.

An adversarial valid input with T=1/2+10^-80 and d=1/2 originally rounded the critical cosine to a fixed-grid endpoint and failed its strict interval-domain assertion. The hardened closed[-1,1] guard uses the already endpoint-safe acos implementation and now returns a safe broad enclosure. This affects reusable API completeness, not any accepted direct-M25 coefficient row; its separately frozen helper remains unchanged.

The return interval encloses the CHOSEN dual-support expression. Its upper endpoint bounds the true constrained face maximum. Its lower endpoint is not generally a lower bound on that maximum for arbitrary nu: for example, zero labels/edges and nu0 produce the uncoupled expression1.5, exceeding the true equilateral area3sqrt(3)/4. The final docstring explicitly states this distinction. Invoking certificates must use the upper endpoint for face majorization and keep assertions enabled. No graph-incidence, neighborhood-allowance or radius conclusion follows from this scalar backend alone.

SHA-256 bindings:

- exact_signed_sine_full_face_support.py: 9771385657022f006daf986057165db0514e296b0538a7e81d99808a772487e3
- SIGNED_SINE_FULL_FACE_LOCALIZATION.md: 6393c6f64784f2abe671817d9976ca01bedad63d893db6e9d84f48c71f177ba7
- signed_edge_metric_20261004/exact_signed_conjugates.py: cbf8cbb7ec769cd504077631be5df971caed8d24996515cce5df9dc389cbab70

This receipt is a local scalar/theorem implementation audit. Conditional graph and family certificates require their own geometric premises, signed-edge cancellation, multiplicity, domain and count reviews.

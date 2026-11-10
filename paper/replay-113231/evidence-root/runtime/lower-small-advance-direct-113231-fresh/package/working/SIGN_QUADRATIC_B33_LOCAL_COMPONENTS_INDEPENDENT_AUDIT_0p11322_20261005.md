# Independent sign-aware quadratic-lens B33 components at R=.11322

2026-10-05 UTC. PASS for the four conditional boundary-functional instances. This receipt does not establish their successive actual-arc domains, a complete B33 branch, or a universal lower bound at .11322.

Frozen SHA-256 bindings:

- `sign_aware_radial_stability_backend.py`: `f49317fcc3b00f7dfbf372d235d6788fea6a7e5064bd4cd8821066a3e9759fb6`
- `sign_aware_lens_cycle_energy.py`: `ecc14faca3cc8bca56bd14988b96c5a746311eff001462d15ff6984abc32213e`
- `SIGN_AWARE_LENS_CYCLE_ENERGY.md`: `eaaf1bcf672256b59a58147862ec56eca98e97dd09c518c7758ea498608dc8ef`
- `quadratic_lens_radial_stability_backend.py`: `0a762d49daf83e318c936abb3d6c26abe1d5971df9ff9c53289ae1cab9a7d8e9`
- `exact_quadratic_lens_node_support.py`: `45940e9ae6ac030a9b69a5322db864db0073310f384674e71c765d8b3ee605e8`
- `verify_sign_quadratic_B33_initial_0p11322.py`: `b2c355a706dbb4b53aac91c7085764633d8a8a834074d472cc28bb1639a56a15`
- `verify_sign_quadratic_B33_stage2_0p11322.py`: `d58b05a5e8f25c3ee91f461b9d811d048ce4cc9666e03981b025462e11dfd12b`
- `verify_sign_quadratic_B33_stage3_0p11322.py`: `d4d1fcce39cfbdd8463ed5081080d200232334e87fa85d1f62011b5dd4af3583`
- `verify_sign_quadratic_B33_final_0p11322.py`: `af27b8f17b9380ca6192150accd27314038f6df1235e19adf11beb4acd2622fc`

I inspected the new mixin's method-resolution order, the four instances and their unchanged quadratic-lens/value/derivative dependencies. A fresh assertions-enabled `python -B -S` process called all four verifiers. Every node guard and exhaustive pair replay passed, with respectively 1255, 1255, 1433 and 1637 visited boxes.

The required actual domains are, in order:

- full arc >.0597, x>=.2636; lambda .04, gamma 3/2
- full arc >.0825, x>=.3642; lambda .08, gamma 23/20
- full arc >.1065, x>=.47; lambda .11, gamma 27/20
- full arc >.134, x>=.591; lambda .14, gamma 33/20

Each of the first three variances must remain entirely unspent until its separate arc-bootstrap implication is proved. The final variance is likewise one budget. These functions prove conditional inequalities, not the listed domain implications themselves.

## Guard substitution and exact node target

The new mixin explicitly substitutes the independently audited K=2+cA+cB energy factor. Its scalar helper retains the original stronger cutoff x0>=2R*sqrt(1-R^2), which every instance satisfies; the separately discussed cutoff-free extension is not used here. It also enforces K>=2, the independent neighbor eta0>asin R guard, actual arc comparison and normalization requirement. It does not silently call an older cone guard for the new smaller K.

The unchanged quadratic-lens coefficients follow from minimizing the neighboring rho*cos product and taking the full rho*sin spread on that actual domain. Their identities give w<=4lambda(R-h)-s<=0 for lambda<=1/4, and b>=0. Hence the upper w clip to zero and lower b clip to zero remain certified clips of the same exact coefficient functional. The new mixin itself checks lambda<=1/4 and the remaining coefficient/monotonicity guards.

The exact node maximum is A|delta|^2+w*Delta+b|t| over the same reflected endpoint lens and norm ball, with A=lambda*K>=0. All zero, horizon and feasible interior-peak candidates are retained. The analytic endpoint/peak derivatives and their kink/uncertain-activity hulls continue to refer to that exact maximum. The older soft bound can tighten its value upper because it bounds the same maximum; it does not change the derivative target. Changing K or the variance coefficient does not invalidate this previously audited continuous argument.

The pair uses natural outward values near h=0 and the correct centered mean-value enclosure only on regular boxes. Its square domain, symmetry and subdivisions are exhaustive. The added gamma quadratic variance is differentiated with the matching target. Summing gives Hactual+lambda sum Lactual^2 <= Q-gamma*sum(a_i-pi/33)^2 with the same single displacement-loss allocation.

For the final conditional instance the exact Q upper is

    89384917857293177360127 / 250000000000000000000000,

below 17877/50000 by

    82142706822639873 / 250000000000000000000000 > 0.

The explicit whole-cover norm premise is at R=5661/50000, before its diagram/B count is classified. No larger-radius normalization or historical graph is inherited. A future composition must independently establish each preceding actual domain and check all face/count/profile/variance interfaces; the frozen universal .11321 proof is unaffected.

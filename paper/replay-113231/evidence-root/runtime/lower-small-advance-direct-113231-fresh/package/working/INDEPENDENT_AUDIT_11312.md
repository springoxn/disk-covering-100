# Independent global checkpoint audit: r_D(100) > 0.11312

Date: 2026-10-04. Result: PASS.

The complete frozen proof, all new continuous inequalities and geometric/count reductions were independently inspected. Every changed component was freshly replayed, followed by a fresh complete `python -S verify_all_11312.py` run. All seven subprocess components and the final integrated result passed. Assertions were enabled; the integrated entry also rejects optimized Python.

This independently verifies

`r_D(100) > 707/6250 = 0.11312`

for 100 equal closed disks with unrestricted centers covering the closed unit disk. The independently certified upper bound remains `.1155018241946`. The exact optimum and global optimality of a construction remain unresolved.

## Exhaustive branches

The current-radius E criterion excludes at most 99 effective centers and leaves exactly B32 through B37. The universal restricted-Voronoi, straight-center-triangulation, anchor and signed-area reduction is the previously audited foundation; every new-radius scalar count comparison is rerun.

- B32: all 20 complete three-label face supports, 774 unrestricted vertex-type inequalities, both U-sign cases and K3/K5 geometry passed. The k=0 marked support and direct H-concavity boundary baseline were independently checked. No actual-triangle acuteness or variance-deficit hypothesis is used. Minimum area margin exceeds .0005792723. Separate receipt: `lower_bounds_extension_20261004/B32_FACE_INDEPENDENT_AUDIT_0p11312.md`.
- B33: fresh full-apex geometry, sharp simultaneous radial-center support, global marked penalty guards and all 8,112 inequalities over 169 zero/one-ear cases passed. Minimum exact area margin is `52113330775123282437/(5*10^23)`, at e=0,N=24. The detailed mathematical audit is described below.
- B34: the complete same-radius sharp-ear method passed all 1,446 supports, 18 final cases and quantitative boundary-variance checks. Minimum margin exceeds .0000496242. Separate receipt: `sharp_ear_B34_0p11312/INDEPENDENT_AUDIT.md`.
- B35: the unchanged q4 method freshly passed its geometry, source supports and 285 additional q4 types, including the full charge for eight potential q4 vertices. Minimum margin exceeds .00031316. Existing scoped receipt: `lower_bounds_extension_20261004/B35_Q4_INDEPENDENT_AUDIT_0p11312.md`.
- B36/B37: unrestricted q-marked triangle caps and all 97,111 full-domain pair boxes freshly passed. Margins exceed .00114153 and .00495785. No ear/fan/actual-angle acuteness premise is required.

All six boundary counts are therefore closed at the same radius. No stronger-radius transfer, graph catalog or later local improvement is required by this checkpoint.

## Independent B33 mathematical review

The old loss budget is below .562. The new minimum-degree lemma uses global slope -1/2 majorants for both Q(alpha)=sin(alpha)(1+cos(alpha)) and the unpenalized marked envelope on [0,pi]. Its degree-at-most-four deficit exceeds .84467. Thus degree at least five does not assume marked-apex acuteness. The complete q0 angle bounds, degree upper bound16, K4/K5 restrictions, at-most-one-ear argument and positive full-arc cutoff .0695 were inspected and replayed.

The sharper analytic radial node proof was independently reconstructed from endpoint radical guards, including monotonic neighboring radial products, tangential range rather than an unrelated sum of extrema, and the middle-node monotonicity. It is valid on the entire [.307,1] domain at lambda=.039. Its exact normal margin exceeds .00080319.

The stable radial-pair production replay visits 1,015 boxes. A focused reviewer additionally derived direct polar-edge/x-coordinate derivatives and completed a distinct exhaustive proof over 2,037 boxes, with 961 accepted leaves and 58 symmetry skips. Closed endpoints, positive denominators, singular fallbacks, exchange symmetry, forced PENDING propagation and simultaneous-instance isolation were checked. The inherited derivative mean-value backend is unchanged.

The marked squared-edge envelope is genuinely global on [0,pi] at .039. The low-angle endpoint, convex middle unrestricted score and high-angle endpoint are all revalidated. Its branch-safe implementation does not evaluate a low-angle trigonometric derivative at2pi. The q0 compatible potential's coefficient .42, splice1.1027 and complete current angle domain are separately checked. It is a zero-sum face majorant, not a universal actual-triangle quadratic deficit.

For every actual p3 apex, K5 forces a contiguous three-edge fan. Distinct fan edges are disjoint; endpoint blocks overlap only at adjacency endpoints. The centered weighted-Cauchy inequality and its integer coefficient33/133 were independently checked, including k=11's whole-cycle exception. This gives one global variance charge linear in the actual integer p3 count. Passing subsequently to a continuous LP relaxation is safe. In the one-ear branch this charge is omitted and the single three-arc ear variance is used instead; the variance is never spent twice.

The two negative ear edge-square penalties cancel precisely the same positive terms in the cyclic boundary score. Star closure, all48 types, all169 N/ear cases, nonnegative marked-apex multiplier, q0 boundary-angle identity and conjugate signs were inspected. All marked mean domains extend to pi as required; no old pi/2 restriction remains.

Four malformed star inputs reject wrong ear count, types, N range and negative marked-apex multiplier. Both new entry points reject optimized Python. The unsupported .06 global marked parameter is rejected, rather than silently receiving the .039 full-apex guarantee.

## Strictness and scope

Every auxiliary and final comparison has a positive exact margin. The inherited finite-type limiting argument uses vanishing radius enlargement before passing closed geometric/angle inequalities to a limit; exact-radius generic perturbation is not assumed. Projection gives a compact center domain and the covering-radius functional is continuous, so its optimum is attained. Excluding radius <=R therefore establishes the strict lower bound.

## Frozen identities

| File | SHA-256 |
|---|---|
| verify_all_11312.py | 15618c338070790577cc35aa7e4719279d22a58775918b6be5173c7e92f84196 |
| PROOF_11312.md | 4afc17957c63337ac19cc31d16f4909194bcbe901a9869f760331197960579c3 |
| MULTIPLE_FAN_RADIAL_STAR_0p11312_PROOF.md | 59a3ecf50a9227bc71c4e5a2316d6e6c46fe65e65df6104310729bb2003defba |
| verify_multiple_fan_star_0p11312.py | a9ef12ebdd4998d3443975c3fe5e4f05805b760dc922421ce8654e831eb46f61 |
| multiple_fan_star_0p11312_proposals.json | 85bbdb434492b47d6111320ad08f81723a8e5598e1004d311a2ad05d5d92e3e9 |
| global_marked_penalty_backend.py | a76b970f3acbcbb9aabfa6647aa02899e6e4907eaf5dda37bc3bdba7562d4321 |
| radial_sharp_node_backend.py | a7bea340987fd7e3bd721a5b760386356174d91c03dfc6c0cbe75067bf84f013 |
| verify_radial_stability_support_0p11312.py | 1a7367844a4c1e85e335b58f51a8d0e89f779d5d70d10ca5443cc5006c9066a3 |
| radial_stability_backend.py | a26e1b89116ea926dbbe0c5c5164b0c50803b625166178f461c038dcec2bdee3 |
| MULTIPLE_P3_FOOTPRINT_VARIANCE.md | 0e94d304b35cadadd40ef604d58568f1ab4195d3880fa2889933cd28346ed5a4 |
| verify_multiple_p3_footprint_variance.py | 1f8f6cc9974f8d8f271181da12b0a3cf93cd87d519242d44a0146e9d812cab53 |
| lower_bounds_extension_20261004/check_one_ear_structure_0p11312.py | 2ae53c1f3af97cdffcbc1d01f2af501948ffbe9ec12d53d4fe1adcb4cb24594d |
| lower_bounds_extension_20261004/check_global_apex_minimum_degree.py | fa99e1a3b33cf17aaa06374cad0dc4ca88303e924ba116c5710353f60f940544 |
| lower_bounds_extension_20261004/check_B32_face_0p11312.py | 5836133045b15efb8a7834459474b7470f547dcecb3cfb1a165a4f8f2fc78d79 |
| sharp_ear_B34_0p11312/verify.py | 8f7213a4f1ba98acbfd8dca11043030b5798e16d40a9db1c578febd338a0fcc8 |
| lower_bounds_extension_20261004/check_B35_q4_0p11312.py | 41312e2d68931afa0360c434aaee012ee75801490f7a6e8176e8cfbb5c525418 |
| verify_B36_B37_0p11312.py | 8391ee8601a123c4e19f3169efc9eca158a19aefa60f09b1acc9d10529db4abb |

The immutable exact kernels and geometric dependencies retain their separately audited identities. Every import of the unchanged ear ZIP rechecks SHA-256 `3f8e603344f4996d66acde7bcf0631628a1df879734fab8110c63c120f6f6324` and its internal manifest. Numerical proposals never decide acceptance.

Later lens-cone/spectral refinements, stronger branch bounds, Jensen-slab ear caps and conditional finite graph families are not dependencies of this certificate. This is independent mathematical/software verification, not proof-assistant formalization.

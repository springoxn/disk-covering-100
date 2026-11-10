# Independent recovered-chain audit: r_D(100) > 11321/100000

Date: 2026-10-05 UTC. Result: PASS for the complete universal lower-bound chain described below. The exact optimum and a global optimal configuration remain unresolved.

## Frozen authoritative files

- `verify_all_11321.py`: SHA-256 `a0138dbd7f11e23fae29d8d560c3f2b2e2abbc323bec5390c54059d1a98d9514`
- `PROOF_11321.md`: SHA-256 `21869f2415b2ff5eb84ea89351aacfb6f8bd6cb6c0830908663edf40963ba6c6`
- Author's raw fresh result `integrated_11321_recovered_result.json`: SHA-256 `c282ffa8aa350d3bc4bf2e13087cd92f8f6e42029615ec56c087e753a9cea8fb`

I inspected the frozen integration source and its complete proof and independently ran `python -B -S verify_all_11321.py` from the recovered working root. It terminated with exit code 0 and final status PASS. All six top-level fresh-process branches passed, including every one of the 402 B33 metric certificates and the complete 3,371,339-box capped-pair tail. The tool's final returned output was length-truncated; I do not represent it as an independently archived full log. The author's raw result above is a descriptive record, while the acceptor recomputes all exact comparisons from source and bound inputs.

## Mathematical scope and classification

The whole cover is normalized at the target radius before its restricted Voronoi/Delaunay diagram, irredundant centers and boundary count are classified. The reflection identity preserves coverage of the target unit disk; it does not preserve a pre-existing graph or boundary count. The same-radius exact bridges exclude m <= 99 and leave m = 100, B = 31,...,38. Every normalized B32--B35 branch concerns that common normalized diagram and the target norm bound 1 - (11321/100000)^2.

The unrestricted B31 theorem at .11322 and unrestricted B >= 36 theorem at .11323 apply as inequalities with a larger bounding radius to the same diagram. Neither transfer introduces another normalization or reclassifies B. Assertions, exact radii, count lists, norm requirements, nested PASS results and strictly positive margins are explicitly checked by the frozen integration.

The genericity/endpoint argument is compatible with normalization: slightly enlarge, normalize all centers at the enlarged radius, move norm-boundary centers inward and perturb within the uniform strict-coverage margin, then select an irredundant subset of already generic positions. Hereditary generic conditions and finite type selection allow passage to the closed inequalities. The final strict exclusion gaps give the stated strict lower bound, including degenerate covers.

## Independently reviewed branches

- B31: the unrestricted complete-star curvature contradiction forces all interior degrees at least six, violating the self-contained nonpositive-curvature disk isoperimetry for F = 167, B = 31.
- B32: the same-radius normalized low/high-M reductions, coherent weighted deep-five metric replacement, complete 41-mask/16-core catalog and all 16 metric exclusions were reviewed. Actual centers remain unrestricted; lattice development classifies combinatorics. Recovered polygon support arithmetic has a fresh identity, rather than an asserted old byte identity.
- B33: independently reviewed scalar domains and recursive variance-to-arc links establish each successive actual domain before use. Their budgets are alternative inequalities, not summed. The final profile forces the no-ear M26 degree-six/unique q3 degree-seven case; the core and complete 57-core/442-placement/402-representative bridge discharge the metric family's geometry. Every graph is regenerated and compared with its metric input. Signed-sine full-face supports include all required simplex boundary-edge caps. Actual acuteness and equal circumradii are not assumed. All 402 arithmetic certificates passed in the complete independent replay.
- B34: the exact normalized endpoint-lens maximum, full-apex linear-halfside supports, all 48 full-face/1455 vertex supports and three affine ranges were reviewed and freshly replayed. Arbitrary ears and all-boundary q0/q1 faces have correctly signed coefficients. The entire variance is safely discarded in this branch; no isolated-five special case or graph catalog is required.
- B35: the simultaneous norm/lens displacement bound, global compensated boundary envelope, overlap-safe paid q4 allowances, all 70 face/1913 vertex supports and the M25 simple chordless-core incidence restriction were reviewed and freshly replayed. Its specialization is at the target radius itself.
- B >= 36: the pointwise capped-pair strengthening uses the exact necessary adjacent-center distance <= 2R and covers the entire domain. The complete exact tail replay passed and its affine boundary-count improvement is positive.

## Scoped receipts and recovered identities

These files are part of this audit and should accompany the universal receipt:

- `B32_B35_SAME_RADIUS_INDEPENDENT_RECOVERED_AUDIT_20261005.md`: `aaa41826b95c75a2f6d4d113ecd803f47ff67dd1e96739cbd1bba5af6690bddd`
- `LINEAR_LENS_B34_INDEPENDENT_RECOVERED_AUDIT_20261005.md`: `bfad503532ef80b7f42ddd248b19e94a5d136316ceef66835713310d954272a1`
- `POLYGON_STAR_RECOVERY_INDEPENDENT_AUDIT_20261005.md`: `4cb494dfd3a3985f667ba4a3b9fae1cd99ac81c000ed4a3fdbd5426067f4bfd3`
- `B33_0p11321_INDEPENDENT_RECOVERED_AUDIT_20261005_COMPLETE.json`: `76bc086fe46297c733af4ec71ff29043ea73c9169891b84ffbf80e8e974bbee2`
- The B33 64-file audit manifest aggregate is `28ffbd02b741dcef337260fd0ebdad4a7f36aa356428d92fedbd6193044188ec`; its 402 graph/certificate binding aggregate is `4ebdee504e255a67583e34dc3bdcbf292dcd919b7ff64a7dcf9f5ec2b9eccb57`.
- Reconstructed `polygon_star_perimeter_support.py`: `426c5eb338326931ce581d24697e1463815ed826ebfd24e926a1b12f9fa01a94`; reconstructed `POLYGON_STAR_AREA_PERIMETER.md`: `d4e6fb8830c36a7be1f45175507b4d67e2553ff9302e40f7db20276c8021fab1`
- Recovered formal `NORMALIZED_CENTER_DISPLACEMENT_PENALTY.md`: `1b6a85fb5c1a1f2b11cede7c5d243e93e753a0e0e0c6d9e526c90e93b3ee2b11`
- Byte-identically recovered hardened signed-sine helper: `9771385657022f006daf986057165db0514e296b0538a7e81d99808a772487e3`; hardened Sturm helper: `e85c5fb42eabb12c17e05d62ff484e757dc7fa019dd32d9eb6ecd1804116fb6d`

Fresh recovered rounding changes in auxiliary intervals were accepted only by fresh exact replays and are not described as historical byte identities. No damaged legacy descriptive JSON is consumed as an acceptance input. The optional graph-free quadratic-lens high-M route, newer radii, and graph-specific extensions are outside this frozen universal receipt.

Conclusion: the frozen, recovered and independently replayed chain proves r_D(100) > 0.11321. It supplies a stronger lower bound; it does not identify the exact algebraic optimum or prove a global optimal configuration.

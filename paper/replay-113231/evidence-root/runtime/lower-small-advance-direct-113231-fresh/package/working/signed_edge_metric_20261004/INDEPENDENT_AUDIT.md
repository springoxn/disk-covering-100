# Independent audit of signed shared-edge certificates

Date: 2026-10-04. Result: PASS for the supplied graph-conditional certificates.

The full signed-edge and wider-localization proofs were independently inspected. A focused reviewer freshly replayed the three supplied graph certificates, all four continuous nonacute localization squares, 4,209 supplied scalar consistency/sample checks and malformed-input/optimized-mode tests. The reviewer added 4,787 independent scalar/radius samples, ten exact special-angle tests, connectivity/face/edge checks and matching-hash malformed-graph rejection tests. After the requested explicit three-corner/three-edge guards were added, I freshly replayed both wider graph certificates and the final supplied tests, plus eight additional malformed-shape rejections. Original graph and coefficient data were preserved.

## Exact results

| Graph | Radius | Exact positive area margin |
|---|---|---|
| flat_N27_0009, narrow certificate | .11309 | 1841643475257158103/15625000000000000000000 |
| flat_N26_000_special_01, wider certificate | .11312 | 16170721676878106167/50000000000000000000000 |
| flat_N27_0009, wider certificate | .11310 | 366613752753568194619/250000000000000000000000 |

Each graph has 165 distinct faces, 264 edges, 33 boundary edges, 172 q0 shared edges and 52 zero-potential q0/marked interfaces. The four localization-table replays use 141/143/163/181 visited boxes and 71/72/82/91 accepted leaves. The stored N27 wider result has an older reporting layout; its substantive area margin agrees with the current replay.

## Mathematical checks

- Opposite signed coefficients cancel the same physical shared edge length, including unequal incident circumradii. Actual lengths and center positions remain unrestricted.
- The local score is convex in the circumradius ratio on [0,1]. Both endpoints are retained; simplex vertices also represent the zero-radius linear maximum in the unit-radius branch.
- Both localization proofs compare the full signed score with its equilateral value. They constrain a score maximizer, not actual triangle acuteness. The wider square parametrization includes every nonacute or degenerate triple and all endpoints, and accepts only after its queue is empty.
- The acute scalar support considers both endpoints and both quadratic critical roots. Discriminant signs, uncertain root clipping, radical bounds, inverse-cosine endpoint handling and monotone parameter enclosure were checked. Concavity of an individual signed sine score is not assumed.
- Every face multiplier, complete interior angle sum, marked-apex guard, opposite-edge assignment and final strict comparison has the stated sign. Full graph validation rejects reversed orientation, duplicate faces, wrong apices, incorrect outer cycles and unsupported branches.
- Final wide APIs explicitly require exactly three corners and three edge coefficients. All entry points reject optimized Python. Acceptance uses standard-library exact outward intervals; sample tests are corroboration, not the continuous proof.

## Frozen core identities

| File | SHA-256 |
|---|---|
| PROOF.md | 8fc90dbec2aae45e7cca07f5702c0a094ce41b470198cacffb98bff827013205 |
| WIDE_LOCALIZATION_PROOF.md | 95bcbc167b91935a34c85ae8af2dcc7bac62c274284e4037dc7f4e6f1479d462 |
| exact_signed_conjugates.py | cbf8cbb7ec769cd504077631be5df971caed8d24996515cce5df9dc389cbab70 |
| wide_metric_conjugates.py | 645480196605d1d71060bb51f2c4973dca99f458605d8663ad0e410e218825a6 |
| verify_signed_graph.py | f43d2c57d7c049238b96b2b596fe0923094579922bb6f35290fcba8d269beca3 |
| verify_signed_graph_wide.py | 7120af396454ca813c307fa8489afd058424470b2e0a9da00c7de32d6d788b3a |
| test_signed_supports.py | 6f741c8316ca1b22a486f2449262d0b62c19b6a326874b8045c269344947d3c8 |
| graph_N27_0009.json | 6d0078a9504a2e320b6edfb3d8df7023707b94a2b3e422edcac655f58158d20f |
| certificate_N27_0009.json | aba80e4ebd1f7a009ec6fe34ee37c552d8fe7780fa009c1dd73b07e333c2c4bb |
| graph_N26_0001.json | e8a9b8243996f00d3be981a2c8b83f2bddb18d27b62a3821a5b74352f48a4222 |
| certificate_N26_0001_wide_11312.json | b25b2ee4b24ae722902795d8b00d88d721a31fda815647a770ee23157139a652 |
| certificate_N27_0009_wide_11310.json | 37588cc190d2c55e8d1d1cf470b11486434eaf013d94734dac26194e0432f3b1 |

Inherited exact kernels and graph validators were also hash-bound during review: `../verify_star_lp_duals.py` = 23568fed518e451d3d6b7f11603e080546bb74afa020ef0fd8fbb1a3b02be6d7; `../verify_potential_star_duals.py` = d4609b4441dae93c105966dd28f72b2e9d84342f012dd519dca25f2515e3e2c3; `../exact_angle_conjugates.py` = cee5e03352e7b6c94ecbe5dbf0cd43f97342c9c23492b6820e7fc935fc8d1cb9; N26 exporter = 88bb141202e69bea9b891e0f9d09343901dc4ab11fe5ed0544a9fb4ebf0c458a; N27 exporter = 5f04e05c2980ca90ca2a6d9e77c6b622085efcc13efef0a3800efa2fcdf188f2; lattice mesh utilities = 40502bf904831be6307194b41a0237eb77396b8a2bf6565bdc6cffa414a3a939.

## Scope

These exclude the specified marked combinatorial graphs under the inherited covering-triangulation and signed-area reduction. They do not establish completeness of any graph catalog, a universal improved covering bound or the exact optimum. This is independent mathematical/software verification, not proof-assistant formalization.

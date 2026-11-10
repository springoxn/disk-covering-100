# Independent audit: normalized B33 branch at 0.11319

Date: 2026-10-04 UTC. Result: PASS, based on mathematical inspection and a focused independent fresh replay of both unpenalized bootstraps, both boundary supports and all final face/type/range comparisons. Exact optimality remains unresolved.

Scope is B33 of the diagram formed after the entire cover is normalized to center norm at most sqrt(1-R^2), R=11319/100000. Reflection can change ownership, redundancy and boundary count. The conclusion must not be transferred to an original fixed B33 diagram before normalization.

The global cap 229.203 gives full assigned arc>.0748 and normalized half-sine>.33. The independent M<=25 cap 228.99 gives full arc>.107 and half-sine>.4724. Neither bootstrap uses the later radial or marked-edge-square deductions. The low-M pure pair (lambda=.056, variance=1.5) passes 909 boxes; the high-M reflected pair (lambda=.095, variance=.25) passes 1063 boxes. They apply on disjoint ranges and their budgets are not added.

The final verifier passes 80 full-face supports, 1950 vertex inequalities and five integer ranges. Its minimum area gap is 132833605620796209261/(5*10^23). The compulsory flag is restricted to actual deep low-degree vertices, which have no boundary-center neighbor. Exactly the four triples containing both deep and boundary labels are omitted; all sixteen remaining triples, including repeated deep labels, are checked. Nondeep low vertices remain unflagged and explicitly checked. The weighted deep-curvature witness supplies two units for M<=23 and a deep witness for M24/25. The range-below-one face theorem retains its mandatory degenerate-vertex cap. Terminal-edge credits, shifted ear coefficients and fan-variance charges have compatible signs, and each row uses the edge penalty and variance of its own boundary support. All remaining integer ranges are covered by their checked affine slopes. Optimized mode and malformed coefficient proposals are rejected.

The integrated global entry must separately invoke both bootstrap and both radial verifiers: the face module imports support objects but does not by itself replay those dependencies.

SHA-256 bindings:

- verify_deep_face_B33_0p11319.py: dcd4f7c6745f9606f10487271bd5c721763a16a74adc60166670f30b08d70214
- DEEP_FACE_B33_0p11319_PROOF.md: 79fbb5ff4ee74917a476e15a38764de52065c1113be7ddeecee6e7c1ad91edde
- deep_face_B33_0p11319_proposals.json: ac8325cc546c8f1f0e0ec5abda65f2d2c193f0a72c78c3a9a0a8106d5a53f175
- DEEP_CORE_CURVATURE_WITNESSES.md: 33984c68b5d4d111d535f8a0c1e33ef9cf0b9a4418b97a833a96f93cab32b667
- lower_bounds_extension_20261004/verify_B33_arc_bootstrap_0p11319.py: 256f2c6094b6f48cd2cbd6ddd8f53e063f0f19d2bc5f23519d36f40575da0616
- verify_B33_small_core_arc_bootstrap_0p11319.py: ce0cabf66f864e0315a111b9c8029b0242890375851339d14c8c825e64e72185
- verify_radial_B33_lowM_bootstrapped_0p11319.py: 0fc42230bf4dfdf1b7e6cb7cdc0bf841392e50238097e859f3183c485555084b
- verify_reflected_radial_B33_stronger_0p11319.py: 20d095a9c72233ccbef2cffed7ed8170ed620e822578bf0ff2f8bf904082fe0c
- lower_bounds_extension_20261004/B33_arc_bootstrap_0p11319_result.json, repaired raw-Python report: e3f23aafc0edceea9efc368ac646b0e0448cfe66cccce3f65ac46d68120c2b7f

The repaired report corrects auxiliary interval metadata serialization. No acceptor reads it, and the exact comparisons are recomputed. This receipt is a branch audit, not a universal-radius claim by itself.

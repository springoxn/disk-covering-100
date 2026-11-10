# Independent global checkpoint audit: r_D(100) > 0.11311

Date: 2026-10-04. Result: PASS.

The complete proof and all new geometry, scalar bounds, type/count reductions and stronger-radius transfers were independently inspected. Each changed component was freshly replayed, followed by a fresh complete `python -S verify_all_11311.py` run. Every component and the final integrated result passed, with assertions enabled and fresh subprocess isolation.

This independently verifies the universal strict lower bound

`r_D(100) > 11311/100000 = 0.11311`

for 100 equal closed disks with arbitrary centers covering the closed unit disk. The independently certified upper bound remains `.1155018241946`. The exact optimum and global optimality of any supplied construction remain unresolved.

## Exhaustive chain

1. The new-radius original E criterion excludes at most 99 effective centers and leaves exactly B32,...,B37 at 100 centers. Its Voronoi nonreturn, straight dual triangulation, marked-anchor and signed-area reduction are inherited from the previously independently audited checkpoints. Every new-radius count comparison is rerun.
2. B32: fresh same-radius geometry and all 2,352 ordinary-star inequalities across 84 integer cases passed. The current individual-face loss budget justifies the actual q0 variance coefficient .73; it is not applied to arbitrary triangles without that budget. Minimum area margin: `34916381428585019561/(5*10^23)`.
3. B33: fresh same-radius domains, at most one ear, simultaneous radial-center support and all 9,100 footprint-aware scalar inequalities across 247 cases passed. The complete analytic audit is recorded in `FOOTPRINT_RADIAL_STAR_0p11311_INDEPENDENT_AUDIT.md`. Minimum area margin: `16726610263154651319/(5*10^23)`.
4. B34: the independently audited complete .11312 branch freshly passed inside the integrated replay, including 1,446 vertex supports, all 18 U/q4 cases and the .29 boundary-variance support. Its separate receipt is `sharp_ear_B34_0p11312/INDEPENDENT_AUDIT.md`. Minimum margin exceeds .0000496242.
5. B35: the unchanged independently audited .11312 q4 branch freshly passed, including new-radius K4/K6 geometry and 285 extra q4 vertex cases. Its existing receipt is `lower_bounds_extension_20261004/B35_Q4_INDEPENDENT_AUDIT_0p11312.md`. Minimum margin exceeds .00031316.
6. B36 and B37: the unrestricted .11312 method freshly replayed all q-marked triangle caps and all 97,111 full-domain lens-pair boxes. No ear, fan or actual-angle acuteness condition is needed. Final margins exceed .00114153 and .00495785.

Using stronger-radius branch exclusions is valid: keep the hypothetical .11311 cover's centers and original restricted-Voronoi diagram fixed and enlarge only the common bounding radius. All geometric covering inequalities remain true and its boundary count is unchanged. Irredundancy at the enlarged radius is not required for this fixed original diagram. This transfer was independently inspected in the combined proof.

## Additional independent checks

The .11311 radial production replay visited 1,107 boxes. A distinct direct polar-edge/x-derivative exhaustive proof also passed over 2,273 boxes. Closed endpoint coverage, nonsingular denominators, singular fallbacks, swap symmetry, PENDING propagation and isolation between different checkpoint instances were checked.

The p3 footprint applies to at least four distinct complete assigned arcs even if the three marked edges are not consecutive. The p<=2 branch's N>=17 lower bound follows from its distinct-apex count and the established terminal-fan incidence inequality. The sharper ear cap retains both edge-square penalties and cancels them exactly once. Potential splices, conjugate signs, all branch partitions and the one global variance charge were inspected.

Four malformed star inputs reject wrong branch, type set, N range and negative marked-apex multiplier. The new integrated, star, radial, B32 and B36/B37 entry points reject optimized Python. These checks supplement, rather than replace, the continuous exact proofs.

The generic-limit/strictness argument is sound: perturbations may use vanishing radius enlargement; finite topology and bounded coordinates admit a fixed-type subsequence. The same-radius strict auxiliary and final margins pass to the limiting closed inequalities. No exact-radius generic perturbation is assumed. Compactness and continuity give attainment of the optimum, so excluding radius <=R establishes the stated strict bound.

## Frozen top-level and changed source identities

| File | SHA-256 |
|---|---|
| verify_all_11311.py | 34253591ddcc6ce26dcd12c15b42fc14d971ea47f565013ba40a3f1a3beb229a |
| PROOF_11311.md | ebf523c9e6fb6a8b1a96571794c6bed4c16fa6ab31af1229703302fb153842ab |
| FOOTPRINT_RADIAL_STAR_0p11311_INDEPENDENT_AUDIT.md | bf714448815710d985233ceb0d965ddc3c80b0096da528ecd2426b08924f77e4 |
| verify_footprint_star_0p11311.py | 1b23260ddb4293ac0a2703b598c19216a8b30d7b48bd301829447cc6fd982195 |
| footprint_star_0p11311_proposals.json | f4bb1167fbc72ee7de9b22080a0cc12ae8dde527d3edc9adceaf24c30fbde803 |
| radial_stability_backend.py | a26e1b89116ea926dbbe0c5c5164b0c50803b625166178f461c038dcec2bdee3 |
| verify_radial_stability_support_0p11311.py | 2b0a7ea0afe9bb808f08b04f99cfbd82178894d5651e30fb6239f8db685e0b1e |
| lower_bounds_extension_20261004/check_one_ear_structure_0p11311.py | d406b1e6ea2d241fd69c5d4ec8d0cdb3224643f7d1ea4156bd4374ea1fa3dc6f |
| lower_bounds_extension_20261004/check_B32_full_0p11311.py | edb5495514d10bc5ce714f5a79d0588ada0c2318a7addce0a14d7f8b77e44597 |
| lower_bounds_extension_20261004/check_B32_star_0p11311.py | 7a4792122c80367c529fe2f1ac8c2bcdf6f0bfae580d0254bcb9959f820a0dbe |
| lower_bounds_extension_20261004/B32_duals_0p11311.json | 80b4127066ab0b0ed367b7f0a533859680c4cd6f4209be12f742fd7fe8e9e608 |
| sharp_ear_B34_0p11312/verify.py | 8f7213a4f1ba98acbfd8dca11043030b5798e16d40a9db1c578febd338a0fcc8 |
| sharp_ear_B34_0p11312/INDEPENDENT_AUDIT.md | fd448ab2e13865b9390a01afb78a35e12103b3cb5d8526921f530e076e184f30 |
| lower_bounds_extension_20261004/check_B35_q4_0p11312.py | 41312e2d68931afa0360c434aaee012ee75801490f7a6e8176e8cfbb5c525418 |
| verify_B36_B37_0p11312.py | 8391ee8601a123c4e19f3169efc9eca158a19aefa60f09b1acc9d10529db4abb |

The unchanged pinned ear archive SHA-256 is `3f8e603344f4996d66acde7bcf0631628a1df879734fab8110c63c120f6f6324`; its 26-member internal manifest is rechecked before import. The immutable exact kernels and earlier geometric dependencies retain their separately audited identities. Numerical proposals never determine an acceptance sign. This is independent mathematical/software verification, not proof-assistant formalization.

Finite lattice graph catalogs, signed-edge graph experiments and later graph-free face refinements are not dependencies of this global checkpoint.

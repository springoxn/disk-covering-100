# Independent audit: complete B33 exclusion at .11317

PASS, 2026-10-04 UTC. This is a complete B33 component at R=11317/100000. Other boundary counts, including newly surviving B31, require their own exclusions.

I inspected the complete proof, executable and new-radius bootstrap, and freshly replayed the arc bootstrap, corrected radial entry and full five-row face verifier. They passed 50 complete q0 face supports, 1935 unrestricted vertex supports, all 1067 radial pair boxes and all five final ranges. Optimized-mode acceptance rejects. The minimum area margin is `374676556409929231141/10^24`, greater than .0003746765564.

The new bootstrap retains zero halfside, squared-edge and fan penalties. Its independently derived normalized center cap 229.203 gives full arcs greater than .088 and normalized sine greater than .3886 before any radial support is used. It rechecks the current count bridge, K4/K5 geometry and arbitrary-ear shifts. Its short-arc contradiction margin is `3805660705908761767815078350003/10^35`. It does not assume marked-apex acuteness.

This instance uses the older retained soft correction, lambda=.065 and stability=1.25, not the separate reflected-center sharpening. The full-apex two-branch conjugate remains valid for lambda≤1/8. All face labels, interface credits, centered angle signs, corner charges and edge-square cancellation are unchanged from the independently audited complete .11316 method and refreshed for these rows.

The newly audited K≤1 disk isoperimetry gives at least two units of unmarked positive curvature when M≤23. The first row's local allowance subtracts `f*max(6−d,0)` on unmarked vertices, so the final deduction is 2f, not two unproved distinct degree-five vertices. M24/25 uses one compulsory low vertex; M≥26 uses no flag. The rows with ears use only one ear's variance charge and negative shifted-ear coefficients cover every e≥1. No-ear rows use only the multiple-p3 variance charge. The single variance budget is never added twice.

All slopes and endpoint choices are correct: no-ear M22, M24 and M26, plus e1/U24 and e1/U28 for positive-ear ranges. The old loss is freshly below one, giving M≥22. The inherited finite-type limiting argument extends the positive inequalities to nongeneric threshold covers. No symmetry, actual-center radial optimality, actual-q0 acuteness or lattice restriction is introduced.

SHA-256 bindings:

- `verify_radial_face_B33_0p11317.py`: `ec2087b195dc8bce456971020ee5d6b123e78741fedf2da7d6f3b42dc7858014`
- `RADIAL_FACE_B33_0p11317_PROOF.md`: `745446a3a26b8934da1b574ab50c077cf4cdf8bd1275bc016a7078c5c13425c2`
- `radial_face_B33_0p11317_proposals.json`: `86b68c697bf0a301b2d2d3b61fcf838204ad1415ef243b0c6e0e7e162598f508`
- `verify_radial_corrected_support_0p11317.py`: `27f6629aeffeea67b455bf5d558a88b8559467f8a4cab7082331d4944cece626`
- `lower_bounds_extension_20261004/verify_B33_arc_bootstrap_0p11317.py`: `01786dc2f11dbc3ab840cf1bdbe36646b701a4d2c014e4add7810bba3bf405c6`
- Hardened marked conjugate: `a54af21d3b405b468e74f93ec53cab24714c5bb0fb4c66a61bd16987edfdfb6d`
- Weighted-curvature scoped receipt: `54c6a1b0c7c86afb2d797ccb579e660e5689a42558355bb9b0dec63e74868122`

No reviewed source was changed. Exact optimality remains open.

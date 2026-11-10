# Exact metric exclusion of the 16 reduced B32 graphs

## Result and scope

All16 abstract graphs B32_P26_F108_000 through015 in the SHA-pinned reduced catalog are excluded at R=2829/25000=.11316, with unrestricted actual center coordinates. The minimum exact area contradiction is

`1489203281333688909383 / 10^24 > .00148920`,

at family001. This metric component combines with the separately proved complete B32 reduction and exhaustive catalog to close the B32 branch. By itself it is a finite-family exclusion, not a theorem covering every boundary count.

## Exact graph adapter

`verify_all_graphs.py` regenerates all16 graphs using export_B32_P26_F108_families.py, pins the catalog SHA-256, and checks each graph against the rational certificate bound to its exact serialized hash. The exporter validates the oriented166-face,265-edge triangulated disk and all100 vertex links. There are68 interior vertices,32 boundary vertices,134 q0 faces and32 ordinary q1 faces. Every boundary edge is exactly one ordinary q1 base; q0 faces contain no original boundary edge.

Each certificate specifies68 interior angle weights u, zero weights on all32 boundary vertices, signed coefficients on every q0--q0 shared edge, and one scalar multiplier for each q0 face. The two halfedges of every shared edge receive exactly opposite coefficients. q0--q1 interfaces receive zero. Integer inputs and array/edge incidences are explicitly checked. No coordinate realization or numerical triangulation is assumed.

## Full-domain signed q0 support

The proof and exact scalar implementation are unchanged from the audited signed_edge_metric_20261004/PROOF.md and WIDE_LOCALIZATION_PROOF.md. For a q0 triangle with circumradius ratio rho in[0,1], angles alpha and opposite-edge coefficients tau, its area-plus-metric-minus-angle score is

`rho^2*2 product sin(alpha_i)+rho*sum tau_i sin(alpha_i)-sum u_i alpha_i`.

The metric halfedge term equals tau times the physical edge length/(2R), so opposite signs cancel globally even for unequal incident circumradii. Convexity in rho reduces the support to0 or1. Simplex vertices of the rho1 branch already realize the maximum pure linear rho0 score.

Every local face satisfies an independently verified wide localization domain: potential range at most.3 and absolute edge coefficients at most.25. The complete nonacute/degenerate angle simplex is bounded strictly below the equilateral score, so the scalar maximizer is acute; actual triangles are not required to be acute. For any rational face multiplier eta, its support is bounded by pi*eta plus the sum of the three audited one-angle conjugates. Each conjugate checks both endpoints and every real quadratic stationary root. The exact interval backend includes uncertain endpoints and uses no floating acceptance.

## Marked faces and total angle restoration

A q1 face plus its anchor, minus u_apex times its apex angle, is bounded by the full-domain marked conjugate G(u_apex). Its concave majorant is valid for every apex angle through pi. The supplied marked weights are in the safe conjugate domain and are checked by the exact implementation; no actual apex acuteness is assumed.

Add2*pi times the sum of all68 interior weights. The complete interior angle sums then cancel every weighted-angle term. Boundary weights are exactly zero in this accepted certificate, regardless of the numerical optimizer that proposed the inputs. Thus the resulting dimensionless center/anchor upper bound C requires only the ordinary outer H-concavity bound

`R^2*C+32*H_R(2*pi/32)`.

There is no boundary-angle reduction, metric-window bootstrap, equal-arc hypothesis, or reserved radial-loss budget in this proof. The largest exact C is below229.796456. The final bound is strictly below pi in every graph, proving the stated exclusion.

## Replay

Run `python -S signed_edge_metric_B32_20261004/verify_all_graphs.py` with assertions enabled. Only standard Python is required. All supports and signs are freshly verified; numerical proposal files and saved PASS results are not read by acceptance. The rational certificates are in certificates/. The complete run takes less than a second on the current cloud CPU.

The catalog hash is6bc2f1e934d36d6ee35a2aeb6ee7ee68f2eac8d3faa473975fceb2447ebb5742. Its geometric reduction, classification of all flat cores and41-mask enumeration remain separate proof components and must be combined before asserting the complete B32 branch. The inherited finite-type limiting argument is needed when applying the generic diagram method to degenerate covers.

# Independent audit of the recovered polygon-star primitive

Date: 2026-10-05 UTC. Result: PASS. This binds the equivalent-formula recovery, not the lost original byte identity.

The recovered geometric proof correctly establishes polygonal isoperimetry by convexification, compactness, outward perturbation of padded collinear vertices before Lagrange multipliers, and the equal-length/equal-turn stationarity equations. It applies to the actual simple neighbor polygon of a complete star. Sine concavity bounds its perimeter by2R*T_d, and the polygon inequality bounds its area byR^2*S_d. The negative-perimeter support follows by convexity in area, with endpoints0 andS_d; the positive-perimeter case follows from the separate endpoint bounds. Thus max(0,a*S_d+b*T_d) is valid for every a>=0 and real b, including d3 and degenerate limits.

The recovered scalar code evaluates S_d andT_d with the already reviewed outward sine/cosine routines instead of the original radical special cases. This changes only conservative interval rounding, not the geometric formulas. Consequently old exact output numerators are not reused as fresh byte/result identities. The current complete B32 replay recomputes its 81 M25 cases and all downstream inequalities with this recovered helper. No unweighted star deficit is added to an already charged face sum; its invoking M25 proof reserves and replaces the affected central areas and retains all corner potentials.

Bindings:

- polygon_star_perimeter_support.py: 426c5eb338326931ce581d24697e1463815ed826ebfd24e926a1b12f9fa01a94
- POLYGON_STAR_AREA_PERIMETER.md: d4e6fb8830c36a7be1f45175507b4d67e2553ff9302e40f7db20276c8021fab1

This is a local theorem/recovery audit. Sampling is regression evidence, not the geometric proof, and the result is not a radius exclusion by itself.

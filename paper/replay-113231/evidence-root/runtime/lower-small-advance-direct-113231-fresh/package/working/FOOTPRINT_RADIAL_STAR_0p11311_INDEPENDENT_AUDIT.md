# Independent B33 audit at radius 0.11311

Date: 2026-10-04. Result: PASS for the complete B33 branch, conditional on the retained universal restricted-Voronoi/straight-dual reduction.

The same-radius geometry, radial support and all 9,100 scalar dual inequalities across 247 integer cases were independently read and freshly replayed. The exact minimum final area margin is `16726610263154651319/(5*10^23)`, attained in the no-ear/p3 branch at N=23. This is a boundary-count exclusion, not an exact optimum or an all-B theorem by itself.

## Geometry and compatibility

- The fresh count bridge excludes at most 99 effective centers and leaves B32 through B37. For B33 it establishes the .517 loss budget, complete q0 and ordinary marked angle domains, degrees 5 through 14, p at most three, no all-boundary q0/q1 face, zero or one ear, and every full assigned arc greater than .0755. The degree-five proof uses the uniform loss-budget criterion; it does not inherit an invalid older angle-mean argument.
- At an actual p3 apex, its three distinct marked boundary edges touch at least four distinct boundary sites. All four complete assigned arcs lie in one radius-3R disk centered at that apex, so their total angle is at most .6932. Their cells need not be consecutive. One Cauchy variance charge applies to four chosen arcs and their complements; no multiple-footprint disjointness is assumed.
- In the no-ear p<=2 branch, at least ceil(33/2)=17 distinct marked apices are needed. The independently established fan-terminal incidence bound gives N at least their number. The N>=17 scalar range is therefore exhaustive.
- One ear forces a three-arc total at most .4566. Its normalized anchor-minus-edge-square maximum per edge is `(sqrt(1+16*lambda^2)-4*lambda)/2`. Keeping both negative penalties gives exactly the stated ear cap. They cancel the same two positive edge penalties already included in the cyclic radial boundary support, without double counting.
- The q0 face potential is a compatible zero-sum majorant, not a universal variance deficit. Its new coefficient .45, splice 1.1005 and endpoint pi/2+.205 are exactly revalidated. Its concavity and tangent domination follow from the stated one-inflection-tail test. The acute penalized marked envelope is rechecked at lambda=.037.
- The p/j type sets, good-marked and q0 face counts, boundary-angle conjugate `(e-2)*pi*eta`, nonnegative marked-apex multiplier, mandatory variance charges and all three branch partitions were checked. No actual symmetry or equal-gap condition enters the proof.

## Independent radial checks

The production natural/mean-value replay passed all 1,107 visited boxes, with 508 accepted leaves and 46 symmetry skips. Its largest accepted upper is `11334998674129392813893/10^24`, strictly below .011335.

A focused independent reviewer additionally derived the direct polar edge and x-coordinate derivatives and completed a separate exact exhaustive proof over 2,273 boxes, with 1,073 accepted leaves and 64 skips. Endpoint/singular fallback, positive denominators, swap symmetry, PENDING propagation and simultaneous-instance isolation were checked. The .3336 lower endpoint exceeds 1/3 by 1/3750. The exact node-normal margin is `370653503459246062943/(2*10^23)`.

## Frozen identities

| File | SHA-256 |
|---|---|
| FOOTPRINT_RADIAL_STAR_0p11311_PROOF.md | 7aff5879f57ff0b2f5930d83e6952f95fa2700ac6775c617ac2b5d9664e8a8c9 |
| verify_footprint_star_0p11311.py | 1b23260ddb4293ac0a2703b598c19216a8b30d7b48bd301829447cc6fd982195 |
| footprint_star_0p11311_proposals.json | f4bb1167fbc72ee7de9b22080a0cc12ae8dde527d3edc9adceaf24c30fbde803 |
| radial_stability_backend.py | a26e1b89116ea926dbbe0c5c5164b0c50803b625166178f461c038dcec2bdee3 |
| verify_radial_stability_support_0p11311.py | 2b0a7ea0afe9bb808f08b04f99cfbd82178894d5651e30fb6239f8db685e0b1e |
| lower_bounds_extension_20261004/check_one_ear_structure_0p11311.py | d406b1e6ea2d241fd69c5d4ec8d0cdb3224643f7d1ea4156bd4374ea1fa3dc6f |
| lower_bounds_extension_20261004/ONE_EAR_STRUCTURE_0p11311.md | c3cb9b981978f812e9322d4319bd8eb515740fc1f4a04af30d4fbe5cd779fb14 |

Acceptance used Python's standard library and exact outward intervals, with assertions enabled. Numerical proposals were not treated as evidence. The strict generic-limit argument was inspected: radius enlargement is allowed only before taking a fixed finite-type limiting subsequence; no exact-radius generic perturbation is asserted.

An integrated universal theorem must also independently close every other surviving boundary count. Exact global optimality remains open.

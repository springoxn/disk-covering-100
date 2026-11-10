# Independent high-M B33 starting-domain audit at R=.11322

2026-10-05 UTC. PASS for the actual arc-domain implication in normalized m100/B33/M>=26 diagrams. This is a domain lemma, not a covering-radius exclusion.

SHA-256 bindings:

- `verify_B33_highM_unpenalized_arc_0p11322.py`: `6d63ed2468faf3b513caac987840c5a0b32326ae2021d85a28c8fac4fcb87d5d`
- `B33_HIGHM_UNPENALIZED_ARC_0p11322.md`: `238b3943b43ece77ec2e7e0c65cc8669a128a6dfdfb08a45ab2067bf0f9b0550`
- `B33_highM_unpenalized_arc_0p11322_proposals.json`: `e7da396658798c32cc7f8790e523ffd3b5058416c57acdd8bdd9b26af9e5e8d4`
- `lower_bounds_extension_20261004/verify_B33_arc_bootstrap_0p11322.py`: `c837aa5aece62ad77edfeea0daf75275209866d287d8ca21840ff0c5f85486fb`
- Pinned inherited angular archive: `3f8e603344f4996d66acde7bcf0631628a1df879734fab8110c63c120f6f6324`
- `exact_quadratic_marked_conjugate.py`: `a54af21d3b405b468e74f93ec53cab24714c5bb0fb4c66a61bd16987edfdfb6d`
- `exact_range_one_face_support.py`: `a33023537a5f20e406e2fac79dc16f6ce79ac152798e08563a7097e48a1414ef`
- `verify_jensen_slab_ear_support.py`: `1c8d46f5e08714519e1545199fdd6edebe7b1defec0df3b693649be0ad6c4e4b`

I inspected the strengthened source/proof, inherited domain source and its pinned full-apex marked-conjugate specialization, and freshly ran `PYTHONDONTWRITEBYTECODE=1 python -B -S verify_B33_highM_unpenalized_arc_0p11322.py`. It exited 0 with status PASS. The inherited archive/manifest, new-radius complete count bridge and angular reduction, all 32 new face supports, 780 vertex inequalities and the Jensen comparison were recomputed. The rational proposal has no floating coefficient fields.

The starting count bridge excludes m<=99 and leaves m100/B31,...,39. The four-cell radius-2R cluster comparison excludes bad all-boundary q0/q1 faces; it does not incorrectly exclude three-cell q2 ears. Ears are permitted and have a strictly negative shifted coefficient. The six-cell radius-3R comparison initially gives q<=4. Its q4 support allowance is paid at most floor(33/4)=8 times because every q4 apex uses four distinct marked boundary-cycle edges. Only after the preliminary paid center cap 229.363 excludes every five-boundary-neighbor footprint is q<=3 and the four-consecutive-cell window used to restore the uncharged cap 229.203.

This sequence is not circular. The original angular rows use no radial displacement, fan variance or marked-apex acuteness assumption. Their full-apex k=0 conjugate has the valid concave acute endpoint and conservative obtuse endpoint; the archived helper is specialized in a fresh process before cache use. Its q0 label range is below one-half, satisfying the inherited complete-simplex localization. The low-M witness is supplied by the general induced-core obstruction. The new high-M rows need no compulsory witness.

The strengthened rows check every allowed degree from three through 99, both deep and nondeep unmarked low-degree types, and all 16 full-face label multisets without an impossible deep/boundary edge. Range-below-one supports include the degenerate-vertex cap. Nonnegative terminal BI credits are retained with the correct once-only count. The M26 row is used only at M=26; its positive M slope is not extrapolated. The second row has a negative slope and covers every M>=27. Both shifted-ear coefficients are negative.

The exact center uppers are at most 57294182175388450322604237/250000000000000000000000 and 229172432381487357539725229/10^24, both below 229177/1000. H(a)=a-sin(a)*(cos(a)-sqrt(R^2-sin(a)^2)) is strictly concave on the allowed domain. If one half-arc is at most .0597/2, the equal-other-32 Jensen expression is increasing in that short half-arc, because H'(a)>H'((pi-a)/32) below the mean. Evaluating at the upper short endpoint is therefore valid. The source verifies its feasible square-root domain and proves a contradiction margin

    9599858496401094353/10^24 > .00000959985.

Thus every actual full arc exceeds 597/10000 and its normalized half-sine exceeds 659/2500. No radial or variance budget has been spent. Whole-cover normalization remains the common classification convention for downstream normalized branches, though these angular inequalities themselves do not use the stronger norm constraint. Other M ranges and all future covering exclusions require their own independently valid arguments.

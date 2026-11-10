# Optional stronger arc bootstrap when M<=25

At R=.11318, assume the independent B33 geometry: m100, no all-boundary
q0/q1 face, marked incidence at most3, and M=U-2e<=25. The general core
obstruction forces at least one unmarked vertex of degree at most5.

The one rational row in B33_small_core_arc_0p11318_proposal.json uses
the complete three-label face support and the global marked conjugate
with zero penalty. It contains no radial or variance term. Its reserved
BI credits, local score, and centered-angle cancellation are exactly
the full-face formulas in RADIAL_FACE_B33_0p11316_PROOF.md.

The ten full-face supports and387 vertex types pass. The M coefficient
is positive, so evaluate at25. The shifted-ear coefficient is negative,
so e0 bounds every ear count. After the compulsory low-type flag the
normalized center/anchor score is less than228.99.

Concavity of the half-arc function H shows that an assigned full arc
at most.114 would give total area at most

    R^2*228.99 + H(.057) +32H((pi-.057)/32).

Its exact gap below pi is112692465944399762721/10^24. Therefore every
full arc exceeds.114, and sin(half arc)/R>1/2. The inequalities are
checked by verify_B33_small_core_arc_bootstrap_0p11318.py.

This is a conditional domain improvement for M<=25, not a radius
exclusion. It is not needed by the completed split-penalty B33 .11318
candidate, which uses the weaker common arc domain independently.

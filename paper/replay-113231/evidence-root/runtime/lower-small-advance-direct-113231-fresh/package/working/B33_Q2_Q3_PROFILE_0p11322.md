# Conditional two-type degree-seven profile at R=.11322

This is a necessary-profile reduction, not a radius exclusion. Assume a
normalized m100/B33 diagram at R=5661/50000 with M=U-2e>=26, no bad
all-boundary q0/q1 faces, ordinary marked incidence at most three, and
boundary neighbors in at most four consecutive cells. In addition it
requires the still-separate actual boundary inequality

    sum Hactual_i+(7/50)*sum actual marked-edge length squared
       <=17877/50000=.35754.

The same-radius unpenalized angular bootstrap already supplies the count,
bad-face and four-cell premises. It does not supply this new boundary Q.

Reuse the R-independent corner potentials and rational local allowances
from the .11321 q3-profile table. All 16 full-simplex face supports and
390 full-angle vertex cases are rechecked. The arbitrary-penalty Sturm
conjugate, rather than the old lambda<=1/8 backend, supplies lambda=7/50.
Deep/boundary face pairs remain forbidden by the actual deep-label
assignment. Both deep and nondeep low-degree types are included.

The maximum at M26,e0 has raw area excess at most

    799847568053744389853/10^24.

The negative M slope excludes M>=27 with margin
1261125662814877589641/(5*10^23). The freshly evaluated negative shifted
ear coefficient excludes e>=1 with margin1382619460842099297577/10^24.
Thus M26,e0 is necessary.

For every interior type other than degree six or (q,d)=(2,7),(3,7),
one integer occurrence pays a reduced-cost deficit greater than the
entire remaining excess. The tight forbidden type is (q,d)=(0,7), with
positive area margin4440853106016731363/(5*10^22). The Euler degree sum
is27-M=1, so exactly one degree-seven vertex remains, with marked
incidence two or three; all other66 interior vertices have degree six.

The subsequent flat-core/catalog bridge is separate. Under that bridge
the unique q2 defect selects a straight core-boundary vertex, giving861
symmetry families from940 raw placements. The q3 defect selects a corner,
giving402 families from442 raw placements. The shared core catalog has57
patches. Neither those metric exclusions nor the boundary-Q assumption
are proved by verify_B33_q2q3_profile_0p11322.py.

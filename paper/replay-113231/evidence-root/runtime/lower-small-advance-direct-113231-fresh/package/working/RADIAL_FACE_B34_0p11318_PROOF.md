# Complete B34 exclusion at .11318, with arbitrary ears

Set R=5659/50000. The entry is
`verify_radial_face_B34_0p11318.py`. This is a complete B34 component,
not an all-count radius theorem. All previous checkpoints remain intact.

## 1. Exclude every low-core case at the new radius

`verify_B34_low_core_0p11318.py` replays the unchanged normalized
full-face/interface/mixed-fan supports and freshly evaluates every
radius-dependent comparison. It excludes at most99 centers, forces
m100, and checks no all-boundary q0/q1 faces using the four-arc span
.4568. The exact margin is positive even though the earlier asserted
.001 threshold is no longer available; the new required threshold is
1/5000. The six-arc span.693 gives marked incidence at most4, and the
endpoint-union calculation bounds the number of q4 vertices by5.

The coupled boundary baseline minus.29 times the one total half-arc
variance is rechecked on the complete domain. The joint ear cap, every
integer mixed-fan budget, and all shifted-ear coefficients are also
refreshed. The general core theorem forces a degree3,4,or5 unmarked
vertex when M=U-2e<=25. Its exact reduced cost excludes M<=23, M24,
and M25 using the three existing rational rows. Arbitrary ears are
allowed; the shifted-ear coefficients are negative.

Only M>=26 remains. No upper bound on M, degree histogram, or graph
catalog is assumed in the next steps.

## 2. Independent unpenalized cap, now allowing all ears

The two normalized unpenalized full-face rows from the preceding
.11317 method remain valid: their complete face and vertex inequalities
are radius-independent and are replayed. The row at M26 is checked
there directly. The other has negative M slope and covers every M>=27.
The radius-dependent joint ear cap is refreshed at R. For both rows,
the shifted-ear coefficient is negative, so evaluation at e0 bounds
every e>=0 while keeping M fixed.

Thus, for every remaining diagram,

    normalized center/anchor score <=228.352.

This bound uses neither a radial claim nor an edge-square/variance
penalty. Let H be the standard half-arc function. If a full assigned
arc were at most.055, concavity would give

    area <=R^2*228.352+H(.0275)+33H((pi-.0275)/33)<pi.

The strict gap is2886102192991414131/(125*10^21). Therefore every
full arc exceeds.055, and the fresh sine comparison gives normalized
half-sine greater than.2429.

## 3. New radial pair and one final full-face row

`verify_radial_corrected_B34_0p11318.py` proves on that complete domain

    outer_actual+.06 sum(marked base length)^2 <= Q,
    Q=34*(.00870146)+2pi*(-.001951680).

Its cone factor is3.81314, and its775-box replay uses the older2h
positive radial correction. Reflection normalization is unnecessary
for this B34 component. The Q upper endpoint is
56717374579936748932943/(2*10^23).

The same normalized final face row is replayed with the direct global
marked conjugate at lambda=.06. It checks all ten label multisets and
all482 q<=4 vertex types. Both its M slope and its refreshed shifted-ear
coefficient are negative. Therefore its e0,M26 evaluation bounds all
remaining M>=26 and every ear count. The final strict area gap is

    570991791159239548143/10^24 >.0005709917911.

The new bootstrap/final stages check30 complete face supports and1446
vertex supports, as well as the full pair domain. The least gap of the
complete chain occurs in the earlier low-core stage and exceeds.0001076.

## 4. Exact conclusion

The low-core stage excludes every M<=25, and the independent cap plus
radial/full-face stage excludes every M>=26. Bad q0/q1 faces are excluded
by the fresh geometry, while arbitrary ears are retained throughout.
No finite lattice family or equality-spacing hypothesis is used.

The actual result is `radial_face_B34_0p11318_result.json`; it records
both the final-stage gap and the minimum over the complete chain.
Numerical optimization is absent from acceptance. The inherited
constant finite-type limiting argument includes nongeneric endpoint
covers. All other boundary counts remain separate requirements for a
universal .11318 lower-bound checkpoint.

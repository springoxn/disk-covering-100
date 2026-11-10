# Independent B33 angular domains at R=.1132

These are domain bootstraps, not a radius exclusion. They use no squared
edge, radial displacement, fan variance or marked-apex acuteness premise.

`lower_bounds_extension_20261004/verify_B33_arc_bootstrap_0p1132.py`
freshly checks the old constants, n99 exclusion and every boundary count.
The survivors are B31,...,38. For B33 the four-arc2R footprint excludes
all-boundary q0/q1 faces, and the six-arc3R footprint gives q<=4.
The old five-arc exclusion is no longer assumed.

The frozen unpenalized face rows have20 exact full-face supports and774
q<=3 vertex inequalities. Add the190 q4 vertex inequalities, each with
an additional normalized allowance .02. Since each q4 apex uses four
distinct marked boundary edges, at most floor(33/4)=8 such apices exist.
The preliminary normalized center cap is therefore229.203+.16=229.363.
Its negative shifted-ear coefficients cover arbitrary ears.

If an apex had five boundary-center neighbors, their assigned cells
would lie in its3R footprint, of total full angular span at most .6931.
Constrained concavity of H bounds the outer term by

    5H(.6931/10)+28H((pi-.6931/2)/28).

Combined with the independently established preliminary center cap,
this is below pi by more than .0020159. Thus no five-neighbor apex
exists, and q<=3 follows. Reapply the original uncharged rows to get
center cap229.203. A single assigned full arc at most .0685 then gives
another constrained-H contradiction, with exact margin
278577766254570416945655433541/(125*10^32)>0. Consequently every full
arc exceeds .0685 and sin(half arc)/R>.3025.

The order is essential: pay q4 first, exclude five neighbors, then remove
the q4 allowance. It is not legitimate simply to reuse the earlier
q<=3 geometric premise at this larger radius.

For M=U-2e<=25, `verify_B33_small_core_arc_bootstrap_0p1132.py` separately
checks the frozen .11319 angular row at the new radius. Its independent
center cap228.99 and negative shifted-ear coefficient imply full
arc>.1004 and normalized half-sine>.4432. The exact short-arc gap is
666425496242869107/10^23. This conditional stronger domain is used only
for M<=25 and is not inferred from a later radial inequality.

Both scripts serialize exact integer results directly from Python.

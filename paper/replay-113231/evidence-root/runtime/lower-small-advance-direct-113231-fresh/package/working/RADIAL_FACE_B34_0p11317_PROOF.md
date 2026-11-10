# Complete B34 exclusion at .11317 without a new graph catalog

Set R=11317/100000. The entry is
`verify_radial_face_B34_0p11317.py`. Its three logical stages are ordered
to avoid a circular arc-domain argument. This excludes B34 only.

## 1. Earlier exact necessary-profile reduction

The entry first replays `verify_B34_flat_reduction_0p11317.py` in full.
Despite that research filename, no lattice development or catalog is
needed here. The already established exact consequences used are:

* m100 and B34;
* no all-boundary q0/q1 face, marked incidence at most4;
* every branch except e0,M=U in{26,27} is excluded.

The reduction's additional degree and integer-profile information is
safe but unnecessary for this completion. Its old low-M flags and
negative shifted-ear coefficients provide strict exclusions for every
discarded case. Consequently the remainder has66 interior vertices,
130 q0 faces,34 ordinary q1 faces, and no ears.

## 2. A non-radial center cap forces a positive arc domain

Two new rational rows, one for each remaining U value, use zero
squared-edge penalty and no boundary variance charge. They label
degree-at-least-seven interior vertices by-a, other interior vertices
by0, and boundary vertices by-b. Complete-simplex face localization
and the exact sine conjugate prove all ten label triples. Nonnegative
reserved BI credits pay at least2tau per marked high-degree vertex,
by the previously audited fan-terminal incidence argument.

For an ordinary marked face use the full-apex conjugate C_0(s) from
QUADRATIC_MARKED_CONJUGATE.md. Every vertex type p=0,...,4 and
d=max(3,p+1),...,99 satisfies the proposed affine majorant. Summing
the exact incidences gives the normalized center/anchor bound

    130A+34C_0(0)+66u0+34beta+(28-U)eta+Uv+U p_b
       -b(2pi+U*pi/3) <=228.352.

Both U26 and U27 are checked directly. This cap does not use any
radial-center claim, minimum assigned arc, or squared-edge penalty.

Let H(t)=sin(t)*sqrt(R^2-sin(t)^2)+t-sin(t)cos(t) for a half-arc t.
Concavity and the total half-arc sum pi imply that if any full arc is
at most .062, the entire area is bounded by

    R^2*228.352 + H(.031) +33H((pi-.031)/33).

The constrained one-arc expression is increasing up to the uniform
half-arc, so this also bounds smaller arcs. Its exact gap below pi is
23708521179630832519/10^24. Thus every full arc exceeds .062, and the
fresh trigonometric comparison gives normalized half-sine greater
than .2738.

## 3. New radial edge support and one final face row

On this independently established domain,
`verify_radial_corrected_B34_0p11317.py` proves

    outer_actual + .06 sum(marked base length)^2 <= Q,
    Q=34*(.0087044)+2pi*(-.001975862).

The cone factor is3.76212. The731-box exact replay retains the original
larger positive radial correction and does not require the newer
reflected-center sharpening. No variance is charged in this stage.

The last rational face row uses the direct global marked conjugate
C_.06(s). Its negative base-square terms cancel the one positive outer
edge-square sum. The same ten full-face label supports and482 vertex
types are rechecked for these new coefficients. Its U slope is strictly
negative, so evaluation at U26 also bounds U27. The total area upper
bound is strictly below pi by

    1127885818690774225793 / 10^24 > .0011278858186.

The new stages check30 complete face supports and1446 vertex supports,
in addition to the complete earlier reduction and the full radial pair
replay. The three rows are in
`radial_face_B34_0p11317_proposals.json`; numerical optimization is not
used by acceptance.

## Conclusion and scope

The initial exact reduction discards every other B34 case. The
independent unpenalized cap gives the domain for the final penalized
radial/face argument, which excludes both remaining cases. All actual
center coordinates are unrestricted. A new lattice catalog is neither
assumed nor enumerated by this proof.

The inherited fixed finite-type limiting argument handles nongeneric
diagrams and closed endpoints. This is a complete B34 radius theorem,
but the new B31 case and every other boundary count at .11317 remain
separate dependencies of any universal checkpoint.

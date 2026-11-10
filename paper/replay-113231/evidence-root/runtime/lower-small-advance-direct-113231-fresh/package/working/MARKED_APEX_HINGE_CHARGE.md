# An all-count marked-apex charge from a boundary hinge deficit

Assume a generic irredundant center triangulation has B boundary cells,
at least two interior vertices, and ordinary marked q1 faces. A marked
boundary edge has exactly one incident center face; if that face has an
interior apex, that apex owns the edge. Bad all-boundary faces and ears
may be present and are simply not ordinary owners.

Suppose a separately verified boundary inequality has the exact form

    boundary contribution <= constant - sum_i delta(t_i),

with delta(t)>=0 for every possible half-arc, and additionally

    delta(t)>=c*(T-t)_+.

Let an interior apex own p>0 marked edges. It cannot own the entire
boundary cycle, since then its complete triangular fan would fill the
disk and leave only one interior vertex. A proper p-edge subset of a
cycle has at least p+1 distinct endpoints. Select any p+1 of these
boundary cells, without requiring that the edges form a single fan.

Every selected cell's site is within2R of the apex, and every point of
its assigned arc is withinR of its site. Its full assigned arc therefore
lies in the radius3R disk about the apex. For3R<1, that disk cuts an arc
of length at most2asin(3R) from the unit circle. The selected half-arcs
consequently have sum at most asin(3R). If L>=2asin(3R), then

    sum_selected delta(t_i)
       >=c*((p+1)*T-L/2)_+.

Each boundary cell is incident to only two boundary-cycle edges. It can
therefore be an endpoint cell for at most two distinct ordinary owner
apices. This remains true for split fans and after arbitrary subset
selection. Summing the preceding bound gives

    sum_i delta(t_i)
       >=sum_apices [c/2*((p+1)*T-L/2)_+].

Thus define the normalized per-apex charge

    gamma_p=c*((p+1)*T-L/2)_+/(2R^2).

The center/face functional may subtract gamma_p at each ordinary marked
apex. No qmax, contiguous-fan, no-ear or no-bad-face premise is required.
There must be at least two interior vertices to ensure p<B. These hinge
charges spend the scalar deficits and cannot be added to a separate
variance allocation from those same deficits unless a combined scalar
lower bound is verified.

At R=.11322,B33,k=.44, exact interval checks establish c=.03,T=.092 and
L=.6934. The global nonnegative-deficit certificate and the hinge
certificate are separately replayed. In particular gamma_3 is positive;
all higher p are handled by the same formula. The source
verify_B33_marked_hinge_charges_0p11322.py reports the full exact table.
This is a local allocation theorem, not by itself a covering exclusion.

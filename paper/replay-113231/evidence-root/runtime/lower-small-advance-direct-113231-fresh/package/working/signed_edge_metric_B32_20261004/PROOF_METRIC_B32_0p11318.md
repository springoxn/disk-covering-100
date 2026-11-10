# The sixteen B32 metric exclusions at .11318

The entry is verify_all_graphs_0p11318.py. It freshly replays every
unchanged rational coefficient row, graph identity, signed-edge
cancellation and full-domain scalar support in verify_all_graphs.py.
Those checks produce a rational upper bound C_g for the normalized
center/anchor score of each graph. The score and its support inequalities
are independent of the bounding radius: actual side lengths are divided
by that radius, and all triangles have normalized circumradius at most one.
All boundary angle potentials are zero. No small-arc or radial-window
lemma is used.

For R=5659/50000, ordinary boundary concavity gives the total area bound

    R^2 C_g + 32 H_R(2 pi/32).

Here H_R(theta)=sin(theta/2)*sqrt(R^2-sin(theta/2)^2)
+(theta-sin(theta))/2. The new wrapper computes this expression from
freshly accepted rational C_g with outward integer intervals. It does
not reuse the saved result JSON or infer a radius result by floating
interpolation. Every one of sixteen area margins is strictly positive.

The minimum gap, for B32_P26_F108_001, is

    161731994484994196963 / (5*10^23) > .000323463988969.

This is a radius-only extension of a complete fixed finite metric
family. A universal B32 result at .11318 additionally requires the
separate same-radius reduced-cost and catalog-completeness bridge.
Original .11316 sources and coefficient files are unchanged.

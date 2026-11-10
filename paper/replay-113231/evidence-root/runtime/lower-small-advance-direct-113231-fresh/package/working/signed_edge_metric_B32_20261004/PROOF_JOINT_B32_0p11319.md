# Direct current-radius replay at .11319

Run verify_all_joint_0p11319.py. It uses the same sixteen immutable graph
files and rational coefficient files as the .1132 joint certificate,
but computes every final radius-dependent arc and area expression
directly at R=11319/100000. The new helper differs only in its explicit
target-radius guard. The old helpers and coefficient files are unchanged.

The wrapper checks that each stored coefficient file records its
historical .1132 target, then creates an in-memory copy with the new
target. All coefficients, graph SHA bindings and support multipliers
stay fixed. These are rational proposals, not saved acceptance results.

Every pure-support, cancellation, marked-potential and neighbor-weight
guard is freshly recomputed. The independent C<=230 metric-window
lemma applies throughout radii<=.1132 and supplies the same .08/.9
arc/base conditions at the present smaller radius. No reflection or
change of centers/diagram is used.

All sixteen current-radius bounds pass. The exact minimum is recorded
in joint_0p11319_result.json. Catalog completeness at .11319 is supplied
separately by the complete B32 wrapper, which must match each saved
graph against the regenerated family. This file alone proves only the
sixteen graph-conditional exclusions.

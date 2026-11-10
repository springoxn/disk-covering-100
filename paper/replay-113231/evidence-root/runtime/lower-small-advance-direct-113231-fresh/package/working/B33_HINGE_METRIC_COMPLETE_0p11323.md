# Complete normalized B33 branch at R=.11323

Entry: verify_B33_hinge_metric_complete_0p11323.py. This is a B33 branch
theorem, not a universal radius theorem or an exact-optimum claim.

The low-M prerequisite checker replays the unchanged rational face and
vertex rows at the new radius. It excludes M22/23 and M24. For M25 it
proves that the selected deep degree5 witness is the only original
interior degree5 vertex. Its remaining66 interior vertices have degree6..8.
Euler gives total high-degree curvature3-e-b<=3, so at most three neighbors
of the selected five have the high label. Its strict core-interior location
excludes original BC neighbors. No other positive-labelled vertex exists.

These are precisely the prerequisites of the independently supplied local
coherent replacement verify_B33_M25_coherent_five.py. That checker retains
the original M25 corner labels, charges and H-B interface credits; reserves
three tenths of the five central triangle areas for a joint polygon cap;
and pays all canceling positive outside-edge supports. Its six possible
neighbor cycles cover zero through three high neighbors. Its normalized
gain is additional face slack within the same original row, not a second
use of the boundary hinge or a post-hoc unweighted area deficit.

The complete entry verifies that every reference row coefficient is
identical to the .11322 table used by the local replacement. Only the
radius metadata is changed in the new prerequisite table. It adds R²
times the local gain to the exact raw M25 area margin, yielding a strictly
positive contradiction. Prior uniqueness reduced costs remain valid
because the face replacement only strengthens the same coherent bound.

For M>=26, the new all-degree5 contradiction colors every degree5 vertex,
including marked and boundary-adjacent ones, and verifies all20 label
triples. It proves minimum degree6 with a strict positive margin. The
remaining Euler profiles are excluded by the radius-independent topology
and same-radius metric evaluations in B33_HIGHM_METRIC_0p11323.md:

* M26/one7/e0/b0: seven metric patterns on a chordless P26/F106 core
* M27/all6/e0/b0: seven patterns with at most two core chords
* M26/all6/e1/b0: five patterns, one BBR q0 face, and the paid q2 ear cap
* M26/all6/e0/b1: impossible by core connectedness and the empty-side ear argument

The no-ear metric source files retain their .11322 filenames, but each
runs in a fresh process with R explicitly set to11323/100000. Every
normalized boundary scalar and final area expression is freshly evaluated
at that radius, and the reported norm bound is checked. No stronger-radius
normalization is transferred between diagrams.

The entire entry requires no lattice catalog, boundary-turn window, or
conditional quadratic radial bootstrap. All exact arithmetic uses the
standard-library interval and algebraic-support backends; numerical
optimization supplied proposals only. Independent review is still needed
before promoting this new branch into a universal checkpoint.

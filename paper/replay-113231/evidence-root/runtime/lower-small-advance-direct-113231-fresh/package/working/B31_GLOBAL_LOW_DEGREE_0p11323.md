# A full-face B31 exclusion at R=.11323

Set R=11323/100000. The branch concerns diagrams whose centers lie in the
unit disk before classification. Orthogonal projection provides this
without increasing coverage radius, but changes of boundary ownership
must be allowed before B is chosen. The stronger whole-cover reflection
used by the global proof also supplies this condition. No radius-dependent
norm cap or reflected boundary functional is otherwise needed here.

## 1. Same-radius necessary geometry

The original exact inequalities freshly exclude every cover by at most99
effective disks. Hence this B31 branch has m100, I69 and F167. The
five-cell grouped-H exclusion at radius-3R span .6933 has margin>.02235.
Every ordinary apex therefore has marked incidence at most three.

The original normalized area-loss budget is below the independently
proved degree-four complete-star loss. The global full-angle star caps
and their large-degree monotonicity therefore restrict every interior
degree to5,...,8. No actual apex acuteness is required.

## 2. Global degree-five counts, without a deep-label restriction

At least one interior site has degree five. Otherwise every interior
degree is at least six, so the disk inequality F<=B^2/6 contradicts
6*167-31^2=41>0.

Write M=U-2e. If M<=23, at least two sites have degree five. If there
were at most one, the positive strict-interior curvature of every
face-bearing induced-core block would total at most one. The proved
one-positive-curvature inequality applies blockwise, giving

    Fcore <= sum(block perimeters squared)/5 <= M^2/5.

The general induced-core identities simultaneously give
Fcore>=2I-2-M=136-M and total frontier length at most M. They permit
disconnected components, bridges, ears and all-boundary faces. At M23,
5*(136-23)-23^2=36>0, and the contradiction is stronger for smaller
nonnegative M. Thus two degree-five sites are compulsory there.

These are global counts. The positively labeled degree-five sites may
have boundary neighbors and may themselves be marked apices. They are
not assumed to be deep or pairwise nonadjacent.

## 3. Two complete full-face/count rows

Use four corner labels: one for degrees7/8, one for original boundary
sites, zero for degree6, and a positive label for EVERY degree-five site.
Each row checks all20 multisets of three labels, including every
positive/boundary combination. The full-simplex support includes its
degenerate-vertex cap and requires label range below one.

Nonnegative interface credits may be assigned to each of the three
interior labels on a boundary/interior edge of a q0 face. Every marked
apex has at least two terminal q0 incidences, so its vertex score can
receive the corresponding two credits. All unspent credits are safely
discarded. The positive degree-five label is included in this accounting.

For each row, all16 types p=0,...,3 and d=5,...,8 are checked using the
global marked conjugate with ZERO squared-edge and half-side penalties.
The vertex majorant subtracts one nonnegative flag multiplier for each
degree-five site. Its sum therefore subtracts two flags when M<=23 and
one flag otherwise.

The first row is evaluated at M23 and has strictly positive M slope,
covering every M<=23. The second is evaluated at M24 and has strictly
negative M slope, covering every M>=24. Both have strictly negative
shifted-ear coefficients and bad-q1 coefficients. The actual-ear cap
and bad-face radial slab use only centers inside the unit disk, so
arbitrary ears and all-boundary faces are permitted from the outset.

The unchanged concave outer boundary bound is simply31H(pi/31).
No lens variance, fan charge, metric edge support or local catalog is
used. All40 full-face supports and32 vertex inequalities pass. The
minimum area gap is

    3797228001573004612011/10^24 > .003797228.

## 4. Scope and replay

Run python -B verify_B31_global_low_degree_0p11323.py with assertions
enabled. It rechecks the99-disk exclusion, footprint, degree-window
constants, both global curvature-count consequences, every rational
face/vertex support and all coefficient signs. The rational proposals
and actual raw-Python result are separate files; no optimizer is called
by acceptance.

This excludes the projected/normalized B31 branch at R. Other boundary
counts and a new universal radius bound are separate obligations.
The inherited finite-type strict-margin closure covers nongeneric
endpoint configurations. Earlier frozen checkpoints are unchanged.

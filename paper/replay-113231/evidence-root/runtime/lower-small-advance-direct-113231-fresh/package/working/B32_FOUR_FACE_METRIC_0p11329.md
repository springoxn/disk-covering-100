# Conditional four-face B32 metric bound at R=.11329

Assume a cover has first been normalized at R=11329/100000. Its center
triangulation has B32 and68 interior sites of degree6, and the induced core
is a simple chordless disk with26 boundary vertices and108 triangular faces.
Assume the ordinary annulus consists of32 marked triangles and26 outer-ring
q0 triangles. These are explicit structural premises, not proved here.

There are42 deep sites. Every core-boundary edge is incident to a distinct
core triangle with one deep and two ring vertices; chordlessness excludes
a second boundary edge or third ring vertex. Thus26 faces have type DRR.
Every other core face has at least two deep vertices. The total deep core
incidence is42*6=252. The ring incidence is324-252=72, of which52 belongs
to DRR. Hence exactly20 DDR faces remain and62 are DDD. Outer ring faces
have type BRR, one original boundary site and two ring sites.

Assign the same potential0 at each deep site, LR=-.20663069056 at each ring
site and LB=-.72993038978 at each original boundary site. Put coefficient
-tau opposite the core-boundary side in each DRR face and+tau opposite
the same side in the adjoining BRR face, tau=.6623191134.
Each signed term is its coefficient times L/(2R), so the26 pairs cancel
exactly regardless of individual circumradii.

The exact generic signed-sine helper bounds each entire closed angle
simplex, including every degenerate boundary edge. The guard
range(labels)+sum(negative coefficient magnitudes)/2<1 is checked for
each of the four patterns. Convexity in circumradius ratio reduces to
rho0/rho1; the rho0 pure-angle maximum is covered by the vertex caps.
No actual face is assumed equilateral, acute, or circumradius-saturated.

The marked faces contribute32*C_k(LR-LB), k=.44. The q0 centered-angle
sum gives the correction
    -32*LR*pi/3 + LB*(2*pi+26*pi/3).
Add the separately replayed same-radius normalized linear-halfside boundary
envelope. It uses one outer loss and no boundary-turn window, fan charge,
or hinge charge. The exact four-pattern sum is strictly below pi.

Run python -B -S verify_B32_four_face_metric_0p11329.py. This is a conditional
structural-family exclusion. A universal bound also needs a same-radius
reduction proving the premises and treatment of every other boundary count.
The existing independently audited .11325 sixteen-family result is unchanged.


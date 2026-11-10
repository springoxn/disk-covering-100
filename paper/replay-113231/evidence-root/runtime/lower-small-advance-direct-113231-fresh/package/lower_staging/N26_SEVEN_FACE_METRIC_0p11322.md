# Seven-pattern metric exclusion of the B33/M26 profile

## Conditional topology, independent of any lattice catalog

Assume m100, B33, M26, no ears or bad q1 faces, and exactly one interior
degree7 vertex, every other interior degree6. These are one of the two
survivors of verify_B33_highM_no_ears_0p11322.py. Let c be the number of
components of the graph induced by the67 interior sites, and n_j the
number of q0 faces with j original boundary sites. The already proved
induced-core identities give

 b_core=26-4(c-1)-n3, F_core=106+2(c-1)+n3,
 n2+n3=2(c-1).

If c>=2, blockwise nonnegative-curvature disk isoperimetry would give
108<=22²/6, impossible. Hence c1 and n2=n3=0. The induced core is connected,
has total frontier walk length26, and has106 triangular faces. A bridge
would leave total face-block perimeter at most24, contradicting106>24²/6.
Multiple cyclic blocks would give at most(3²+23²)/6 faces. It is therefore
one simple disk. A boundary chord would split it into perimeters at least3
whose sum is28, giving at most(3²+25²)/6<106 faces. Thus it is chordless.

If the degree7 vertex were strict inside this core, its net strict degree
excess would be1. First boundary peeling gives frontier at most19, hence
F<=26+19+19²/6<106. Thus that vertex lies on the26-vertex core boundary.
All41 deep vertices have degree6. No metric equilateral development,
injectivity theorem, or finite catalog is needed for these conclusions.

The original outer-boundary chords are also absent: an adjacent face
would have at least two original boundary vertices and would be a q0-B2,
q0-B3, bad q1, or ear, all excluded above. The annulus between the two
simple boundary cycles consists of33 marked faces and26 q0 ring faces.
Every ring vertex meets exactly two ring faces. If its marked count is p,
its number h of incident core triangles satisfies d=h+p+2. Chordlessness
gives h>=2, so the special vertex has p=0,1,2,or3; ordinary ring vertices
have p<=2.

## Three face regions

Every core-boundary edge has a core triangle with one deep and two ring
vertices. Two boundary edges cannot belong to the same triangle, since
that would force a boundary chord. Hence there are exactly26 distinct
interface triangles. The other80 core triangles have at least two deep
vertices. All26 outer ring triangles have one original boundary vertex
and two ring vertices. There is only one special ring vertex.

Assign common corner labels D=0 to deep sites, O=-13/100 to ordinary ring
sites, H=-12/25 to the special vertex, and B=-14/25 to original boundary
sites. The seven possible patterns are

 DDD, DDO, DDH; DOO, DOH; BOO, BOH.

Put the signed term -tau*rho*sin(alpha), tau=49/100, at the deep corner of
each interface face, and +tau*rho*sin(alpha) at the boundary corner of
the matching outer ring face. Here rho is that face's circumradius divided
by R. Both magnitudes equal tau times the common edge length divided by2R,
so the26 signed pairs cancel exactly, even when circumradii differ.

For each face, the exact generic support bounds area/R² plus these signed
terms and PLUS sum ell*(angle-pi/3). It checks the whole angle simplex,
all three boundary-edge caps, and the localization guard
range(ell)+sum(max(-tau_i,0))/2<1. The minimum guard here is11/40.
For actual rho<=1, the score is convex in rho; the rho0 endpoint is covered
by the same vertex caps. No actual face is assumed acute or saturated.

If the special marked count is p, the core corner incidences are246 deep,
67+p ordinary ring, and5-p special. The outer ring incidences are26 B,
50 O, and2 H. The seven exact supports produce region intercepts and
shared per-label charges, whose sums use exactly these incidences.
All corner labels remain the same across core, ring, and marked faces.

## Closing area inequality

Use the unconditionally verified normalized boundary support with linear
halfside coefficient k=11/25. It contributes

 Q=33[H(pi/33)+k*R*sin(pi/33)*rho_inner(pi/33)].

The marked faces contribute (33-p)C_k(O-B)+p C_k(H-B). Summing the centered
corner labels gives the exact correction

 -[(33-p)O+(p-1)H]*pi/3 + B*(2pi+26pi/3).

The shared-edge metric terms cancel before this sum. No hinge charge is
spent in this final metric inequality. Prior hinge arguments are used
only to establish the structural premise.

The executable verify_N26_seven_face_metric_0p11322.py checks seven local
supports and all four integer p cases. Its smallest strict area margin is
1062564945331002350661/(5*10^23)>.00212512. Thus the entire stated M26
profile is impossible at R=5661/50000. M27 and other B branches are outside
this local theorem's scope.

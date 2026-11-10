# Independent audit: B33 M26/M27 regional metric exclusions at R=.11322

Date: 2026-10-05 UTC. Result: **PASS, conditional scope only**.

This is a fresh mathematical and implementation audit of the two regional methods, not a reliance on earlier constructor or reviewer reports. No reviewed source was changed. The four staged regional sources were byte-identical to their current working counterparts when reviewed.

## Scope and excluded claims

Assume the normalized generic simple straight center-triangulation model at R=5661/50000, with m=100, B=33, no ears and no bad marked faces. The normalized center-norm hypothesis is |z|^2<=1-R^2=2467953079/2500000000. The two separately supplied degree/count profiles are:

- M26: exactly one of the 67 original interior vertices has degree seven; all other original interior vertices have degree six
- M27: all 67 original interior vertices have degree six

Under those premises both profiles are impossible. This receipt does not certify the hinge/high-M reduction supplying these premises, any low-M branch, another B branch, or a universal R=.11322 lower-bound claim. No catalog, equilateral development, lattice injectivity, acuteness of actual faces, or saturation of actual circumradii is used. Generic-to-degenerate and normalization-before-classification remain assembly-level premises; this audit does not claim reflection preserves an already fixed graph.

## Fresh complete regional replays

Both complete staged scripts were run with Python 3, assertions enabled and PYTHONDONTWRITEBYTECODE=1. Their BASE resolution imported the shared working dependencies without moving or changing reviewed files.

- verify_N26_seven_face_metric_0p11322.py: PASS, seven supports, four p cases
- verify_N27_metric_chord_cases_0p11322.py: PASS, seven supports, three chord-count cases

The respective exact minimum area margins are

- M26: 1062564945331002350661/500000000000000000000000 > .00212512, at p=0
- M27: 675506006906614092373/125000000000000000000000 > .00540404, at chord count two

The minimum regional/core face-majorization slack is, for both scripts,
79999999999999/8000000000000000000000 > 0.
The minimum localization guards are 11/40 and 51/100 respectively.

Both scripts were also run under -O; each rejected execution with RuntimeError('Assertions must remain enabled') before certifying anything. The nonzero exits for those two negative tests are expected. The generic full-face helper freshly passed all 1,224 exact grid diagnostics and five invalid-domain rejection cases.

For the two marked multipliers actually used, s=43/100 and s=2/25 with k=11/25, an independent closed-form stationary-root evaluation overlapped each bisection conjugate interval. The acute cosine solves 4c^2+(1-k)c+s-2=0; the obtuse cosine is c=s/(1-k). Both branches and their endpoint regimes are part of the support, so this comparison does not presume acute actual apices.

## Induced topology, holes and blocks

At e=0, Euler plus actual face-edge incidences give, for component count c and q0 counts n_j,

b=M-4(c-1)-n3,
F=132-M+2(c-1)+n3,
n2+n3=2(c-1).

Every bounded region of the induced original-interior graph is filled with surviving original triangles: an original outer-boundary vertex cannot lie inside an interior-edge cycle. Thus there is no missing bounded hole. Splitting at cut vertices and bridges produces face-bearing simple disk blocks. A strict block-interior vertex retains its full original star, since an edge leaving the block would cross its outer cycle. All such degrees are at least six in both profiles. The independently reconstructed /6 disk isoperimetry therefore applies blockwise; unused bridges consume exterior-walk length without adding faces.

For M26, c>=2 would require F>=108 with b<=22; for M27 it would require F>=107 with b<=23. Both contradict F<=b^2/6. Consequently c=1 and n2=n3=0. A bridge leaves face-block perimeter at most24 or25, contradicting 106>24^2/6 or 105>25^2/6. Two or more cyclic blocks have maximal square sum at perimeters (3,23) or (3,24), also too small. Each core is consequently one simple disk, with (P,F)=(26,106) or (27,105).

The original outer boundary has no chord. A face adjacent to such a chord would have at least two original boundary vertices, and would be an excluded q0-B2/q0-B3, bad marked face, or ear. Each exposed core-boundary edge has exactly one q0-B1 triangle on its removed side. Thus the outer ring has precisely P triangles, one per core-boundary edge. Every ring vertex occurs in exactly two of those triangles, the two exposed edges incident to it. Every ordinary marked apex is on the core boundary because it has original outer-boundary neighbors.

## M26 specific structure and exact incidences

A core chord would split the P26 disk into two subdisks of perimeter at least three whose sum is28. The maximal /6 upper bound is (3^2+25^2)/6=105+2/3<106. Hence the core is chordless. If the unique degree-seven vertex were strict inside it, the strict degree excess would be one. Chordless first peeling leaves total frontier at most19 and gives

F<=26+19+19^2/6=105+1/6<106.

The special vertex is therefore on the ring, and the 41 deep vertices all have degree six.

No core triangle can have two boundary edges without a third-edge boundary chord. The core triangle incident to any boundary edge has one deep and two ring vertices. There are exactly26 distinct interface triangles. The other80 core triangles have at least two deep vertices. The 26 outer-ring triangles have one original boundary and two ring vertices. With only one special ring vertex, the exhaustive patterns are DDD, DDO, DDH; DOO, DOH; BOO, BOH.

For a ring vertex, original degree d=h+p+2, where h is its number of core-triangle incidences and p its marked count. Chordlessness gives h>=2, so the special marked count is p in {0,1,2,3}. Its core incidence is 5-p. The other25 ring vertices have total core incidence 25*4-(33-p)=67+p; the deep incidence is 41*6=246. The total is 318=3*106. Outer-ring incidence is26 original-boundary corners,50 ordinary-ring corners,2 special-ring corners. The marked counts are33-p ordinary and p special. These are actual incidence identities, not relaxed or catalog-dependent counts.

## M27 chord and ear completeness

There are exactly40 deep vertices. At any stage after t empty-side ear removals, the disk has P=27-t and F=105-t, with all40 deep vertices still strict interior and degree six.

A chord with deep vertices on both sides would give two subdisks each having perimeter at least six: a disk with strict degrees at least six and perimeter at most five has no strict interior vertex, by the curvature/ear argument. For t=0,1,2 the maximal split bound is [6^2+(23-t)^2]/6<105-t. Such a chord is impossible.

Every remaining chord therefore has an empty-deep side, a triangulated polygon. That side has an ear vertex other than the chord endpoints. This follows directly from the rooted polygon triangulation (or the two-ear theorem, since the closing-edge endpoints are adjacent in that polygon). Removing that ear removes exactly one boundary vertex and one face. The ear has core degree two, so it has no deep neighbor; all40 deep stars and their strict status are preserved. Its opposite edge is a chord that becomes a boundary edge, while its two incident boundary edges disappear. There are no other chords at the degree-two ear. The chord count therefore falls by exactly one.

Three such removals would leave P24,F102, contradicting 102<=24^2/6=96. Hence the original core has zero, one or two chords. This argument includes multiple chords sharing endpoints and arbitrary nesting of empty polygonal sides.

For each core triangle, j is its number of ring corners, k its number of actual core-boundary edges, and h=binomial(j,2)-k its chord incidence. The exhaustive signatures at chord count <=2 are (0,0),(1,0),(2,1),(2,0),(3,2),(3,1). The signature (3,0) needs three distinct chords; (3,3) would force the entire outer cycle to be a triangle. The seventh support is the outer-ring BLL pattern. All40 deep stars give240 incidences; hence ring incidence is3*105-240=75. The exact remaining totals are sum k=27 and sum h=2*chord_count, since every chord has two core incident faces. This does not assume any prescribed distribution of ring degrees.

## Signed metric and full-simplex support accounting

Labels are D=0, O=L=-13/100, H=-12/25, B_label=-14/25, and tau=49/100. A negative signed term is placed opposite each core-boundary edge on its core side, and the matching positive term opposite the same edge on the outer-ring side. For an actual triangle of circumradius ratio rho,

rho*sin(opposite angle)=edge_length/(2R).

The pairs cancel exactly edge by edge, including unequal circumradii and faces carrying two boundary edges. No assumption about similar triangles or angle matching is used.

The score supported by the generic helper is area/R^2 plus signed metric terms plus centered corner labels. Its scaling and nu-lambda sign agree with that definition. The guard range(labels)+sum max(-edge,0)/2<1 localizes every nonacute interior maximizer away. All three angle-simplex boundary edges are nevertheless explicitly retained. For T<=0 their scores are convex and endpoints suffice; for T>0 an interior stationary cap is retained whenever |d|<T. Equality cases are endpoint cases. Thus degenerate edge/vertex caps are not discarded.

For rho in [0,1], the physical score is convex in rho because its quadratic coefficient is nonnegative triangle area. The rho=1 branch uses the full-simplex bound. The rho=0 linear branch is included in the same vertex caps. Neither the actual radius ratio nor the actual face is assumed saturated or acute.

The helper return lower endpoint is not generally a lower bound on the constrained face maximum for an arbitrary chosen nu. Both regional scripts correctly use the helper upper endpoints for face majorization. Allowances are exact rational charges computed from those upper endpoints and the lower equilateral enclosure A.l/S; replacing that lower value by the true A in the final sums is safe. Epsilon=10^-8 gives strictly positive face gaps. Negative interface/boundary charges are multiplied by exact incidence counts, not a loose upper count.

## Centered-angle and marked/half-side closure

At an interior vertex the full angle sum is2pi; at original boundary vertices the total is(33-2)pi. Removing ordinary marked angles and their centered incidence counts yields the following exact residual corrections after combining the marked-face supports:

M26: -[(33-p)O+(p-1)H]*pi/3 + B_label*(2pi+26*pi/3)
M27: -33L*pi/3 + B_label*(2pi+27*pi/3).

The marked multipliers are respectively O-B_label=43/100 and H-B_label=2/25, or L-B_label=43/100. The code signs agree, including the N26 augmented subtraction using lb=-B_label.

The full-apex marked conjugate bounds triangle-plus-anchor area minus k times normalized half-base plus the relative apex multiplier. The normalized boundary envelope adds the same half-base payment with k=11/25 and curvature zero, so it is spent and restored once. At mu=pi/33 and rho_inner=cos(mu)-sqrt(R^2-sin(mu)^2),

H(mu)=mu-sin(mu)*rho_inner,
R^2*sin(asin(sin(mu)/R)-mu)=R*sin(mu)*rho_inner.

Therefore the Q used by each script is exactly
33*[H(mu)+k*R*sin(mu)*rho_inner].
Both set R, B=33, k=11/25 and curvature zero before freshly invoking the boundary verifier, and both check the center-norm hypothesis returned by that verifier. The normalized lens displacement and perimeter costs are accounted only once. Neither final regional inequality spends a hinge charge; prior hinge work is needed solely to establish structural premises.

## Outcome

All checked local domains, seven-pattern/signature completeness, geometric edge multiplicities, exact actual angle incidences, interval rounding directions and final strict margins are consistent. No correctness defect was found within the stated conditional scope. Machine replay alone would not prove the topology; the independent combinatorial reconstruction above is part of this receipt.

## SHA-256 bindings

- `lower_staging/verify_N26_seven_face_metric_0p11322.py`: `be804ee16012ee559627155c1275e5b12090bdd3dbad5740ee69a144a9dd8f15`
- `lower_staging/N26_SEVEN_FACE_METRIC_0p11322.md`: `66c16a5bdf0790b49e6ab8b3ef8f8fac8f29e5003b6c472896754fd23e74d70c`
- `lower_staging/verify_N27_metric_chord_cases_0p11322.py`: `e4c6e4c6697480e969b9a4d477db0712da507b02e7a98dca07f5f42cc347fac8`
- `lower_staging/N27_METRIC_CHORD_CASES_0p11322.md`: `5294f6673e946912d1a796ab54f7baa33716c7896b4d719fc6549f69aa041340`
- `working/exact_signed_sine_full_face_support.py`: `9771385657022f006daf986057165db0514e296b0538a7e81d99808a772487e3`
- `working/SIGNED_SINE_FULL_FACE_LOCALIZATION.md`: `6393c6f64784f2abe671817d9976ca01bedad63d893db6e9d84f48c71f177ba7`
- `working/signed_edge_metric_20261004/exact_signed_conjugates.py`: `cbf8cbb7ec769cd504077631be5df971caed8d24996515cce5df9dc389cbab70`
- `working/exact_linear_halfside_marked_conjugate.py`: `12308a08e76ead613dc36555bc16026bfaf0ea928dda6f18d18b1f4e8ccc23e4`
- `working/FULL_APEX_LINEAR_HALFSIDE_CONJUGATE.md`: `185362d74fb02d89ecb07472b3f4efc71c8bbb301ce3ef49eb2617f76f7c5356`
- `working/verify_star_lp_duals.py`: `23568fed518e451d3d6b7f11603e080546bb74afa020ef0fd8fbb1a3b02be6d7`
- `working/verify_potential_star_duals.py`: `d4609b4441dae93c105966dd28f72b2e9d84342f012dd519dca25f2515e3e2c3`
- `working/exact_angle_conjugates.py`: `cee5e03352e7b6c94ecbe5dbf0cd43f97342c9c23492b6820e7fc935fc8d1cb9`
- `working/verify_exact_lens_boundary_0p11322.py`: `3c6e6a762c5681a70d06606c27e755743e5c851fe92055495207924e7a6737b1`
- `working/EXACT_NORMALIZED_LENS_PENALTY.md`: `cf9b4a8f68bb9cf8c1c06888cfd70a437c91a4f6234d42dea5b5ffc35f957ca7`
- `working/UNMARKED_LOW_DEGREE_CORE_OBSTRUCTION.md`: `79372435a76d0b935a41ce3b003d4a96d39f44b172bdccb5c2f426dc0039ae5e`
- `working/GENERAL_FIRST_BOUNDARY_PEEL_CHORDS.md`: `baf1def00b7dceceb95c4b34564120ae064241a7c67d1096abc4b736d5b3f56f`
- `working/lower_bounds_extension_20261004/GENERAL_DISK_ISOPERIMETRY.md`: `3dd646f173e5b840370d725260d98500d7c2e1b6b7ce87feecbfaf7e8a92de38`

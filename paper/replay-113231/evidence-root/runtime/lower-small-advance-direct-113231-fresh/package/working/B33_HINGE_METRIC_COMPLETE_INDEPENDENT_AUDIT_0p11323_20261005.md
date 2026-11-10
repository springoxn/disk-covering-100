# Independent mathematical audit: complete B33 branch at R=.11323

Date: 2026-10-05 UTC. Result: PASS for the normalized B33 branch.

This is a fresh audit of the argument and its implementation, not an acceptance of the author or constructor status. The companion JSON contains a fresh complete entry result, source hashes, primitive replays, and the optimized-mode rejection. All reviewed sources were preserved. The result excludes the entire normalized B33 branch at R=11323/100000. It does not certify other boundary counts, a universal .11323 lower bound, or the exact optimum.

## 1. Radius, normalization, and replay binding

The hypotheses are the inherited generic simple straight center-triangulation for a cover of the closed unit disk, with m=100, B=33, I=67, every selected triangle circumradius at most R, and every center satisfying norm squared at most 1-R^2=9871789671/10000000000. This is a condition obtained after normalizing the whole cover, before determining irredundancy or any boundary count.

For a center d*u outside C=sqrt(1-R^2), the replacement d'=C^2/d satisfies

|x-d'u|^2-R^2 = (d'/d)(|x-du|^2-R^2)+(1-d'/d)(|x|^2-1).

Since 0<d'/d<1, this preserves the center's covered subset of the target disk and sends it inside C. It need not preserve an already classified graph. The .11322 normalization cap cannot be imported into a .11323 diagram.

The exact entry was freshly replayed with Python -B -S and assertions enabled. Its six component outputs all PASS, and the complete JSON equals the constructor receipt exactly. Its .11322-named regional modules run in fresh subprocesses with their R explicitly overwritten by 11323/100000; each then resets the boundary module to that same R, B=33, k=11/25 and zero variance before computing the final area expression. Their local signed-simplex supports are radius-free. Thus their filenames do not hide a transferred stronger norm hypothesis. The entry correctly rejects Python -O before certifying anything.

The old and new low-M proposal tables have identical rows. Replacing only the old table's top-level radius metadata yields exact equality of the entire tables. The local M25 replacement therefore uses the same original coherent coefficients that the .11323 raw row uses.

## 2. Low-M premises and the original charged row

Write e for q2 ears, b for all-boundary bad q1 faces, U for q0 boundary-corner incidences, and M=U-2e. Direct incidence and Euler identities are

q0=132+e, ordinary q1=33-2e-b,
sum p=33-2e-b, sum(d-6)=27-M-e-b,
q0 boundary-angle sum=Gamma+(e-2)*pi, U=M+2e.

The old normalized area budget is freshly evaluated at R. Its strict comparison with the degree-four loss threshold proves the full degree window 5..8, including marked or boundary-adjacent interior vertices. The degree-at-least-nine exclusion follows from the complete-star/anchor loss and the positive derivative checked at degree nine; it does not rely on a marked-incidence maximum or acute actual triangles. A proper marked fan satisfies p<d because a complete all-marked interior fan would cone off the whole disk and leave only one interior vertex.

Deleting original boundary sites yields only surviving triangular bounded faces: no original boundary site can lie inside a cycle of interior edges. If c counts induced-interior components and n_j counts q0 faces with j original boundary sites, then

n2+n3=e+2(c-1), frontier=M-4(c-1)-n3,
Fcore=132-M+2(c-1)+n3.

Strict vertices of a face-bearing block retain their original full stars. Blockwise /6 and /5 isoperimetry applies even with bridges, isolated sites, cut vertices, or disconnected frontiers. The metric core-area/perimeter comparison excludes M<=21. The core-curvature deductions guarantee two distinct strict-block-interior degree-five witnesses for M22/23 and one for M24/25, after the degree window. Each selected witness has no original boundary neighbor; merely p=0 would not suffice for the restricted face list, but the block argument supplies the stronger premise.

The boundary hinge is spent once. Its scalar loss dominates .03*(.092-t)_+, and a p-owner chooses p+1 endpoint cells with total half-arcs at most asin(3R). A cell belongs to at most two such owner sets, including split fans and arbitrary ears/bad faces. Consequently gamma_p=.03*((p+1)*.092-.6934/2)_+/(2R^2). The factor 1/2 is essential and present. No variance allocation is added to these same losses.

For label l, degree d and marked count p, subtracting centered angles and summing marked supports gives the checked vertex score

p*(C_k(l+lb)-C_k(0))-l*(6-d+p)*pi/3
 +(d-p)*charge_l-2*tau_l*[p>0]-gamma_p.

The terminal BI credit is justified by at least two transitions between a proper nonempty marked subset and q0 faces in that interior vertex link. The face credit counts those actual edge occurrences. Split fans and q0-B2 faces do not break this count. The exact vertex majorization uses the exact Euler sum, the exact marked-incidence sum, and the apex count at most U. Its M slope is s=-eta+apex+charge_B-lb*pi/3. The ear and bad-face coefficients are respectively

A-2*C_k(0)+M2-2*beta+eta+lb*pi+2*s,
M1-C_k(0)-beta-eta.

Both are strictly negative in every low-M row, so ears and bad faces are retained before their nonpositive contributions are dropped.

The M22 row has negative M slope and excludes M22/23. The M24 profile row forces uniqueness of the original degree-five vertex by its extra neutral-five reduced cost. The independent /5 chordless-core and peeling argument then isolates all its neighbors as degree six, validating the special eleven-face list and the fresh M24 isolated row. The first row is used to derive that premise; its loss is not added again to the second row.

At M25 the raw area margin is negative,
-28994002536586408383/100000000000000000000000.
Every extra neutral degree-five vertex has slack at least 1683876589/10000000000. The resulting uniqueness margin is positive, 186896368934501372617/100000000000000000000000. Thus the guaranteed selected deep degree-five is the unique original degree-five vertex. Its remaining 66 interior sites have degrees 6..8. Euler gives total high-degree excess 3-e-b<=3, so the selected five has at most three high-labelled neighbors. No other positively labelled site can occur in an outside face.

## 3. Coherent M25 replacement and no double-counting

The replacement retains exactly the original potentials
H=-.33285141, B=-.27065539, O=0, P=.30011312,
and charges cH=.0242021094, cB=.0138623045, cO=.00000005, cP=.0343633517. Every H-B edge retains credit .0195349539 in its original allowance U(f)=A+sum charges-credit*number(H-B edges), where A=3sqrt(3)/4. All sixteen original full-face inequalities are rechecked before the replacement.

The selected degree-five vertex has a simple five-cycle link. Its five central triangles are distinct q0 faces. Each opposite link edge is II, so its other incident face is q0 and outside the central star. An outside face can meet one or two selected link edges, never three, since a five-cycle has no triangle. If j faces meet two edges, j is 0,1,2 and the other 5-2j meet one. A two-edge outside face is paid once with its joint support, rather than twice with one-edge supports. The twelve ordered one-edge H/O,H/O,H/O/B signatures and eight two-edge H/O signatures are complete under relabelling.

Reserve epsilon=3/10 of the actual central star area and give its actual perimeter coefficient -kappa/(2R), kappa=39/100. The polygon-star theorem bounds this contribution by support(5,epsilon,-epsilon*13/10). Its proof uses polygonal isoperimetry on the shared actual neighbor coordinates and P/(2R)<=5*sin(2pi/5). For a negative perimeter coefficient the resulting support is the maximum of the convex area expression at its zero and maximal-area endpoints. This is a joint polygon inequality; it is not a sum of independently optimized triangles.

The remaining central area coefficient is 7/10. For each of the six cyclic high-neighbor patterns, retain the neighbor potentials and replace the center potential temporarily by a rational y. The full center angle sum is 2pi, so the centered sum is pi/3; the correction -(y-P)*pi/3 is therefore exact. Each residual complete-simplex support checks range(potentials)<7/10. All closed simplex-edge caps remain included.

Each outside selected side receives +kappa*L/(2R). These terms cancel the central perimeter exactly, since rho*sin(opposite angle)=L/(2R) for each actual face; equal circumradii are unnecessary. Each outside support is compared against the SAME old U(f), including any H-B credit. The maximum excesses D1 and D2 are paid through max_j[(5-2j)*D1+j*D2]. Thus unselected faces, all original corner-potential terms, all interface credits, marked-face supports, vertex charges and the original hinge allocation remain unchanged.

The original five central allowances total 5*A+5*cP+2*k*cH+(10-2*k)*cO. Subtracting the supported joint central value and the paid outside excess gives, in every one of six neighbor cycles, normalized gain at least

17237402312060949175547/250000000000000000000000
= .068949609248243796702188... > .06894960924.

This gain is slack inside the original coherent q0 row. It is not an unweighted star deficit appended to faces already spent. There is only one selected region, so no overlap with another replacement is charged. Multiplying by the SAME R squared and adding to the negative raw margin gives

1485162958120034752274159624963/2500000000000000000000000000000000
= .00059406518324801390090966... > 0.

The uniqueness reduction is a structural deduction from the weaker original row. Strengthening that same row cannot invalidate it, and its reduced cost is not stacked a second time in the final M25 comparison.

## 4. High-M degree theorem and exhaustive profiles

The fresh high-M row gives the positive label to EVERY degree-five vertex, including marked and boundary-adjacent sites. It verifies all twenty label multisets, rather than omitting positive/boundary faces, and all 26 degree/marked-count types d=5..8, p<d. Its positive flag is subtracted at least once if any degree five exists. The strictly negative M, shifted-ear and bad-face coefficients prove a contradiction for all M>=26, with exact area margin

146810961635931078341/1000000000000000000000000
= .000146810961635931... .

Hence every original interior degree is at least six. Euler then leaves precisely four integer profiles:

1. M26,e0,b0, exactly one degree seven
2. M26,e1,b0, all degrees six
3. M26,e0,b1, all degrees six
4. M27,e0,b0, all degrees six

The separate region proofs do not spend the earlier hinge again; they use it only through the established degree/profile premises.

For M26/e0, c>=2 would require F>=108 with frontier<=22, contradicting /6. Thus the induced interior graph is connected. Any original BC chord separates the disk; connectedness puts all interior sites on one side. The empty side is a triangulated boundary polygon and has an ear at a vertex other than the chord endpoints. That is an original q2 ear, contradicting e0. A bad q1 face necessarily has an original BC chord. Profile 3 is consequently impossible without any extra area charge.

For profile 1 the induced core is one simple chordless P26/F106 disk: bridges consume two frontier units, multiple cyclic blocks give at most (3^2+23^2)/6 faces, and a chord gives at most (3^2+25^2)/6<106. If the degree seven were strict inside, peeling gives frontier<=19 and F<=26+19+19^2/6<106. Thus it is a ring site and all 41 deep sites have degree six. There are 26 distinct DRR interface faces, 80 bulk faces with at least two deep corners, and 26 BRR outer-ring faces. Seven signatures, four possible special marked counts p=0..3, and exact incidences retain one common set of labels and cancel 26 physical shared-edge terms. Their minimum .11323 area margin is 1565990173293773571673/1000000000000000000000000.

For profile 4 the same block argument gives one simple P27/F105 disk with 40 degree-six deep sites. Any chord having deep sites on both sides violates the split /6 bound at the first three stages. Every chord therefore has an empty side with a degree-two ear other than its endpoints. Removing the ear preserves all deep stars and reduces chords by exactly one. Three deletions would give P24/F102, impossible by /6. Thus there are at most two chords. The six core signatures and one outer-ring signature are complete; their exact totals are 105 core faces, 75 ring incidences, 27 boundary-edge incidences and twice the chord count. The minimum .11323 area margin is 193819503011713342349/40000000000000000000000.

## 5. The one-ear profile and angle correction

For profile 2, connectedness follows from the same 22^2/6<108 contradiction. With c=1, n2+n3=1. The n3=1 alternative would give P25/F107 and violates /6, so n2=1,n3=0. Bridges, multiple blocks and core chords are excluded by the same P26/F106 comparisons. The simple chordless core has 41 degree-six deep sites.

The core counts are exactly 60 DDD,20 DDR,26 DRR: 246 deep incidences and 72 ring incidences determine them. There are 26 BRR outer-ring q0 faces and one BBR q0 face, so q0 has 133 faces, 28 original-BC incidences and 125 ring incidences. The remaining marked faces are 31 ordinary q1 and one q2 ear. These give the five-pattern count vector [60,20,26,26,1] in the source.

Use D=0,Rlabel=-1/5,Blabel=-7/10 and tau=16/25 on the 26 interface pairs. Their actual physical length terms cancel once. The q0 ring centered-angle sum is 31*pi/3-Gamma, and the q0 BC centered-angle sum is Gamma-pi-28*pi/3. Subtracting them and applying the 31 marked multipliers Rlabel-Blabel produces exactly

-31*Rlabel*pi/3+Blabel*(pi+28*pi/3).

This verifies the otherwise easy-to-miss ear shift in the angle correction. The q2 ear cap contains that ear's area, BOTH anchor caps and BOTH -k halfside penalties. The same k=11/25 is paid once by the freshly verified normalized boundary envelope. No extra hinge debit appears. The exact one-ear area margin is 1111363882648582574057/200000000000000000000000>0.

## 6. Local support domains, rounding, and endpoint scope

Every invoked signed-simplex support bounds area/R^2 plus signed L/(2R) coefficients and centered corner labels. The guard is range(labels)+sum negative coefficients/2<positive area weight. The acute scalar dual has the correct nu-label sign. All three closed simplex edges are retained, including stationary edge caps when positive combined sine coefficient and the label difference permit one. Actual circumradius ratios in [0,1] are handled by convexity in that ratio; the zero-radius linear endpoint is among the vertex caps. Neither actual acuteness nor saturated circumradii is assumed.

The helper's lower endpoint encloses its chosen support expression, not necessarily the true constrained maximum. Invoking code consistently uses upper endpoints for majorization and lower allowance endpoints for gains. Regional charges computed using A's lower interval endpoint are safely restored with the true A in final sums, with exact signed incidence totals even when a charge is negative.

Fresh primitive replays PASS: 1,224 signed-simplex diagnostics and five invalid-domain rejections; 582 polygon scalar diagnostics; Jensen/slab ear domains; 18 full-apex marked conjugates; and the range-one simplex backend. These tests supplement the geometric and analytic arguments above; sampling is not substituted for proof.

For arbitrary endpoint covers, the normalized generic branch theorem must be used through the inherited enlarged-cover, normalize-first, generic-perturbation, fixed finite-type subsequence and closed-domain limit argument. The strict final margins persist in those limits. This receipt does not claim same-radius arbitrary perturbation, or reflection preserving a fixed diagram. Promotion to a universal .11323 theorem still requires independently verified same-radius exclusions for every other surviving B and the full assembly. Determining the optimum remains separate.

## Bindings and outcome

No mathematical correctness defect was found in the stated B33 branch. The companion JSON binds all reviewed sources and records every fresh component result. Its minimum reported area margin is the all-degree-five contradiction, 146810961635931078341/10^24. The proof and receipt are additive; no constructor file or reviewed verifier was overwritten.

# Complete B34 exclusion at .11315

`verify_weighted_fan_face_B34_0p11315.py` proves that a cover by at most 100 equal disks of radius R=2263/20000=.11315 cannot have B=34 boundary cells. This is one boundary-count theorem, not a global radius bound or an exact optimum.

The exact checker accepts 30 complete-triangle supports, 1446 vertex supports, 156 integer fan-budget inequalities and three final U branches. Its weakest exact area margin is

`10434999083600543573196802828257/100000000000000000000000000000000000`,

approximately .000104349990836. No graph enumeration or floating-point acceptance is used.

## 1. Same-radius geometric prerequisites

The inherited K4 footprint at full span .4566 and containing radius 2R excludes a q1 marked face whose apex is another boundary center. Its exact margin exceeds .0025629. K6 at span .693 and radius 3R gives every interior apex at most five consecutive boundary neighbors and at most four ordinary marked incidences, with margin exceeding .0107755.

Each q4 apex is therefore one four-edge fan on five boundary cells. Distinct apices have disjoint ordinary marked edges. If there are t q4 vertices, their endpoint union has at least 4t+1 cells. Each individual full arc is less than .22685, verified by sin(.22685/2)>R. The endpoint-union bound excludes t=6,7,8, so t<=5. Ears, boundary chords and unmarked all-boundary q0 faces remain allowed.

## 2. Three-label full-face supports with mixed-edge reservation

Each U branch uses three labels: -a at interior degree>=7, zero at other interior vertices, and -b at boundary vertices, with 0<b<a<1/2. Full-simplex score localization permits the exact conjugate bound

`S(l1,l2,l3)=pi*nu+sum H(nu-l_i)-(pi/3)*sum l_i`,

where `H(t)=sup_[0,pi/2](sin(2x)/2-tx)` and nu is an arbitrary rational proposal. This bounds the complete triangle support even when its actual angles are not acute.

Choose per-label charges p_l and a nonnegative interface credit tau. For every one of the ten three-label multisets, the verifier proves

`S(l1,l2,l3) <= A+sum p_li-tau*n_AB`,

where n_AB counts edges joining a degree>=7 interior label to the boundary label. It is 1 for the three-distinct-label triple, 2 for either repeated-endpoint triple, and 0 otherwise. The labels are distinct and assigned by vertex role, so this is an actual BI-edge count, not merely a sign pattern.

Every marked interior apex has at least two terminal BI edges separating its marked fans from q0 faces. An opposite face cannot be an ear, whose vertices are all boundary, and cannot be another marked face outside the same fan. Thus it is q0. Distinct marked high-degree apices have distinct terminal edges. Summed q0 mixed-edge incidences therefore number at least twice the number of marked degree>=7 vertices. Additional q0/q0 BI incidences only strengthen this bound.

Consequently the complete score of a vertex (q,d), with its label l and charge p_l, is at most

`q*[C_k(l+b)-C_k(0)]-l*(6-d+q)*pi/3+(d-q)*p_l`

`-2*tau*1_(q>0 and d>=7)`.

This deduction is already reserved in the exact q0 face inequality. It is not a second independent area charge. The general argument is also recorded in the root file `FACE_LABEL_INTERFACE_CHARGES.md`.

All labels have range below 1/2. All actual degrees from max(3,q+1) through 99 and q=0,...,4 are checked. No actual-angle acuteness or quadratic variance coefficient is assumed.

## 3. Strong actual-ear score

The common linear halfside multiplier is k=.25. Ordinary marked faces use the verified full-domain C_k support, including its obtuse endpoint.

For an actual all-boundary ear, `JENSEN_SLAB_EAR_SUPPORT.md` gives the sharper normalized cap

`M=w+sqrt(2w-w^2)-k*sqrt(2w)`,

`w=2/(1+sqrt(1-2R))`.

This follows from Delta/R^2<=min(t,w) and concavity of the combined anchor-minus-halfside function. The scalar maximum is at t=w. The exact uniform derivative guard and the cap at the actual R,k are rechecked. Here M is approximately 1.69730025, rather than the older loose 1.79.

The marked and ear penalties use exactly the same k as the boundary compensation. Each ordinary anchor is counted once and each ear includes precisely its two anchors.

## 4. One global selected-fan variance

The original nonsymmetric halfside boundary argument is rechecked at R,k with the additional deficit

`-.29*V`, `V=sum(a_i-pi/34)^2`,

where a_i are actual assigned half-arcs. Its good-arc strong-concavity guard, small-arc penalty concavity and all 24 piecewise tangent comparisons pass at R.

Let n3,n4 count q3 and q4 apices. They satisfy n4<=5 and 3n3+4n4<=34. There are exactly 52 such integer pairs.

`MIXED_FAN_SELECTION_VARIANCE.md` proves that four cells can be selected per q3 apex and five per q4 apex with at most N=n3+n4 double-counted cells. The key step is a matching among the shared gap endpoints of split three-of-four-edge fans. With W=4n3+5n4, the weights therefore satisfy

`sum w_i=W`, `sum w_i^2<=W+2N`.

Each chosen group has full-arc span at most .693. Centered weighted Cauchy gives

`V >= (W*pi/34-N*.693/2)^2/[W+2N-W^2/34]`.

Every numerator and denominator sign is checked. For each integer pair the verifier may strengthen this with the q4 endpoint-union bound or the single-q3 group/complement bound by taking their maximum. It never adds separate full-variance bounds.

`mixed_fan_variance_backend.py` enumerates all 52 pairs with exact Fractions and a rigorous lower bound for pi.

## 5. Coupled finite dual and complete U/ear coverage

For each of three U branches, the vertex inequality is

`vertex_score <= u0+beta*q+eta*(d-6)+alpha3*1_(q=3)+alpha4*1_(q=4)`.

The same row supplies a rational fan budget Z satisfying, for all 52 integer pairs,

`alpha3*n3+alpha4*n4-.29*V_lower(n3,n4)/R^2 <= Z`.

This single inequality combines the star-incidence charges with the one global boundary variance. It is valid even if either alpha coefficient is negative; no sign is silently assumed.

With U counting q0 boundary-angle occurrences and e the ear count, the exact identities remain

`sum q=34-2e`, `sum(d-6)=28+e-U`,

`q0 boundary-angle sum=Gamma+(e-2)*pi`.

The intercept u0 is nonnegative, so at most 66 interior vertices cost at most 66u0. The total normalized correction, after the fan budget, is

`66u0+34beta+eta*(28-U)-b*(2pi+U*pi/3)+U*p_boundary+Z`.

Every ear contributes the additional coefficient

`A-2C_k(0)+M-2beta+eta+b*pi`,

which is strictly negative in each row. Thus arbitrary allowed ear counts are covered. The U coefficients are positive at the U<=23 endpoint and negative at the U>=25 endpoint; the middle row covers U=24. These three branches exhaust all nonnegative integer U.

The exact final area bound is the inherited common-boundary baseline plus R^2 times this correction. Each is strictly below pi, with the minimum stated above.

## Reproducibility and limiting cases

The proposals are `weighted_fan_face_B34_0p11315_proposals.json`. Numerical optimization only generated these rational numbers. The verifier rechecks every face, vertex, fan-budget, geometric, ear and final sign. The original source ZIP and all manifest entries are hash-verified and imported read-only.

The Hall selection and terminal-edge lemmas are geometric/combinatorial hypotheses of the exact arithmetic comparisons, fully proved in the cited proof files. There is no assumption about the optimizer's chosen graph or active types.

The nonnegative q0 baseline and intercept make the argument valid for m<=100. Strict margins and the inherited fixed-finite-type limiting argument include degeneracies. Other boundary counts and exact optimality remain separate obligations.

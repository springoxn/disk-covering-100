# B32 low-M exclusion at exact radius .11323

This excludes only B32,M<=25 for a normalized100-center cover at
R=11323/100000. Normalize every center together to norm<=sqrt(1-R^2)
before constructing the actual center diagram. The high-M branch and
other boundary counts remain separate; this does not identify the optimum.

Run `python -B -S verify_B32_M25_direct_interface_0p11323.py` with
assertions enabled. Acceptance imports only the standard library and
recomputes all premises, scalar supports and81 integer cases. The exact
least final area gap is

    438410317278753918281/10^24 > .0004384103172787539.

## Fresh prerequisites

The entry freshly executes refresh_B32_low_core_0p11323.py. It establishes
the full original degree window5..8, excludes all-boundary q0/q1 faces,
allows ears, and gives at most3 marked incidences at each interior vertex.
For M<=25 there is exactly one degree5, a deep core witness with no
original boundary neighbor or marked face. Weighted core curvature
excludes M<=23. The isolated-five M24 row has area gap>.0003262447.
These are structural deductions; their old variance payments are not
also subtracted in the new functional.

For M25, with e ears and U q0 boundary-angle occurrences, U=25+2e.
Euler leaves exactly

    (e,high degrees)=(0,[7,7]),(0,[8]),(1,[7]),(2,[]).

All other interior vertices except the selected5 have degree6. The
five-cycle of neighbors of that5 consists of interior sites and all
central/exterior faces around its edges are q0 faces.

## One norm-aware boundary deficit

Use k=11/25. The entry freshly replays verify_tight_hinges_B32_0p11323
case0, which certifies at R and B32

    boundary<=Q-sum delta(t_i), delta(t)>=0,
    delta(t)>=(119/2000)*(187/2000-t)_+.

Writing mu=pi/32, s=sin(mu), rho=cos(mu)-sqrt(R^2-s^2),

    Q=32*(mu-s*rho+k*R*s*rho).

An ordinary apex owning p marked edges has at least p+1 endpoint cells.
Their assigned half-arcs sum to at most asin(3R), by the3R footprint.
Each boundary cell belongs to at most two distinct owner endpoint sets,
including split fans. Thus the single global deficit pays normalized

    gamma_p=(119/2000)*((p+1)*(187/2000)-asin(3R))_+/(2R^2).

The factor1/2 is retained. Acceptance checks sin(3467/10000)>3R, allowing
each high p3 vertex the charge

    G=(119/2000)*(4*(187/2000)-3467/10000)/(2R^2)
      =624750/9862333 > .063.

Other nonnegative owner charges are ignored. No variance is simultaneously
spent. The Jensen-plus-slab actual-ear support, at the same R,k, is

    E=w+sqrt(2w-w^2)-k*sqrt(2w), w=2/(1+sqrt(1-2R)).

Its radius domain R<=1400/11449 holds.

## Face potentials and terminal edge credit

Labels are H=-a on the at most two high vertices, B=-b on original
boundary sites, and O=0 on ordinary degree6 sites and the selected5.
Use accepted rational a,b, corner charges cH,cB,cO and terminal credit T
from B32_M25_direct_interface_0p11323_proposal.json. Define

    Phi_f=area(f)/R^2+sum label_i*(angle_i-pi/3),
    A=3sqrt(3)/4.

All9 H/B/O unordered signatures except impossible HHH satisfy the checked
complete-simplex inequality

    Phi_f<=A+sum corner_charge_i-T*N_HB(f),

where N_HB counts H-B edge occurrences in q0 faces. Every high vertex with
p>0 has a nonempty proper set of marked faces in its cyclic star. Each run
has two terminal H-B occurrences in adjacent q0 faces. Therefore the
global terminal credit is at least2T for each marked high vertex. This
is a geometric incidence credit, separate from the boundary deficit.
The selected central star has no B corner. Its removal loses no H-B
credit, and all exterior replacement supports retain that original credit.

## Coherent central-star replacement

Reserve epsilon=1/2 of the five actual central face areas. With
W=1-epsilon=1/2, tau=13/10, kappa=epsilon*tau=13/20 and
X=sum_cycle L/(2R), the audited polygon-star theorem gives

    central_area/R^2-tau*X<=max(0,S5-tau*T5),
    T5=5sin(2pi/5), S5=T5*(1+cos(2pi/5)).

Keep the original corner potentials in the residual W areas. A common
auxiliary label y at the selected5 contributes exactly y*pi/3, so correct
by -y*pi/3. Complete-simplex supports with labels divided by W bound
the residual faces; every resulting range is explicitly below1.

The exhaustive central patterns, with k high neighbors and counts of
faces having0,1,2 high base corners, are

    k0:(5,0,0), k1:(3,2,0),
    k2 adjacent:(2,2,1), k2 separated:(1,4,0).

Eight residual supports give K_pattern for sum_central Phi_f-kappa*X.
Across each cycle edge put +kappa*L/(2R) in the outside q0 face. A distinct
outside triangle contains at most two selected5-cycle edges. If n1,n2
count one/two-edge outside faces, n1+2n2=5 and n2<=2. Acceptance checks
all11 admitted one-edge and7 admitted two-edge ordered signatures,
retaining every full-simplex boundary edge and its positive sine terms.
The support is its original corner allowance and H-B credit plus D1/D2.
Consequently the total outside excess is at most

    J=max(5D1,3D1+D2,D1+2D2).

The actual signed edge lengths cancel exactly with -kappa*X. Replace
the entire five-face original allowance by K_pattern+J. Areas and angle
potentials are used once; no unweighted star loss is stacked on a
previously charged face budget.

## Exact global count formula

For each Euler profile let d_j,p_j be high degrees/marked counts,
n=67-number_high, P=32-2e-sum p_j, and U=25+2e. Let C_k(t) be the
full-apex marked conjugate with linear halfside penalty k; C0=C_k(0).
The baseline normalized center cap is

    (134+e)A+(32-2e)C0+eE
    +P*(C_k(b)-C0)-b*((2-e)*pi+U*pi/3)
    +(6n-P+5)cO+U*cB
    +sum_j[p_j*(C_k(b-a)-C0)+a*(6-d_j+p_j)*pi/3
           +(d_j-p_j)cH-G*1_(p_j=3)-2T*1_(p_j>0)].

For a central pattern with k high neighbors subtract

    5A+(15-2k)cO+2k*cH

and add K_pattern+J. The subtraction includes all five center and ten
base incidences. Enumerate all high p_j in0..3 and all patterns with
k<=number_high. These81 cases contain every realizable case and may
retain extra cases. Every one satisfies

    pi>R^2*normalized_center_cap+Q

by the stated positive exact margin. This completes B32,M<=25 only.
Numerical logs and saved result JSON are diagnostic; they are not proof
inputs. All source changes are additive.

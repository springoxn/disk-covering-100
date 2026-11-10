# Shared-apex interface for the next B33 metric refinement

This is a local support target for research, not a new covering bound.
The .1132 checkpoint is unchanged. Any use at another radius needs its
own actual diagram/domain reduction and boundary support.

## Objective and normalization

Let R be the covering radius. Let v be an interior center and c0,c1,c2,c3
four consecutive boundary-center vertices. Suppose the three ordinary
marked faces are (v,c0,c1),(v,c1,c2),(v,c2,c3), with disjoint interiors
and consistent orientation. Write L_i=|c_i-c_{i+1}| and gamma_i for the
angle at v. Define J_R(L)=(L/2)*sqrt(R^2-L^2/4).

The quantity needing a joint bound is

    S = sum_i [ area(v,c_i,c_{i+1})/R^2 + J_R(L_i)/R^2
                -lambda*(L_i/R)^2 + t*gamma_i ].

The existing separate-face allowance is3*C_lambda(t), where

    C_lambda(t) = max over a in[0,pi/2] of
      sin(a)*(1+2cos(a))-4lambda*sin(a)^2+t*a,
      sin(a)-4lambda*sin(a)^2+t*(pi-a).

The exact implementation is `exact_quadratic_marked_conjugate.conjugate`.
For0<=lambda<=1/8 this is a valid global-apex conjugate, without an
actual marked-apex acuteness assumption. A useful local certificate would
prove S<=3*C_lambda(t)-epsilon under the shared-center and actual
boundary-lens constraints. A raw ordinary-area deficit cannot simply be
subtracted from this already tilted and squared-base-penalized score.

## Existing exact dual point

The frozen final high-M row in `deep_face_B33_0p1132_proposals.json` has

    lambda = 11/100
    interior high-degree potential = -36702176/100000000
    boundary potential = -35686535/100000000
    t = -1015641/100000000
    high-degree q0 corner charge = 253747367/10000000000
    high-degree terminal BI credit = 232854236/10000000000.

Its q3,d7 vertex score is

    3*(C_lambda(t)-C_lambda(0))
    -2*interior_potential*pi/3
    +4*corner_charge-2*BI_credit.

The full area term for every q0 face is accounted separately. The two BI
credits are reserved in the q0 support on the two terminal boundary/
interior edges; they are not unused q1 losses. A new epsilon in the
displayed three-face objective may be subtracted once per eligible
shared-apex fan. Distinct apices own disjoint q1 faces.

## Necessary geometry available in the completed checkpoint

Whole-cover reflection precedes diagram classification. Therefore every
boundary center has norm in[1-R,sqrt(1-R^2)]. Every center face has
circumradius<=R, every marked base length<=2R, and all three faces share
the same actual point v. Consecutive boundary cells have covered circle
transition points. Each boundary center lies in the intersection of
the two radius-R endpoint disks assigned to its cell.

At .1132, an independent angular bootstrap excludes five boundary-center
neighbors at an apex. Hence a q3 apex has exactly four such neighbors
and its three marked boundary edges form one contiguous fan. Its four
assigned arcs lie in a3R footprint. The final high-M branch also has
every full assigned arc>.092 and the norm bound above. These conditions
must not be silently transferred to a different radius.

## Next-target diagnostic, explicitly conditional

Near .11321 the current relaxation admits roughly .0003 to .0005 excess
area. A normalized joint loss epsilon around .03 to .04 at the compulsory
q3,d7 apex could therefore be significant. A separate numerical row at
lambda=.12 has t approximately .01104818. That is only a useful support
parameter to test, not an accepted global certificate.

The reduced-cost pattern suggests that a sufficiently sharp same-radius
boundary support might leave only no-ear M26 with one degree7,q3 vertex,
or M27 with all interior degrees6. This profile reduction has not yet
been exactly established at .11321, and the M27 alternative requires
its own exclusion. Do not infer a compulsory q3 fan for every cover.

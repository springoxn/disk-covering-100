# Conditional actual-anchor fee interface for the B33 q3 profile

This document gives the exact interface needed from a separate local
three-face theorem. It does not certify that local theorem or replace
the completed 402-graph route by itself.

Set R=11321/100000, lambda=7/50, and t=1071883/20000000. The retained
high-M face row, after its independent arc/domain and radial checks,
forces e=0, M=26, 66 degree-six interior vertices and one degree-seven
interior apex incident to three marked faces. Its raw area surplus is

    delta=255452797335856006499/10^24.

The actual full boundary arcs exceed .136, their normalized half-sines
exceed .6, and marked bases exceed .9R. All centers were normalized at R
before the diagram was formed. The marked faces have circumradius at
most R; equality of those circumradii is not a premise.

## Signed accounting

Orient the boundary center cycle counterclockwise. Let z_i be the actual
circle transition point shared by successive centers c_i,c_(i+1), and
let L_i=|c_i-c_(i+1)|. The signed anchor is

    A_i=det(z_i-c_i,c_(i+1)-c_i)/2.

For each assigned half-arc a_i, with midpoint unit direction u_i, the
remaining signed outer triangle plus circular segment is exactly

    Hactual_i=a_i-sin(a_i)*u_i dot c_i.

The inherited oriented-edge cancellation, using absolute center-face
area as an upper bound if needed, gives

    pi <= sum(center-face areas)+sum A_i+sum Hactual_i.

The ordinary bound A_i<=J_R(L_i) is a relaxation of this identity.
The reflected radial Q bounds only

    sum Hactual_i + lambda*sum L_i^2.

It contains neither the signed anchor A_i nor the slack J_R(L_i)-A_i.
Consequently a joint local theorem may retain the actual A_i on a chosen
fan without changing Q or subtracting any anchor slack a second time.

## Required local theorem

For the three actual marked faces T_i at the unique q3 apex, let gamma_i
be the apex angles. A sufficient local inequality is

    sum_{i=1}^3 [area(T_i)/R^2 + A_i/R^2
                 - lambda*(L_i/R)^2 + t*gamma_i]
       <= 3*C_lambda(t)-epsilon,

where C_lambda is the same global marked conjugate used by the retained
profile verifier. This is an actual-signed-anchor theorem. It must not
be described as the corresponding statement with three independent
J_R(L_i) terms, unless that different statement is separately proved.

The profile's high-apex and boundary potentials add to this exact t.
All other marked faces may still use their separate J majorants. The
angle-potential cancellation and q0 face supports therefore give the
same global upper bound as the retained row, less epsilon*R^2.

The q0 terminal boundary/interior credits are already reserved in that
row. The local theorem must not count those credits again. There is only
one q3 apex in the forced profile, so any disjoint-three-face incidence
requirement is automatically satisfied for this one application.

## Exact sufficient comparison

The needed strict normalized fee is

    epsilon > 255452797335856006499/12816504100000000000000.

For epsilon=1/40=.025, the exact area gap would be

    R^2/40-delta=64959805164143993501/10^24 > .00006495980516.

This numerical comparison is exact. The local theorem's actual scope,
orientation conventions, continuous proof and arithmetic verifier remain
separate dependencies that must be supplied and independently audited.

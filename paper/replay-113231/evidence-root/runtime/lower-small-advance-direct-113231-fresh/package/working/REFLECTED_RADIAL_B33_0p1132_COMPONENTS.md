# Conditional B33 boundary supports at R=283/2500

This note records three independently instantiated exact boundary inequalities.
It does not close the center-face/count branches and does not assert a global
covering-radius bound by itself.

The reflected-cover preprocessing, lens-cone expansion and soft normal
correction are the unchanged arguments in REFLECTED_CENTER_RADIAL_CORRECTION.md,
LENS_CONE_RADIAL_NODE_GUARD.md and RADIAL_WEAK_MONOTONICITY_GUARD.md. In particular,
one reflects the hypothetical whole cover first, redoes its covering reduction,
and then takes a fixed-topology limit. Every selected center has norm at most
C=sqrt(1-R^2). The local radial correction is

    P(a)=(C-rho(a))*max(F_K(a),0),
    rho(a)=cos(a)-sqrt(R^2-sin(a)^2).

All three exact node guards absorb the tangential remainder. No proof that
the actual centers equal their inward radial lens tips is assumed.

For half assigned arcs a_i, let V=sum(a_i-pi/33)^2. Each instance certifies

    outer circular contribution + lambda*sum(marked edge length^2)
       <=33*L+2*pi*mu-gamma*V.

The certified pair inequality includes half of each neighboring correction
P and half of the gamma variance at each endpoint. Its affine term is
mu*(a+b), so summing around the boundary gives exactly2*pi*mu. The exact
exchange-symmetric box subdivision includes the full closed domain x=sin(a)/R
from the indicated lower endpoint to1. Natural radical bounds are retained
at h=0, and the positive-part correction has a derivative hull at its kink.

## 1. Low-core branch

verify_reflected_radial_B33_lowM_0p1132.py certifies

    lambda=7/125, gamma=3/2, x>=277/625,
    K=67349/20000, L=10526931/10^9, mu=-615539/50000000.

Its independent required full-arc cutoff is251/2500=.1004. It passed1011
pair boxes. The low-core arc bootstrap and its core-count scope are separate
dependencies; this file does not infer that arc bound from its own conclusion.

## 2. Initial high-core stability support

verify_reflected_radial_B33_bootstrap_0p1132.py certifies

    lambda=9/100, gamma=1/4, x>=121/400,
    K=370909/100000, L=2286447/250000000,
    mu=286697/500000000.

Its required full-arc cutoff is137/2000=.0685, supplied by the independent
unpenalized angular/bootstrap argument. It passed1011 pair boxes.

To use this instance as a new arc bootstrap, combine it with a center-face
upper bound WITHOUT spending gamma*V on any ear, fan or other variance loss.
If the resulting total bound is pi+delta-gamma*V, coverage requires
V<=delta/gamma. Since sum(a_i-pi/33)=0, a selected deviation d_i obeys

    V>=33*d_i^2/32.

Thus a proposed smaller arc is excluded whenever its rationally certified
33*gamma*(pi/33-a_cut)^2/32 exceeds the separately certified delta. That
new face/surplus calculation is not performed by this boundary file.

## 3. Final high-core support

verify_reflected_radial_B33_highM_0p1132.py certifies

    lambda=11/100, gamma=0, x>=2031/5000,
    K=173537/50000, L=166667/20000000, mu=6369/781250.

Its required full-arc cutoff is23/250=.092, which must come from the
separate unspent-variance calculation just described. It passed1037 pair
boxes. This final instance has no remaining variance charge; it cannot
also reserve a fan/ear variance saving.

## Exact replay and scope

All arithmetic uses the unchanged fixed-point outward interval routines,
integer square roots, rational trigonometric bounds and exact Fractions.
A timeout is PENDING, never PASS. Assertions must remain enabled. Actual
PASS result JSON files are stored beside the three entry points.

These conditional supports can be used with separate valid face/ear duals
at the same radius. A universal result additionally requires the full
effective-center and boundary-count bridge, every surviving B branch,
and endpoint/compact-attainment closure. The fresh bridge includes B31;
it must not be silently omitted when assembling a global statement.

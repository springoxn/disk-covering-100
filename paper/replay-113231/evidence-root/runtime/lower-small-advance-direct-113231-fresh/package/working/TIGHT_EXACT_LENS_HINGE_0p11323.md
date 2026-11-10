# Tighter exact boundary hinge at R=.11323

The exact normalized-lens geometry and whole-boundary signed accounting are
the unchanged theorem in EXACT_NORMALIZED_LENS_PENALTY.md. This supplement
only improves interval dependency in its affine-deficit check.

Let B=33, R=11323/100000, k=11/25, mu=pi/B, and use that theorem's concave
function F and exact displacement penalty P. Define

    delta(t)=F(mu)+F'(mu)*(t-mu)-F(t)-P(t).

The new wrapper independently rechecks delta>=0 on the whole arc domain.
It also proves, for 0<=t<=T=23/250,

    delta(t)>c*(T-t), c=181/5000=.0362.

Together these give delta(t)>=c*(T-t)_+ on the entire domain. This scalar
support needs whole-cover norm normalization before diagram classification.
It alone is not a center-face bound or a universal radius exclusion.

## Algebraically equivalent tighter enclosure

For an interval box centered at m, concavity gives
F(t)<=F(m)+F'(m)*(t-m). Instead of evaluating the two affine slope terms
separately, combine them before interval arithmetic:

    delta(t)-c*(T-t)
      >= F(mu)+F'(mu)*(m-mu)-F(m)-c*(T-m)
         +[F'(mu)-F'(m)+c]*(t-m)-P_upper(box).

This is the same tangent inequality as the earlier checker, with no new
assumption. Near an affine-hinge contact the bracketed coefficient is
small. Evaluating the two terms separately needlessly loses the cancellation
of their slopes. The new helper uses outward integer intervals and the same
certified z-tangent upper support of the concave local penalty. Its floating
calculations only propose tangent locations; all acceptance is exact.

The same-radius complete scalar replay uses1000 global-envelope boxes and
1000 hinge boxes. The hinge's minimum accepted lower margin is

    261188165752116677/10^24 > 0.

Executable: verify_tight_hinge_B33_0p11323.py. The new helper is
verify_exact_lens_hinge_deficit_tight.py. All earlier completed checkpoint
files are unchanged. Applying this stronger scalar support to joint
apex/ear ownership or to a future center-face dual requires that application's
own exact bookkeeping and arithmetic acceptance; it must not be added as
an extra loss to an already exhausted boundary deficit.

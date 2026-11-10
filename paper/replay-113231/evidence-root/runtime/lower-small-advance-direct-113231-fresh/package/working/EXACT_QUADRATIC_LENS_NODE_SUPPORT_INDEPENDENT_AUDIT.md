# Independent audit of the optional exact quadratic reflected-lens support

2026-10-04 UTC. **PASS, scoped to the local lemma and the conditional B33
boundary functional at R=11321/100000.** No reviewed source was changed.
The published universal bound .1132 is unaffected; this receipt authorizes
no newer universal covering claim, metric graph absorption claim, arc
bootstrap, or full face/count composition.

## Local continuous proof checked

For 0<R<1, s=R*u, c=sqrt(1-s²), h=R*sqrt(1-u²), rho=c-h and
N=sqrt(1-R²), the reflected endpoint lens is

    (Delta-h)²+(|y|+s)² <= R²,
    (rho+Delta)²+y² <= N².

Its first inequality implies Delta>=0 and
|delta|²<=2h*Delta-2s*|y|. At fixed Delta the objective
A*|delta|²+w*Delta+b*|y| increases with |y| when A,b>=0.
The endpoint-circle bound increases up to Delta=h, while the norm-ball
bound decreases; they intersect before h. On the subsequent norm-ball
boundary, |delta|²=2rho*(h-Delta), and all three terms of the objective
decrease when A,b>=0 and w<=0. Thus no later ball segment improves the
initial endpoint arc. The zero displacement is feasible throughout.

Writing alpha=asin(u), the initial arc is

    Delta=R*(cos(alpha)-cos(alpha+2z)),
    |y|=R*(sin(alpha+2z)-sin(alpha)),
    0<=2z<=acos(R)+asin(s)-alpha<=pi/2.

The score is R²*[p*(1-cos(2z))+v*sin(2z)], with
p=2A+(w*h-b*s)/R² and v=(w*s+b*h)/R². Its only possible strict interior
maximum has p<0,v>0, and it belongs to the arc exactly when the terminal
derivative p*sin(2Z)+v*cos(2Z) is nonpositive. Its value is
R²*(p+sqrt(p²+v²)). In every other sign case the maximum is zero or the
terminal score. Equality at the horizon is already represented by the
terminal score. The algebraic horizon identities in the source agree
with the independently derived absolute endpoint angle
psi=acos(R)+asin(s), whose cosine/sine are R*c-N*s and N*c+R*s.

The implementation always includes zero and the endpoint. A possibly
feasible peak enters only the upper until all strict signs and horizon
membership are certified. A peak cannot be incorrectly excluded when
its strict interior feasibility holds: its interval p lower is negative,
v upper is positive, and terminal derivative lower is negative. A peak
exactly at the horizon may be omitted because its value equals the
included endpoint. Lower endpoints therefore remain feasible lower
bounds of the true maximum. Clipping the horizon sine/cosine to [0,1]
uses identities valid on the whole stated domain.

At h=0, the endpoint lens forces Delta=y=0. This is naturally retained
by the value enclosure; the pair method avoids its singular derivative
and uses its natural bound. Broad input boxes may need subdivision to
prove rho>0, as enforced by the kernel's assertion. That is an enclosure
availability limitation, not an invalid accepted inequality.

## Backend target, coefficients, and derivatives checked

The inherited neighbor guard proves eta(a0)>asin(R), with eta increasing.
Consequently both neighbor products rho(a)*cos(a+t) and
rho(a)*sin(a+t) increase over the allowed neighbor range. Their endpoint
minimum/spread give exactly the implemented upper coefficients w and b.
Their analytic signs apply to these coefficient functions themselves:

    rho(a0)*cos(a0+t)>=cos(t)-R,
    w<=4lambda*(R-h)-s<=0 when 0<=lambda<=1/4.

The last inequality follows from R-h=s²/(R+h) and s<=R+h. The b formula
is nonnegative because N²-rho0*c0=h0*rho0>=0 and
R*N-rho0*s0>=0. Therefore clipping outward w.u to zero and b.l to zero
does not change the exact coefficient functional used for differentiation.

The old correction bounds this **same** local maximum: first use
|delta|²<=2h*Delta-2s*|y|, then Delta<=N-rho and |y|<=R-s. Its coefficients
are exactly w+2lambda*K*h and b-2lambda*K*s. Positive parts and the two
coordinate caps produce the inherited old upper. The new value enclosure
can therefore use min(new.u,old.u), retaining the new feasible lower.
Its derivative remains that of the exact new maximum, rather than that
of a minimum of two relaxation functions. The mean-value bound starts
from an upper of this exact functional, so the tightening is consistent.

All h',rho',w',b',p',v' and horizon derivatives were independently
differentiated. The endpoint and peak formulas are correct. A sole peak
derivative is selected only after its activity is proved; otherwise the
hull contains zero, endpoint, and every possibly feasible peak derivative.
If sqrt(p²+v²) may vanish, the bound by sqrt(p'²+v'²) is the valid norm
Lipschitz derivative enclosure. At a horizon transition the two values
and derivatives agree, because the angular derivative vanishes there.
Zero/value crossings retain both branches. These hulls therefore cover
the relevant piecewise/Danskin derivatives and support the inherited
mean-value enclosure, including kinks.

For the cycle energy, the safe general factor is max(2,4cos²(eta0)).
The current code explicitly requires K>=2 and separately proves
eta0<pi/4. Thus the instance's K=3.18937 is valid; no K<2 stronger-cutoff
substitution is accepted. A stronger-cutoff factor-two extension is a
future implementation obligation, not a premise of this instance.

## Covering and pair scope

Every center must be reflected to norm<=N **before** recomputing the
diagram, assigned arc endpoints, midpoint order, and cyclic expansion.
The exact identity for c'=N²*c/|c|², k=N²/|c|² is

    |x-c'|²-R²=k*(|x-c|²-R²)+(1-k)*(|x|²-1).

It preserves coverage and strict coverage inside the target unit disk.
The separately documented strict-cover/generic limiting argument is
needed if generic topology is assumed. Original pre-reflection topology
cannot be retained. Consecutive consistently ordered assigned arcs and
the single allocation of the outer displacement loss remain premises.

The numerical instance has B=33, lambda=7/50, gamma=0, x>=1/2 and
K=318937/100000. Its exact guards pass, including independent cone
factor, eta<pi/4, neighbor monotonicity, normal monotonicity, and actual
arc-domain comparison sin(.1133/2)>R/2. The last is only a comparison:
an independent full-arc lower bound .1133 is still required. This audit
does not prove that bootstrap. In particular the unrelated recovered
metric certificates requiring x>.6 keep that stronger obligation.

Fresh `python -B -S verify_quadratic_lens_radial_B33_0p11321.py` replay
passes 1,153 visited boxes, 514 accepted boxes and 63 symmetry skips.
Every accepted upper is below the rational target; the largest is
177777287131632869857/25000000000000000000000. The conditional summed
boundary-functional upper 33*intercept+2*pi*slope is at most
22342969807217685203019/62500000000000000000000, below .35748752 by
192782314796981/62500000000000000000000. The genuine same-radius arc,
face, graph, and count premises remain external.

## Fresh independent regressions and rejections

`python -B -S exact_quadratic_lens_node_support.py` passes its 120 checks.
`python -B -S audit_quadratic_lens_node_support_20261004.py` passes:

- Seven exact rational zero/endpoint/peak/horizon regressions, each with
  an exactly matching zero-width source enclosure
- Two exact h=0 zero maxima
- An uncertain-root box whose peak enters only the upper
- 1,008 point inputs checked by a separate Fraction/isqrt(10^-60)
  coordinate-arc formulation, across R=.1,.11321,.3,.9
- 500 independently differentiated coordinate/radical point inputs for
  the B33 instance, with 91 endpoint and 409 zero active branches
- A derivative box crossing the zero kink and an h=0 pair natural fallback
- Eight invalid local-input rejections and three invalid node guards
  (insufficient actual arc, lambda>1/4, and K<2)
- Rejection of optimized `-O` entrypoint execution for both verifiers

The separate high-precision regressions use an exact rational 10^-50
cancellation allowance, far below the implementation's 10^-24 scale;
they supplement, rather than replace, the continuous proof above. The
seven rational regressions and two h=0 regressions use no such allowance.
No float determines an accepted proof inequality.

## Final SHA-256 bindings

Primary audited sources:

- exact_quadratic_lens_node_support.py: 45940e9ae6ac030a9b69a5322db864db0073310f384674e71c765d8b3ee605e8
- EXACT_QUADRATIC_LENS_NODE_SUPPORT.md: 6126386718cbaf5cbe7a2ca0bcc16886d2b43da402eed771cb008359a6883f72
- quadratic_lens_radial_stability_backend.py: 0a762d49daf83e318c936abb3d6c26abe1d5971df9ff9c53289ae1cab9a7d8e9
- verify_quadratic_lens_radial_B33_0p11321.py: b17ba3f1f003e86ad892e7509804725d8e54a5874ecab73b14506f29b1b5fdc7
- QUADRATIC_LENS_RADIAL_BACKEND.md: 1d35bc48aac95a13dadf17d9ce9f42bdc821a58db782dfc9c4b5abf4b26979b6
- audit_quadratic_lens_node_support_20261004.py: 86e76194f4f395b118eb6aadb01dbbc265fae6e961f4d2e7374c2186d3e87660

Arithmetic and inherited backend dependencies inspected:

- general_tangential_reflected_backend.py: 419554793999897a2aeaeed9d8dcf1b699cad3c5602987addb0ab33caf9ac98f
- reflected_radial_stability_backend.py: 97d8548129dbcb0a5d347e6ed013af4f33d4add0b840d82b5e55a73f8b4085aa
- radial_weak_monotonicity_backend.py: f31a65463d84efc22adbd00d973eefaedd0e3ad71a903d41bf9b5521a9410d96
- radial_corrected_stability_backend.py: a861443f1d6e279f8796148e80593df3909ff402662355db400ad30b1b42ee40
- radial_stability_backend.py: a26e1b89116ea926dbbe0c5c5164b0c50803b625166178f461c038dcec2bdee3
- verify_star_lp_duals.py: 23568fed518e451d3d6b7f11603e080546bb74afa020ef0fd8fbb1a3b02be6d7
- verify_potential_star_duals.py: d4609b4441dae93c105966dd28f72b2e9d84342f012dd519dca25f2515e3e2c3
- verify_radial_boundary_support_0p11309.py: 45049507987fb9a40b996ea8ef9c4f51bf21eb260788f41b5ecc885f44b5abb7

Geometric premises inspected:

- LENS_CONE_RADIAL_NODE_GUARD.md: ccf52ab13967175e9bb70d6b9d934eaa8817456a108f29564bf3f0dedbc433a1
- RADIAL_WEAK_MONOTONICITY_GUARD.md: ab483b3ae47d08eeeae7c2984dd17017112007e7a18edd5124a1a5e26d7832ca
- RADIAL_TANGENTIAL_REMAINDER.md: 3dee0ea14e53de8878fd41bec52047ad2b11d17b9f6a953faba01b7faab9d0dc
- REFLECTED_CENTER_RADIAL_CORRECTION.md: b2bbd52c4780e6b5681e5bd08f76208853cc8b624ae726e3a5cfb2e2e65f1fa5

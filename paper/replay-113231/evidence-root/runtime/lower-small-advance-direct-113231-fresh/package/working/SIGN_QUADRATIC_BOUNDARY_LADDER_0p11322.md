# Exact normalized boundary ladder at R = .11322

This is a reusable necessary-condition component, not a covering-radius
exclusion or an exact optimum. The complete high-M domain/profile entry is
`verify_B33_highM_profile_arc_0p11322.py`. Its independent angular starting
domain and center-face certificates are separate from the five boundary
instances documented here.

Set R=5661/50000, B=33. Normalize the entire hypothetical cover before
constructing its clipped Voronoi diagram. If a center c has norm d>C,
replace it by c'=C^2*c/d^2 and put k=C^2/d^2. The exact identity

    |x-c'|^2-R^2=k*(|x-c|^2-R^2)+(1-k)*(|x|^2-1)

preserves all old covered points in the target disk, including strict
coverage. Repeating this restricts all center norms to C=sqrt(1-R^2).
Generic enlarged covers and fixed-topology limits justify the same closed
inequalities at the claimed radius. See the reflected-lens proof for the
subsequent intersection of the endpoint disks with this norm ball.

## Boundary functional and exact pair support

Let a_i be the assigned half-arcs, with sum a_i=pi. Write

    s_i=sin a_i, h_i=sqrt(R^2-s_i^2),
    rho_i=cos a_i-h_i, p_i=rho_i*u_i,
    center_i=p_i+delta_i.

The actual signed outer contribution is

    Hactual_i=a_i-s_i*(u_i dot center_i).

The sign-aware cycle-energy theorem gives

    sum |delta_i-delta_next|^2 <= K sum |delta_i|^2.

The saved strong-cutoff theorem and its exact guards are sufficient for
every instance here. No cutoff-free extension is needed. After expanding
the squared marked bases around p_i, each remaining node has the objective

    lambda*K*|delta_i|^2 + w_i*Delta_i + b_i*|t_i|,

where Delta_i and t_i are its radial and tangential displacements. The
actual w_i is nonpositive for lambda<=1/4. The exact reflected-lens support
is proved in `EXACT_QUADRATIC_LENS_NODE_SUPPORT.md`; its value and derivative
semantics are specified in `QUADRATIC_LENS_RADIAL_BACKEND.md`.

Each exhaustive pair verifier establishes, on its stated full domain,

    .5*(Hradial(a)+Hradial(b)+P(a)+P(b))
      +lambda*|p(a)-p(b)|^2
      +.5*gamma*((a-pi/B)^2+(b-pi/B)^2)
      <= L+mu*(a+b).

Consequently the cyclic sum gives the single inequality

    sum Hactual_i + lambda*sum |center_i-center_next|^2
      <= B*L+2*pi*mu-gamma*V,
    V=sum (a_i-pi/B)^2.

The factor two in 2*pi*mu is essential. The boundary functional contains
neither the signed anchors nor the slack between their J-majorants and
their actual values.

## Exact instances

Every row uses denominator 10^12 for mu and L. These integers include a
strict intercept safety allowance; floating optimization never accepts a
box or a certificate.

| Module suffix | Required full arc | x lower | lambda | gamma | K | mu numerator | L numerator | Pair boxes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| initial | .0597 | .2636 | .04 | 3/2 | 3719/1000 | -18314153960 | 11168857530 | 1255 |
| stage2 | .0825 | .3642 | .08 | 23/20 | 3464437/10^6 | -3158664550 | 9544332986 | 1255 |
| stage3 | .1065 | .470 | .11 | 27/20 | 3110078/10^6 | 8207952507 | 8325939577 | 1433 |
| final | .134 | .591 | .14 | 33/20 | 2597478/10^6 | 19574569565 | 7107546168 | 1637 |
| profile_final | .147 | .6485 | .14 | 37/20 | 462873/200000 | 19574569565 | 7107546168 | 1769 |

The full filenames are `verify_sign_quadratic_B33_SUFFIX_0p11322.py`.
The first four raw fresh results are in
`sign_quadratic_B33_four_stages_0p11322_replay.json`; the fifth is in
`sign_quadratic_B33_profile_final_0p11322_result.json`.

The angular/domain entries establish successively the stronger actual
full-arc bounds .0825, .1072 and .134. In particular .1072 discharges the
weaker .1065 requirement of the third boundary instance. Their center-face
rows reserve the entire applicable gamma*V, making no fan deduction.

The fourth pair has

    Qupper=89384917857293177360127/250000000000000000000000
          <17877/50000=.35754.

This discharges the conditional Q target of
`verify_B33_q2q3_profile_0p11322.py`. The retained profile is e=0, M=26,
66 degree-six interior vertices and one degree-seven interior vertex with
marked incidence two or three. The same center upper and the entire
fourth variance budget give, by zero-sum Cauchy,

    V >= (33/32)*(pi/33-a_i)^2

if a_i lies below its mean. The exact comparison excludes a_i<=.147/2,
with margin 692378883496257457/(5*10^23). Thus every full arc exceeds .147,
and sin(.147/2)/R>.6485. No metric catalog or local anchor fee is used to
establish this stronger actual domain.

The fifth pair is then independently valid on that domain, with the same
Qupper and gamma=37/20. It retains one fresh final variance budget. The
earlier inequalities were used to establish actual domains and are not
added to this fifth inequality. In particular no earlier variance budget
may be counted a second time in a later fan or metric application.

All five wrappers reject disabled assertions, require both node and pair
PASS, and use outward integer intervals, certified radicals/trigonometry
and exhaustive binary box subdivision. A timeout returns PENDING rather
than PASS. Remaining local profile exclusions and the other boundary-count
branches must be supplied independently before any universal threshold is
claimed.

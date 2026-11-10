# Integrating the exact quadratic reflected-lens node support

The new backend quadratic_lens_radial_stability_backend.py leaves all old
checkpoint sources unchanged. It uses the same cyclic radial-tip expansion,
same separately certified displacement-cone energy factor K, and same
reflection-before-diagram preprocessing. Only the local node maximum changes.

For a central half-arc a and all neighboring half-arcs at least a0, let

    s=sin a,c=cos a,h=sqrt(R^2-s^2),rho=c-h,
    s0=R*x0,c0=sqrt(1-s0^2),rho0=c0-R*sqrt(1-x0^2),
    N=sqrt(1-R^2).

The inherited endpoint monotonicity guards give upper coefficients

    w=4lambda[(1-rho0*c0)c+rho0*s0*s-h]-s,
    b=2lambda[s(N^2-rho0*c0)+c(R*N-rho0*s0)]>=0.

The actual residual node is bounded by

    lambda*K*|displacement|^2+w*Delta+b*|tangential displacement|.

The cutoff-free identity in EXACT_QUADRATIC_LENS_NODE_SUPPORT.md ensures
w<=0 for lambda<=1/4. The inherited guard still checks the positive-arc
endpoint monotonicity needed by these sharper w,b coefficients. Clipping
an outward interval's w upper to0 and b lower to0 is justified by those
analytic signs, not by a sampled numerical observation.

## Value enclosures

The local radical helper computes the exact maximum of this coefficient
objective over the reflected endpoint lens. Endpoint scores are always
feasible. A stationary radical is included in a lower only when its sign
and horizon membership are certified. Undecided membership may enlarge the
upper alone. The horizon sine/cosine use the exact algebraic identities and
can safely be clipped to[0,1].

The previous soft residual is another upper bound on this same local maximum:
the endpoint lens gives

    |displacement|^2<=2h*Delta-2s*|tangential displacement|,

followed by Delta<=N-rho and |tangential displacement|<=R-s. Consequently
the new natural-value upper can take the smaller of the new and old outward
upper endpoints. It retains the new true-max lower, not the old soft lower.
The derivative target remains the exact new local maximum, so this natural
upper tightening does not create an inconsistent minimum-function gradient.

## Derivative enclosures

For h>0, use h'=-s*c/h and rho'=s*rho/h. Differentiate w,b and the exact
coefficients p,q and horizon cosine M,sine V. The endpoint derivative is

    R^2[p'(1-M)-p*M'+q'*V+q*V'].

The interior radical derivative is

    R^2[p'+(p*p'+q*q')/sqrt(p^2+q^2)].

If a box includes zero norm, its second term is enclosed instead by
plus/minus sqrt(p'^2+q'^2), the norm's Lipschitz derivative bound. The code
selects a unique active branch only when all its signs/domain conditions
are proved. Otherwise it takes a hull of0 and every possible endpoint or
interior derivative. At a horizon transition the endpoint and stationary
values agree; their derivatives also agree because the z derivative is0.
Thus these are legitimate piecewise/Lipschitz mean-value bounds. Boxes with
h=0 use the inherited natural bound and never divide by h.

## Conditional replay instance

verify_quadratic_lens_radial_B33_0p11321.py certifies R=.11321,B33,
lambda=.14,gamma=0,x>=.5,K=3.18937 with1153 exact pair boxes. It uses the same
tight affine constants as the separately recovered final radial support,
so its Q upper meets the conditional q3-profile requirement .35748752.
It requires an independent full-arc bound .1133 and reflection normalization.

This can replace the weaker-domain boundary-functional step, but it does
not remove a different certificate's stronger actual-arc assumption. In
particular, the current402 metric graph certificates still require x>.6
for their marked-weight absorption. Their third arc bootstrap remains an
independent obligation. No global radius claim is made here.

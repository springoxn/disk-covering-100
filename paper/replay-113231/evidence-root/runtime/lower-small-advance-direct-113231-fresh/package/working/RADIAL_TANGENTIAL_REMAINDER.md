# A reflected radial correction without the zero-tangent guard

The previous reflected support absorbed every tangential coefficient.
At a smaller positive arc cutoff that guard may fail. The following
extension retains the unabsorbed term explicitly. Earlier frozen
certificates are unchanged.

Use0<R<1/2, lambda>=0, positive normalized sine cutoff x0, and the audited
cone factor K>=2. Retain the weaker radial-neighbor guard x0*rho0>R.
Put C=sqrt(1-R^2), s=sin(a), c=cos(a), h=sqrt(R^2-s^2). The tangential
neighbor product rho(b)*sin(a+b) increases with b, so its endpoint spread
is

    D_T(a)=s*(C^2-rho0*c0)+c*(R*C-rho0*s0).

The exact cyclic expansion and cone substitution have residual node

    w_r*Delta+w_t*t-2K*lambda*s*|t|.

Radial-neighbor monotonicity gives w_r<=F_K(a), while the endpoint spread
gives |w_t|<=2lambda*D_T(a). Consequently the residual is at most

    F_K(a)*Delta+k(a)*|t|,
    k(a)=2lambda*max(D_T(a)-K*s,0).

No claim that k is zero is made. Reflection supplies0<=Delta<=D=C-rho.
The original endpoint lens inequality implies

    (Delta-h)^2+(s+|t|)^2<=R^2,
    |t|<=R-s.

Therefore a safe node correction is

    P(a)=D*max(F_K(a),0)+k(a)*(R-s).

This is one bound on the already combined displacement functional.
The two coordinate caps hold simultaneously; their separate maximization
only enlarges the support. The correction enters each paired arc score
with coefficient one half, so every node is counted once around the cycle.

## Exact derivative

Write A_T=C^2-rho0*c0, B_T=R*C-rho0*s0. The untruncated tangential
coefficient and its derivative are

    k_raw=2lambda*[s*(A_T-K)+c*B_T],
    k_raw'=2lambda*[c*(A_T-K)-s*B_T].

The new correction derivative adds k'*(R-s)-k*c to the previous reflected
normal derivative. A positive-part crossing uses the hull of the zero
and positive derivative branches. Endpoint h=0 boxes retain the natural
value bound, as in the earlier exact pair backend. No smooth derivative
is assumed across either positive-part kink.

general_tangential_reflected_backend.py implements this support. The
actual arc bootstrap, reflection normalization, full pair replay and
complete face/count proof remain explicit dependencies at each radius.

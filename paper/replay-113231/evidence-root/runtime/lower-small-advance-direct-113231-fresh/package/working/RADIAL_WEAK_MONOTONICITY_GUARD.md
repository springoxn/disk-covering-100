# A weaker radical guard for small-arc radial neighbor products

This extends the audited lens-cone soft-correction theorem. Earlier frozen
instances and their stronger sufficient guards are unchanged.

Let0<R<1/2, a in[a0,A], A=asin R, a0=asin(R*x0), and

    eta(a)=asin(sin(a)/R)-a,
    rho(a)=cos(a)-sqrt(R^2-sin(a)^2).

Then eta increases. Its endpoint sine is

    sin eta(a0)=x0*rho0.

The sufficient guard x0*rho0>R therefore implies eta(a0)>A. For every
neighbor middle half-arc b<=A, the exact identity

    rho(a)*cos(a+b)=cos b-R*cos(eta(a)-b)

is strictly increasing in a:0<eta(a)-b<pi/2, so its derivative is
R*sin(eta(a)-b)*eta'(a)>0. The endpoint h=0 is included by continuity.
This replaces the stronger condition x0^2>4R^2(1-R^2).

Similarly

    rho(a)*sin(a+b)=sin b+R*sin(eta(a)-b)

increases, because the cosine of the displayed argument is positive.
The difference of its two endpoint values, divided by sin b, is

    C^2-rho0*c0+(R*C-rho0*s0)*cot b,
    C=sqrt(1-R^2).

It decreases when R*C-rho0*s0>=0. The same tangent-spread endpoint guard
as the audited cone theorem consequently makes the residual tangential
coefficient nonpositive. The normal residual and correction P(a) remain
exactly those in RADIAL_NODE_SOFT_CORRECTION.md; radial-normal negativity
is not required.

The subclass radial_weak_monotonicity_backend.py checks this weaker guard,
the cone factor, the tangent spread, actual arc cutoff and the other
radical signs. Its pair arithmetic is inherited unchanged from the
audited soft-correction backend. An exact same-radius pair and complete
score/count proof remain necessary before any radius claim.

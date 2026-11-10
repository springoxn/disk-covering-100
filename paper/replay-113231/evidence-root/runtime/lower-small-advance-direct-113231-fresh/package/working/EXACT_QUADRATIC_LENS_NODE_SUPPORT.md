# Exact quadratic support in the reflected endpoint lens

Let0<R<1, N=sqrt(1-R^2), t in[0,asin R], and define

    s=sin t, c=cos t, h=sqrt(R^2-s^2), rho=c-h,
    u=s/R, alpha=asin u.

Normalize the whole covering BEFORE constructing its diagram, so each center
has norm at most N. A displacement(Delta,y) from the inward radial endpoint-
lens tip is feasible exactly when

    (Delta-h)^2+(|y|+s)^2<=R^2,
    (rho+Delta)^2+y^2<=N^2.

In particular Delta>=0. For every A>=0,w<=0,b>=0, the exact local maximum of

    A*(Delta^2+y^2)+w*Delta+b*|y|

has the radical formula below. This file establishes a local lemma only;
its numerical backend and global covering applications remain separate.

## 1. Reduction to one circular arc

At fixed Delta the objective increases with |y|. Its largest feasible |y|
is the smaller of the endpoint-circle and normalized-ball bounds

    -s+sqrt(R^2-(Delta-h)^2),
    sqrt(N^2-(rho+Delta)^2).

The former increases until Delta=h, and the latter decreases. They meet
once before h. After their intersection the ball is limiting, and on it

    Delta^2+y^2=2rho*(h-Delta).

Thus the squared displacement, |y| and w*Delta all decrease there; it cannot
improve the objective. The maximum lies on the initial endpoint-circle arc,
or is the zero displacement. Parameterize that arc by

    Delta=R[cos alpha-cos(alpha+2z)],
    |y|=R[sin(alpha+2z)-sin alpha],
    0<=z<=Z=[acos R+t-alpha]/2.

Its far endpoint has center norm N; 0<=Z<=pi/4 and alpha+2Z<=pi/2. These
identities also follow by inserting the parametrization in the norm equation.
The limiting cases s=0 and h=0 are included continuously.

## 2. Exact radical maximum

Define

    p=2A+(w*h-b*s)/R^2,
    q=(w*s+b*h)/R^2.

The objective on the arc is

    R^2*[p*(1-cos(2z))+q*sin(2z)].

Its derivative is2R^2*[p*sin(2z)+q*cos(2z)]. On0<=2z<=pi/2 there is an
interior maximum only if p<0 and q>0. It is unique and has value

    R^2*[p+sqrt(p^2+q^2)].

It belongs to the allowed interval exactly when the derivative at Z is
nonpositive. Equality means it is the far endpoint. All other cases have
their maximum at0 or Z: p>0,q<0 gives a minimum, and the same-sign cases
are monotone. Zero-coefficient cases follow by continuity.

Therefore take the maximum of0, the far endpoint score and the radical
stationary score ONLY when those sign/horizon conditions hold. If interval
arithmetic cannot decide horizon membership, overincluding that stationary
value is safe for an upper, but it must not become a purported feasible lower.

## 3. Algebraic horizon

Set eta=alpha-t. Then

    sin eta=s*rho/R, cos eta=(c*h+s^2)/R,
    cos(2Z)=c*h+s^2+N*s*rho/R,
    sin(2Z)=N*(c*h+s^2)/R-s*rho.

These sine/cosine quantities lie in[0,1]. Thus the endpoint value and its
derivative-domain test require only radicals in the original half-arc sine,
not a numerical angle or transcendental stationary-root proposal.

## 4. Cutoff-free squared-edge coefficient guard

After the existing cyclic radial-tip expansion and a separately certified
cycle-energy factor K, the node objective has the preceding form with
A=lambda*K. The linear radial coefficient includes the negative outer
contribution -sin t. The identity

    rho(a)*cos(a+t)=cos t-R*cos(eta(a)-t)>=cos t-R

implies, for all neighbors and without a positive minimum arc,

    w<=4lambda*(R-h)-s
      =s*[4lambda*s/(R+h)-1]<=0, if0<=lambda<=1/4.

The full-domain tangential spread is at most

    R[(1-R)*sin t+sqrt(1-R^2)*cos t],

so b may be bounded by twice lambda times that expression. A separately
proved positive arc cutoff permits the sharper existing neighbor-endpoint
bounds. The local exact cap does not require such a cutoff.

## 5. Strong-cutoff cone factor

If eta_i>=eta0, adjacent displacement directions differ by at most
pi-eta_i-eta_next. For eta0<=pi/4 the norm-product argument gives the safe
energy factor4*cos(eta0)^2. For eta0>=pi/4 adjacent dot products are
nonnegative, giving factor2. The combined valid factor is

    K=max(2,4*cos(eta0)^2).

The unmodified formula below2 would be unjustified: an isolated nonzero
displacement already has cycle-energy ratio2.

## Implementation obligations

A new backend can replace the old looser reflected residual with this
local cap. It must enclose derivatives across sign/horizon/max transitions,
retain natural bounds at h=0 and use the covering-normalization and cycle
premises explicitly. An uncertain root can be overincluded only for an
upper. Existing completed sources need not be edited. No numerical PASS or
new covering threshold is claimed by this analytic file.

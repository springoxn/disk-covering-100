# Exact normalized endpoint-lens support

This recovered proof concerns a cover normalized before its diagram is
classified, so all centers have norm at most C=sqrt(1-R^2). It does not
claim that reflecting centers preserves a previously fixed graph.

## Normalization and exact local support

For a center d*u with d>=C, replace it by (C^2/d)*u. The identity

    |x-(C^2/d)u|^2-R^2
      =(C^2/d^2)(|x-du|^2-R^2)+(1-C^2/d^2)(|x|^2-1)

shows that its old covered portion of the unit disk is preserved.

For a boundary half-arc t, set s=sin t,c=cos t,h=sqrt(R^2-s^2),rho=c-h,
u=s/R,a=asin u. A displacement (Delta,b) from its inner radial lens tip
rho has exact constraints, after reflecting b to be nonnegative,

    (Delta-h)^2+(b+s)^2<=R^2,
    (rho+Delta)^2+b^2<=1-R^2.

For every k>=0, the maximum of R*k*sqrt(Delta^2+b^2)-s*Delta is

    P(t)=max_{0<=z<=Z(t)} 2R^2 sin z [k-u sin(z+a)],
    Z(t)=[acos R+t-a]/2.

For fixed Delta the objective increases with b. The lens-boundary branch
is active up to its unique intersection with the normalized circle.
Beyond that intersection the circle imposes
d^2=C^2-rho^2-2rho*Delta, so both d and the objective decrease with Delta.
The maximum is therefore on the initial lens-circle branch. Parametrize it
by theta=a+2z:

    Delta=R(cos a-cos theta)=2R sin(z+a)sin z,
    b=R(sin theta-sin a)=2R cos(z+a)sin z,
    d=2R sin z.

The norm-circle intersection is theta=acos R+t. Along the initial arc the
actual center norm squared has derivative2R sin(theta-t)>=0. This proves
the stated feasible interval. Since theta<=pi/2, the objective g has

    g'/(2R^2)=k cos z-u sin(2z+a),
    g''/(2R^2)=-k sin z-2u cos(2z+a)<=0.

Thus it is concave, and every tangent is an upper support. Its derivative
at zero is k-u^2, so P=0 for u^2>=k. The zero displacement is always a
candidate. At h=0 the lens collapses and Z=0. At t=0 the formula gives
P(0)=k R^2 sqrt(2(1-R)); neither endpoint requires division by h or s.

## From local support to a whole-boundary half-side bound

Write H(t)=s*h+t-s*c and eta(t)=asin(s/R)-t. Let mu=pi/B and
b0=R^2*k*cos(eta(mu)), F=H+b0*eta. The reference edge between adjacent
radial lens tips has length2R*sin((eta_i+eta_(i+1))/2). Triangle inequality
and the sine tangent at eta(mu) show that actual outer area plus
(R*k/2)*sum(marked base lengths) is bounded by

    B*R^2*k*sin(eta(mu))-B*b0*eta(mu)+sum_i[F(t_i)+P(t_i)].

Here each displacement appears on its two incident edges with total
coefficient R*k and is combined with its actual outer loss s*Delta exactly
once. Hence a verified scalar inequality

    F(t)+P(t)<=F(mu)+F'(mu)(t-mu)-v*(t-mu)^2

implies the useful global upper bound

    B*[H(mu)+R^2*k*sin(eta(mu))]-v*sum_i(t_i-mu)^2.

This replaces the previous displacement estimate; it is not an extra loss
to add to a radial length bound that already spent the same outer loss.

## Exact scalar certification

The identities

    eta''=s*(1-R^2)/h^3,
    (H+R^2*eta)''=-2s(c-h)^2/h

make F concave for b0<R^2. On u^2>=k its negative half-second derivative
is at least sqrt(k)*(1-R^2)*(1-b0/R^2)/(2*(1-k)^(3/2)). Since P=0 there,
this certifies the requested variance coefficient on the good interval.

On the bad interval the checker covers t by1000 closed rational boxes.
For each box it verifies a z tangent over the entire allowed z interval,
and a midpoint tangent for F. Floating calculations only suggest the z
tangent location; all domains, values, derivatives and final comparisons
are verified with outward rational intervals. The pre-reset B35 .11322,
k=.44,v=.03 checker was recovered byte-identically with SHA
3c6e6a762c5681a70d06606c27e755743e5c851fe92055495207924e7a6737b1
and freshly reproduced its exact output after recovery. Specializations
must set R,B,k,v explicitly and rerun the scalar comparisons.

The geometry and original k=.44 replay were independently checked before
the reset. This recovered proof has newly explicit global accounting and
must be bound by a fresh receipt when assembled into a new checkpoint.

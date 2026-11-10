# A stronger marked-ear support from Jensen and the radial slab

For 0<r<=1400/11449 and 0<=k<=1, let an actual all-boundary q2 ear have area Delta, two marked edge lengths 2r*sqrt(z1), 2r*sqrt(z2), and their usual anchor caps. Put

`w=(1-sqrt(1-2r))/r=2/(1+sqrt(1-2r))`.

Then its complete normalized area and anchor score, including the linear halfside penalties, is bounded by

`Delta/r^2+sqrt(z1(1-z1))+sqrt(z2(1-z2))-k*(sqrt(z1)+sqrt(z2))`

`<= w+sqrt(2w-w^2)-k*sqrt(2w)`.

This applies only to an actual all-boundary ear, whose center triangle has the radial-slab bound. It is not a score bound for an arbitrary two-marked triangle, nor a global covering-radius theorem.

## 1. Two compatible elementary bounds

The marked edges satisfy 0<=z_i<=1. Let t=z1+z2. Directly from the triangle area and AM-GM,

`Delta/r^2 <= 2sqrt(z1*z2) <= t`.

The independently proved boundary-annulus slab gives `Delta/r^2<=w`. These bounds hold simultaneously, so the area is at most min(t,w).

For h_k(z)=sqrt(z(1-z))-k*sqrt(z),

`h_k''(z)=[k-(1-z)^(-3/2)]/(4z^(3/2))<=0`

on the interior of [0,1]. Continuity covers both endpoints. Jensen therefore bounds the **joint** anchor-minus-length contribution by

`h_k(z1)+h_k(z2)<=sqrt(2t-t^2)-k*sqrt(2t)`.

No equality of actual marked edges is assumed. Combining gives the scalar upper bound

`F(t)=min(t,w)+sqrt(2t-t^2)-k*sqrt(2t)`, `0<=t<=2`.

## 2. The scalar maximum is at t=w

The radius domain gives 1<w<=1.07. On 0<t<=w, the branch is

`F(t)=t+sqrt(2t-t^2)-k*sqrt(2t)`.

Its second derivative is

`-(2t-t^2)^(-3/2)+k*(2t)^(-3/2)<=0`,

because 2t-t^2<=2t and k<=1. Hence F' decreases, and its minimum on this interval is at w. Uniformly for 1<=w<=1.07 and k<=1,

`F'(w)=1+(1-w)/sqrt(2w-w^2)-k/sqrt(2w)`

`>=1-7/sqrt(9951)-1/sqrt(2)>0`.

Thus F increases up to w. For w<=t<2, the area branch is constant and

`F'(t)=(1-t)/sqrt(2t-t^2)-k/sqrt(2t)<0`,

since t>=w>1. Therefore the global maximum is F(w), proving the stated cap. Degenerate endpoints follow by continuity.

The exact relation `1-2*(1400/11449)=(93/107)^2` verifies the radius/width domain. `verify_jensen_slab_ear_support.py` checks the derivative margin and encloses the support for several relevant rational radii and multipliers. The helper `cap(radius,multiplier)` returns an exact outward interval.

## 3. Use in future certificates

This replaces a deliberately loose actual-ear cap such as 1.79 only after the complete ear-aware vertex/U coefficients and final area inequalities are recomputed. The common halfside potential must be the same k as in the ordinary marked-face and boundary compensation scores. No second anchor or edge charge may be added independently.

The function is increasing with w and hence with r in the stated domain, and decreasing with k. At k=.24 in the current radius range it is about 1.71, substantially below 1.79. All previously frozen certificates remain unchanged.

## 4. Squared-edge variant

For a squared-edge multiplier 0<=lambda<=1/5, the two normalized negative penalties are `-4lambda*(z1+z2)`. Jensen for the two anchors now gives

`score <= min(t,w)+sqrt(2t-t^2)-4lambda*t`.

The left branch is concave and its derivative at w is at least

`1-7/sqrt(9951)-4/5>0`.

The right branch decreases for t>=w>1. Thus the maximum is again at w, giving

`Delta/r^2+anchor1/r^2+anchor2/r^2-lambda*(L1^2+L2^2)/r^2`

`<=w+sqrt(2w-w^2)-4lambda*w`.

This retains exactly the same two squared-edge penalties as the corresponding positive boundary compensation. It improves the bound obtained by separately maximizing the two penalized anchors. The helper `quadratic_cap(radius,penalty)` evaluates this cap exactly; its derivative-domain comparison is included in `verify()`.

# Normalized center-displacement compensation

Normalize the entire cover before constructing its diagram. Put C^2=1-R^2.
For a center d*u,d>=C, replace it by (C^2/d)u. The exact identity

    |x-(C^2/d)u|^2-R^2
    =(C^2/d^2)(|x-du|^2-R^2)+(1-C^2/d^2)(|x|^2-1)

preserves every point covered inside the unit disk. The normalized diagram
is then classified; no assertion of fixed-graph preservation is used.

For a half-arc t, let s=sin t,c=cos t,h=sqrt(R^2-s^2),rho=c-h. Write a
center as its inner radial lens tip plus delta, with d=|delta| and radial
displacement Delta. Endpoint constraints imply

    d^2<=2h*Delta,     s*d<=R*Delta.

For the second inequality, the stronger endpoint condition is
d^2-2h*Delta+2s*|delta_tangent|<=0. Hence h*Delta>=s*|delta_tangent|,
which gives Delta/d>=s/R because h^2+s^2=R^2. The collapsed h=0 lens is
handled as delta=0.

The norm constraint also gives

    d^2+2rho*Delta<=C^2-rho^2=2h*rho.

Together these imply d^2<=2h^2*rho/c. On q=s^2/R^2<=k<=1/2, the ratio
h/c=R*sqrt(1-q)/sqrt(1-R^2*q) decreases with q. Therefore

    d<=beta_k*h,
    beta_k=sqrt(2*(1-R*sqrt(1-k)/sqrt(1-R^2*k))).

The actual outer displacement loss is s*Delta. When q<=k,

    R*k*d-s*Delta<=R*(k-q)*d
       <=beta_k*R^2*sqrt(1-q)*(k-q).

When q>=k the left side is nonpositive. Thus the displayed positive-part
expression is a valid local compensation and spends this loss only once.

For P(t)=beta_k*R^2*sqrt(1-q)*(k-q) on the bad interval, direct
differentiation gives

    P''=beta_k*A(q)/(1-q)^(3/2),
    A(q)=-6q^2+9q-k-2
       +R^2*q*(9q^2-(14+k)q+2k+4).

The sufficient derivative guard
9-12k-2R^2*(14+k)*k>0 makes A increasing on[0,k]. Its endpoint is
2(1-k)*(3k-1+2R^2*k*(1-2k)). At the checked k=.3 and.33 this is negative,
so P is concave. Combining it with the concave function
F(t)=H(t)+R^2*k*cos(eta(pi/B))*eta(t), as defined in the exact-lens proof,
allows midpoint-tangent checks over the whole bad interval. On the good
interval P=0 and the exact curvature identity supplies the reported
quadratic deficit.

The same reference-edge sine tangent gives the global boundary bound

    B*[H(pi/B)+R^2*k*sin(eta(pi/B))]-v*sum(t_i-pi/B)^2.

The recovered scalar modules recompute every guard and endpoint comparison
and check the reflection identity as a polynomial identity. Their norm
bound is radius dependent, so a different target radius requires a fresh
same-radius specialization before its diagram is classified.

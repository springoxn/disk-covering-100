# Full-simplex localization with signed sine coefficients and explicit edge caps

Let alpha_i>=0, sum alpha_i=pi, a>0, and let t_i and lambda_i be real. Define

    F(alpha)=a/2*sum sin(2alpha_i)
             +sum t_i*sin(alpha_i)
             +sum lambda_i*(alpha_i-pi/3).

If

    range(lambda)+(1/2)*sum max(-t_i,0)<a,

then every interior global maximizer is acute. Thus a full-simplex upper support is the maximum of an acute support and all three explicitly evaluated simplex-edge supports. Positive sine coefficients have no size restriction when range(lambda)<a. This does NOT permit dropping the boundary edge supports.

## Interior localization

Divide by a, so it suffices to prove the statement for a=1. Suppose an interior maximum has alpha>=pi/2 and other angles beta,gamma. Put c=-cos(alpha)>=0, s=sin(alpha)>0, z=cos(beta-gamma)>0. Along v=(1,-1/2,-1/2), second-order necessity gives

    s*(4c-z-t_alpha)
      -(t_beta*sin(beta)+t_gamma*sin(gamma))/4 <=0.

Consequently

    z>=4c-t_alpha
             -(t_beta*sin(beta)+t_gamma*sin(gamma))/(4s).

The inward directional derivative, along -v, equals

    1-2c^2+cz+t_alpha*c
       +(t_beta*cos(beta)+t_gamma*cos(gamma))/2
       -lambda_alpha+(lambda_beta+lambda_gamma)/2.

Substitution of the second-order bound makes this at least

    1+2c^2
      +sum_(theta=beta,gamma) t_theta*
         [cos(theta)/2-c*sin(theta)/(4s)]
      -range(lambda).

Since 0<theta<=beta+gamma=pi-alpha<=pi/2,
cos(theta)>=c and sin(theta)<=s. Each bracket lies in [0,1/2]. The last expression is therefore at least

    1-range(lambda)-(1/2)*sum max(-t_i,0)>0,

contradicting the first-order condition for a maximum. The nonacute coefficient t_alpha cancels, so the displayed guard is conservative when it is the only negative coefficient. The same calculation handles alpha=pi/2. A vertex with alpha=pi belongs to the boundary cases below.

## Mandatory simplex-edge supports

On the edge alpha_k=0, write alpha_i=x, alpha_j=pi-x, 0<=x<=pi. Let

    T=t_i+t_j, d=lambda_i-lambda_j,
    mean_lambda=(lambda_1+lambda_2+lambda_3)/3.

The complete edge score is

    T*sin(x)+d*x+pi*(lambda_j-mean_lambda).

The sine terms generally do not vanish there.

If T<=0, this function is convex (linear when T=0), so its maximum is at an endpoint. If T>0, it is concave. Retain the two endpoints and, when |d|<T, the stationary point x=acos(-d/T). Its value is

    sqrt(T^2-d^2)+d*acos(-d/T)
                         +pi*(lambda_j-mean_lambda).

For d>=T the maximum is the x=pi endpoint; for d<=-T it is the x=0 endpoint. All three unordered edge pairs must be checked. Endpoint values are pi*(lambda_i-mean_lambda) and pi*(lambda_j-mean_lambda), so the degenerate-vertex cap is included automatically.

Example guarding this distinction: t=(0,0,.51), lambda=(0,.5,0). The edge alpha_1=0 has an interior stationary maximum with cosine -.5/.51, exceeding both of its endpoint scores. Vertex-only boundary acceptance is consequently insufficient without an additional domination argument.

## Acute scalar dual and physical scale endpoint

For any auxiliary real nu, an acute upper bound is

    nu*pi-pi*mean_lambda
      +sum_i sup_(0<=x<=pi/2)
          [a/2*sin(2x)+t_i*sin(x)+(lambda_i-nu)*x].

This uses the exact angle-sum identity. Scalar critical points and both endpoints must be included; no scalar concavity is required for arbitrary signed t_i. With nonnegative t_i the individual scalar functions are concave. Existing exhaustive signed-sine conjugate backends may be used with the matching sign and coefficient units.

For an actual q0 triangle of circumradius ratio rho in [0,1], the physical score is

    a*rho^2/2*sum sin(2alpha_i)
       +rho*sum t_i*sin(alpha_i)
       +sum lambda_i*(alpha_i-pi/3).

Triangle area is nonnegative on the angle simplex, so this is convex in rho. Its maximum occurs at rho=0 or1. The rho=1 case is the localized full-simplex support above; the rho=0 case is purely linear and is already covered by the included vertex caps. There is no hidden assumption that every actual triangle or its maximizer at rho=0 is acute.

A physical coefficient multiplying L/(2R) contributes t_i*sin(alpha_i), while one multiplying L/R contributes 2t_i*sin(alpha_i). The chosen units must match the shared-edge cancellation. For weighted area a, keep the guard range(lambda)+sum negative magnitudes/2<a without silently reverting to a=1.

This is a local support lemma. It does not supply incidence multiplicities, compatible reference allowances, a neighborhood replacement or a global covering-radius exclusion. Those must be verified separately by the invoking certificate.

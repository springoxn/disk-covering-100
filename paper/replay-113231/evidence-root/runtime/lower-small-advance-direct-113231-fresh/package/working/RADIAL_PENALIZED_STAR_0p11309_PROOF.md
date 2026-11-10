# A compact B33 boundary-edge and interior-angle coupling

This proof is scoped to the B33 branch at R=11309/100000. It uses the exact
same-radius geometric premises in RING_STAGE_PREMISES_0p11309.md: m100,
I67,F165, no all-three-boundary faces, p<=3, interior degrees5 through13,
unmarked angles at most pi/2+.121, and acute marked apices. Other B branches
are separate. No equal boundary gaps, symmetry of centers, or actual
triangular-lattice realization is assumed.

## 1. Positive arc domain

The separate exact one-arc Jensen checker proves every full assigned arc
theta_i>.08935, so its half-angle a_i>1787/40000. Endpoint coverage gives
a_i<=asin(R). Set s_i=sin(a_i), c_i=cos(a_i), h_i=sqrt(R^2-s_i^2), and
rho_i=c_i-h_i. The exact trigonometric comparison gives x_i=s_i/R>.3949.
The radial-boundary checker conservatively includes the closed domain
x_i in[.3949,1]. No division by a vanishing half-angle is needed.

Let u_i be the radial unit vector at the midpoint of arc i and v_i its
positively oriented perpendicular. The inward endpoint-lens corner is
p_i=rho_i*u_i. Write an arbitrary boundary center as

C_i=p_i+d_i*u_i+t_i*v_i.

The two endpoint distance inequalities imply

2h_i d_i >= d_i^2+t_i^2+2s_i|t_i|.

Thus d_i>=0, |C_i-p_i|^2<=2h_i d_i-2s_i|t_i|, and
s_i|t_i|<=h_i d_i. This includes the degenerate h_i=0 case by continuity
(the endpoint lens then consists of its single corner). The actual signed
outer-fan/arc contribution is H_R(2a_i)-s_i*d_i, with
H_R(2a_i)=a_i-s_i*rho_i.

## 2. Summing before taking lens supports

Take lambda=1/25. Let delta_i=C_i-p_i. Expanding the cyclic marked-edge sum
before optimizing any center gives

lambda sum |C_i-C_(i+1)|^2
=lambda sum |p_i-p_(i+1)|^2
 +sum 2lambda delta_i dot(2p_i-p_(i-1)-p_(i+1))
 +lambda sum |delta_i-delta_(i+1)|^2.

The last term is at most4lambda sum|delta_i|^2, hence at most
sum[8lambda h_i*d_i-8lambda s_i|t_i|]. After the outer-fan loss, the
remaining node objective is

w_(r,i)d_i+w_(t,i)t_i-8lambda s_i|t_i|,

where, in middle-arc radial coordinates, for neighboring half-arcs a,b,c,

w_r=2lambda[2rho_b-rho_a cos(a+b)-rho_c cos(b+c)]+8lambda h_b-s_b,
w_t=2lambda[rho_a sin(a+b)-rho_c sin(b+c)].

Put k=max(|w_t|-8lambda s_b,0). The node objective is at most
[w_r+(h_b/s_b)k]d_b. The exact three-variable interval checker proves
s_b*w_r+h_b*k<=0 over the entire closed sine-parameter cube. Therefore

sum outer_actual +lambda sum actual_marked_edge^2
<=sum H_R(2a_i)+lambda sum radial_marked_edge^2.

This is a simultaneous center bound. The individual node supports are
summed using the same cyclic expansion; independently favorable neighboring
tangential directions are not assumed compatible.

There is also a simple analytic guard: x_i>=.3949>1/3 gives k=0 because
|rho_a sin(a+b)-rho_c sin(b+c)|<=s_b+R<=4s_b. Further, rho>=1-R and
cos(a+b)>=1-2R^2 give
w_r<=4lambda[1+R sqrt(1-x_b^2)-(1-R)(1-2R^2)]-R*x_b.
The right side decreases in x_b, and its value at.3949 is below-.00631.
The interval cube certificate is retained as an independent explicit replay.

## 3. Exact affine pair support

For two radial corners let a,b be their half-arcs. The pair score is

f(a,b)=[H_R(2a)+H_R(2b)]/2+lambda*L0(a,b)^2.

A stable exact length formula is

L0^2=(rho_a-rho_b)^2
 +2rho_a rho_b(s_a+s_b)^2/(1+c_a c_b+s_a s_b).

It equals the usual radial-point squared distance, since the quotient of
the sine square by the denominator is1-cos(a+b). The checker exhaustively
proves

f(a,b)<=11223/1000000-(2338/125000)(a+b)

on the complete domain x_a,x_b in[.3949,1]. Its1,514,617 visited boxes,
754,227 accepted leaves and3,082 symmetric skips cover the full square.
The small rational slack above the uniform-point diagnostic makes the
certificate finite; the diagnostic is not an equality assumption.

Summing pairs and using sum a_i=pi gives the global outer/edge upper bound

Q=33*(11223/1000000)+2pi*(-2338/125000).

## 4. Cancelling the marked-edge penalty

The separately proved acute marked envelope G_lambda bounds

(marked triangle area+anchor-lambda*marked_edge^2)/R^2.

It is the concave curve sin(g)(1+2cos(g))-4lambda*sin(g)^2 through pi/3,
then its tangent with value sqrt(3)-3lambda and slope
-.5-2sqrt(3)lambda. This envelope is explicitly restricted to acute apices;
the exact same-radius premises supply that restriction. The negative
marked-edge penalties cancel exactly against the positive edge sum in Q.

Use the unmarked face potential phi with coefficient1/2, splice1.09 and
angle endpoint pi/2+.121. At each interior star (p,j), Jensen gives the
scalar score

sup_g[p G_lambda(g)+j phi((2pi-pg)/j)+eta*p*g].

The incidence constraints are sum x67,sum p*x33,sum j*x396-N and
sum_(p>0)x<=N, with N11 through94. Boundary-angle conjugacy contributes
N C(eta)-2pi*eta, where C(eta)=sup_a[phi(a)-eta*a]. Rational LP duals bound
every one of the36 types for every N. The final area upper bound is

R^2[67u0+33u1+(396-N)u2+Nv+N C(eta)-2pi*eta]+Q.

`verify_penalized_star_0p11309.py` checks all3,024 scalar inequalities and
every final N margin using directed integer interval arithmetic. Its
floating-point proposal generator does not participate in acceptance.
The actual result is saved separately. Combined with the other local
checkers and same-radius premises, this is a compact B33 exclusion route;
it does not require enumerating its possible inner-core graphs.

Endpoint genericity is handled by approaching a hypothetical radius<=R
cover with generic slightly enlarged covers, selecting a fixed finite
topology and passing all closed inequalities to a convergent subsequence.
The final strict area margin contradicts the limiting configuration.
No perturbation is claimed to preserve the covering radius exactly.

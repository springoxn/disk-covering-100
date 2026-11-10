# A sharper localized triangle support

Let a_i>=0, sum a_i=pi, delta_i=a_i-pi/3 and

`f(a)=2 product sin(a_i)=(1/2)sum sin(2a_i)`.

Let the three real corner potentials lambda_i have range at most 6/25. Then, with A=3sqrt(3)/4 and C=4219/5000=.8438,

`sup_a [f(a)+sum lambda_i*delta_i] <= A+sum (lambda_i-mean(lambda))^2/(4C)`.

The weaker uncentered bound with sum lambda_i^2 is therefore also valid. This is a support theorem over the complete angle simplex. It does **not** claim that every triangle has deficit at least .8438 times its variance.

## 1. Locate the support maximizer

The existing complete-simplex localization proof applies because the potential range L is below 1/2. Every nonacute or degenerate triple has centered score at most

`max(1+pi/12, pi/3, sqrt(3)/2+pi/8)<A`.

The equilateral triple has score A, so every maximizing triple is strictly acute and interior. Lagrange stationarity at such a maximizer gives

`cos(2a_i)+lambda_i=constant`.

Consequently range(cos(2a_i))<=L<=.24.

Let a be the largest maximizing angle and b the smallest. Some other angle is at most (pi-a)/2. Since cosine is decreasing on [0,pi],

`cos(2a)+cos(a)>=-L`.

Likewise some other angle is at least (pi-b)/2, giving

`cos(2b)+cos(b)<=L`.

The function cos(2t)+cos(t) is strictly decreasing for 0<t<pi/2. Exact endpoint comparisons at pi/3-.1 and pi/3+.1 show that every maximizing angle has

`|delta_i|<1/10`.

Since three deviations sum to zero, the convex polytope |delta_i|<=d has vertices which are permutations of (d,-d,0). Hence `V=sum delta_i^2<=2d^2=1/50`.

## 2. A local variance deficit at that maximizer

The exact identity for the centered area is

`A-f = (sqrt(3)/4)sum(1-cos(2delta_i))+(1/4)sum sin(2delta_i)`.

For |delta_i|<=.1, expand sine through degree four at zero. Its fourth coefficient vanishes, so the polynomial is t-t^3/6, while the degree-five Lagrange remainder has absolute value at most |t|^5/120. This is not the weaker degree-three expansion with a fourth-order remainder. The cosine bound follows from its degree-four expansion with the nonpositive degree-six remainder on |t|<=.2. These give

`1-cos(2delta_i)>=2delta_i^2-(2/3)delta_i^4`,

`sin(2delta_i)>=2delta_i-(4/3)delta_i^3-(4/15)|delta_i|^5`.

Write T=sum delta_i^3. The zero-sum identities imply sum delta_i^4=V^2/2 and |T|<=sqrt(V^3/6). The latter follows, for example, from the nonnegative product of squared pairwise differences, equal to V^3/2-3T^2. Also sum|delta_i|^5<=.001 V. Therefore

`A-f >= V*[sqrt(3)/2-sqrt(3)*V/12-sqrt(V/6)/3-1/15000]`.

The bracket decreases with V>=0. At V=1/50 it equals

`sqrt(3)/2-sqrt(3)/600-sqrt(1/300)/3-1/15000`,

which exceeds .8438 by more than .00002697. Thus the localized deficit `A-f>=C V` holds at every relevant support maximizer.

## 3. Complete the square

At a maximizing triple,

`f+sum lambda_i*delta_i <= A-C*sum delta_i^2+sum(lambda_i-mean(lambda))*delta_i`

`<= A+sum(lambda_i-mean(lambda))^2/(4C)`.

Every actual triple is bounded by this maximizing score, so the claimed support holds on the full simplex, including obtuse and degenerate actual triangles. For a triangle of circumradius at most R, actual normalized area is at most f, so the same inequality applies to its area score.

`verify_localized_triangle_support_08438.py` checks all non-symbolic comparisons with exact outward-rounded rational intervals. The remaining steps are the analytic identities and convex-polytope argument above. This lemma can replace the localized .75 coefficient in a future ear-aware certificate only after its scalar vertex supports and final area comparisons are rechecked; it does not retroactively change any frozen certificate.

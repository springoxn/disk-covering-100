# A quantitative boundary-arc deficit for B34

At R=.11312, B=34 and the original linear-halfside multiplier k=.24, the coupled-edge boundary proof can retain the extra negative term

`-.3*sum_i(t_i-pi/B)^2`,

where t_i are the actual assigned half-arc angles. This is a boundary-support lemma, not a complete radius exclusion. It leaves the original source ZIP unchanged.

## Inherited exact functions

Use the notation of `research/coupled_edges/PROOF.md` inside the SHA-pinned ear archive. Write s=sin(t), h=sqrt(R^2-s^2), eta(t)=asin(s/R)-t, t0=pi/B, and

`b=R^2*k*cos(eta(t0))`,

`F(t)=s*h+t-s*cos(t)+b*eta(t)`,

`P(t)=2R^2*sqrt(1-u^2)*(k-u^2)_+`, where u=sin(t)/R.

The actual outer signed area and the complete linear marked-edge compensation sum are bounded by a constant independent of the arc lengths plus sum(F(t_i)+P(t_i)). This inherited reduction sums actual center displacements before using their endpoint-lens constraints, and allows arbitrary unequal arcs.

Let tc=asin(R*sqrt(k)). The original proof establishes F concave on the entire half-arc domain and P=0 for t>=tc. On t<=tc it establishes concavity of F+P, using the displayed exact second derivative and R<1/5.

## Good arcs

The inherited second-derivative identity gives

`F''(t) <= -sin(t)*(1-R^2)*(R^2-b)/(R^2-sin(t)^2)^(3/2)`.

On t>=tc the magnitude on the right increases with sin(t). Its minimum therefore gives the strong-concavity coefficient

`c_good=sqrt(k)*(1-R^2)*(1-k*cos(eta(t0)))/(2*(1-k)^(3/2))`.

The exact checker proves c_good>.3. Hence, since t0>tc,

`F(t)<=F(t0)+F'(t0)*(t-t0)-.3*(t-t0)^2`

on the full good-arc interval, including the endpoint by continuity.

## Small arcs

Divide [0,tc] at the rational points j/200, j=1,...,11. On each of these 12 subintervals, use the midpoint tangent to the concave function F+P as an upper bound. The difference between the requested quadratic support and this affine tangent is concave. It is therefore enough to check positivity at both subinterval endpoints.

`verify_coupled_boundary_variance_0p11312.py` checks all 24 endpoint comparisons with exact outward-rounded intervals. The uniform-point and midpoint inverse sines are computed using the already audited closed-form arctangent backend. No sampling or floating-point acceptance is used.

Combining both arc regions and using sum t_i=pi=B*t0 eliminates the linear terms and proves the claimed total deficit.

## Use with several q4 fans

Suppose there are t positive q4 fans, each with four consecutive marked edges, and each five-cell footprint has full-arc span at most L. Their covered-cell union has k>=4t+1 cells unless it covers the full boundary. The union half-arc sum is at most tL/2, even when endpoint cells overlap. If tL/2<k*pi/B, Cauchy on that union and its complement gives

`sum_i(t_i-pi/B)^2 >= B*(k*pi/B-tL/2)^2/[k*(B-k)]`.

For k above tLB/(2pi), this bound increases with k, so substituting k=4t+1 is conservative. The full-cycle case is impossible when tL/2<pi. This uses one global variance budget once, and does not assume that different fan footprints are disjoint.

The fan geometry, upper bound on t, and all q4-star charges remain separate premises. They must be checked at the same radius before this lemma is used in a complete covering certificate.

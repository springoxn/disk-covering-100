# Exact B33 exclusion with radial stability and at most one ear

This is the B33 branch at R=1131/10000=.1131. It is intended to be combined
with the separately verified remaining boundary counts. It does not identify
the exact100-disk optimum. All completed .11309 sources remain unchanged.

## 1. Same-radius starting geometry

The original count bridge gives m100. In this branch I67 and F165. The
separate exact checkers EAR_STAR_PREMISES_0p1131.md and
ONE_EAR_STRUCTURE_0p1131.md establish:

- every unmarked angle lies in(.44,pi/2+.17);
- every singly marked interior-apex angle lies in(.44,pi/2);
- interior degrees are5 through14, and an interior apex has at most3 marked
  incidences;
- every full assigned boundary arc is greater than.08;
- no unmarked or singly marked face has all three centers on the boundary;
- the number e of doubly marked all-boundary ear faces is0 or1.

The last reduction combines one forced three-arc footprint with the sum of
the independently valid slab losses of two distinct ears; it never assumes
their footprints are disjoint. Unmarked faces with two boundary centers and
boundary chords are still allowed. N counts unmarked boundary-angle
occurrences, not just faces.

## 2. Simultaneous radial boundary-center support

Use lambda=37/1000. For half-arcs a_i set s_i=sin(a_i), c_i=cos(a_i),
h_i=sqrt(R^2-s_i^2), rho_i=c_i-h_i and radial tips p_i=rho_i*u_i. Write
each actual boundary center as p_i+d_i*u_i+t_i*v_i. The two endpoint-lens
constraints give

2h_i*d_i >= d_i^2+t_i^2+2s_i|t_i|.

The cyclic expansion and tangent charge are the same exact identity proved
in RADIAL_PENALIZED_STAR_0p11309_PROOF.md. Its node coefficients are

w_r=2lambda[2rho_b-rho_a cos(a+b)-rho_c cos(b+c)]+8lambda h_b-s_b,
w_t=2lambda[rho_a sin(a+b)-rho_c sin(b+c)].

The full-arc cutoff implies x_i=s_i/R>.3535>1/3, by an exact sine comparison.
Both nonnegative neighbor terms in w_t are at most s_b+R, so their difference
has absolute value at most s_b+R. Thus |w_t|<=8lambda*s_b and the tangent
residual k is zero. Using rho>=1-R and cos(a+b)>=1-2R^2 gives

w_r<=4lambda[1+R sqrt(1-x_b^2)-(1-R)(1-2R^2)]-R*x_b.

This decreases with x_b. The exact checker evaluates its upper bound at
x_b=.3535 and obtains a strictly negative value. Consequently every node
residual is nonpositive, including h_i=0 by continuity, and

sum outer_actual +lambda sum actual_marked_edge^2
<=sum H_R(2a_i)+lambda sum radial_marked_edge^2.

No equality of actual gaps or favorable independent tangential movements is
assumed. The squared displacement sum was bounded only after its global
cyclic expansion.

## 3. A quantitative radial-pair stability certificate

Let a0=pi/33. The exact two-variable checker proves, for all x_a,x_b in
[.3535,1],

[H_R(2a)+H_R(2b)]/2+lambda*L0(a,b)^2
+(3/4)[(a-a0)^2+(b-a0)^2]
<=56697/5000000-(1981163/100000000)(a+b).

Here L0 is the distance between the two radial tips. Its stable squared
formula is unchanged. Summing this support gives

Q<=33L+2pi*mu-(3/2)sum(a_i-a0)^2,

where L=56697/5000000 and mu=-1981163/100000000.

The exhaustive interval search covers the complete square, with symmetry
only discarding boxes entirely on the reflected side. It uses natural
interval bounds and, where h_a,h_b are positive, an independently valid
mean-value enclosure. The required derivatives are

rho'=sin(a)*rho/h,
H'=1-cos(a)*rho-sin(a)*rho',
partial_a L0^2=2rho_a'(rho_a-rho_b cos(a+b))+2rho_a rho_b sin(a+b).

The stability-score derivative adds(3/2)(a-a0)-mu. Multiplication by
R/cos(a) converts it to the sine parameter x. The interval derivative is
evaluated on the entire box, so its maximum absolute value times each
coordinate radius is a rigorous mean-value error bound around the midpoint.
If h has a zero lower bound the checker retains the natural enclosure.
The minimum of two valid upper bounds is valid. This accelerates acceptance
but changes no inequality or domain. The completed replay visits911 boxes,
with420 accepted leaves and36 symmetry skips.

## 4. The forced variance of one ear

An ear has three consecutive boundary-center sites. Its interior Voronoi
vertex lies within R of all three centers, so their covering disks lie in
a radius-2R disk. This contains the three complete assigned arcs in a
connected short circle footprint. The exact comparison sin(.4566/2)>2R
shows their full-arc total is at most L3=.4566.

Therefore their half-arc sum S is at most L3/2<3pi/33. Cauchy applied to
these three deviations and their30 complements gives

sum(a_i-a0)^2 >= (3pi/33-L3/2)^2*(1/3+1/30).

The lower bound is about.00120384494 and its stability charge is greater
than.00180576740. Only one footprint is used. In the e0 branch the
nonnegative variance term may simply be dropped.

## 5. Marked and unmarked angle budgets

The acute marked envelope with lambda=.037 is rechecked explicitly in
verify_one_ear_penalized_star_0p1131.py. It bounds a good marked triangle's
area-plus-anchor minus lambda times its marked-base square. Its curve and
tangent are those of MARKED_EDGE_PENALTY_ENVELOPE.md, now with this exact
parameter. The active-cap derivative, curve concavity and convex-unrestricted
support endpoint guards all pass.

For the one ear, radial slab geometry bounds its center-triangle area by
R*(1-sqrt(1-2R)) and each anchor by R^2/2. Dropping its nonpositive edge
penalties gives the normalized cap

E=1+(1-sqrt(1-2R))/R.

The positive lambda edge sum in Q is over every marked boundary edge,
including both ear edges. It cancels the negative edge penalties before
they are dropped in the ear cap, so none is charged twice.

For unmarked faces use the concave per-angle potential with coefficient
47/100, splice11019/10000 and endpoint pi/2+.17. The sum of the underlying
positive/negative square potential dominates normalized triangle area by
the zero-sum deviation identity. The exact tangent endpoint check supplies
its concave envelope phi. It is not a claimed universal quadratic deficit.

## 6. Complete zero/one-ear star counts

For e0 or1 the good marked count is M=33-2e and the unmarked count is
U=132+e. Interior star types(p,j) satisfy p<=3 and5<=p+j<=14, so40 types
are checked. Their multiplicities satisfy

sum x=67, sum p*x=M, sum j*x=3U-N, sum_(p>0)x<=N.

The fan-terminal count gives the last inequality even when an ear is
present. Hence11<=N<=94+e. Complete interior stars have angle sum2pi.
Subtracting good marked boundary angles and the e all-boundary ear angle
sums from the total boundary sum gives

sum unmarked boundary angles=Gamma+(e-2)pi,

where Gamma is the sum of good marked apex angles. Thus the boundary
conjugate contributes N C(eta)+(e-2)pi*eta.

Jensen within each star and rational LP duals bound its score by
u0+u1*p+u2*j+v*[p>0], with v>=0. Every type is checked in every integer N
case. The complete area upper bound is

R^2[67u0+M u1+(3U-N)u2+Nv+N C(eta)+(e-2)pi*eta+eE]
+33L+2pi*mu-e*(3/2)*(3pi/33-L3/2)^2*(1/3+1/30).

All169 cases and6,760 scalar inequalities pass. The minimum strict margin
is46844124028087756751/10^24, attained at e0,N23. Numerical optimizers only
propose rational duals and never decide acceptance.

## Replay and endpoint closure

Run the stable radial support checker and the one-ear penalized-star checker
with assertions enabled. The actual receipts are
radial_stability_support_0p1131_result.json and
one_ear_penalized_star_0p1131_result.json. The superseded slow natural-only
pair run was interrupted after the complete mean-value proof passed; it is
not counted as a successful replay.

As before, a hypothetical radius<=R cover is approached by generic slightly
enlarged covers. Select a fixed finite topology and convergent centers,
arc endpoints and angles, then pass the closed scalar and geometric
inequalities to the limit. The exact same-radius strict margins preserve
the required count/angle/ear restrictions in that limit. The final strict
area upper bound contradicts coverage. No same-radius generic perturbation
is asserted.

Combining this B33 result with the other same-radius boundary counts is a
separate integrated universal lower-bound theorem. Exact optimality remains
unresolved.

# Sharp area caps for complete interior stars

Let a complete interior star have degree d and center-triangle circumradii
at most R. Its d angles at the central vertex lie in[0,pi] and sum2pi.
With Q(a)=sin(a)*(1+cos(a)), each incident triangle has area at most
R^2*Q(a). The exact angle maxima are

    S_3=2;
    S_d=d*sin(2pi/d)*(1+cos(2pi/d)), d>=4.

Thus the total area of every complete interior star is at most R^2*S_d.
Marked anchors are not included in this cap. The result applies to marked
and unmarked interior vertices and to limiting degenerate triangles.

The degree-three/four proof is in UNMARKED_LOW_STAR_AREA_DEFICIT.md.
Here is the remaining argument for all d>=5.

## 1. Interior stationary points

As in the earlier proof, Q' is a quadratic in cos(a), and Q'' changes sign
only at a*=acos(-1/4). A local maximum can have at most one angle greater
than a*. All other angles must be equal because Q' strictly decreases
below a*. An angle equal to a* would force all angles equal to a*, which
does not satisfy the star sum for d>=5.

If there is one large angle b and d-1 equal small angles a, stationarity
gives cos(a)+cos(b)=-1/2. Here a=(2pi-b)/(d-1)<pi/2, so x=cos(a)>0.
The requirement cos(b)>=-1 implies x<=1/2, hence a>=pi/3. Therefore

    b=2pi-(d-1)a<=2pi/3.

But cos(b)=-1/2-x<-1/2 instead implies b>2pi/3, a contradiction.
Consequently every interior maximum has all angles equal to2pi/d.

## 2. Compact-domain boundary

The sequence d*Q(2pi/d) strictly increases for integers d>=4: on
0<t<=pi/2, Q(t)/t=(sin(t)/t)*(1+cos(t)) strictly decreases. This follows
from sin(t)-t*cos(t)>0, whose derivative is t*sin(t)>0.

If a boundary angle is zero, delete it and apply the preceding-degree
bound inductively. This is strictly smaller than S_d. If a boundary angle
is pi, the other angles sum pi. For d=5 their score is at most4A<S_5,
where A=3sqrt(3)/4 and

    S_5^2=25*(25+11sqrt(5))/32>27=(4A)^2.

For d>=6, Q(a)<=2a gives total remaining score at most2pi. This is less
than S_6=6A, and therefore less than every S_d with d>=6. Compactness
now proves the claimed maximum. The local regular-star configuration
attains S_d: place d neighbor centers regularly around the central center
so every incident triangle has circumradius R and its central angle is
2pi/d. This is a local extremizer, not a claim about a100-disk cover.

## 3. Conserved star-area multipliers

For a triangulated disk choose nonnegative multipliers tau_v on complete
interior stars. Require w_T=1-sum_(v in T)tau_v>=0 for every face. Exact
face bookkeeping gives

    sum_T area(T)
      =sum_T w_T*area(T)+sum_v tau_v*sum_(T incident to v)area(T)
      <=sum_T w_T*area(T)+R^2*sum_v tau_v*S_(degree(v)).

This permits adding sharp star-area constraints to a fixed-graph or
finite-label dual without counting any actual triangle twice. The
remaining face supports must use their new coefficient w_T. A linear
corner-potential localization guard scales with w_T; an old unweighted
guard must not be silently reused.

For a marked face with interior-apex multiplier tau and zero boundary
multipliers, put w=1-tau. Its center-triangle area coefficient is w while
the anchor and squared-base penalty retain their original coefficients.
At fixed half-base x and apex g, the support is

    w*x^2*cot(g/2)+x*sqrt(1-x^2)-4lambda*x^2+t*g.

Convexity in g again gives endpoint branches, with a=asin(x):

    w*sin(a)+(w+1)*sin(2a)/2-4lambda*sin(a)^2+t*a;
    w*sin(a)+(1-w)*sin(2a)/2-4lambda*sin(a)^2+t*(pi-a).

For0<=w<=1 and0<=lambda<=w/8 both branches are concave on[0,pi/2].
The same elementary |cos(2a)|<=sin(a) bound used in the unweighted
conjugate proves this. Exact scalar checks and all global multiplier
constraints remain required before a new radius theorem uses the tool.

verify_complete_star_area_caps.py checks the algebraic base comparisons
and exact sample caps. The continuous maximum theorem is analytical;
the checker alone is not a covering-radius exclusion.

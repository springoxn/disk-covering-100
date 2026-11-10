# Exact area deficits for unmarked degree-three and degree-four stars

Let Q(a)=sin(a)*(1+cos(a)) for0<=a<=pi. A triangle of circumradius at
most R having angle a at a specified vertex has area at most R^2*Q(a):
at fixed a and circumradius, the other two angle sines are maximized when
they are equal. For a complete unmarked interior star its angles sum2pi.

The following finite-angle maxima are exact:

    max sum_(i=1..3) Q(a_i)=2,       sum a_i=2pi;
    max sum_(i=1..4) Q(a_i)=4,       sum a_i=2pi.

All angles lie in[0,pi]. The first maximum includes a degenerate endpoint
configuration(pi,pi/2,pi/2); the second is attained at four right angles.
The inequalities apply to limiting degenerate triangulations as well.

## 1. Stationary-point reduction

Q'(a)=cos(a)+cos(2a) is a quadratic in cos(a), so at a constrained interior
stationary point there are at most two distinct angle values. Put
a*=acos(-1/4), which lies between pi/2 and2pi/3. One has

    Q''(a)=-sin(a)*(1+4cos(a)).

Thus Q' strictly decreases below a* and strictly increases above a*.
At an interior local maximum at most one angle can exceed a*: varying
two such angles in opposite directions gives a strictly positive second
variation. An angle exactly a* would force every angle to equal a*, since
Q' takes its unique minimum there; this does not satisfy either angle sum.

Consequently an interior maximum is either the all-equal configuration,
or one large angle b and all other angles equal to a<a*. The stationary
condition for unequal roots is

    cos(a)+cos(b)=-1/2.

## 2. Three angles

The all-equal configuration has angle2pi/3>a* and cannot be a local maximum.
In the unequal case b=2pi-2a, so with x=cos(a), stationarity gives

    4x^2+2x-1=0.

The sum condition and a<a* require x in(-1/4,0). Neither root
(-1+sqrt(5))/4 or(-1-sqrt(5))/4 lies there. Hence the maximum occurs on
the compact domain boundary. If one angle is0, the others are both pi,
giving zero. If one is pi, the other two are a and pi-a, giving
Q(a)+Q(pi-a)=2sin(a)<=2. This proves the three-angle bound.

## 3. Four angles

The all-equal configuration has four angles pi/2 and score4. In the
unequal case b=2pi-3a, and x=cos(a) lies in(0,1/2). Stationarity gives

    8x^3-4x+1=(2x-1)*(4x^2+2x-1)=0.

The root1/2 corresponds to the boundary b=pi, and the negative quadratic
root is outside the domain. The only interior candidate has
x=(sqrt(5)-1)/4, a=2pi/5, b=4pi/5. Its score squared is exactly

    [3Q(2pi/5)+Q(4pi/5)]^2=25*(5+2sqrt(5))/16<16.

Thus it is smaller than4. On any boundary configuration one angle is0
or pi; its Q value vanishes, and each remaining Q is at most
A=3sqrt(3)/4, its global maximum at pi/3. Hence that score is at most
3A<4. Compactness completes the four-angle proof.

## 4. Use in the covering loss budget

An unmarked interior degree-three star has three distinct q0 faces and
area sum at most2R^2, instead of its old allowance3A R^2. Its mandatory
normalized loss is3A-2. The degree-four loss is4A-4. Therefore, whenever
the old global nonnegative face-loss budget d satisfies

    d<4A-4=3sqrt(3)-4,

there can be no unmarked interior degree-three or degree-four star.
This does not require an actual-angle window, marked-apex acuteness,
chordlessness or flat development. It uses complete interior stars and
the same original face-loss budget once; it cannot be added again to a
dual already charging those same faces.

In such a branch the weighted unmarked curvature condition K0>=2 from
ONE_POSITIVE_CURVATURE_ISOPERIMETRY.md means at least two distinct
unmarked degree-five vertices. The general weighted flag remains valid
without this additional area premise.

verify_unmarked_low_star_area_deficit.py checks the exact algebraic
constants and sample old-loss comparisons. It establishes no covering
radius exclusion without the rest of the branch proof.

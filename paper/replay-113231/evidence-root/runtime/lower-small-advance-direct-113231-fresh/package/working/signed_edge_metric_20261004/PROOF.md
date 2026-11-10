# Signed shared edge supports for a fixed covering graph

## Scope and first result

This method adds actual shared-edge metric compatibility to the earlier full-face angle dual. The current rational certificate excludes the explicit graph flat_N27_0009 at R=11309/100000. Actual center coordinates are unrestricted. The lattice development labels specify only a combinatorial graph; they are not prescribed center positions.

This is a graph-conditional exclusion. A universal lower bound additionally requires a complete graph-family reduction and every remaining graph/case to be excluded.

## 1. Opposite signed half-edge potentials

Every unmarked center triangle f has circumradius R*rho_f with 0<=rho_f<=1. If its angles are a_1,a_2,a_3, then

    area(f)/R² = rho_f² A(a),   A(a)=2 product sin(a_i),
    length(edge opposite a_i)/(2R)=rho_f sin(a_i).

For every edge shared by two unmarked triangles choose an arbitrary rational number tau_e. Assign +tau_e to its opposite corner in one triangle and -tau_e to its opposite corner in the other. Assign zero on every unmarked/marked interface edge. The sum of all signed normalized edge lengths is exactly zero, because the same physical edge has the same length on both sides, even when its incident circumradii differ.

For an unmarked face, therefore, use the local score

    rho² A(a)+rho sum_i tau_i sin(a_i)-sum_i u_i a_i.

Marked-face supports are unchanged. No independent side-length or equal-circumradius assumption is introduced.

## 2. Eliminate the circumradius ratio safely

On the closed angle simplex a_i>=0, sum a_i=pi, A(a)>=0. The score is convex in rho, so its maximum on [0,1] occurs at rho=0 or rho=1.

At rho=0, maximizing the pure linear score gives -pi*min_i u_i. This value is also realized at rho=1 by a simplex vertex (pi,0,0), because every sine term vanishes. Hence the complete rho/angle maximum equals the complete rho=1 angle maximum. The implementation retains an explicit max with the rho=0 bound as an additional safe check.

At rho=1 the triangle identity gives

    A(a)+sum tau_i sin(a_i)-sum u_i a_i
      =sum_i [sin(2a_i)/2+tau_i sin(a_i)-u_i a_i].

The sum identity uses sum a_i=pi. The individual terms need not be positive for an actual nonacute triangle.

## 3. A complete-angle localization guard

Let L=max u_i-min u_i<=1/2, let a0=pi/3, s0=sqrt(3)/2 and A0=3sqrt(3)/4. For the angle-only centered score A(a)-sum u_i(a_i-a0), the earlier full-simplex lemma proves that every nonacute or degenerate triple has score at most

    M(L)=max{1+L*pi/6, 2L*pi/3, sqrt(3)/2+pi*(1+L)/12}.

For completeness, the positive sum of three zero-sum deviations equals their largest absolute deviation d. The linear term is at most Ld. If d is the largest-angle excess, fixing theta>=pi/2 gives A<=sin(theta)(1+cos(theta)); its tilted maximum occurs at an endpoint. If d is the smallest-angle deficit, that smallest angle t is at most pi/4 and A<=sin(2t); its tangent at pi/6 gives the third displayed bound.

Relative to the equilateral triple, the additional signed-edge term satisfies

    sum tau_i(sin(a_i)-s0) <= s0 sum |tau_i|,

since |sin(a)-s0|<=s0 on [0,pi]. Consequently the exact sufficient guard

    A0 > M(L)+s0 sum |tau_i|

places every global maximizer strictly inside the acute simplex. The actual triangle need not be acute. The verifier checks all three strict comparisons separately, for every face, with exact outward intervals.

No concavity of the individual signed sine functions is assumed. A negative tau can introduce a small nonconcave tail near pi/2, which the scalar verifier handles explicitly.

## 4. Exhaustive scalar supports

Define

    H(tau,w)=max_[0,pi/2] {sin(2a)/2+tau sin(a)-w a}.

The endpoint scores are 0 and tau-w*pi/2. Every interior critical point has x=cos(a) in [0,1] satisfying

    2x²+tau*x-1-w=0.

Thus both roots

    x=(-tau +/- sqrt(tau²+8(1+w)))/4

are considered whenever the discriminant is nonnegative. Each in-domain critical score is

    (x+tau)*sqrt(1-x²)-w*acos(x).

There are no other extrema on the compact scalar domain. The checker uses exact integer discrimination, outward root intervals, both signs, both endpoints and safe domain clipping. An uncertain near-endpoint root is retained for upper bounds rather than discarded. The scalar result is increasing in tau and decreasing in w, so interval parameters are enclosed by the corresponding endpoint choices.

Arccos is enclosed throughout [-1,1], including endpoints. For x>=0 it uses

    z=sqrt((1-x)/(1+x)),
    acos(x)=4 atan(z/(1+sqrt(1+z²))).

The final atan argument is at most sqrt(2)-1<1/2. Forty alternating Taylor terms are used; the omitted positive remainder is bounded by the next term. Negative x uses acos(x)=pi-acos(-x). The pi enclosure and integer interval operations come from the previously audited exact arithmetic kernel.

For any rational face multiplier eta, the full-triangle support is

    S_f=pi*eta+sum_i H(tau_i,u_i+eta),

provided the complete-angle localization guard holds. It follows by evaluating the global acute maximum and using sum a_i=pi. This is not a pointwise acuteness assumption about a cover.

## 5. Graph summation and the area contradiction

Put u_v=0 at every outer-boundary vertex, and use arbitrary rational potentials at the 67 interior vertices. Interior angle sums are exactly 2pi. For each of the 33 marked triangles with interior apex v, retain the prior global marked-apex conjugate G(u_v), with its checked condition u_v>-1/2.

Summing local supports cancels every interior-angle potential and every signed q0-q0 edge term. Therefore

    center-face and anchor area / R²
      <= 2pi sum_v u_v + sum_marked G(u_apex) + sum_q0 S_f.

The previous signed outer-area decomposition and concavity add at most 33 H_R(2pi/33), with

    H_R(theta)=sin(theta/2)*sqrt(R²-sin²(theta/2))+(theta-sin(theta))/2.

The exact verifier checks the graph's 100 vertices, 264 edge incidences, 165 faces, vertex links, marked-edge labels, every opposite-edge assignment, all signed cancellations, every localization guard and the final strict area contradiction. Degenerate configurations are included by the same continuous limiting argument as the earlier fixed-graph angle certificate.

For flat_N27_0009 it checks 172 shared edges and 132 q0 face supports. The exact area margin at .11309 is

    1841643475257158103 / 15625000000000000000000 > 0.

The coefficients have denominator 10^10. Numerical optimization only proposed them; acceptance uses Python's standard library and exact integer/Fraction intervals. This is mathematical/software verification, not a proof-assistant formalization.

## Replay

    python -S verify_signed_graph.py graph_N27_0009.json certificate_N27_0009.json

Keep assertions enabled. The supplied graph is SHA-bound to the rational coefficient file. This certificate does not depend on the optimizer or assume the angular relaxation has an actual Euclidean realization; failure of realizability only strengthens its use as an upper bound.

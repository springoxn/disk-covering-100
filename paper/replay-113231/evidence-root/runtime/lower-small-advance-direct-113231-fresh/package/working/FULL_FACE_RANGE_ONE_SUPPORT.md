# Full-simplex face supports for corner-potential range below one

Let alpha,beta,gamma>=0 with sum pi. For rational corner potentials lambda_i define

    F = (sin(2alpha)+sin(2beta)+sin(2gamma))/2
        + sum_i lambda_i*(alpha_i-pi/3).

If max(lambda)-min(lambda)<1, the global maximum of F is attained either in the closed acute-angle simplex or at a degenerate simplex vertex. Consequently a valid upper bound is the maximum of

    pi*nu + sum_i H(nu-lambda_i) - (pi/3)*sum_i lambda_i,
    pi*(max_i lambda_i - (lambda_1+lambda_2+lambda_3)/3),

for any real nu, where H(t)=sup_{0<=a<=pi/2}(sin(2a)/2-ta). The first expression is the existing exact sine-conjugate dual bound. The second expression is mandatory; the acute bound alone need not suffice when the old half-unit range restriction is removed.

## Proof

The closed angle simplex is compact. On its boundary at least one angle is zero, and the other two sum to pi, so the area term vanishes identically. A linear function on this boundary reaches its largest value at one of the three simplex vertices, giving the displayed second cap.

Suppose an interior local maximum has alpha>=pi/2. The other two angles are positive and beta+gamma<=pi/2. Set

    c=-cos(alpha)>=0, z=cos(beta-gamma)>0.

Along the sum-preserving direction v=(1,-1/2,-1/2), the second derivative of the area term, and hence of F, is

    sin(alpha)*(4c-z).

Local maximality therefore implies4c<=z. The derivative of the area term in the opposite, inward direction -v is

    1-2c^2+cz = 1+c*(z-2c) >= 1.

The linear-potential part of that derivative is

    -lambda_alpha+(lambda_beta+lambda_gamma)/2
    >= -(max(lambda)-min(lambda)) > -1.

Thus the inward derivative of F is strictly positive, contradicting local maximality. No nonacute interior maximum is possible. The closed acute simplex includes the right-angle boundary case, and its usual conjugate bound proves the result.

This proof concerns the maximum of an area-plus-linear support score, not a restriction on actual triangle angles. For a triangle with circumradius at most r, its normalized area is at most the area term above; therefore the same support applies in the covering inequalities without assuming actual acuteness.

The strict range<1 guard and the degenerate-vertex cap must be checked for every new label multiset. Existing frozen certificates are unchanged.

# Full-apex marked support with a linear half-side penalty

Let the covering radius be r, let x=L/(2r) be the normalized half-length of the marked base, and let gamma be the opposite triangle angle. Circumradius at most r implies

    asin(x) <= gamma <= pi-asin(x).

For the fixed base and opposite angle, the triangle area is at most r^2*x^2*cot(gamma/2), with equality for an isosceles triangle. Its adjacent boundary-anchor contribution is at most r^2*x*sqrt(1-x^2). Thus the normalized score, including a half-side penalty kx and a linear apex multiplier s*gamma, is at most

    x^2*cot(gamma/2)+x*sqrt(1-x^2)-k*x+s*gamma.

This expression is convex in gamma. Consequently it suffices to use its two allowed endpoints. Writing a=asin(x), the acute and obtuse endpoint scores are

    (1-k)*sin(a)+sin(2a)+s*a,
    (1-k)*sin(a)+s*(pi-a),

respectively, on 0<=a<=pi/2. For 0<=k<=1 both are concave: their second derivatives are -(1-k)sin(a)-4sin(2a) and -(1-k)sin(a). This is a full-apex bound and does not assert acuteness of actual triangles.

The exact helper `exact_linear_halfside_marked_conjugate.py` maximizes these two concave functions using rational interval derivative brackets and supporting tangents. Beyond the uncertain rational enclosure of pi/2 it continues each expression by its exact endpoint tangent, preserving concavity and a safe upper bound. When an outward endpoint can affect the reported lower endpoint, it takes that lower bound from a feasible exact endpoint, as in the already-audited squared-edge helper.

At k=0 the result agrees with the existing full-apex zero squared-edge conjugate. The checker verifies overlap at six signed multipliers and evaluates eighteen parameter cases, including endpoint and equilateral feasible lower bounds. These tests supplement the analytic proof; sampling is not the proof of validity for untested rational multipliers.

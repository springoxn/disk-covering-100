# Independent audit: arbitrary-penalty full-apex marked conjugate

Date: 2026-10-04 UTC. Result: PASS for the hardened scalar kernel. A fresh standard-library replay passes all30 samples, all five exact root-count fixtures, zero-polynomial rejection and the fixed-grid rational-root precision regression. Optimized-mode execution is refused.

The fixed-base geometric reduction is valid for every rational penalty lambda>=0. At half-base x and apex gamma, circumradius<=1 gives gamma in[asin(x),pi-asin(x)]. Triangle area is at most x^2*cot(gamma/2); adding the anchor, base-square penalty and linear angle term remains convex in gamma. Thus the two displayed endpoint functions on a in[0,pi/2] give the complete relaxed scalar support. Large penalties do not justify assuming scalar concavity, and this kernel does not do so.

I independently differentiated both endpoint functions and expanded the quartics. Their rational coefficient arrays match (4c^2+c-2+t)^2-64lambda^2*c^2*(1-c^2) and (c-t)^2-64lambda^2*c^2*(1-c^2). Every interior stationary cosine lies in[0,1] among these roots. Retaining squared extraneous roots is safe for both bounds: they are still feasible scalar arguments, while no actual stationary point is omitted.

Rational long division, gcd and squarefree reduction preserve all distinct roots, including repeated ones. Endpoint roots are recorded before deflation. The negative-remainder Sturm chain uses only positive individual rescaling; its variation differences count all remaining roots between nonroot rational endpoints. The multiple-root subdivision trials include more distinct rational points than the degree, so a nonroot cut is available. One-root refinement either finds an exact rational midpoint or chooses the correct unique subinterval. The explicit fixtures independently cover repeated zero, endpoint one, two rational interior roots, four strictly interior roots and a three-interior/one-endpoint quartic.

The radical and transformed-atan acos enclosures are outward. Forty alternating terms leave a positive next-term remainder; the transformed argument is below1/2. Monotone endpoint evaluation gives the entire acos bracket. Endpoints and every retained root score are evaluated, so taking the maximum upper endpoint covers the global scalar maximum. The maximum lower endpoint is also legitimate here: each included root, even an extraneous squared root, is a feasible point of the scalar interval. This distinguishes the scalar maximum from an arbitrary full-face dual-support expression.

Two adversarial API cases found during review were corrected before this binding. roots_unit now rejects zero and empty polynomials instead of reporting no roots. With branch(0,3/10,obtuse=True,precision=10^-40), a rational cosine exactly on the fixed grid could remain between dyadic endpoints forever. The hardened two-unit plateau path tests enclosed grid points against the exact polynomial, recovers cosine3/10 when present, or retains the full safe broader enclosure. A request smaller than fixed-point resolution is not misrepresented as an achieved precision. The fresh regression passes and returns an outward interval wider than the impossible request.

SHA-256 bindings:

- sturm_quadratic_marked_conjugate.py: e85c5fb42eabb12c17e05d62ff484e757dc7fa019dd32d9eb6ecd1804116fb6d
- STURM_QUADRATIC_MARKED_CONJUGATE.md: 3db58ff7a9caa119450d5e3fa2f9ad62ea32f56c0fae79ca603956a85fca2547

This is a full-apex scalar-support audit. Any radius certificate still needs compatible edge-square cancellation, the actual domain/normalization proof, complete face/vertex/count constraints, remaining boundary counts and the generic endpoint reduction. The sample tests are regression evidence; completeness rests on the geometric endpoint reduction and exact root enumeration above.

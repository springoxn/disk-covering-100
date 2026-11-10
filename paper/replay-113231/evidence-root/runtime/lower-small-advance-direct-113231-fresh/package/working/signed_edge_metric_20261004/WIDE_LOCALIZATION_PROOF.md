# Wider signed edge localization by exact two variable subdivision

This extends the complete-angle localization step in PROOF.md. All edge cancellation, circumradius reduction, scalar critical-point enumeration, graph incidence and final area arguments remain unchanged.

Let L bound the range of the three corner potentials and let epsilon bound the absolute value of each signed edge coefficient. Write a0=pi/3, s0=sqrt(3)/2, and A0=3sqrt(3)/4. For a nonacute angle triple, its signed score minus its equilateral score is at most

    A(alpha)-A0 + L max_i |alpha_i-a0|
      +epsilon sum_i |sin(alpha_i)-s0|.

The linear-potential estimate follows from the zero sum of the three angle deviations; their positive sum equals their largest absolute deviation. The signed sine estimate uses the triangle inequality. No claim about an actual triangle being acute is made.

Because this upper bound is symmetric, label the largest angle theta and the smallest beta. Every nonacute or degenerate triple has the exact parametrization

    theta=pi(1+x)/2,
    beta=pi(1-x)y/4,
    gamma=pi(1-x)(1-y/2)/2,
    0<=x,y<=1.

These angles sum to pi, with theta>=pi/2 and beta<=gamma. At theta=pi, beta=gamma=0, independently of y, so no division or missing endpoint arises. The largest absolute deviation is

    max(theta-pi/3, pi/3-beta).

The verifier bounds, over this entire closed square,

    G=2sin(theta)sin(beta)sin(gamma)
      +L max(theta-pi/3,pi/3-beta)
      +epsilon[|sin(theta)-s0|+|sin(beta)-s0|+|sin(gamma)-s0|].

It bisects integer-grid rectangles until each has outward interval upper bound at most the stated cap. Every box is retained until accepted; there are no symmetry skips. All trigonometric arguments lie in [0,pi], and the inherited Taylor-remainder enclosures include their endpoints. Acceptance requires an empty queue and cap<A0. A resource-limit exception is failure, never PASS.

The four exact verified tradeoffs are:

| L | epsilon | cap | visited boxes | accepted leaves |
| --- | --- | --- | --- | --- |
| 3/10 | 1/5 | 63/50 | 141 | 71 |
| 3/10 | 1/4 | 129/100 | 143 | 72 |
| 2/5 | 3/20 | 129/100 | 163 | 82 |
| 1/2 | 1/20 | 259/200 | 181 | 91 |

Each cap is strictly below A0. Therefore the global full-simplex signed score maximum is acute under any of these checked coefficient bounds. The existing exact scalar conjugate on [0,pi/2] is then valid for every actual triangle, including nonacute ones, through this global-maximizer localization argument.

`wide_metric_conjugates.py` checks a face against these domains, replays the corresponding cached exact square certificate, and otherwise falls back to the narrower analytic guard. An unsupported or invalid domain is rejected. `verify_signed_graph_wide.py` replays all four square certificates and changes only the two declared support functions in the common graph verifier.

## Graph-conditional applications

The hard N26 graph flat_N26_000_special_01 is excluded at R=.11312, with exact margin

    16170721676878106167 / 50000000000000000000000 > 0.

The supplied coefficients have maximum face range .399 and absolute signed-edge coefficient at most .15. Its rational data are graph_N26_0001.json and certificate_N26_0001_wide_11312.json.

The N27 graph flat_N27_0009 is excluded at R=.11310, with exact margin

    366613752753568194619 / 250000000000000000000000 > 0.

Its data are graph_N27_0009.json and certificate_N27_0009_wide_11310.json.

Run the wide graph verifier on the indicated graph and coefficient files with ordinary Python and assertions enabled. These are exclusions of the specified combinatorial graphs with unrestricted actual coordinates, not new universal radius lower bounds. No graph enumeration completeness claim is made here.

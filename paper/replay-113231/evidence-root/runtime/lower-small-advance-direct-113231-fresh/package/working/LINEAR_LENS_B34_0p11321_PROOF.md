# Complete normalized B34 exclusion at R=.11321

Set R=11321/100000 and K=1/2. Normalize ALL centers at R before forming
the diagram, giving norm<=sqrt(1-R^2). This is a complete B34 branch,
not an all-boundary-count radius theorem. All counts refer to that same
normalized diagram; no center is moved during the proof.

## 1. Fresh geometry and the exact normalized lens

The exact count bridge excludes m<=99 and leaves m100,B31,...,38.
The six-cell3R footprint with full span .6932 gives ordinary marked
incidence<=4. All-boundary q0/q1 faces and arbitrary ears are allowed.
The old normalized loss d is recomputed and is above1; its actual value
is used in the core cut pi*(109A-d)>21^2, proving M=U-2e>=22.

The same-radius scalar wrapper verify_exact_lens_boundary_B34_0p11321.py
checks1000 bad-arc boxes and the complete good-arc curvature argument
at K=.5 and variance .03. It uses the exact intersection of the endpoint
lens with the normalized center ball, as proved in
EXACT_NORMALIZED_LENS_PENALTY.md. Floating root proposals only choose
tangents; every accepting inequality is an outward rational comparison.

Write mu=pi/34,s=sin(mu),rho=cos(mu)-sqrt(R^2-s^2), and H(mu)=mu-s*rho.
The global linear-halfside boundary compensation is bounded by

    outer +(K*R/2)*sum(marked base lengths)
      <= Q - .03*sum(a_i-mu)^2,
    Q=34*[H(mu)+K*R*s*rho].

The final rows discard the nonnegative variance deduction entirely.
The endpoint-lens proof, tangent to the global sine term, supplies this
Q for all actual arcs; no independent positive arc cutoff is assumed.

## 2. Matching center-face supports

The full-apex linear-halfside conjugate is

    C_K(t)=max over a in[0,pi/2] of
       sin(a)*(1-K+2cos(a))+t*a,
       (1-K)*sin(a)+t*(pi-a).

It majorizes area/R^2+J_R(L)/R^2-K*L/(2R)+t*apex_angle for every
marked triangle, without actual-angle acuteness. Its negative halfside
term cancels exactly the boundary compensation above.

The q0 supports use four labels: high-degree interior, boundary, ordinary
interior and distinguished deep low-degree. No deep vertex has a boundary
neighbor. Every one of the16 remaining unordered triples is checked by
the range-below-one full-simplex theorem with its degenerate cap. All
ordinary incidence0..4 and degrees max(3,q+1)..99 are covered, including
separate deep/nondeep unmarked low types. Terminal BI credits are reserved
on q0 faces before being used at marked vertices.

The topology forces two weighted deep-curvature units for M<=23, one
deep low-degree vertex for M<=25, and no flag for larger M. These are the
only geometric flags in this proof. No unique-five isolation lemma or
finite graph enumeration is required.

## 3. Arbitrary ears and bad faces

Let e count q2 ears and b count bad all-boundary q1 faces. There are130+e
q0 faces and34-2e-b ordinary q1 faces. Interior degree excess is
28+e-b-U, and the boundary q0 angle sum is Gamma+(e-2)pi.

Put w=2/(1+sqrt(1-2R)). The joint Jensen/slab ear cap is
w+sqrt(2w-w^2)-K*sqrt(2w). For a bad q1 face, a valid cap is
w+sqrt(1-y^2)*(y-K), with y=(K+sqrt(K^2+8))/4. The checker verifies a
negative shifted-ear coefficient and a negative bad-face coefficient
in each row. Thus every e,b>=0 is covered. All-boundary q0 triangles
are already included in the face table, including the BBB triple.

All M slopes are negative. Evaluate the weighted row at M22, the one-
flag row at M24, and the flag-free row at M26. They cover M22..23,
M24..25 and every M>=26 respectively.

verify_linear_lens_B34_0p11321.py replays the fresh geometry, the scalar
envelope,48 full-face supports and1455 vertex inequalities. Its minimum
area gap is23206990715328095583/(125*10^21), greater than .00018565.
Strict gaps extend through the usual normalized generic-limit closure.

The proof uses normalization at .11321 itself; no stronger-radius norm
bound is transferred. Other B counts remain separate obligations.

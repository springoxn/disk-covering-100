# Conditional q3-corner metric certificates at .11321

The entry verify_conditional.py checks one supplied q3-corner graph and a rational coefficient file. It checks the graph against the regenerated402-family catalog, reconstructs every shared-edge incidence, and recomputes132 q0,33 marked-face and33 arc supports. No saved PASS report is used as input.

The first six supplied graphs pass exactly, with minimum margin greater than .0022. A separate402-family proposal/replay batch is in progress. No unconditional graph or universal radius claim follows until the geometric premises below and the complete profile/catalog reduction are independently established.

## 1. Explicit geometric premises

At R=11321/100000 the actual cover must have the supplied no-ear graph, all ordinary marked faces, and:

- sin(t_i)/R>3/5 for every assigned boundary half-arc
- every marked base length exceeds9R/10
- the radial-tip reference edge length exceeds3R/5, with the orientation-error bound9/(4R)
- the weighted outer-area/angle absorption lemma applies to adjacent boundary-potential differences at most79/1000
- the ordinary unequal-base marked-face square charge25/16 applies.

The first arc premise implies t_i>679/10000; the verifier checks sin(679/10000)<3R/5 exactly. The absorption arithmetic has strict room because (3/5)^2>(9/2)*(79/1000). The earlier pure-window coefficients are not reused as an unexplained new-radius hypothesis. The profile/arc work must independently prove these actual-diagram conditions.

The stronger arc premise actually makes the reference-length bound much easier. The lower-bound worker is preparing a separate exact checker connecting the profile dual to the actual marked-base bound. Those facts are not silently assumed to follow from a numerical proposal.

## 2. Full q0 support and shared physical lengths

Use arbitrary subtractive vertex potentials u_v and opposite signed half-edge coefficients tau. For a q0 face with angles alpha and circumradius rho*R, its score is

    area/R^2 + sum tau_i*L_i/(2R) - sum u_i*alpha_i.

The exact full-simplex helper uses centered PLUS labels lambda_i=-u_i. It applies the independently derived theorem SIGNED_SINE_FULL_FACE_LOCALIZATION.md:

    range(lambda)+sum max(-tau_i,0)/2 < 1.

Under this strict guard every interior maximum at rho1 is acute, but all three simplex boundary edges are retained explicitly. The scalar conjugates enumerate every admissible critical root and both acute endpoints; no scalar concavity assumption is needed. Each boundary edge has its two endpoints and, when applicable, its one exact cosine stationary point.

The helper's centered support is converted back to the required uncentered score by subtracting pi*sum(u_i)/3. Convexity in rho reduces the actual scale to rho0 or1, and the rho0 linear score is included by the vertex caps. No actual triangle is assumed acute or to have maximal circumradius.

Every selected q0-q0 edge is reconstructed from the oriented triangle lists and receives equal-and-opposite coefficients. Its physical length is the same in its two incident triangles even when their circumradii differ. Thus all such terms cancel exactly.

## 3. Unequal-base marked support

For a marked face with apex v and boundary base a,b, define

    mean=(u_a+u_b)/2,
    tilt=u_v-mean,
    difference=u_a-u_b.

Its full face-plus-anchor support is

    C(tilt)-pi*mean+(25/16)*difference^2.

Here C is the all-apex Gbar conjugate from exact_angle_conjugates.py; the accepted tilt interval is checked explicitly. The quadratic charge is justified by the actual marked-base>.9R premise and the audited unequal-base lemma. It is not a claim that the actual marked triangle is isosceles.

## 4. Boundary-angle coupling

Let w_i be the boundary potentials in actual cyclic order, T=R^2, and let

    beta_i=T*(w_(i-1)-2w_i+w_(i+1))/2,
    alpha_i=2T*w_i+zeta.

The weighted radial-tip comparison bounds the original outer-area-plus-boundary-angle functional, without moving the cover or preserving any adjacency after a move. Its exact assembled cap is

    pi*(zeta+T*sum w_i)
      +sum_i sup_t [H_R(t)-alpha_i*t+beta_i*eta_R(t)],

where

    H_R(t)=sin(t)*sqrt(R^2-sin(t)^2)+t-sin(t)cos(t),
    eta_R(t)=asin(sin(t)/R)-t,
    679/10000<=t<=asin(R).

The arbitrary rational zeta uses the exact identity sum t_i=pi. The arc helper retains both endpoints and all in-domain roots of its squared quadratic stationary equation, including extraneous roots. Keeping extras can only enlarge the bound. It also checks beta_i<T.

This is a single weighted outer-area comparison. The prior profile support is used only to establish necessary geometry, never added as a second area loss.

## 5. Final cancellation and exact acceptance

Sum the q0 and marked supports and add2pi*sum_(interior)u_v. The actual interior angle sums cancel; the remaining boundary term is the weighted polygon-angle expression already bounded above. After multiplying center terms byR^2 and adding the boundary cap, the result is strictly less than pi.

All coefficients are integer numerators over10^12. The certificate SHA-binds the graph bytes, and the graph is also compared semantically with the generated catalog. The numerical optimizer, its success flag and floating diagnostics are not acceptance inputs. Every accepted local inequality and final margin is recomputed with exact outward intervals.

A complete family theorem additionally requires all402 distinct regenerated families to pass. A universal B33 theorem additionally requires the new-radius profile/geometry reduction to show that every remaining cover belongs to that family and meets the displayed premises.

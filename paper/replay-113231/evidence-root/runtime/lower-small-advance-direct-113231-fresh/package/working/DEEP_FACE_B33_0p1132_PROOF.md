# Complete normalized B33 exclusion at R=.1132

Set R=283/2500. Reflect ALL centers to norm at most sqrt(1-R^2) before
constructing and classifying the diagram. This proof treats B33 of that
normalized diagram. It is not an all-count radius theorem.

## 1. Unpenalized starting domains

B33_ANGULAR_BOOTSTRAPS_0p1132.md establishes m100, the same-radius count
bridge B31,...,38, no all-boundary q0/q1 faces, and ultimately ordinary
marked incidence q<=3. The last step is new: initially only q<=4 is
known.190 additional q4 vertex checks cost at most8*.02, giving center
cap229.363; a five-arc footprint is then impossible. The original
uncharged cap229.203 follows and gives full arc>.0685, x>.3025.

The independent M=U-2e<=25 center cap228.99 gives full arc>.1004 and
x>.4432. Neither angular bootstrap assumes a radial inequality, fan
variance or actual marked-apex acuteness. The old loss budget below1
and core-cut inequality give M>=22.

## 2. A second, independent high-M domain

For M>=26, `verify_B33_highM_variance_arc_0p1132.py` first replays the
original domain and the initial reflected radial support at
lambda=.09, gamma=.25, x>=.3025. This pair uses1011 exact boxes.

One four-label face row checks16 full-face supports and390 vertex types,
with no fan or ear variance deduction. Its M slope and shifted-ear
coefficient are negative, so evaluation at M26,e0 bounds all M>=26 and
all e>=0. Together with the initial boundary support it gives

    pi <= T - (1/4) sum_i(a_i-pi/33)^2,
    T-pi <= 532913581958414786537/10^24.

If a particular half-arc a_i<=.046, Cauchy on that arc and the other32
gives variance at least(33/32)(pi/33-.046)^2. This leaves a contradiction
margin91152020501515693307/10^24. Thus every full arc exceeds .092 and
x>.4062 on the high-M branch.

The entire .25 variance coefficient is reserved for this domain proof.
It is not also spent on fan charges. The resulting actual arc condition
is then used in a different final inequality; the initial and final
boundary bounds are never added together. There is no circular appeal
to the stronger final domain.

## 3. Final low/high boundary supports

The low-M final support has lambda=.056, gamma=1.5, x>=.4432 and1011
boxes. The high-M final support has lambda=.11, gamma=0, x>=.4062 and1037
boxes. Both use the proved reflected-center displacement cap. Their
same-radius entries are

* `verify_reflected_radial_B33_lowM_0p1132.py`
* `verify_reflected_radial_B33_highM_0p1132.py`

Only the support appropriate to the actual M range is used.

## 4. Four complete face/count ranges

The final rows use the global two-branch marked conjugate, the full-face
range-below-one theorem including its degenerate cap, and the deep-core
curvature witnesses. A deep vertex has no boundary-center neighbor;
precisely the16 label triples without a deep/boundary pair are checked.
Both deep and nondeep unmarked low-degree types are included, so a
compulsory curvature flag is assigned only to a genuine deep witness.
Nonnegative terminal BI credits are reserved on q0 faces.

`verify_deep_face_B33_0p1132.py` checks64 faces and1560 vertex types:

* e0,M22..23: two weighted deep-curvature units, evaluated at M23
* e0,M24..25: one deep low-degree vertex, evaluated at M24
* e>=1,M22..25: one such vertex, evaluated at e1,M22
* all e,M>=26: no flag, evaluated at e0,M26

For the no-ear low-M rows, the one global fan variance budget uses the
safe full footprint span .6931. The ear-low row uses the safe three-arc
span .4568 and one ear variance charge; its negative shifted-ear
coefficient covers all larger ear counts. The high-M row spends no
variance, and its negative shifted-ear coefficient covers arbitrary
ears directly. All required M slope signs are checked.

The minimum final area gap is

    1062118256560764921/31250000000000000000000 > .00003398778.

## 5. Complete reproducible entry and closure

`verify_complete_B33_0p1132.py` runs five fresh subprocesses: the high-M
domain chain (which includes the initial domain and pair), the low-M
unpenalized domain, both final pairs, and the final face chain. It checks
all nested PASS results, exact radius/domain constants, reflection
requirements and support counts. Assertions must remain enabled.

Whole-cover normalization precedes classification. Slight enlargement,
normalization, inward movement from the norm boundary and a generic
perturbation within the strict coverage margin give the inherited
finite-type limit argument. Every final gap is strict, so the closed
endpoint is excluded. Other B counts remain separate obligations.

# A less restricted boundary-potential certificate for all sixteen B32 graphs

Run verify_family.py with assertions enabled. It regenerates the sixteen
B32_P26_F108 graphs, compares each saved graph semantically against that
generated object, checks the catalog hash and graph/certificate byte
bindings, and replays every local support.

At R=.1132 all sixteen pass. The minimum exact area gap is

    102938320914941227681/62500000000000000000000.

This is a finite-family metric statement. A universal B32 theorem at
a chosen radius still requires the separate same-radius reduction
showing that every hypothetical B32 diagram belongs to this family.

## 1. The domain bootstrap is independent of the final coefficients

The helper first reads the unchanged pure coefficient file in
signed_edge_metric_B32_20261004/certificates, checks its SHA identity,
and freshly calls verify_pure_metric.verify on the same graph bytes.
Its radius-independent normalized center cap is at most230, and its
marked-apex potentials are explicitly checked in[-.3,-.2].

The radius field in that earlier coefficient file is historical. No
old-radius area exclusion is used as a new-radius bound: only its
freshly proved radius-independent center support sum and its full-domain
cancellation/potential conditions are used.

Those hypotheses invoke the separately proved uniform B32 window
through .1132, giving every full assigned arc>.08 and every marked
base>.9R. This logical domain restriction is established before using
the new joint dual. Its old area budget is not subtracted again.

The joint coefficients can therefore differ completely from the pure
bootstrap coefficients. They need not satisfy the bootstrap's particular
marked-potential interval; their actual full marked-conjugate inputs
are checked by that separate scalar backend instead.

## 2. Only neighboring boundary differences matter

The radial-corner absorption proof uses telescoping differences of
successive boundary weights, and requires |w_i-w_(i+1)|<=1/40.
It does not require |w_i|<=.0125. The new coefficients use the actual
difference constraints, together with complete per-face localization
and marked-conjugate guards.

All134 q0 supports,32 marked asymmetric-base supports and32 arc supports
are recomputed. Opposite metric terms cancel on every actual shared
edge. The scalar arc sum multiplier compensates sum(half-arcs)=pi.
No center is moved and no new reflection hypothesis is used.

The numerical proposer fixed the mean boundary weight to zero as a
gauge only; acceptance does not need that gauge. A common shift of all
vertex potentials, with corresponding face/arc multiplier shifts, leaves
the exact assembled area bound unchanged. The diagnostic gauge replay
also checks this invariance independently of the proof.

## 3. Scope and provenance

All accepted coefficients are rational integers of denominator10^12.
The bounded two-process numerical proposal batch is not part of the
acceptance replay. Every graph, pure bootstrap and new coefficient row
is checked afresh. Saved JSON PASS status is never treated as evidence.

This is separate from the earlier .1132 joint family and every published
global checkpoint. Its increased margin comes from more flexible vertex,
shared-edge and cyclic boundary weights, not a change to the geometry.

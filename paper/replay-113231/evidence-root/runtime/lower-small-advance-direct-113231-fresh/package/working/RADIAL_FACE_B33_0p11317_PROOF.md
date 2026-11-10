# B33 exclusion at .11317 with a weighted core-curvature flag

This extends the complete full-face/radial argument in
RADIAL_FACE_B33_0p11316_PROOF.md. All continuous face, marked-conjugate,
terminal-credit, and angle-incidence formulas there are retained. New
radius-dependent quantities and the strengthened curvature flag are
checked independently; no old-radius interval is silently reused.

Set R=11317/100000 and B=33. The theorem here excludes only B33.
The fresh original all-count bridge now leaves B31 through38, so in
particular a universal .11317 theorem would need a new B31 exclusion.

## Independent arc-only bootstrap

`lower_bounds_extension_20261004/verify_B33_arc_bootstrap_0p11317.py`
replays the unpenalized full-face center cap229.203 at the new radius,
allows arbitrary ears, and checks the four-arc bad-face exclusion with
span .4568 and the five-arc marked-incidence bound. The one-arc concavity
test gives

    full arc > .088,   sin(half arc)/R > .3886,

with strict area contradiction margin greater than1/30000. The bootstrap
does not assert marked-apex acuteness, which the direct two-branch
conjugate does not require. The fresh all-count list is[31,...,38].

## New corrected radial pair

`verify_radial_corrected_support_0p11317.py` proves on the complete
sine domain[.3886,1]

    outer + .065 sum(marked base length)^2 <= Q -1.25 V,
    Q=33*(10173/10^6)+2pi*(-8987839/10^9).

The cone factor is175821/50000. The exact pair replay has1067 visited
boxes. Its Q upper endpoint is
279236742051904332658819/10^24. The same proved weak neighbor-product
guard and positive radial residual correction are used.

## Two units of compulsory unmarked curvature

ONE_POSITIVE_CURVATURE_ISOPERIMETRY.md proves that a triangulated disk
whose total positive strict-interior curvature is at most1 has
F<=b^2/5. The proof is the earlier boundary-peeling induction with
stripped frontier U<=b-5, including chord and small-boundary cases.

Applied to all face-bearing induced-core blocks, it implies that for
B33 and M=U-2e<=23,

    sum_(unmarked interior vertices) max(6-d,0) >=2,

because 132-M<=M^2/5 fails even at M23. This permits a weighted flag
-f*max(6-d,0) on each unmarked vertex and a final deduction2f. It does
not assume two distinct degree-five vertices. The older one-low-vertex
flag remains valid for M24/25. The old total loss<1 and core cut are
freshly rechecked, giving M>=22.

## Five complete affine branches

The exact conjugate is the two concave endpoint branches of
QUADRATIC_MARKED_CONJUGATE.md, valid globally for0<=lambda<=1/8. Here
lambda=.065. This checkpoint has five rational rows and
checks all ten unordered label triples in each, for50 face supports.
It checks1935 unrestricted vertex types in total.

The no-ear variance charge uses full footprint span L4=.69285. In the
ear branch use just one ear and span L3=.4568. Both sine-domain guards
are checked at R. These two uses of the one variance budget remain
separate. Every e>=1 row has a strictly negative shifted-ear coefficient
E+2c_U, so e1 dominates every larger ear count.

The five ranges and endpoints are:

* e0,22<=M<=23: weighted curvature flag2, endpoint U22;
* e0,24<=M<=25: one-low-vertex flag, endpoint U24;
* e0,M>=26: no flag, endpoint U26;
* e>=1,22<=M<=25: one-low-vertex flag, endpoint e1,U24;
* e>=1,M>=26: no flag, endpoint e1,U28.

Each M slope is negative. The exact verifier checks all five final
area bounds, every local support, and all sign and count conditions.
Its least strict area gap is

    374676556409929231141 / 10^24 > .0003746765564,

in the no-ear M>=26 range. The low M22/23 range has gap>.00167015.

## Replay and scope

The entries are the independent arc-bootstrap script, the corrected
radial script, and `verify_radial_face_B33_0p11317.py`. The latter calls
both core-obstruction checkers, the direct conjugate implementation,
and the integer multiple-fan lemma. It preserves the full-face and
interface proofs from the .11316 component. The generic limiting
argument is unchanged; all final inequalities are strict.

The .11316 checkpoint files remain unchanged. This B33 result alone
does not exclude the additional B31 case or the other boundary counts
at .11317, and it does not determine the exact minimum.

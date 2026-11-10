# Failed and conditional routes: what not to repeat

The accepted universal result is .11323 < r_D(100) <= .1154469548855829.
Only working/verify_all_11323.py composes this complete target-radius chain.
A negative final margin means a particular valid bound is insufficient;
it need not be a mathematical error. A local/case-specific PASS cannot
replace a missing universal geometric premise.

## 1. B32: the inherited one-low scalar residual is negative

At R=.11323 the old high-M four-label row has a raw M26/e0/b0 area gap
about -.003847176. One positive-curvature unit still leaves

    -227296368701491309709/500000000000000000000000
      approximately -.000454593.

The row cannot by itself force original minimum degree six. Its valid
reduced costs leave one unmarked degree-five, one compensating degree-seven,
all others degree six, with M26/e0/b0. Unmarked does not imply no original
boundary-site neighbor.

The [catalog-free high-M proof](lower_staging/B32_HIGHM_CATALOG_FREE_COMPLETE_0p11323.md)
retains the negative diagnostic and splits on that neighbor question. A
coherent five-star support closes the interior-neighbor case. Otherwise
blockwise isoperimetry gives one simple chordless P26/F108 core, and four
metric supports cover deep excess h=0 and h=1. The ring centered correction
is -(32+h)LR*pi/3. Dropping h=1 or retaining the h=0 correction misses a
surviving profile.

See the [checker](lower_staging/verify_B32_highM_complete_0p11323.py),
[exact result](lower_staging/B32_highM_complete_0p11323_result.json) and
[independent audit](working/independent_global_0p11323_20261005/B32_HIGHM_CATALOG_FREE_INDEPENDENT_AUDIT_0p11323_20261005.md).
This is a failed direct target row replaced by a complete coherent closure,
not an analytic error in the inherited row.

## 2. B34: the old short-arc bootstrap does not transfer to .11323

The [historical raw-deficit argument](working/B34_EXACT_LENS_RAW_DEFICIT_BOOTSTRAP.md)
is conditional at R=.11322. Its cutoff requires an independent raw-surplus
bound before hinge/variance spending. It is insufficient at R=.11323 and
is not a premise of the final branch. A radius change does not preserve
that budget.

The [replacement proof](lower_staging/B34_0p11323/PROOF_B34_11323.md) uses
fresh M>=22 and q<=4 geometry, a normalized k=.5 envelope, one
owner-multiplicity-two hinge allocation and three complete M ranges.
Arbitrary ears, bad q1 and BBB q0 remain allowed. The
[independent audit](lower_staging/B34_0p11323/B34_HINGE_COMPLETE_INDEPENDENT_AUDIT_0p11323_20261005.md)
checks the single bank rather than adding the old bootstrap to the new rows.

## 3. B35: the ordinary M26 direct row fails

The ordinary M26 row at R=.11323 has a negative area margin about
-.00043648643. The [v2 checker](working/lower_staging/B35_0p11323/check_B35_complete_0p11323_v2.py)
reports FAIL, diagnostic only; that row is never a direct exclusion.
Positive paid reductions leave M26/e=b=0 and original minimum degree six.

The core is a simple P26/F102 disk. Removing two degree-two core boundary
sites contradicts /6 isoperimetry, so at most one exists. The new coherent
row pays this exceptional local type; assuming none would be unjustified.
The [v2 proof](working/lower_staging/B35_0p11323/B35_COMPLETE_0p11323_PROOF_v2.md)
and [independent audit](working/lower_staging/B35_0p11323/B35_PARENT_INDEPENDENT_AUDIT_0p11323.md)
check 80 face and 2382 vertex inequalities. Use v2 in compositions;
earlier entries and reports are historical.

## 4. Higher-radius branch certificates remain scoped

- [Sixteen B32 families at .11325](working/B32_TURN_FAMILY_0p11325_PROOF.md)
  are regenerated and exactly excluded. This does not prove every .11325
  hypothetical cover belongs to those sixteen families
- [The .11329 four-face B32 metric](working/B32_FOUR_FACE_METRIC_0p11329.md)
  excludes the stated all-six simple chordless P26/F108 core/annulus. Its
  [result](working/B32_four_face_metric_0p11329_result.json) does not claim a
  universal .11329 theorem
- [Higher B33 halfside hinges](working/HIGHER_HALFSIDE_HINGES_B33_0p11324.md)
  retain their own radius-dependent prerequisites and scope
- Files labelled NUMERICAL, such as
  [the B35 .11325 proposal](working/B35_exact_lens_0p11325_NUMERICAL_proposals.json),
  are proposals rather than exact acceptance evidence

Stronger conditional radii cannot be promoted without complete same-radius
domains, topology and every other boundary-count branch.

## 5. The Q3 402-graph route still had geometric premises

The [premise document](working/metric_q3_corner_diagnostics_20261004/PROOF_CONDITIONAL.md)
and [compact 402-case result](working/metric_q3_corner_diagnostics_20261004/fresh_all_family_result.json)
record exact graph exclusions at .11321 conditional on actual normalized
half-arc sine >3/5, marked bases >9R/10, reference edges >3R/5 with the
stated orientation constant, neighbor-weight absorption and the unequal-base
25/16 cap. Catalog completeness does not establish those actual-diagram
premises.

A [representative certificate](working/metric_q3_corner_diagnostics_20261004/flat_N26_000_q3_corner_00.conditional_certificate.json),
[its result](working/metric_q3_corner_diagnostics_20261004/flat_N26_000_q3_corner_00.conditional_result.json)
and [checker](working/metric_q3_corner_diagnostics_20261004/verify_conditional.py)
are retained. The repetitive 28 MB batch is omitted. This route is not a
dependency of the final B33 .11323 chain.

## 6. Actual signed A fee and independent J fee differ

The [accepted-local package](../conditional_local_lemmas/README.md)
preserves two distinct results at R=.11321, lambda=7/50 and
t=1071883/20000000:

- The actual signed-anchor three-triangle A score has a certified .025 fee,
  including negative anchors and zero-area closure
- An explicit 37-site local diagram has 33 connected covered assigned
  unit-circle arcs, canonical switches and the stated q3 star. Its
  independent cap-anchor J loss is about .018317365588123673, below .019931551

The J example certifies unit-circle coverage and those local premises only.
It does not certify the whole closed unit disk, a 100-site covering diagram,
unknown outer Q or the complete global profile. It is not a full 100-disk
counterexample.

The [actual local proof](../conditional_local_lemmas/research/q3_actual_quadratic_support/PROOF.md),
[explicit J proof](../conditional_local_lemmas/research/q3_unequal_explicit_family/PROOF.md)
and [budget interface](../conditional_local_lemmas/research/q3_actual_quadratic_support/ROOT_QUADRATIC_BUDGET_INTERFACE.md)
retain their exact scopes. A signed local fee cannot be silently subtracted
from an independently J-majorized completed row. The interface retains
Q_actual, shoelace equality, eligible disjoint face/anchor allowances, ears,
interface/centered credits and variance once. Whole-cover composition was
external to that local package; the final .11323 theorem does not promote it.

## 7. The archived conjugate proof had a factor-two analytic error

The [archived status](../conditional_local_lemmas/research/quadratic_lambda14_conjugate/history_factor2_correction/STATUS.json)
identifies the superseded proof: its second-derivative sin(2a) coefficient
must be -4 rather than -8. The corrected safe guard is
-2sqrt(3)+4lambda<0. Roots/values did not change; unchanged certificate
numbers did not validate the old analytic source.

Only the [corrected current proof](../conditional_local_lemmas/research/quadratic_lambda14_conjugate/PROOF.md)
and source, with fresh replay/independent review, are accepted. Both versions
remain so the incorrect guard is not reintroduced.

## 8. Failed exact attempts and reporting corrections are separate

The J example's [first attempt](../conditional_local_lemmas/research/q3_unequal_explicit_family/first_exact_attempt/STATUS.json)
failed because a Fraction lacked its interval wrapper before sqrt. The
[second attempt](../conditional_local_lemmas/research/q3_unequal_explicit_family/second_exact_attempt/STATUS.json)
passed geometric/score guards but failed its final source guard by calling
read_bytes on a string. Neither produced an accepted completed certificate.
The final accepted source/receipts and the historical pre-footprint-guard
success remain separately preserved.

The [metadata correction note](working/METADATA_CORRECTIONS.md) concerns
large integer tokens rounded in auxiliary JSON by a JavaScript round trip.
Exact Python sidecars correct the reporting. No mathematical input,
acceptance verifier or proved sign changed. Saved PASS JSON never replaces
fresh exact replay.

## 9. Common scope and accounting traps

- Normalize all centers before the common diagram/count classification;
  coverage preservation does not preserve old ownership, m, graph or B
- Recompute radius-dependent norm caps and supports at the target radius
- A bootstrap can establish a domain for a fresh functional, but its old
  hinge/variance gain cannot then be added as a second spend
- Cancel signed half-edge terms only across the same actual edge in
  compatible supports; retain residual potentials, outside allowances and
  interface credits
- Keep full-simplex degeneracies and zero-circumradius endpoints. Numerical
  optimizers do not justify assuming actual triangles acute, equilateral,
  equal-radius or saturated
- Endpoint strictness uses enlarged-radius normalization, perturbation within
  strict coverage, finite-type limits, uniform positive gaps and attainment;
  same-radius arbitrary perturbation is not asserted

See the [universal proof](working/PROOF_11323.md) and
[independent composition audit](working/GLOBAL_11323_INDEPENDENT_COMPOSITION_AUDIT.md).

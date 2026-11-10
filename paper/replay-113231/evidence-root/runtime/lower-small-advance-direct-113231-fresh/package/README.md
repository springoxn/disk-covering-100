# 100 congruent disks covering the closed unit disk

## Certified interval

Let r_D(100) be the smallest radius of 100 congruent closed disks, with
arbitrary centers, whose union covers the closed unit disk. This release proves

    0.11323 < r_D(100) <= 0.1154469548855829

The lower endpoint is exactly 11323/100000. The upper endpoint is exactly
1154469548855829/10000000000000000. The unresolved absolute gap is

    0.0022169548855829 = 22169548855829/10000000000000000.

The endpoints do not match. No exact optimum, optimal polynomial, unique
optimal configuration or complete solution of the original problem is claimed.

## Reproduce the accepted certificates

From this directory, with standard Python and assertions enabled:

    python3 -B -S verify_package.py
    python3 -B -S run_certificates.py

The first command checks the release hashes. The second checks those
hashes, runs the universal lower certificate in fresh component processes,
and verifies the exact 100-center upper construction. It prints the complete
recomputed JSON results. No network, optimizer or external Python package is
needed, and saved PASS reports are not acceptance evidence. Python -O is
rejected. The long step is the exhaustive 3,371,339-box capped-pair tail;
the original complete lower replay took about 3.6 minutes.

Direct mathematical commands are:

    python3 -B -S working/verify_all_11323.py
    python3 -B -S working/upper_configuration/verify_cover.py working/upper_configuration/centers.csv 0.1154469548855829

The CSV gives 100 distinct exact finite-decimal rational centers. Upper
acceptance uses exact integer/surd predicates on all finite critical
candidates. Floats only choose witnesses and report approximations; exact
fallbacks check other disks when necessary.

## Proof and independent evidence

Start with the [universal proof](working/PROOF_11323.md), then the
[independent composition audit](working/GLOBAL_11323_INDEPENDENT_COMPOSITION_AUDIT.md)
and [source-bound receipt](working/GLOBAL_11323_INDEPENDENT_COMPOSITION_RECEIPT.json).
The [fresh original full replay](working/integrated_11323_fresh_result.json)
records all six complete branches. Saved receipts do not replace source replay.

The same-diagram surviving boundary counts B=31,...,39 are exhausted by:

- B31: [global curvature rows](working/B31_GLOBAL_LOW_DEGREE_0p11323.md)
  and [independent audit](working/independent_global_0p11323_20261005/B31_INDEPENDENT_AUDIT_0p11323_20261005.md)
- B32: [canonical v2 composition](lower_staging/B32_COMPLETE_0p11323_V2_PROOF.md),
  [low-M coherent closure](lower_staging/B32_M25_DIRECT_INTERFACE_0p11323_PROOF.md),
  [catalog-free high-M closure](lower_staging/B32_HIGHM_CATALOG_FREE_COMPLETE_0p11323.md),
  and independent [low-M](working/independent_global_0p11323_20261005/B32_M25_INDEPENDENT_AUDIT_0p11323_20261005.md)
  / [high-M](working/independent_global_0p11323_20261005/B32_HIGHM_CATALOG_FREE_INDEPENDENT_AUDIT_0p11323_20261005.md) audits
- B33: [coherent hinge/metric composition](working/B33_HINGE_METRIC_COMPLETE_0p11323.md)
  and [independent audit](working/B33_HINGE_METRIC_COMPLETE_INDEPENDENT_AUDIT_0p11323_20261005.md)
- B34: [one-bank hinge proof](lower_staging/B34_0p11323/PROOF_B34_11323.md)
  and [independent audit](lower_staging/B34_0p11323/B34_HINGE_COMPLETE_INDEPENDENT_AUDIT_0p11323_20261005.md)
- B35: [canonical v2 one-core-ear proof](working/lower_staging/B35_0p11323/B35_COMPLETE_0p11323_PROOF_v2.md)
  and [independent audit](working/lower_staging/B35_0p11323/B35_PARENT_INDEPENDENT_AUDIT_0p11323.md)
- All B>=36: [unrestricted capped-pair tail](working/CAPPED_PAIR_B36PLUS_0p11323_PROOF.md)
  and [independent audit](working/CAPPED_PAIR_B36PLUS_0p11323_INDEPENDENT_AUDIT.md)

Normalize every center at the same radius before constructing and classifying
the new common diagram. No old graph, ownership or boundary count is assumed
to survive normalization. The proofs explain topology, continuous geometry,
enlarged-radius limits and attainment; programs verify finite exact
inequalities. These are executable certificates, not proof-assistant proofs.

## Historical and conditional material

The established [.11322 fallback proof](working/PROOF_11322.md) and
[independent audit](working/INDEPENDENT_AUDIT_11322_20261005.md) remain available
as history. The final acceptance entry is working/verify_all_11323.py, using
B32 v2 and B35 v2. Earlier sources keep their original radii and scopes.

Read [FAILED_AND_CONDITIONAL_ROUTES.md](FAILED_AND_CONDITIONAL_ROUTES.md)
before extending a scalar row, borrowing a local fee or promoting a catalog
result. It separates insufficient rows, scoped exact results, implementation
failures, analytic corrections and reporting-only corrections. The local J
obstruction is a unit-circle/local diagram, not a full 100-disk counterexample.

## Layout and curation

- working/ and sibling lower_staging/ preserve the tested relative paths;
  working/lower_staging/B35_0p11323/ is a distinct nested directory
- SOURCE_MANIFEST.json lists original copied files and SHA-256 hashes
- MANIFEST_SHA256.json binds the complete payload except itself
- PORTABLE_REPLAY_RECEIPT.json records independently relocated validation
- Unique originals and compact local history retain the factor-two correction
  and failed exact attempts
- Caches, empty pending reports, search checkpoints, redundant old replay
  output and the 28 MB Q3 batch are omitted; a representative conditional
  case and premise summary remain

No original workspace file or earlier published archive was deleted or
rewritten. Historical documents can cite omitted external/contextual paths;
those are not final acceptance dependencies and do not authorize carrying
constants or scope into a different radius.

## Public-copy scope

Private migration, browser and launcher history are omitted. The selected
scoped local lemmas and corrected failed routes are in the sibling
conditional_local_lemmas directory. This copy changes documentation and
publication manifests only; acceptance sources and inputs remain unchanged.
No new mathematical replay occurred during public copying. The retained
portable receipts describe earlier complete source-bound runs.

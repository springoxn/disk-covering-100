# Conventions for the bilingual n=100 monograph

This file is the written contract for the English source set and its Chinese edition.
It exists so that a later revision cannot silently drift.

## 1. File set

| Role | English | Chinese |
|---|---|---|
| main file | `monograph.tex` | `monograph_zh.tex` |
| preface / summary | `sections/m0_preface.tex` | `sections/m0_preface_zh.tex` |
| Part I problem and evidence discipline | `sections/m1_problem.tex` | `sections/m1_problem_zh.tex` |
| Part II upper bounds | `sections/m2_upper.tex` | `sections/m2_upper_zh.tex` |
| Part III universal analytic lower bounds | `sections/m3_universal.tex` | `sections/m3_universal_zh.tex` |
| Part IV the six-branch engine | `sections/m4_sixbranch.tex` | `sections/m4_sixbranch_zh.tex` |
| Part V the current frontier | `sections/m5_frontier.tex` | `sections/m5_frontier_zh.tex` |
| Part VI route catalogue | `sections/m6_catalogue.tex` | `sections/m6_catalogue_zh.tex` |
| Part VII reproduction and dependencies | `sections/m7_reproduce.tex` | `sections/m7_reproduce_zh.tex` |
| Part VIII open obligations | `sections/m8_open.tex` | `sections/m8_open_zh.tex` |
| Appendix evidence ledger | `sections/m9_appendix.tex` | `sections/m9_appendix_zh.tex` |

The `\input` sequence and the section names are identical in both editions, so section,
equation, table and theorem numbering agree.

## 2. What is never translated or altered

- Rational numbers, decimals, counts, box counts, margins, hashes, radii, and constants.
- Paths such as `verify/out/n100-candidate-complete-225.json`.
- Mathematical notation, `\label`/`\ref`/`\cite` keys, environment structure, table layout.
- Field names of JSON certificates (`status`, `scope`, `machine_verified_geometry`, ...).
- The words `PASS`, `FAIL`, `PASS_PREMISES`, `NOT_CLOSED`, `UNDECIDED`, `EXCLUDED`.
- The file names `lattice97_upperbound_n100.py` and similar identifiers.

## 3. Terminology (first occurrence only: 中文（English）)

| English | Chinese |
|---|---|
| covering radius | 覆盖半径 |
| certificate | 证书 |
| rational interval arithmetic | 有理区间算术 |
| outward rounding | 向外舍入 |
| branch | 分支 |
| boundary cell / boundary arc | 边界胞 / 边界弧 |
| ear | 耳 |
| bad face | 坏面 |
| core | 核心 |
| isoperimetry | 等周 |
| hinge budget | 铰链预算 |
| variance budget | 方差预算 |
| capped-pair relaxation | capped-pair 松弛 |
| intercept / slope / penalty coefficient | 截距 / 斜率 / 罚系数 |
| obstruction point | 障碍点 |
| monotonicity inheritance | 单调性继承 |
| proof interface | 证明接口 |
| precondition | 前提 |
| diagnostic | 诊断 |
| discovery layer | 发现层 |
| certificate chain | 证书链 |

Symbolic names (branch names `B31`, `M24`, `DDD`, `DRR`, `BRR`, `q1`, `e0`, `b0`), JSON keys,
script names and the terms `capped-pair`, `Krawczyk`, `Hall`, `Voronoi`, `Dart map` stay in Latin
script: they are symbols, not descriptions.

## 4. Evidence vocabulary

Every claim carries one of the following, matching `docs/EVIDENCE_LEDGER.md`:

- **A** structured machine artifact (JSON certificate with status, counts, hashes, exit code);
- **B** independent replay (a second script or a second stage rechecking the same sub-assertion);
- **C** discovery material (floating-point search, candidate ranking, failed experiment) — never a decision;
- **D** inheritance reasoning (e.g. exclusion at a larger radius inherited to a smaller one),
  which must be recorded explicitly by the combiner.

Additional state words used throughout:

- `analytic`: proved in prose by a human-checkable argument, not by a proof-assistant kernel;
- `machine_verified_geometry = false`: the finite arithmetic is machine-checked, the geometric
  reduction to it is not;
- `diagnostic`: a computation that records a failure or a bottleneck and is explicitly *not* a
  certificate of closure.

## 5. Chinese typography

Full-width punctuation, 「」 for quotes. Bold math italic (`cmmib8`) and some 8pt sizes are absent
from the offline Tectonic bundle; the Chinese edition therefore uses `\mathbf` for Latin vectors
and plain italic Greek letters, and this compromise is recorded in the main file. It is
intentional, not a bug.

## 6. Shared typography, and the calibration to the reference manuscript

Both editions use identical page geometry and line-breaking parameters, so a rendered page of one
can be compared with the corresponding page of the other. The settings below were calibrated
against the reference manuscript `AImath/paper/completion/main.tex` (compiled with tectonic);
a change to any of them invalidates that calibration and must be re-measured.

| Setting | Value | Why |
|---|---|---|
| body size | `11pt` (renders 10.9pt) | matches the reference's measured 10.9pt body |
| fonts | Computer Modern / Latin Modern | same family as the reference |
| margins | `left=72pt, right=72pt` | 1in; keeps every edge inside the box `artifact_qc.py` measures |
| `textheight` | `648pt` | reference-like page fill |
| `microtype` | protrusion **only** | reference relies on protrusion; tectonic is XeTeX, which microtype refuses for font expansion |
| `\tolerance` | `9999` | at 3000 TeX gave up and emitted very loose lines; 9999 lets it pick the least-bad break |
| `\emergencystretch` | `3em` | absorbs the residual loose lines that tolerance alone cannot |
| `\hbadness` | `2500` | stops reporting lines that are only slightly loose |

Notes that must not be "fixed" later:

- **`article`, not `amsart`.** The reference is `amsart`, whose layout yields a 547pt measure. That
  measure does not fit inside a 1in margin on letter paper, and indeed the reference's own text
  reaches 5pt *past* its nominal margin. This document keeps a ~475pt measure so that all content
  stays inside the measured box. The visible difference is line count, not type size.
- **No font expansion.** `\microtypesetup{expansion=true}` is a build error under XeTeX.
- **A residual `Overfull \hbox` in `monograph.toc` is not a defect.** The TOC leader glue is set to
  the full measure, so LaTeX reports a few points of overfull while every visible glyph ends
  ~30pt short of the margin (verified at 510.2–510.3pt against a 540pt edge). The same applies to
  the remaining sub-2pt table-cell warnings in `m5_frontier`: the worst *visible* right-edge excess
  anywhere in the document is ~4.3pt, all of it microtype protrusion.
- **`artifact_qc.py` allows 6pt of protrusion** (`PROTRUSION_TOL`). That allowance is what makes the
  margin gate meaningful with microtype enabled; it is still far below the 10–21pt that real
  overfull lines produced before this revision.
- **Exact rationals are never abbreviated** to make a line fit. The long in-line `\frac`s in
  `m9_appendix` that force loose lines are content, and stay.


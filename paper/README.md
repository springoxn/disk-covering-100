# n=100 双语研究文档

本目录提供**两套**模块化 LaTeX 源文件与重新编译的 PDF。

## 1. 专著（当前主交付）

系统讲解全部路线、聚焦上下界最新进展的长文，英文与中文各一份：

| 角色 | 英文 | 中文 |
|---|---|---|
| 主文件（只做装配，≤10 KB） | `monograph.tex` | `monograph_zh.tex` |
| 前言/一页现状 | `sections/m0_preface.tex` | `sections/m0_preface_zh.tex` |
| 第 I 部分 问题、约定、证据纪律 | `sections/m1_problem.tex` | `sections/m1_problem_zh.tex` |
| 第 II 部分 上界 | `sections/m2_upper.tex` | `sections/m2_upper_zh.tex` |
| 第 III 部分 普适解析下界 | `sections/m3_universal.tex` | `sections/m3_universal_zh.tex` |
| 第 IV 部分 六分支引擎 | `sections/m4_sixbranch.tex` | `sections/m4_sixbranch_zh.tex` |
| 第 V 部分 当前前沿 | `sections/m5_frontier.tex` | `sections/m5_frontier_zh.tex` |
| 第 VI 部分 路线总目录 | `sections/m6_catalogue.tex` | `sections/m6_catalogue_zh.tex` |
| 第 VII 部分 复现与依赖 | `sections/m7_reproduce.tex` | `sections/m7_reproduce_zh.tex` |
| 第 VIII 部分 未完成义务 | `sections/m8_open.tex` | `sections/m8_open_zh.tex` |
| 附录 证据台账与精确算术 | `sections/m9_appendix.tex` | `sections/m9_appendix_zh.tex` |
| 产物 | `build/monograph.pdf` | `build/monograph_zh.pdf` |

构建（单一入口，先跑结构门禁，再编译，再查产物新鲜度，最后跑四层版本校验）：

```powershell
.\build_monograph.ps1
```

单独调用：

```powershell
python structure_check_monograph.py   # 模块化、\input 目标、脚本不回写源
python edition_check.py               # 四层校验：源级 / 数学段 / 成品 / 目视普查
python artifact_qc.py                 # 成品页边距检查（含中文标点悬挂的显式豁免）
python normalize_sources.py           # 对英中两侧施加同一组机械规范化（幂等）
```

`edition_check.py` 的退出码：`0` 全通过 / `1` 有检查失败 / `2` 检查器本身无法运行。
`artifact_qc.py` 同理。中文版使用 `ctexart`；离线 Tectonic bundle 缺粗体数学斜体 `cmmib8`
与部分 8pt 字号，故中文版拉丁向量用 `\mathbf`、希腊向量用普通斜体希腊字母，此取舍写在
`monograph_zh.tex` 的注释与 `CONVENTIONS.md` 第 5 节。

翻译与改版约定见 `CONVENTIONS.md`：数字、路径、`\texttt` 载荷、`\label`/`\ref` 键、
环境结构与 JSON 字段名一律不译；中文只在散文层替换。

## 2. 短文（第一版，保留）

- `paper.tex` + `sections/{background,upper_bound,lower_bound,routes,reproducibility,ledger}.tex`：英文短文；
- `paper_zh.tex` + 对应 `*_zh.tex`：中文短文；
- `build.ps1`：其构建入口；`structure_check.py`：其结构检查；
- `build/paper.pdf`、`build/paper_zh.pdf`：其产物。

该短文只覆盖六个小节，属于专著的早期版本，保留以备追溯，不再作为主交付。

## 3. 证据边界

论文明确区分：构型上界、六分支下界、半径单调继承、局部诊断、未决障碍和失败路线。
所有定量结论应回查仓库根目录的 `docs/EVIDENCE_LEDGER.md` 及 `verify/out/` 证书。
专著附录 A.6 另记录了撰写本文档时实际执行的审计项（包括产物覆盖率与绑定一致性检查）。

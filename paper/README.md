# n=100 研究专著（英文版）

> 重放状态更正：`0.113235` 未成功完成重放，暂不作为已验证下界。原专著与短文保留历史章节；两份重新编译的 PDF 首页均附状态更正。成功的 `0.113231` 同半径算术重放、独立论文与证据包见 [replay-113231](replay-113231/README.md)。下文的“主交付”布局指历史专著结构，不代表确认其旧接受值。

本目录提供一套模块化 LaTeX 源文件与其重新编译的 PDF。中文版已撤除：两版并行时的那套
逐段对齐门（数字多重集、标签、行内/行间公式比对）只对"两套源保持一致"这件事有意义，
只剩一套源之后它只会让构建链长期红着，因此连同中文源、中文 PDF 与 `edition_check.py`、
`normalize_sources.py`、`CONVENTIONS.md` 一并删除。

## 专著（主交付）

| 角色 | 文件 |
|---|---|
| 主文件（只做装配，≤10 KB） | `monograph.tex` |
| 前言/一页现状 | `sections/m0_preface.tex` |
| 第 I 部分 问题、约定、证据纪律 | `sections/m1_problem.tex` |
| 第 II 部分 上界 | `sections/m2_upper.tex` |
| 第 III 部分 普适解析下界 | `sections/m3_universal.tex` |
| 第 IV 部分 六分支引擎 | `sections/m4_sixbranch.tex` |
| 第 V 部分 当前前沿 | `sections/m5_frontier.tex` |
| 第 VI 部分 路线总目录 | `sections/m6_catalogue.tex` |
| 第 VII 部分 复现与依赖 | `sections/m7_reproduce.tex` |
| 第 VIII 部分 未完成义务 | `sections/m8_open.tex` |
| 附录 证据台账与精确算术 | `sections/m9_appendix.tex` |
| 参考文献 | `sections/m10_references.tex` |
| 产物 | `build/monograph.pdf` |

构建（单一入口：先跑结构门禁，再编译，再查产物新鲜度，最后跑页边距检查）：

```powershell
.\build_monograph.ps1
```

单独调用：

```powershell
python structure_check_monograph.py   # 模块化、\input 目标存在、无孤立段、脚本不回写源
python artifact_qc.py                 # 成品页边距检查
```

`artifact_qc.py` 的退出码：`0` 全通过 / `1` 有检查失败 / `2` 检查器本身无法运行。

## 短文（第一版，保留）

- `paper.tex` + `sections/{background,upper_bound,lower_bound,routes,reproducibility,ledger}.tex`；
- `build.ps1` 是其构建入口；`structure_check.py` 是其结构检查；
- `build/paper.pdf` 是其产物。

该短文只覆盖六个小节，属于专著的早期版本，保留以备追溯，不再作为主交付。

## 历史重放论文（R=0.113231）

`replay-113231/` 保存该半径的六分支完整算术重放论文、PDF、转换后源码快照及审计脚本。仓库还记录了更高的 `r_D(100)>0.113235` 主张，但该半径没有成功完成重放；此处不把它列为已验证结论。`0.113231` 的材料单独绑定其成功重放证据。

## 证据边界

论文明确区分：构型上界、六分支下界、半径单调继承、局部诊断、未决障碍和失败路线。
所有定量结论应回查仓库根目录的 `docs/EVIDENCE_LEDGER.md` 及 `verify/out/` 证书。
专著附录 A.6 另记录了撰写本文档时实际执行的审计项（包括产物覆盖率与绑定一致性检查）。

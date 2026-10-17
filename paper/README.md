# n=100 双语研究综述

本目录提供模块化LaTeX源文件与重新编译的PDF：

- `paper.tex` + `sections/*.tex`：英文版；
- `paper_zh.tex` + `sections/*_zh.tex`：中文版；
- `build.ps1`：单一构建入口；
- `structure_check.py`：模块结构检查；
- `build/paper.pdf`：英文PDF；
- `build/paper_zh.pdf`：中文版PDF。

构建：

```powershell
python structure_check.py
.\build.ps1
```

构建脚本只生成`build/`派生文件，不回写正文源文件。中文版本使用`ctexart`，首次构建可能下载中文字体和TeX宏包；构建日志保存在`build/*.log`。

论文明确区分：构型上界、六分支下界、半径单调继承、局部诊断、未决障碍和失败路线。所有定量结论应回查仓库根目录的`docs/EVIDENCE_LEDGER.md`及`verify/out/`证书。

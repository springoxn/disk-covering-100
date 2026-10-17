# n=100：约化角能量 Hessian 负见证的独立审计（**受限**审查记录）

本文件是**受限审计**，不是 `r_D(100)` 的最优性/下界证明，不构造可行覆盖反例，
**不**对任何矩阵作惯性计数主张。主证明是父方的两份精确回执；本文只做
(a) CAS 恒等式独立确认、(b) SHA 绑定核对、(c) **中点权重盒**重放、(d) 有限步反例重放。

被审对象（只读，未修改）：

| 回执 | 内容 |
|---|---|
| [n100-angular-energy-negative-witness.json](../verify/out/n100-angular-energy-negative-witness.json) | 精确有理负见证（父方主证明之一） |
| [n100-angular-energy-independent.json](../verify/out/n100-angular-energy-independent.json) | 无 NumPy/无特征求解器的独立**全 q 盒**区间复核（父方主证明之二） |
| [n100-harmonic-energy-relaxation-counterexample.json](../verify/out/n100-harmonic-energy-relaxation-counterexample.json) | 精确有理旋转的有限步能量下降反例 |

审计脚本（**不 import** 上述任何脚本）：
[n100_audit_angular_energy_obstruction.py](../verify/n100_audit_angular_energy_obstruction.py) →
[n100-angular-energy-obstruction-audit.json](../verify/out/n100-angular-energy-obstruction-audit.json)。
**实测 exit 0，约 1.9 s**。接受判定**只用** CAS 符号恒等式与精确有理/区间算术；
无浮点、无特征求解器参与判定。

## 0. 本审计的能力边界（**必须与结论同时引用**）

| 命题 | 谁建立 |
|---|---|
| `H[i][i]+=a, H[i][j]-=a, a=2c_ij⟨q_i,q_j⟩` 是 `E(θ)=Σc_ij|q_i−q_j|²` 的 Hessian | **本审计独立**（SymPy CAS，n=3 全项 + 行和恒零） |
| 各输入/生成器脚本的 SHA256 绑定一致 | **本审计独立** |
| 见证二次型在 **`c_ij` 权重盒**上、**q 取中点** 时严格负 | **本审计独立**（逐对端点，精确有理） |
| 见证二次型在**整个 1e−58 Krawczyk q 盒**上严格负 | **父方** [n100-angular-energy-independent.json](../verify/out/n100-angular-energy-independent.json)（本审计**未**重做，仅引用并核对 SHA） |
| 根在整个 q 盒上严格位于角域内部 | **父方**（同上；本审计只给中点余量） |
| 有限步旋转使能量下降 | 本审计**中点重放**确认 `< 0`；全 q 盒结论归父方 |

## 1. 结论摘要

| 问题 | 结论（含作用域） |
|---|---|
| 父的 Hessian 公式是否正确？ | **正确**，CAS 符号恒等式独立确认：`∂²E/∂t_i∂t_j = −2c_ij cos(t_i−t_j)`（i≠j），`∂²E/∂t_i² = 2Σ_{j≠i}c_ij cos(t_i−t_j)`，行和恒 0。 |
| 见证值是否可精确重现？ | **是**，与存储值（157 位分子 / 分母 10^160）**逐位相等**。 |
| 权重盒内是否严格负（中点 q）？ | **是**，逐对端点得 `[−2.1635817807659617e−05, −2.1635817805632518e−05]`，**上端 < 0**。 |
| 全 q 盒是否严格负？ | **父方回执给出 `interval_quadratic_form` 上端 < −1e−5**；本审计**未重做**，只核对来源 SHA 与 `verified=true`。 |
| 根是否在角域内部？ | 本审计给出**中点**余量 `min⟨q_i,q_j⟩ − (1−2(t_mid−ρ)) = 7.993223069118e−05 > 0`、32 个相邻叉积 > 0；**全盒**结论归父方。 |
| 反例是否可重放？ | **可**：精确有理旋转下中点权重重算 `ΔE = −1.0817322663e−11 < 0`；父方存储上界 `< −1e−12`。 |
| 是否给出惯性计数？ | **否**。 |
| 是否给出 `r_D(100)` 结论？ | **否**。 |

## 2. 勘误：v1 审计的两处错误（已撤回）

v1（备份 `verify/n100_audit_angular_energy_obstruction.py.bak-badgapinertia`、
`verify/out/n100-angular-energy-obstruction-audit.json.bak-badgapinertia`）有两处错误，
父 agent 指出后经 CAS 复核确认**父方正确**：

1. **惯性 `+25/−6` 撤回。** 用 CAS 确认的公式在真实数据上算：32×32 角度坐标 **1 负**（另 1 零 = 整体旋转），
   投影到 31 维 gap 坐标**仍 1 负**（`K` 的列是平移算子的一组基，限制到 31 维子空间不可能增加负方向数）。
   先前的 `−6` 来自我临时脚本里一个**带符号错误的旋转矩阵**加上参量取 `v/2` 后又除以 `h²`，
   把伪力项当成了曲率。**本项目不再作任何惯性主张。**
2. **"父公式有符号错"撤回。** CAS 与有限差分都确认父的构造正确。

另外修正的表述错误：
* v2 曾把"见证在权重盒上负"写成"在根盒上负"——已改为**中点权重盒**，全 q 盒明确标注为父方结论；
* v2 曾写"父方全盒最小化只会加强结论"——方向说反了，全盒最小化**更难**（更严格），已删除；
* v2 曾用"落在存储区间 1e−15 邻域内"作为接受判据——已删除该邻近性判据。

## 3. 机制说明（**不是**证明）

中点 q 下 **256/496** 对满足 `⟨q_i,q_j⟩ < 0`（最负 `cos = −0.999996`），故应力
"Laplacian"的边权 `2c_ij⟨q_i,q_j⟩` 有负值。**负边权只是机制**，不是不定性的证明；
证明是第 1 节的精确见证（中点权重盒）+ 父方的全 q 盒回执。
这也解释了 cover19（12 锚点、近邻对占多数）能用同一模板而 n=100 不能。

## 4. 范围（必须与结论同时引用）

* 本文只审**固定权重应力能量** `E(θ)=ΣC_ij|q_i−q_j|²` 在候选根附近的凸性/局部极小性。
* **不**否证上游 54 维 `ker B` 上的严格局部极小（SOSC）。
* **不**给出 `r_D(100)` 的全局下界或最优性；**不**构造可行覆盖或更小半径配置。
* 组合拓扑的全局穷举（所有接触图）**未完成**，本文不评价。
* 全局力树路线未受影响，本文不评价。

## 5. 复现

```powershell
cd E:\study\ADB
python verify\n100_audit_angular_energy_obstruction.py
# -> verify/out/n100-angular-energy-obstruction-audit.json, exit 0, ~1.9 s
```

脚本断言：各输入 SHA 绑定、CAS 恒等式、中点见证值逐位相等、权重盒上端 < 0、
32 个相邻中点内点判据、反例重放 `< 0`、来源回执 `verified=true`。任一失败即非零退出。

# n=100：KKT distance multipliers → 正权图应力 / Dirichlet 能量全局凸性证书的迁移分析（STATUS）

本文件是一份 **STATUS 记录**，不是全局结论，也不是 `r_D(100)` 的全局最优/下界证明。
机器可执行检查：[analysis.py](../runtime/n100-vonequinox-transfer/analysis.py) →
[result.json](../runtime/n100-vonequinox-transfer/result.json)（实际 exit 0，`elapsed_seconds = 68.74`，全部接受判定为整数/有理/exact boolean）。
独立复核证书：[certificate.json](../runtime/n100-vonequinox-transfer/certificate.json) →
[verify_certificate.py](../runtime/n100-vonequinox-transfer/verify_certificate.py)
（实际 exit 0，0.7 s，8/8 tamper 负测试拒绝；无需重做 214 维求解，
由存储的 `c0/Γ/b_ij/hop/bk` 精确重建 `H0`，并精确复算 `vᵀH0v < 0`）。
复核回执：本项目 `verify/out/n100-vonequinox-transfer-certificate-check.json`；
父 agent 的独立复核 `verify/out/n100-vonequinox-stress-independent-parent.json`（scope：不重做 Kron）。

**最终 SHA256 绑定**（前 32 位便于核对，全量见各回执）：
`analysis.py = 6c58ad6d450d7696063c6b8acaef8c26…`（与 `result.json` 的 `checker.sha256`、与
`certificate.json` 的 `generator_sha256` 一致）；`certificate.json = 30bbc779b2c44aab6513a8c4a2dd145a…`；
`verify_certificate.py = a82f22eebbac3ac0a1f6cd3c979e5880…`；`result.json = cf8763df4bb1f8f2d16770ccb82731e8…`。

## 0. 归属（不得混淆）

| 对象 | 归属 | 本文件如何使用 |
|---|---|---|
| 100 圆精确 KKT 根、932 变量多项式系统、54 维切空间 SOSC、全闭盘覆盖 | **`cjt42554-crypto/disk100-covering-certificates`，固定提交 `67ebf1c5776f72a7b7786a8655eed5463429ae55`**（LF 原字节导出 `runtime/disk100-release-lf-67ebf1c/`，独立副本 fresh 重放 `runtime/external-disk100-strict-local-replay/`） | 作为**唯一输入事实源**，只读，未修改 |
| cover19 primary（42 杆正应力 + 星—网消元 + 有理 Dirichlet 能量凸性）、cover20（force 证书 + 定量锚点隔离） | **VonEquinox/DiskCoveringSolve**（`runtime/VonEquinox-DiskCoveringSolve-0895849`，只含 cover11..cover20 与 theory，**没有 n=100 主张**） | 仅作为**方法模板** |

其余归属与边界见 [result-vonequinox-n100-absorption.md](result-vonequinox-n100-absorption.md)、
[vonequinox-theory-audit.json](../runtime/vonequinox-theory-audit.json)。

输入绑定（脚本内 assert，全部通过）：`SOURCE_BINDING.json` 的上游 manifest SHA
`4bc4d4647c5b5e8e6e7bb01d1ce10f50fae1823139ce0333efffa15f329472e2` 与 8 个拷贝文件 SHA；
`source/krawczyk_verification.json` 的 `verified=true`、`midpoint_denominator=10^60`、`box_radius=[1,10^58]`；
本项目 fresh 记录 `verify/out/external-disk100-strict-local-67ebf1c.json`。
检查脚本自身 SHA256 记在 `result.json` 的 `checker.sha256`。

## 1. 结构不变量（exact）

* `932 = 493 + 439`；`493 = 200`（100 圆心）+ `228`（114 内部孔）+ `64`（32 边界孔）+ `1`（t=492）。
* 约束 `439 = 406` distance（`3×114` 三角 + `2×32` 边界对）+ `32` unit（`|q_k|²=1`，边界孔在单位圆上）+ `1` gauge（`c_74.y`）。
* 单项式总数 **8348**，每行次数 ≤ 2；行分组签名：`f` 行只含几何二次项（`C/HI/HB/t`），`∇L` 行是 `α×几何` 双线性（另有 t 行的一个常数项 1 与 407 个线性 `α` 项）。
* **重放检验**：由 `constraint_metadata + source_configuration` 重新生成全部 932 个多项式，与
  `polynomial_system.json` 存盘内容**逐项相等**（`claims.polynomial_system_regenerates_exactly = true`）。
  这同时把乘子布局钉死：约束 `j` 的乘子位于变量 `493+j`，行 `439..931` 即 `∇L`。

## 2. 乘子分支（dyadic 区间，ρ = 10⁻⁵⁸ 盒）

每个乘子取**精确区间** `[(num−100)/D, (num+100)/D]`（`D=10^60`，`100 = ρD`）；中点只是输入，证书靠区间。

| 块 | 结论 | 区间（exact rational） |
|---|---|---|
| 406 个 distance α | **全部严格正** | 最小 α ∈ `[42348572292783896427988992463908089212057943686769711319,…519]/10^60` ≈ `4.2348572292783896e-5 > 0` |
| Σ_{distance} α | 中点 `= 1 + 7·10⁻⁶⁰`（`distance_sum_numerator = 10^60+7`），盒预算 `406ρ = 4.06e-56`，故**盒内与 1 相交** | t 行方程 `∂L/∂t = 1 − Σα` ⇒ 精确根处 **Σα = 1** |
| 32 个 unit ν | **全部严格负** | 最大 ν ∈ `[−100337382147506928168575716933790682862534826238232434111,…911]/10^60` ≈ `−1.00337e-4 < 0` |
| gauge 乘子 | 中点恰为 0 | numerator 0 |

**关键线索**：KKT 的 t 方程 `Σ_{distance} α = 1` **就是** cover19 的应力归一化 `Σ w_e = 1`。
所以这组乘子天然是一个**归一化的正权图应力**，不需要额外缩放；406 条杆全正。

## 3. 接触图 / 杆图（exact 组合）

246 节点 = 100 圆心 + 114 内部孔 + 32 边界孔；**406 条杆**（唯一，无重边）。
度：内部孔 3、边界孔 2、圆心 3..6；**100 个圆心全部出现在杆图中（无失活圆心）**——
这与 cover19 不同（cover19 的中央圆心 `c_12/c_15` 被有意排除在正权下界图之外）。
图**连通**（1 个连通分支）。

取锚点 = 32 个边界孔（单位圆上的点，`|q_k|²=1`，径向乘子 ν_k），自由节点 214 个。
**能量 PSD 必要条件（exact 组合判定）**：加权图 Laplacian 的接地块 `L_FF ≻ 0`
⟺ 每个连通分支至少含 1 个锚点。本系统满足 ⟹ **`L_FF` 严格正定**。
另给精确有理下界（路径 Cauchy–Schwarz，`x_v² ≤ ρ_v Σ_e w_e Δx_e²`，`M = max_e (Σ_{v:e∈P_v} ρ_v)/w_e`）

```
λ_min(L_FF) ≥ 1/M ,  M ≈ 2.6470168e8  ⇒  λ_min(L_FF) ≥ 3.7779e-9 > 0
```

（M 以 Fraction 精确保存于 `invariants.lambda_min_LFF_lower_bound`。）

## 4. 全 493 维 Hessian 的符号（“negative principal minor”要求）

`H = Σ_j α_j D²f_j = 2·L_rod(α>0) + 2·diag(ν_k 作用在 32 个边界孔坐标对)`；t 行列恒为 0。

* 负 **1×1** 主 minor：**0 个**（即使最负的对角元 `H_qq = 2(Σα+ν)` 也是正的）。
* 负 **2×2 坐标**主 minor：在全部 812 个有耦合的坐标对上**0 个**。
* 但存在**显式 2 维负定 Gram 证书**：取两个整体平移向量 `u_x, u_y`（把 246 个节点同时平移）。
  每条杆两端等量平移 ⇒ `uᵀ(2L_rod)u = 0`；unit 约束给出 `u_xᵀHu_x = u_yᵀHu_y = 2Σ_k ν_k`，
  且 `u_xᵀHu_y = 0`。因 32 个 ν 全负：

```
Σ_k ν_k ∈ [−1.3327999392353652176112898332441474161580939134525383673678e-2, …e-2]  ⇒  2Σν_k < 0
⇒ Gram 2×2 矩阵 2(Σν_k)·I₂ ≺ 0  ⇒  全 493 维 Lagrangian Hessian 非 PSD
```

**读法（重要）**：这只是说**无约束 493 维空间**上 `H` 非 PSD。它与上游 54 维
`ker B` 上的 SOSC **不矛盾**：两个平移方向不在 `ker B`（本系统没有“锚定圆心”平移规范，
只有 `c_74.y` 一个旋转规范），SOSC 也只声明在 `ker B` 上。
它也**不否定约束域上的凸性**。

## 5. 候选图 Dirichlet 能量迁移：模板、假设与结论

模板（cover19 §7–8）：杆图 `(圆心 a, 孔 h)`，权重 = 该孔对应约束的 α>0，`Σw=1`；
`E(q) = min_{自由节点} Σ_e w_e |z_u−z_v|²`，锚点 = 32 个边界孔。
若某覆盖半径 `ρ < r_root`，其孔点放置使**同组合类**每条杆长 ≤ ρ，则 `E ≤ ρ²`；
而 `E(q) ≥ E(q_*) = t_root` 可由「凸角域 + 驻定（KKT 力平衡 `∇L=0`）+ Hessian Loewner 下界」得到，
于是 `ρ ≥ r_root`。整数链条完全可执行：

* 角域：32 个相邻角隙 `∈ [0,δ]`、`Σ = 2π`，在固定 1 个锚点（= 商掉同时旋转）后是 31 维**凸**多面体。
  `δ = 2arcsin(r_root)`，`cos δ = 1−2t_root`；脚本用 `t_hi` 得 **cos δ 的下界** `Bcos`（`T_k` 在 `kδ<π` 时对 δ 单调减），
  并精确证明 `13δ < π`（`sin(π/26) > 0.1205360 > r_hi`，整数平方验证），故 `k ≤ 13` 用 Chebyshev `b_k`，`k ≥ 14` 用 `−1`。
* 候选角隙实测：min `0.1154372`，mean `2π/32 = 0.1963495`，max `0.2310611 < δ = 0.2314099`（数值诊断，非接受依据）。
* 边界 cap：32 个边界孔按角度成环，相邻两孔**恰共享 1 个服务圆心**，共 32 个互异服务圆心；
  每个 cap（单位圆弧）由该圆心支撑——这就是“small caps supports”的结构。
* Kron 约化（严格误差区间）：权重取精确盒区间；候选解用 flint `arb`（160 bit），
  再以 **精确整数残差** `Ẽ = SCALE·B̂ᵀ − Ĉ·X̂`（`SCALE = 2^128`）配 `λ_min(Ĉ) ≥ D/M` 得候选项；
  另 **显式加入根盒扰动预算**（不是硬编码）：`δ_L ≤ 2·NNODE·maxdeg·ρ = 2.952e-55`，
  `β_phys = ‖B̂‖/D`，和声延拓 `P=[I;−C⁻¹Bᵀ]`（`‖P‖ ≤ 1+Mβ`）给出
  `budget_root = δ_L(1+M(β_phys+δ_L))² ≈ 4.187e-39`，脚本 `assert budget_root < grid/10` 通过。

```
Γ = Γ_cand + budget_root ≈ 3.5245e-31  (候选项 3.5245e-31 + 根盒项 4.19e-39；精确有理)
grid 取整 1e-16，误差远低于 grid； c_ij ≤ 2.5074e-3
```

* **逐对收紧（本轮追加）**：固定图假设下每条杆长 ≤ r，故相隔 `h` 跳的锚点满足
  `|q_i−q_j|² ≤ h²t_hi` ⇒ `cosθ_ij ≥ 1 − h²t_hi/2`，与循环序界取 max：
  `b_ij = max(b_k, 1 − h_ij²t_hi/2, −1)`。实测相邻锚点跳数恒为 2、锚点对跳数范围 2..24；
  `b<0` 的对数从 304 降到 301（相邻锚点 `1−2t_hi = 0.9733` 与 `cos δ = b_1` 几乎相同，故增益很小）。
* `H0 = 2Σ_{i<j} c_ij b_ij(e_i−e_j)(e_i−e_j)ᵀ`（`b_ij ≥ 0` 取 `c^lo`，`b_ij < 0` 取 `c^hi`）
  的**精确有理 LDL**：符号 `+++++++++++++++++++++-++++++-++0`
  = 29 正 / **2 负**（≈ `−3.11e-3`、`−3.0e-4`）/ 1 零（常数核，即整体旋转）。
  判定用**精确负见证向量**（存在 `certificate.json`，分母 `10^12`）：
  `vᵀH0v < 0`（exact rational；**只有符号是精确结论**，浮点值仅指示）。
  独立复核见 `verify_certificate.py` 回执（exit 0，8/8 tamper 拒绝）。

**结论（有界、可复核）**：本路线在本单元内**未建立**候选图上的全局能量下界。
障碍出现在**界**而不在几何：32 个锚点使多数点对相隔 ≥ 7 个角隙，那里 `cos(kδ) < 0`，
逐对最坏情形界太弱；加入跳数界后仍不足以转正（`H0` 仍有 2 个精确负主元、有精确负见证向量 `vᵀH0v < 0`）。

**必须同时说明的三点**：
1. `H0` 不定 **只是该下界矩阵**不定；它**不能**否定真实约化能量 `E` 在凸角域上的凸性，也**没有**给出反例覆盖半径。
2. 这不等于方法不可行：cover19 在 12 锚点、`δ` 较大时 `k ≤ 5` 覆盖大多数点对；本系统 32 锚点、`δ ≈ 0.2314`，
   同一标量界的信息量不足。
3. 5 个**必要条件**全部通过：正应力、`Σα = 1`、精确力平衡（`∇L=0`，中点残差 ≈ `4.7e-61`，远小于盒预算）、
   接地块 `L_FF ≻ 0`（组合 + 有理下界）、边界孔严格在单位圆上、`13δ<π`。

### 5.1 本轮新增：真实约化角能量也不是凸的

此前只能证明标量逐对 Loewner 下界 `H0` 不定，尚不能排除真实约化能量 `E` 仍然凸。本轮从同一根箱和精确权重构造了真实角变量 Hessian

`H_ang = 2 Σ_{i<j} c_ij (q_i·q_j)(e_i-e_j)(e_i-e_j)^T`。

数值探索只用于发现见证方向；随后[有理根箱证书](../verify/out/n100-angular-energy-negative-witness.json)用分母 `10^12` 的固定向量、精确 `c_ij` 区间和保守根箱误差证明二次型上界严格为负。另一个[独立实现](../verify/out/n100-angular-energy-independent.json)不调用生成器或特征值计算，重新绑定 `certificate.json`、Krawczyk 根箱和源文件哈希，逐边作有理区间运算，得到相同严格负号；零向量与常数旋转向量两个负控制均被拒绝。

因此，**真实谐延拓应力能量在该候选角域根处已非凸**。这排除了“直接把该能量作为整个角域凸函数并由驻点给出全域下界”的路线。它仍然不是覆盖反例：谐延拓能量只放松逐杆几何约束，负方向不保证存在半径小于根的可行覆盖；54维约束切空间SOSC也不被否定。下一步必须使用局部约束域证书、分支排除或完整其他拓扑枚举。



## 6. 旧建议与本轮修正

以下三条是仅知道粗界失败时的历史建议。第2轮的真实能量反例已经否定当前固定应力的全域下界，不能再把这些建议列为通向该下界的有效步骤。它们只可用于局部估计或其他权重，不改变反例。

1. **利用 `Σgaps = 2π`**：逐对最坏值 `kδ` 不能对所有点对同时取到；把 `b_k` 换成带耦合约束的联合界
   （cover19 §8.3 的 circulant/Fourier 思路在非对称 100 圆上需要一般化）。
   本轮已试的**跳数界**（`1−h²t_hi/2`）只把 `b<0` 对数从 304 降到 301，不足以转正。
2. **近/远分裂 + 精确 Farkas/SOS**：近对（`k ≤ 6`，`b_k > 0`）用 Loewner，远对（`b_k ≤ 0`）单独给一个精确余项证书。
3. **残差逆界收紧**：本轮 `Γ` 已到 `3.5e-31`，若仍需更紧可对 `Ĉ` 做块对角预条件后重算 `λ_min` 下界（当前路径界很保守，`1/M ≈ 3.78e-9`）。
4. **全拓扑缺口（明确未做）**：全局排除需要枚举 100 圆可能出现的深孔拓扑
   （边界弧数/配对 + Delaunay 支撑关联）并配 force 证书；cover19 用 24,127 个幸存轨道，n=100 的规模远大于此。
   因此本文件的能量证书**只在候选图组合类内**有效。

## 7. 范围声明

* 仅候选图（114 内部三角 + 32 边界对，406 杆）；**不是** `r_D(100)` 的全局最优或全局下界。
* 上游 932 变量孤立根与 54 维 SOSC 只给**模同时旋转的严格局部极小性**；本文件不把它升格为全局结论。
* 数值只用于发现（flint/numpy 候选解、特征向量候选）；所有接受判定为整数/有理/精确布尔，
  唯一“浮点”入口的误差由精确整数残差 + 精确有理界 `Γ` 吸收。
* 未修改任何上游/旧目录；产物仅在本目录与 `docs/` 下新增。

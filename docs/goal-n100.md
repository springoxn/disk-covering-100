# n = 100：目标与纲领（goal-n100）

> 本文件与 `docs/goal.md`（n = 12 题面）、`.agents/goal.md`（n = 11 题面）同级，但内容分两部分：
> **A. 形式化题面**（须满足的交付要求，照 benchmark 模板改写为 n = 100）；
> **B–F. 现状、路线、里程碑与纪律**（文献调研结论 + 本仓库地基 + 分阶段验收 + 止损点）。
>
> 写作时间：2026-10（文献检索快照见 §B.1，链接已注明）。

---

## A. 形式化题面

### Optimal Covering of the Unit Disk with 100 Disks

Let
$$
D=\{x\in\mathbb R^2:\|x\|_2\le1\},\qquad
R_D(C)=\max_{x\in D}\min_{1\le i\le100}\|x-c_i\|_2,
$$
where $C=(c_1,\ldots,c_{100})\in(\mathbb R^2)^{100}$, and define
$$
r_D(100)=\inf_{C\in(\mathbb R^2)^{100}}R_D(C).
$$

The covering disks are closed. They may overlap and extend beyond $D$; their centers are not initially restricted to lie in $D$.

Determine $r_D(100)$ and satisfy all of the following requirements:

1. **Minimal polynomial and root isolation:** Explicitly list every coefficient of the normalized integer representation $P(t)\in\mathbb Z[t]$ of the minimal polynomial of the optimal radius $r_D(100)$ over $\mathbb Q$. Require $P$ to be nonconstant and primitive, with positive leading coefficient, and prove that it is irreducible in $\mathbb Q[t]$. Give specific rational numbers $0\le a<b$, prove $P(a)P(b)\ne0$, and prove that $P$ has exactly one real root $\alpha$ in $(a,b)$. Use the configuration and proofs below to establish $r_D(100)=\alpha$.
2. **Explicit configuration:** Give a definite ordered tuple of centers $C_*=(c_1^*,\ldots,c_{100}^*)$, specified exactly by radicals, polynomials and rational isolating intervals, or other explicitly supplied finite algebraic data whose uniqueness is proved. Uniqueness here means that the submitted data uniquely specify these center coordinates; it does not require a proof that the optimal configuration is unique.
3. **Coverage:** Rigorously prove
   $$
   \forall x\in D,\quad\exists i\in\{1,\ldots,100\},\quad
   \|x-c_i^*\|_2\le\alpha.
   $$
   If continuous coverage is reduced to a finite set of checks, prove that the reduction is sufficient and rigorously complete every required check.
4. **Global optimality:** Rigorously prove
   $$
   \forall C\in(\mathbb R^2)^{100},\quad R_D(C)\ge\alpha,
   $$
   and hence $R_D(C_*)=r_D(100)=\alpha$. Do not restrict symmetry, contact relations or combinatorial structure without proof. Every normalization, classification, enumeration or pruning step must be proved not to omit a potentially better configuration. Handle coincident centers, redundant disks and other relevant degeneracies.
5. **Computer-assisted proof:** If the proof relies on computation, deliver the complete code actually used, inputs, certificates, necessary environment information and actual verification results. Explain why those results imply the mathematical statements above.

**Final submission:** Explicitly list every coefficient of $P(t)$ and the rational root-isolating interval $(a,b)$, together with the configuration, complete proof and necessary verification materials. Submit the minimal polynomial of the optimal radius itself. A polynomial for its square or another auxiliary quantity, or an elimination polynomial without a proof of irreducibility, does not satisfy the requirement.

Any rigorous method is allowed. Merely proving existence or algebraicity, or supplying unfinished enumeration, a solution algorithm or a numerical candidate, does not count as completion. Successful numerical optimization, a program printing "passed", or floating-point results without rigorous error control cannot replace a proof. Checking only finitely many sample points, the boundary, or a numerical image cannot replace a proof that the entire closed unit disk is covered.

文章搜索可参考 `E:\study\AImath\tools\lit\README.md`
可以 lean 辅助验证，使用本地 lean
可借鉴 `E:\study\AImath` 的结构/文件规划

---

## B. 文献调研结论（2026-10 快照）

### B.1 各 n 的已知状态

单位换算：文献常用"n 个单位盘能覆盖的最大圆半径"记作 $\rho(n)$，本题 $r_D(n)=1/\rho(n)$。

| n | 上界（构造，已找到） | 下界（全局最优性，已证？） | 来源 |
|---|---|---|---|
| 1–4, 7 | 精确闭式 | ✅ 平凡 | — |
| 5, 6 | 精确闭式 | ✅ K. Bezdek 1979/1983 | [MathWorld](https://mathworld.wolfram.com/DiskCoveringProblem.html) |
| 8, 9, 10 | 精确闭式 $r_D(n)=1/(1+2\cos\frac{2\pi}{n-1})$ | ✅ G. Fejes Tóth 1996/2005 | [G. Fejes Tóth, *Thinnest covering of a circle by eight, nine, or ten congruent circles*](https://library.slmath.org/books/Book52/files/18fejes.pdf) |
| 11–20 | 已找到（Melissen 1997 / Tan 2018） | ⚠️ Friedman 页面 2026 记 "Proved by VoxEquinox"；策展数据库仍记 **Unknown** | [Friedman](https://erich-friedman.github.io/packing/circovcir/) vs [leapsinbounds r(11)](https://leapsinbounds.org/constants/disk-covering-11/) |
| 21–25 | 已找到（Tan 2018） | ❌ 无任何证明声明 | Friedman |
| 26–99 | 无系统公开表格 | ❌ | — |
| **100** | **无公开数据；只有格状构造** | ❌ | — |

三条对本目标最关键的事实：

1. **策展数据库把 r(11) 与 r(25) 的下界都记为 Unknown**（[r(11)](https://leapsinbounds.org/constants/disk-covering-11/)、[r(25)](https://leapsinbounds.org/constants/disk-covering-25/)）。也就是说，即便本仓库第一道题 n = 11，也处在"上界已知、下界未证"的状态；n = 100 更是完全空白。
2. **渐近密度是严格的**：$\lim_{\varepsilon\to0^+}\frac{1}{\varepsilon^2N(\varepsilon)}=\frac{3\sqrt3}{2\pi}$（Kershner 1939；Verblunsky 1949），即覆盖密度 $\delta=\frac{2\pi}{3\sqrt3}=1.2091996\ldots$。这是下界"密度层"的唯一严格基础，且是**渐近**（$\varepsilon\to0$）陈述——把它变成有限 $n$ 的界，必须补一个周界（边界）修正项。
3. **"对称性不是最优性的必要条件"有经典反例**：n = 5 时对称排列给 $r=\varphi-1=0.6180340\ldots$，而真最优是 $0.6093829\ldots$（更小）。即最优构型**只有一条镜像轴（D1）**。这正是 Connelly 2008 提出的问题（"最优构型是否总有 n 重旋转对称？"）——n = 2 是、**n = 5 不是**、n = 3 已被 Csikós 证明是（[Csikós 2016](https://www.degruyterbrill.com/document/doi/10.1515/advgeom-2016-0018/html)、[Csikós slides](https://www.fields.utoronto.ca/programs/scientific/13-14/discretegeom/Slides/Csikos.pdf)）。已知最优的对称性：n = 5, 6, **11** 只有 D1；n = 7…10 为 D6…D9；n = 12 为 D3；n = 25 为 D8（本仓库重构）。

### B.2 方法现状：为什么枚举路线在 n = 100 不可行

严格的计算机辅助最优性证明的成熟范式是"**组合/消去式分类 + 区间 Newton/分支定界**"。Nurmela–Östergård 用这套方法把方形内等圆**堆积**的严格最优性推到 n ≤ 27（[More optimal packings of equal circles in a square](https://scispace.com/pdf/more-optimal-packings-of-equal-circles-in-a-square-27v52zgxcx.pdf)），其自述的代价与瓶颈是：

- "初始组合数随 n 迅速增长"；23 ≤ n ≤ 26 需要**数 CPU 月**；n = 27 若不换算法"即使算力增长也无济于事"；
- n = 21 需要**专门**的误差方块分割论证才收敛；
- 区间 Newton（INTBIS）用来在剩余活动区域证明解的存在。

这与本仓库对 n = 100 的估计一致（覆盖构型空间的轨道数是天文量级），**结论：枚举/分类不能作为 n = 100 的主路线**，只能用于小 n 的校准（例如 §E Stage 2 的 n = 25 试点）。

### B.3 方法现状：唯一有先例的"对称逼定"

G. Fejes Tóth 证 n = 8, 9, 10 的手法是目前**唯一的**"把对称性变成定理"的成功范式：

- 用 **Dirichlet（Voronoi）胞复形**把覆盖问题化为有限多个胞型上的面积估计；
- 用 **边界盘的 radical-axis 反射**（若某盘与 $\partial D$ 相交且圆心在 radical axis 外侧，则对该轴反射仍保持覆盖）把边界盘"压到最内"，从而约束边界层的结构；
- 用面积（密度）估计逼出等号情形，得到"一个同心盘 + 正 $(n-1)$ 边形"的刚性问题。

**注意其适用范围**：该证明只在"1 个中心盘 + 1 个环"的结构下成功；n = 25（中心 + 3 个八边形环）与 n = 100（多环）**没有**对应的定理。

L. Fejes Tóth 的覆盖-密度不等式（1950s，[Some packing and covering theorems](http://acta.bibl.u-szeged.hu/13588/1/math_012_pars_a_062-067.pdf)）给出带**周界项**的覆盖侧密度界（其定理 4 的形式含常数 $\mu\ge 1+(2+\sqrt{27}/\pi)^2/12=2.14\ldots$）；堆积侧的对偶是 Oler/Thue–Groemer 不等式
$$
\tfrac{1}{2\sqrt3}A(C)+\tfrac14P(C)+1\ \ge\ n .
$$
这两类是"逐胞 + 周界修正"的文献原型。

### B.4 合法的对称化清单（哪些能用、哪些不能用）

| 层 | 操作 | 合法性 | 用途 |
|---|---|---|---|
| 构型 | $C\mapsto\bigcup_{g\in G}gC$ | ❌ 盘数改变 | — |
| 构型 | $C\mapsto$ 平均构型 | ❌ 不保覆盖 | — |
| 构型 | **边界盘对 radical axis 反射** | ✅ | 把与 $\partial D$ 相交的盘压到最内（Fejes Tóth 用法）|
| 证书 | 对证书（测度/势函数/SOS 乘子）做 $G$-平均 | ✅ 约束集凸且 $G$-不变 | 证书可设对称，维数塌缩 |
| 组合 | 轨道算术 $n=\sum$ 轨道长 | ✅ 必要条件 | 直接排除大批对称群 |
| 组合 | 胞复形取 $G$-商 | ✅ | 只需检查基本域内的胞型 |
| **（陷阱）** | 全局测度 LP | ⚠️ 只给 $r\ge 1/\sqrt n$ | Lebesgue 测度即饱和，**不要**走这条 |

---

## C. 本仓库已有的地基（可直接复用）

| 层 | 已有产物 | 位置 |
|---|---|---|
| 精确代数 | 数域 $F=\mathbb Q(\sqrt2,\sqrt3,\sqrt{2+\sqrt2})$ 与二次扩张 $F(\sqrt\Delta)$ 的精确零/符号判定；有理区间（`Fraction` 端点） | `verify/exact_n25.py` |
| 覆盖证书 | n = 25：3140 个候选全部覆盖、覆盖半径**精确** $=r$、20 个检查全 PASS | `verify/coverage_cert_n25.py` → `verify/out/coverage_certificate_n25.json` |
| 活动集 | n = 25：544 条紧记录 → 48 点 → **4 个 D8 轨道**（8+8+16+16），其中 C 类洞是本轮新发现 | 同上 `active_set` |
| 对称性 | n = 25：16 阶二面体群的**精确**置换/关系/旋转阶证书 | 同上 `symmetry_certificate` |
| 交叉验证 | 网格 3.46×10⁶ 点 / 400 次随机重启 / 14400 次 mpmath 比对 / 共线分离 | `verify/validate_n25_coverage.py` |
| 消元与极小多项式 | n = 25：9 方程 binding 系统 → $\mathrm{Res}_u(F_1,E_8)=4096(9r^4-18r^2+1)^2$ | `tools/n25_d4_symbolic.py` |
| 答案数据层 | 公布指纹/闭式比对工具 | `verify/probe_reference_answers.py` |
| 数值发现 | 一族环状构型的快速覆盖半径目标函数（切平面 + 精修） | `_recon/benchmark/svg/d8_fast_n25.py` |
| 结构判据 | 轨道算术脚本（本文 §D 的数字来源） | `_recon/benchmark/n100_symmetry_logic.py` |

---

## D. 三个已量化的判断（本目标的定量出发点）

### D.1 轨道算术：n = 100 排除掉 D6/D8

$D_k$（2k 阶二面体）在平面上的轨道长只有 $\{1,k,2k\}$，故 $n=c+ak+2bk$（$c\in\{0,1\}$ 表示是否有中心盘）。据此：

- **D6、D8 对 n = 100 算术上不可能**（100 与 99 均不被 6 或 8 整除）；
- 相容的只有：D1、D2、**D3+中心**、**D4（无中心）**、D5、D9+中心、D10、D11+中心；
- n = 100 恰卡在两个"完美环"之间：**97 = 1+8·12**（D8）、**103 = 1+6·17**（D6）——**必须破对称**；
- 对"100 = 4×25 ⟹ D4"的直觉：D4 可行但**必须没有中心盘**（100 = 8a+4b，2a+b = 25）；六方格直觉指向 **D3 + 中心盘**（1 + 6·16 + 3 = 100）；
- 反向警告：n = 25 的答案是 **D8**（1+8·3）而不是 D6（1+6·4），故"格状直觉"在中 n 不可靠——**必须实测**。

### D.2 下界缺口的量级

用已知 $r_D(n)$（n = 7…12, 19, 25）提取周界缺陷律 $n r^2\ge \delta(1+\lambda r)$（$\delta=1.2091996$）：

| 下界来源 | $r_D(100)\ge$ |
|---|---|
| 平凡面积 $n\pi r^2\ge\pi$ | 0.100000 |
| 平面覆盖密度（渐近）$\sqrt{\delta/n}$ | 0.109964 |
| 周界缺陷项，$\lambda=0.76$ | 0.114655 |
| 周界缺陷项，$\lambda=0.83$ | 0.115096 |
| 周界缺陷项，$\lambda=0.86$ | 0.115286 |
| （外推的期望答案，**非定理**） | ≈ 0.1151 |

**结论：下界缺口 15%，其中"密度层"贡献 ~10%、"周界缺陷层"贡献 ~5%；两者量级相当，都必须证。** 但一旦一条以 $\lambda\approx0.87$ 成立的周界缺陷不等式被证明，n = 100 就被钉到 0.4% 以内——**本目标的核心从"枚举 10⁸⁶ 个轨道"变成"把一条不等式的常数做到 $\lambda\approx0.87$"**。

> **2026-10-11 更正（`docs/notes-lowerbound-n100.md` §1–§2）**：上面这条纲领的前提是错的。
> λ 律若对某个 n 成立，λ 就被该 n 的**已证明最优值**卡住 `λ ≤ (n r_n²/δ − 1)/r_n`：
> n = 8, 9, 10, 19, 25 分别给出 0.697 / **0.669** / 0.734 / 0.752 / 0.763。
> 所以 **λ ≈ 0.87 的全局律不成立**（n = 9 就否证），而 λ\* = 0.6688 至多给
> r(100) ≥ 0.114081（相对最好已知构型 −6.75%）。同时面积-周长型实现（本节所指的
> "周界缺陷层"）在逐胞层面**从不 binding**（0/25），聚合上界只有 0.1540。
> **λ 形状作为 n = 100 的下界引擎已被排除**；目标重心转向构型侧（见 Stage 3 状态）。

### D.3 已知答案的两个正当用法

1. **校准**：任何下界工具先拿到 n = 25（答案精确已知）上量 gap；
2. **作为不等式的等号情形**：先用极值构型确定等号情形，再设计以它为等号的逐胞不等式——这是这类不等式被发现的标准路径。

---

## E. 阶段与里程碑（每阶段可独立验收）

### Stage 0（1 周）—— 答案层定型

**目标**：给出 $r_D(100)$ 的候选构型 + 候选极小多项式 + 完整活动集 + 轨道结构。
**做法**：把 `d8_fast_n25.py` 的一族环状目标函数推广到 100 盘（目标函数改用"候选集 + 局部精修"，避免 $O(n^3)$ 外心枚举），在 §D.1 的相容族（D3+中心 1+6·16+3、D4 无中心 8·12+4、D5、D9+中心…）内做全局搜索。
**交付**：`verify/out/n100_candidate.json`（构型、binding 系统、消元多项式候选、活动集）、覆盖证书（同 n = 25 流程）、独立交叉验证。
**验收**：覆盖证书 20 类检查全 PASS + 四路交叉验证全 PASS；**明确不声称最优**。

### Stage 1（2–4 周）—— 对称类内的严格最优性

**目标**：对固定对称族 $G$，证明 $r_G(100)=\alpha$（族内最优），其中 $r_G$ 只在 $G$-不变构型上取 $\inf$。
**做法**：族内参数只有十几个（每个 8-轨道 2 个参数、每个 4-轨道 1 个参数）→ 参数盒上的分支定界 + 区间/Krawczyk；族内的**组合型**（活动图）是有限的，可逐型闭环。
**交付**：`verify/out/n100_symmetric_optimality.json`，含每个组合型的排除证书。
**验收**：每个组合型都给出"该型内无更好构型"的区间证书；总和覆盖整个对称族参数盒。
**诚实声明**：这一步只给**条件**最优（$r_{D_4}(100)$ 或 $r_{D_3}(100)$），不是 $r_D(100)$。

### Stage 2（研究）—— 下界：逐胞不等式（先在 n = 25 闭环）

**目标**：证明形如 $n r^2\ge\delta(1+\lambda r)$（或等价的分胞不等式；允许带 $O(1/\sqrt n)$ 修正），常数由已知 $n$ 标定。
**做法**：Dirichlet 胞 + Oler/Fejes Tóth 型面积-周长不等式；用 n = 25 的**已知** 48 点活动集（4 轨道）作为等号情形反推胞型常数；对称性在此层的两个正当用途：胞复形取 $G$-商、边界盘 radical-axis 反射。
**交付**：不等式 + 证明 + 常数表 + 在 n = 11…29 已知值上的检验脚本。
**验收**：在 n = 25 上，由不等式导出的下界 ≥ 精确值减去一个不可约的间隙，且该间隙被明确量化（这是本阶段的可证伪指标）。

**状态（2026-10-11，已按 §G 降级）**：在 n = 25 上闭环，**结果是触发 §G 的 >5% 条款**
—— 有效普适界 0.2235441655（精确值 −6.52%；最有利读法 −5.75%），同一条路线在 n = 100
上 −9.34%，周界缺陷常数 λ ≈ 0.15 而门槛要 ≈ 1.01。三条引理（带边界 Euler 记账
`Σ(6−m_i) = 6 + 2b`、边界胞 = 多一条边 `max_Θ g = f(m+1)`、弧覆盖 `b ≥ π/arcsin r`）
与判决见 `docs/notes-euler-clipped.md`；记账本身已出精确证书
（`verify/euler_clipped_n25.py` → `verify/out/euler_clipped_n25.json`，9/9 PASS）。
本阶段据此**降级**为"n = 25 校准过的普适界"，n = 100 的下界转入 Stage 3。

### Stage 3（研究）—— 两区制缝合

**目标**：把 Stage 2 的粗糙界（远对称区）与 Stage 1 的刚性（近对称区）缝起来，中间区是唯一缺口；若中间区无法缝合，则明确给出"缺口的形式"（一个精确的、可被后续工作攻击的数学命题）。
**交付**：`docs/notes-lowerbound-n100.md`。

**状态（2026-10-11，第一步已完成，结论：按 §G 最后一条降级）**：`docs/notes-lowerbound-n100.md`。

1. **λ 形状的下界律被否证（全局版）**：上限 λ\* = 0.6688（由已证明最优的 n = 9 卡住），
   至多给 r(100) ≥ 0.114081，而 5% 门槛要 λ ≥ 1.0079。面积-周长实现更弱：逐胞
   **0/25 binding**、聚合上界 0.1540、oracle 0.1836。**"周界缺陷层"这条路到此为止。**
2. **构型侧也拿不到改进**：四类搜索（12 个自由点松弛 + 39 个边缘点的 (ρ,θ) 坐标下降 +
   3 起点 × ~72k 次退火最深洞移动 + 2730 组结构化混合）**全部无法改进 0.1223432713**。
3. **外推依据撤回 + 无外部标尺**：曾用已证明最优值的 c 带预测"构型还有 5–6% 空间"，
   **该推断已撤回**（小 n 最优值是环状族、n = 100 最好构型是格点族，不可比；格点族在
   n ≲ 30 甚至覆盖不了圆盘，n = 25 时给 0.4615）。外部核查：**Friedman 表止于 n = 25**
   （r(25) = √6+√3 = 4.1815…，与我们的精确值 (√6−√3)/3 ✓ 一致），n > 25 无公开参考值——
   0.12234 **没有外部标尺**。
4. **目标算术**：判据 `(U−L)/U ≤ 5%` ⟺ `U ≤ L/0.95`。用已证下界 L = 0.110914 需构型
   做到 **U ≤ 0.116752**（4.6% 改进）—— 未找到。

**降级后的交付**：① n = 100 覆盖证书（已有，三种独立方法）；② 一条**已证**普适下界
**0.110914**；③ 写清楚的开放命题 **A**（数值：存在 r ≤ 0.11675 的覆盖，目前无证据）
与 **B**（分析：r ≥ 0.1141，λ 形状的理论上限，未证明；已证 0.1109）；④ 诚实声明：
**n = 100 全局最优性未解决**，且无外部标尺。

**建议的重定向（价值最高）**：机具已在 n = 7, 8, 9, 10, 19, 25 上**精确命中已知最优值**，
而 benchmark 覆盖到 **n = 29**、其中 **n = 26 与 n = 27 有已发布参考指纹**。把那套机具
（环族目标函数 + 精确证书链 + 有序 profile beam search）用在 n = 26…29 上，性价比高于
继续攻 n = 100 的 5% 代理指标：答案存在、可对照，且搜索空间可能仍在环族内
（26 = 1+5·5 ✓ D5；27 = 1+2·13 ✓ D13；28 = 4·7 ✓ D7 无中心）。

### Stage 4（可选）—— Lean 形式化

参考 `E:\study\AImath` 的结构与 `proof_graph/` 状态本体；优先形式化 Stage 1（有限、组合性强、不依赖实分析）。本地 Lean：`E:\study\AImath\.local-lean`。

---

## F. 纪律与验收规则

1. 每个"已验证"的说法必须指向 `verify/out/*.json` 里的证书条目；没有证书就写"未验证"。
2. `verify/` 下的判定只用整数/有理数运算与有理区间算术；浮点只用于**发现**。
3. 第三方结果（Friedman/leapsinbounds/文献/PyPI 包）只做**重放与独立复核**，不当作自己的证明。
4. **三种强度必须分开标注**：①覆盖（上界）；②族内最优（对称类内的下界）；③全局最优（对全体构型的下界）。任何把 ① 或 ② 说成 ③ 的表述都算失败。
5. **对称性只能展示、不能假设**（除非给出独立的逼定证明）。文献反例：n = 5, 6, 11 的最优只有 D1。
6. 服务器算力（`zhengyj@10.10.2.161`，8 核 / 61 GB 空闲）用于 Stage 1 的分支定界与 Stage 2 的常数标定；本机负责证书与文档。

---

## G. 止损点（任何一条触发就停下重新设计，不要硬推）

- Stage 0 在 12 个候选对称族内**找不到** $r\le0.116$ 的构型 ⇒ §D 的"格状直觉"有问题，先回到数值全局搜索（不要对称约束）重新定位结构。
- Stage 1 的族内参数盒无法被有限个组合型覆盖（活动图随参数连续变化）⇒ 需要先证明"族内活动图的有限性"，这是一个独立命题，应先写出来再继续。
- Stage 2 在 n = 25 上给出的下界比精确值低 **>5%** ⇒ 逐胞不等式这一层太弱，应转向"局部 + 全局混合"（例如用 n = 25 的活动集直接构造有限个全局约束），并重新评估 Stage 3。
- 若 6 周内 Stage 2 仍无在 n = 25 上闭合的迹象 ⇒ 本目标降级为"n = 100 的覆盖证书 + 对称类最优"，并如实记录全局最优性未解决。

---

## H. 参考文献（本轮实际检索到的）

1. E. Friedman, *Circles Covering Circles* — 各 n（≤25）的构造值与证明归属。https://erich-friedman.github.io/packing/circovcir/
2. Leaps in Bounds, *Disk covering problem* $r(n)$ 策展条目（含逐年上下界更新）。https://leapsinbounds.org/constants/disk-covering-25/ 、 https://leapsinbounds.org/constants/disk-covering-11/
3. G. Fejes Tóth, *Thinnest covering of a circle by eight, nine, or ten congruent circles*（对称逼定的唯一成功范式：Dirichlet 胞 + 面积估计 + radical-axis 反射）。https://library.slmath.org/books/Book52/files/18fejes.pdf
4. L. Fejes Tóth, *Some packing and covering theorems*（覆盖侧带周界项的密度不等式；Thue–Groemer / Oler 的对偶）。http://acta.bibl.u-szeged.hu/13588/1/math_012_pars_a_062-067.pdf
5. K. Bezdek, *Über einige Kreisüberdeckungen* (1983) / *Über einige optimale Konfigurationen von Kreisen* (1984)（n = 5, 6 的最优性；n = 5 的代数特征）。见 MathWorld 条目。
6. R. Kershner (1939), S. Verblunsky (1949)（渐近覆盖密度 $3\sqrt3/(2\pi)$）。见 MathWorld 条目：https://mathworld.wolfram.com/DiskCoveringProblem.html
7. B. Csikós, *Optimal cover of a disk with three smaller congruent disks*（Connelly 问题：n = 3 必三重对称；n = 5 的对称破缺与突变）。https://www.degruyterbrill.com/document/doi/10.1515/advgeom-2016-0018/html
8. K. Nurmela, P. Östergård, *More optimal packings of equal circles in a square*（严格计算机辅助最优性的代价/瓶颈：组合消去 + 区间 Newton；n ≤ 27，CPU 月级）。https://scispace.com/pdf/more-optimal-packings-of-equal-circles-in-a-square-27v52zgxcx.pdf
9. Zs. Gáspár, T. Tarnai, K. Hincz, *Partial covering of a circle by equal circles* I/II（中间问题与力学/张力集成模型；对称性的分叉路径）。https://jocg.org/index.php/jocg/article/download/2929/2623/7236
10. 本仓库上游第三方包（仅重放）：`lit/DiskCoveringSolve/`（cover11/cover12/cover13，含 Krawczyk 盒证书）。

---

## I. 与 n = 11 / n = 12 的关系（为什么顺序是 n = 25 → n = 100）

- **n = 11 不能用对称路线**：其最优构型只有一条镜像轴（§B.1）；且 benchmark 第一题已有上游 Krawczyk 包可重放。对称性论证在 n = 11 上**完全无效**。
- **n = 25 是校准台**：答案的闭式、极小多项式、完整活动集（4 轨道 48 点）与精确覆盖证书本仓库都已具备（§C），是检验任何下界工具的最好靶子。
- **n = 100 是对称路线的主场**：结构格状化、对称性高，而枚举墙最厚（§B.2）。因此本目标的路线是"**先 n = 25 校准工具 → 再 n = 100 攻坚**"，而不是反过来。

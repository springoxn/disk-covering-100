# n = 100 阶段1（下界侧）审计：历史 0.1109141386 链逐条核账与保底 L = 1/10 证书

> **范围**：本文件只承担**下界侧**。不写 `runtime/STATUS-n100.md`、不写主审计报告
> `docs/audit-baseline-n100.md`、不改统一入口、不碰覆盖侧（上界）。
> **结论一句话**：本阶段**唯一已证普适下界是面积（测度）界 L = 1/10**；
> 历史加强界 0.1109141386 **降级为「未证」**（阻塞义务 O1–O9，见 §3.2）。
> **产物**：证书与接口 [verify/lowerbound_n100.py](../verify/lowerbound_n100.py) →
> 证书实例 [verify/out/lowerbound_n100.json](../verify/out/lowerbound_n100.json)；
> 本文档；复现日志 [runtime/n100_cell_bound_repro_2026-10-12.txt](../runtime/n100_cell_bound_repro_2026-10-12.txt)。

**判定纪律**：本文件里凡是「判定」一律只用整数与有理数（`fractions.Fraction`）与整数定点算术；
浮点只出现在**发现层**（`tools/cell_bound.py`、`_recon/*.py`）以及历史记录的字面值里。
审计把**解析推理**（人写的证明，§2.1、§3.4）与**算术认证**（机器可复算的整数/有理检查 L01–L20，§2.2、§6）
**分开标注**，两者都不单独构成结论：解析推理给出不等式，算术认证只给有限恒等式/不等式。

---

## 1. 结论与强度分级

| 层 | 对象 | 本阶段判定 | 证据 |
|---|---|---|---|
| ① 覆盖（上界） | n = 100 存在半径 r 的 100 盘覆盖 | **不在本文范围**（覆盖侧子任务负责） | 历史约 0.1223432713 只是发现层记录 |
| ② 族内最优 | 某对称族内的最优 | **未证明**（无产物） | — |
| ③ **全局最优（下界）** | 对一切 100 中心构型 r_D(100) ≥ L | **L = 1/10 已证**（本文件） | 解析 §2.1 + 算术 L03–L11、L20 |
| ③′ 历史加强界 | r_D(100) ≥ 0.1109141386 | **降级：未证** | §3 逐条；`strengthened_chain.status = not_certified` |

- `r_D(100)` 的精确值、极小多项式、不可约性与根隔离：**均未证明**（与 STATUS 一致）。
- 历史「约 0.1109141386 是已证普适下界」的说法（`docs/notes-lowerbound-n100.md:183`、`:229`、
  `docs/goal-n100.md:223`、`:226-229`）**本轮不成立**，理由与逐条证据见 §3。
- 本文**不使用**对称性假设、不使用任何构型数据、不引用任何外部参考值。

---

## 2. 保底面积下界 L = 1/10

### 2.1 解析推理（**人写的证明**，手段：测度 + 初等代数）

设 100 个**闭**圆盘 `B_i = B(c_i, r)` 覆盖 `D = {|x| ≤ 1}`；圆心**允许**在 D 外
（题面 `docs/goal-n100.md:25`），半径 r ≥ 0。

- **S1（覆盖 + 面积单调）**：`D ⊆ ⋃_i (B_i ∩ D)`，故 `π = area(D) ≤ area(⋃_i (B_i ∩ D))`。
- **S2（有限次可加 + 交的上界）**：`area(⋃_i (B_i ∩ D)) ≤ Σ_i area(B_i ∩ D)`。
- **S3（圆盘面积）**：`area(B_i ∩ D) ≤ area(B_i) = π r²`。
- **S4**：合并得 **`π ≤ 100 π r²`**。
- **S5（消去正 π）**：`π > 0`。本仓库给出**机器整数证书** `π > 3`（§2.3），更强于所需。
  两边同除 π 得 **`1 ≤ 100 r²`**。
- **S6（精确有理，唯一正根）**：整数系数恒等式 `(10r−1)(10r+1) = 100r² − 1`；
  `r ≥ 0 ⟹ 10r+1 ≥ 1 > 0`。故 `100r² ≥ 1 ⟺ 10r − 1 ≥ 0 ⟺ r ≥ 1/10`；
  等号**当且仅当** `r = 1/10`（正根唯一）。
- **S7（过渡到 inf）**：对**任意**构型 C 有 `R_D(C) ≥ 1/10`，故
  `r_D(100) = inf_C R_D(C) ≥ 1/10`。其中 `R_D(C) < ∞` 由 D 紧、中心有限即得。

**这一步只用覆盖性 + 面积的有限次可加性**：不需要一般位置、不需要胞复形、不需要任何
Euler 记账、不需要圆心在盘内、也不需要对退化情形做分类；闭盘/开盘、重合中心、盘外中心
在这一步都不造成分支。这就是它能成为本阶段唯一「无条件」普适下界的原因。

### 2.2 算术认证（**机器可复算的有限检查**，整数/有理）

证书条目：下表 = 证书 `exact_checks`（18 项，L02…L20；由 `_payload_checks` 重算并记录）
**加上**报告级 `L16`/`L17`（只在 `check_certificate` 的报告里，不进 `exact_checks`）。
数值全部是 `int` 或有理数字符串；`L18` 会扫描判定路径、发现任何 JSON 浮点即失败。

| 条目 | 内容 | 判定 | 级别 |
|---|---|---|---|
| L02 | schema/kind 与接口约定一致 | PASS | error |
| L01 | 证书可解析：n 为整数、lower_bound 为有理数字符串 | PASS | error |
| L03 | n == 100（整数比较，不许 bool/浮点冒充） | PASS | error |
| L04 | 声称下界恰为有理数 1/10 | PASS | error |
| L05 | 精确有理检查：100·L² == 1 | PASS | error |
| L06 | 整数系数恒等式 (10r−1)(10r+1) = 100r² − 1 | PASS | error |
| L07 | 10r+1 在 r >= 0 上严格正（常数项>0、斜率>=0 ⟹ 单调不减） | PASS | error |
| L08 | 唯一正根：100r²=1 且 r>0 ⟹ 10r−1=0 ⟹ r=1/10 | PASS | error |
| L09 | 有理见证：r=1/10 取等号；r=9/100 不成立；r=11/100 与历史值均严格成立 | PASS | error |
| L10 | 历史声称 0.1109141386 严格强于保底 1/10（故降级是真实的力量损失） | PASS | error |
| L11 | π > 3 > 0（Machin 定点整数证书，刻度 2^-64） | PASS | error |
| L12 | n=25 实例证书存在且 n==25：作用域=实例；证书显式声明不外推 | PASS | error |
| L13 | 输入 schema 完整（path/role/sha256）且重算哈希一致 | PASS | warn |
| L14 | 加强链状态 = not_certified，且阻塞义务与清单一致 | PASS | error |
| L15 | 条目表与脚本内审计事实源逐项一致（id/状态/等级），引用合法 | PASS | error |
| L18 | 严格判定路径中不含任何 JSON 浮点（只有 int/有理数字符串） | PASS | error |
| L19 | 证据等级/状态词表封闭 | PASS | error |
| L20 | 5% 判据阈值：U <= 20L/19；L=1/10 时精确为 2/19 | PASS | error |
| L16 | 记录条目与独立重算一致（篡改/删条目被抓） | PASS | error |
| L17 | canonical 负载 sha256 一致 | PASS | error |

`L09` 的四个见证是精确有理数：`100·(1/10)² − 1 = 0`（取等）、`100·(9/100)² − 1 < 0`（不成立）、
`100·(11/100)² − 1 > 0`、`100·(1109141386/10¹⁰)² − 1 > 0`（历史值若为真则严格更强）。
`L10` 把降级代价写成一个精确有理数：`0.1109141386 − 1/10 = 109141386/10¹⁰`。

### 2.3 π > 3 的整数定点证书（消去正 π 的合法性）

`verify/lowerbound_n100.py:103-122`：Machin 公式 `π = 16·arctan(1/5) − 4·arctan(1/239)`，
用 `Fraction` 精确部分和 + 交错级数余项界 `|R| ≤ 1/((2n+1)q^(2n+1))`（n = 24 项），
刻度 `2^-64` 得整数包围：

```
π ∈ [14488038916154245681/4611686018427387904, ...]  （下界 ≈ 3.1415926535897932）
下界 > 3·2^64   （整数比较，L11 PASS）
```

**附注（审计者观点）**：面积法只需要 `π > 0`，而 `π > 0` 本身是古典事实（例如单位圆内含
面积 2 的内接正方形）；Machin 证书比所需更强。保留它是为了把「消去正 π」这一步也落在
纯整数算术里，而不是靠引用。这里**没有**用 `math.pi`，也没有任何浮点。

---

## 3. 历史加强链 0.1109141386 的逐条审计

### 3.1 链的形态（`docs/notes-euler-clipped.md:125-148`、`tools/cell_bound.py:41-51,391-417`）

对覆盖构型取 **Voronoi 胞** `V_i = {x ∈ D : |x−c_i| ≤ |x−c_j| ∀j}`（它们铺满 D），
设 `m_i` 为胞 i 的平分线（直线）边数，`b` 为带非退化圆弧的「边界胞」数，`P` 为以
边界顶点为顶点的内接多边形。链是：

```
(L1) Σ_i (6 − m_i) = 6 + 2b                （一般位置；退化分支见 O1/O2）
(L2) max_Θ g(m,Θ) = f(m+1)，f(M) = (M/2) sin(2π/M)      （边界胞多一条边）
(L3) b ≥ π/arcsin r                        （弧覆盖）
(L4) π = Σ_i area(V_i ∩ P) + (π − area(P))（cap 恒等式）
(L5) area(V_i ∩ P) ≤ r² g(m_i,Θ_i)         （扇形分解；前提见 O4）
⟹ area(P) ≤ r² G，G = Σ_i g(m_i,Θ_i) ≤ n f(6 − (6+b)/n)（Jensen，前提见 O7/O8）
⟹ r ≥ sqrt(area(P)/G) ≥ sqrt(areaP_min(r,b)/gmax_clipped(n,b))
```

把 n = 100 代入并按 b 自洽（`b = ⌈π/arcsin r⌉`）的浮点不动点给出 **0.1109141386**。

### 3.2 条目表（唯一事实源：`verify/lowerbound_n100.py:chain_items()`；本表由
`python verify/lowerbound_n100.py --emit-markdown` 生成，与证书 `chain_items` 逐字一致）

| 条目 | 内容 | 状态 | 证据等级 | 引用 |
|---|---|---|---|---|
| P1 | 引理2：max_Θ g(m,Θ) = f(m+1)（边界胞 = 多一条边） | 已证 | 解析已证（通用） | `docs/notes-euler-clipped.md:102-109` |
| P2 | 引理3：弧覆盖 b >= π/arcsin r | 已证 | 解析已证（通用） | `docs/notes-euler-clipped.md:118-123` |
| P3 | 覆盖标准推论：V_i ⊆ B(c_i,r)（故胞顶点都在 c_i 的 r 邻域） | 已证 | 解析已证（通用） | `docs/goal-n100.md:16-25`<br>`docs/notes-euler-clipped.md:122-123` |
| P4 | cap 恒等式：π = Σ_i area(V_i ∩ P) + (π − area(P))，area(P) = ½ Σ_k sin g_k | 已证 | 解析已证（通用） | `docs/notes-euler-clipped.md:125-140`<br>`tools/cell_bound.py:41-51` |
| P5 | 自洽不动点方向：b = ⌈π/arcsin r⌉ 与 G(n,b) 对 b 单调递减 | 已证 | 解析已证（通用） | `tools/cell_bound.py:315-333`<br>`tools/cell_bound.py:391-417`<br>`docs/audit-lowerbound-n100.md §3.4` |
| P6 | 保底面积下界 L = 1/10（本阶段唯一已证普适下界） | 已证 | 解析已证（通用） | `docs/goal-n100.md:150`<br>`handoff-n100-research-plan-2026-10-11.md:20`<br>`verify/lowerbound_n100.py:310-516` |
| P7 | π > 3（整数定点 Machin 证书） | 已证 | 解析已证（通用） | `verify/lowerbound_n100.py:103-122` |
| I1 | n = 25 实例：S = Σ(6−m_i) = 6 + 2b（一般位置等号） | 仅实例支持 | 实例精确证书（只对该实例有效） | `verify/out/euler_clipped_n25.json:1-29`<br>`verify/euler_clipped_n25.py:526-543`<br>`docs/notes-euler-clipped.md:82-100` |
| I2 | n = 100 最好环构型的逐胞实测 + cap 诊断（浮点） | 仅实例支持 | 实例浮点测量（支持性，非判定） | `runtime/n100_cell_bound_repro_2026-10-12.txt:1-43`<br>`tools/cell_bound.py:445-476`<br>`docs/notes-euler-clipped.md:42-45`<br>`_recon/cap_diag.py:34-62` |
| O1 | 引理1 的退化分支（d ≥ 4 度顶点：d 点共圆） | 仅实例支持 | 少量构型数值核查（不构成通用证明） | `docs/notes-euler-clipped.md:64-67`<br>`docs/notes-euler-clipped.md:205-210`<br>`_recon/euler_degen.py:43-78` |
| O2 | 退化顶点落在 ∂D 上时 b 本身会变（S >= 6+2b 的这一支） | 未闭合 | 无证据（未闭合） | `docs/notes-euler-clipped.md:65-67`<br>`docs/notes-euler-clipped.md:207-210` |
| O3 | b 的良定义性：一个胞可能有多段边界弧 / 测度零接触点 | 未闭合 | 无证据（未闭合） | `docs/notes-euler-clipped.md:127-137`<br>`tools/cell_bound.py:216-232`<br>`verify/euler_clipped_n25.py:526` |
| O4 | 扇形分解前提：c_i ∈ V_i ∩ P（否则扇形铺不满 V_i ∩ P） | 仅实例支持 | 实例浮点测量（支持性，非判定） | `docs/notes-euler-clipped.md:141-143`<br>`docs/notes-euler-clipped.md:211-213`<br>`_recon/cap_diag.py:100-121` |
| O4' | cap 项的上界：cap_i <= ½(Ψ_i − sin Ψ_i)（弦长 = 该胞弧的弦） | 未闭合 | 无证据（未闭合） | `docs/notes-euler-clipped.md:125-137`<br>`tools/cell_bound.py:355-360`<br>`_recon/cap_diag.py:26-31` |
| O5 | 盘外中心：投影归约合法，但投影不给出 O4 的前提 | 未闭合 | 无证据（未闭合） | `docs/goal-n100.md:25`<br>`docs/notes-euler-clipped.md:211-213`<br>`docs/goal-n100.md:108` |
| O6 | 重合中心（c_i = c_j） | 未闭合 | 无证据（未闭合） | `tools/cell_bound.py:194-197`<br>`docs/notes-euler-clipped.md:48-62` |
| O7 | 共线三点/平行平分线：顶点跑到无穷、胞边数 m_i = 2 | 未闭合 | 无证据（未闭合） | `docs/notes-euler-clipped.md:58-62`<br>`tools/cell_bound.py:325-332`<br>`docs/notes-euler-clipped.md:111-116` |
| O8 | 冗余盘 / 空胞对 Jensen 求和的影响 | 未闭合 | 无证据（未闭合） | `tools/cell_bound.py:315-333`<br>`docs/notes-euler-clipped.md:111-116` |
| O9 | 边界退化等号情形：相切、单点弧、单中心边界极值 | 未闭合 | 无证据（未闭合） | `docs/notes-euler-clipped.md:64-67`<br>`docs/goal-n100.md:41` |
| O10 | 加强界的算术自洽性本身（不动点迭代收敛到 0.1109141386） | 仅实例支持 | 实例浮点测量（支持性，非判定） | `tools/cell_bound.py:391-417`<br>`runtime/n100_cell_bound_repro_2026-10-12.txt:1-43` |

等级词表（`verify/lowerbound_n100.py:GRADE_LABEL`）：
`analytic_proved`（解析已证，通用）/ `exact_instance_certificate`（实例精确证书）/
`float_instance_measurement`（实例浮点测量）/ `numeric_spot_check`（少量构型数值核查）/
`open_no_evidence`（无证据）。

### 3.3 逐条核账（判定 + 缺口）

**已证（可作为通用推理使用）**

- **P1 引理2**：`∂_Θ g = ½[cosΘ − cos((2π−Θ)/m)] = 0 ⟺ Θ = 2π/(m+1)`，代回得 `f(m+1)`；
  端点 `g(m,0) = f(m) < f(m+1)`、`g(m,2π) = 0`；另一支只给 m ≤ 1。3 行，解析已证
  （`docs/notes-euler-clipped.md:102-109`）。审计者复核：这一步对「一个胞有几段弧」是
  **逐弧**陈述（每条弧贡献一个被固定的角度），因此它本身不依赖 O3；但把它**聚合成**
  `E_i = m_i + 1` 才依赖「每胞一段弧」（见 O3）。
- **P2 引理3**：弧含于 `∂D ∩ B(c_i,r)`，端点都在 `B(c_i,r)` 内 ⟹ 弦长 ≤ 2r ⟹
  弧长 ≤ 2 arcsin r；b 段弧覆盖圆周（最多差有限个测度零点）⟹ `2π ≤ 2b·arcsin r`。
  审计者复核：该论证**对测度零接触点稳健**（零测弧不贡献长度），故 O3/O9 不削弱它。
- **P3**：`x ∈ V_i ⟹ |x−c_i| = min_j |x−c_j| ≤ r`（覆盖性给出某个 j）。标准推论。
- **P4 cap 恒等式**：`V_i ∩ P` 铺满 P（胞铺满 D、`P ⊂ D`），`V_i ∩ (D∖P)` 铺满 `D∖P`；
  `area(P) = ½Σ_k sin g_k` 是内接多边形面积公式。两条都是初等拼贴恒等式，只需 `P ⊂ D`
  与「P 的顶点在 ∂D 上」。**注意**：恒等式里的 `cap_i := area(V_i ∩ (D∖P))` 是「胞落在
  P 外那部分」的面积，把它**上界成某个圆缺**是**额外一步**，见 O4'。
- **P6/P7**：§2。
- **P5（审计者补出的算术方向，解析）**：`gmax_clipped(n,b) = n f(6 − (6+b)/n)` 对 b 递减
  （mbar 递减、f 在 [3,∞) 增）；`areaP_min(r,b)` 在 `b ≥ β := ⌈2π/(2 arcsin r)⌉` 上取**常量**
  （`tools/cell_bound.py:369-388` 里 k 被钳到 β−1）。由 Lemma 3，实际弧数/胞数 `b_actual ≥ β`，
  故 `G_actual ≤ gmax(n,b_actual) ≤ gmax(n,β)`，与 `area(P) ≥ areaP_min(r,β)` 合并得
  `areaP_min(r,β) ≤ r² gmax(n,β)`，即用 **b = β 的 G 与 A** 是**有效方向**。
  审计者另注：当 P 因为退化边界顶点而**边数 m > b** 时，`areaP_min` 的值不变（对 `m ≥ β` 是常量），
  所以「P 的边数到底是几」不影响 `areaP_min`；它影响的是 **b 的记账**（O3）。
  **未证部分**：把「对每个构型 r ≥ φ(r)」升级成「r ≥ 不动点 L*」需要 φ 单调或不动点唯一性，
  代码只跑 400 步浮点迭代，没有区间保证 —— 计入 O10。

**仅实例支持（不得外推）**

- **I1（n = 25 实例精确证书）**：`verify/out/euler_clipped_n25.json` 9/9 PASS：
  `b = 16`、`Σm_i = 112`、`S = 6n − Σm = 38 = 6 + 2b`、`E_s/E = 56/72`、
  `V = V_int + b = 32 + 16 = 48 = 2n−2`、`3V = 2E`（一般位置判据），判定全部在
  数域 `F = Q(√2,√3,√(2+√2))` 与二次扩域内用精确代数完成
  （`verify/euler_clipped_n25.py:526-543`）。**它认证的只是 n = 25 这一个精确构型的
  一般位置等号**：既不是引理1 的通用证明（退化分支完全没覆盖），更不是 n = 100 的普适性。
  证书里 `L12` 用整数比较强制 `n == 25` 且显式记录「作用域 = 实例、不外推」。
  另：`docs/notes-euler-clipped.md:216-219` 明确写「n = 25 本身不需要退化那支」——
  这句话只说明该实例绕开了退化，不能反过来当作退化分支已证。
- **I2 / O1 / O4 / O10（浮点测量与数值核查）**：见下文对应条目。全部是发现层数据。

**未闭合（不能作为已证下界的一部分）**

- **O1 引理1 退化分支（d ≥ 4 度顶点）**：方向有利的论证只是「d 度顶点裂成 d−2 个 3 度顶点
  要新增 d−3 条平分线边，故 Σ(6−m_i) 相对 6+2b **变大**」的草图；现有证据是
  `_recon/euler_degen.py:43-78` 对 6 个退化构型的**浮点**核查（中心+8 共圆 S = 26 ≥ 22、
  3×3 方格 S = 35 ≥ 22、6 点共圆 S = 29/30 ≥ 18/16，全部成立，
  `docs/notes-euler-clipped.md:78-80`）。浮点 + 4096 边形逼近不是证明。
- **O2 退化顶点落在 ∂D 上**：此时 **b 本身会变**（实测 `6 @ ρ=0.75`：退化解 b = 5、微扰后
  b = 6，`docs/notes-euler-clipped.md:65-67`）。b 同时出现在 `gmax_clipped` 的 mbar、
  引理3 的弧计数与 cap 拼接处，因此这一支不闭合则 `S ≥ 6+2b` 不能作为通用引理用。
- **O3 b 的良定义性（一个胞可能有多段边界弧）**：`V_i ∩ ∂D` 是凸集与圆周之交，本应是**单段弧**；
  但一旦出现**测度零接触点**（某胞只在 ∂D 上触到一点，或退化边界顶点把邻胞的弧切开），
  「#边界胞」与「#弧」就不再相等。引擎 `tools/cell_bound.py:216-232` 的实现是「取首个连续
  `circle` 标签段」当该胞的弧（隐含每胞恰一段），`n_boundary_cells` 统计的是弧角 > 1e-9 的**胞数**
  （`tools/cell_bound.py:280-281`）。b 在链上的三处含义——引理1（计数**边界胞**，Euler 记账）、
  引理3（计数**弧**）、cap 链（**b 段弧**拼出 P）——在退化时不一致：若某胞有两段弧，它应贡献
  两条有效边（`E_i = m_i + 2`），而不是 Lemma 2 的 `m_i + 1`。**无任何证明。**
- **O4 扇形分解前提 `c_i ∈ V_i ∩ P`**：`area(V_i ∩ P) ≤ r² g(m_i,Θ_i)` 的扇形分解要把
  `V_i ∩ P` 从 `c_i` 出发扇形铺开，这要求 `c_i` 落在该区域内（凸多边形的扇形分解前提），
  同时要求各扇形角 ≤ π（凸性保证）。两个最有名构型实测满足且有富余
  （n = 25 `max|c_i| = 0.884`、n = 100 `0.917`，均 < P 的内切半径 ≈ 0.981，
  `docs/notes-euler-clipped.md:141-143`；`_recon/cap_diag.py:100-121` 用 1e-9 容差做包含检查）。
  一般情形（尤其**边界胞**的圆心）没有证明。
- **O4' cap 项的上界**：链里用的 cap 上界是「弦长为该胞弧弦的那个圆缺」
  （`tools/cell_bound.py:355-360`）。但 `cap_i = area(V_i ∩ (D∖P))`，而 `V_i ∩ D` 是凸集，
  它**未必**含在那个圆缺里（凸集可以在远离自己弧段的地方贴近 ∂D）。要给出该上界需要一个
  贯通论证（例如「`V_i ∩ D` 的 ∂D-迹是单段弧 + 凸性 ⟹ 它落在弧-弦之间」），正文没有给出；
  现有的是逐胞浮点校验（`_recon/cap_diag.py:26-62`：`(area−cap)/(r²g) ≤ 1`）。未闭合。
- **O5 盘外中心**：题面明确允许圆心在 D 外（`docs/goal-n100.md:25`）。
  **合法归约**：把 c 投影到 D（凸集投影非扩张：`x ∈ D ⟹ |x − π(c)| ≤ |x − c|`），
  故**对覆盖半径**可设 `|c_i| ≤ 1` —— 这一步本身是已证的（`docs/goal-n100.md:108` 同款
  radical-axis/对称化清单里的「证书层可设对称」精神）。
  但 `|c_i| ≤ 1` **不蕴含** `c_i ∈ P`（P 内切半径 < 1），所以它**不解决 O4**；
  边界胞圆心恰好是最危险的一类（它们在 P 之外也可能在 D 边界附近）。
- **O6 重合中心**：`c_i = c_j` 时 Voronoi 退化（空胞或同胞），引擎对 `|c_i−c_j| < 1e-14`
  直接跳过平分线（`tools/cell_bound.py:194-197`），等价于人为打破重合。引理1 的证明用
  `F = n + 1`（n 个胞 + 外脸）与「每条直线边恰被两胞共用」——空胞会同时破坏这两句。
  未证明。
- **O7 共线三点 / 平行平分线**：引理1 的证明用「全部顶点 3 度、有限」（`V = 2n−2`、`E = 3n−3`，
  `docs/notes-euler-clipped.md:58-62`）；共线三元组使 Voronoi 顶点退化到无穷，m_i = 2 的
  平行带胞也会出现。另外 Jensen 步要求所有**非空**胞的有效边数 `E_i ≥ 3`（f 只在 M > 2 上凹，
  `docs/notes-euler-clipped.md:111-116`），而空胞 `E_i = 0`、退化胞 `E_i` 可能为 2。未逐类处理。
- **O8 冗余盘 / 空胞**：`gmax_clipped` 用 `Σ E_i ≤ 6n − 6 − b` 配 Jensen 得
  `n f(6 − (6+b)/n)`，隐式假定 n 个胞都非空、都满足 `E_i ≥ 3` 且 f 在其区间上凹。
  冗余盘（历史记账里的 `w(n)`「不干正事」的盘，`docs/notes-lowerbound-n100.md:118-131`）
  会造出小面积胞。未覆盖。
- **O9 边界退化等号情形**：覆盖用**闭**盘（`docs/goal-n100.md:41` 要求处理等号/退化），
  相切、弧退化为单点、单中心边界极值都必须单独处理；弧退化时 b、Θ_i、cap_i 同时退化，
  链上没有任何一处给出处理。
- **O10 不动点算术自洽**：即使上面的几何前提全部闭合，把逐构型不等式升级为常数下界还需要
  不动点/单调性论证（§3.3 的 P5 末尾）。代码是 400 步浮点迭代（`tools/cell_bound.py:391-417`），
  只保证「跑了并收敛」，不保证「解唯一」或「迭代值是下界」。

### 3.4 n = 100 的具体数字（0.1109141386）与口径核对

复跑 `python tools/cell_bound.py`（退出码 0，日志见
`runtime/n100_cell_bound_repro_2026-10-12.txt`）：

```
=== n=100 best ring ===  r = 0.123177917970  (n = 100)
  clipped Euler (b=33)     G <= 252.4779 -> r >= 0.1115483861 (-9.44%)   [conditional on b]
  [INVALID: no cap] arc covering  r >= 0.1113684992 (-9.59%)   [b* = 28]
  VALID (cap term, rigorous)  r >= 0.1109141386 (-9.96%)   [b = 29]
  VALID, best case b=33      r >= 0.1112115001 (-9.71%)
  [superseded] plane b=0    G <= 258.4850 -> r >= 0.1102445816 (-10.50%)
  classical density bound   = 0.1099636111 (-10.73%)
```

三点核对结论：

1. **数字可复现**：`0.1109141386` 与 `docs/notes-euler-clipped.md:169` 完全一致（b = 29）。
2. **该值不依赖构型**：`bound_clipped_cap(n)`（`tools/cell_bound.py:391-417`）只吃 n；
   n = 100 时给出 0.1109141386，与构型无关。因此上下界两侧的构型口径差异不影响它。
3. **口径差异（需在别处修正的记账问题）**：`tools/cell_bound.py:437-442` 的 `_n100_best()`
   读 `runtime/n100_polar_probe.json[0]`，其 `radius` 字段是 **0.123177917970**；而
   `docs/notes-euler-clipped.md:163` 与 `runtime/STATUS-n100.md` 提到的历史最好构型是
   **0.1223432713**。所以同一脚本打印的百分比不同（−9.96% vs 文献记录 −9.34%）。
   这**不影响** 0.1109141386 本身（第 2 点），但说明「相对百分比」的分母在仓库里有两个口径。
4. **同样重要**：`0.1109141386` 的成立**不依赖**任何构型数据、不依赖覆盖证书、
   不依赖 n = 100 的 100 个中心坐标 —— 它只依赖 n 与（未闭合的）几何引理。
   所以「下界侧」不需要等待构型输入恢复；反之，构型侧再精确也不能把这条链变成已证。

### 3.5 明确禁止的外推

- `verify/out/euler_clipped_n25.json`（9/9 PASS）是 **n = 25 单个精确构型**的
  **一般位置**等号证书。它**不**证明引理1（退化分支全缺），**不**证明 Lemma 2/3，
  **更**不能作为 n = 100 的普适性依据。证书 `L12` 与本文档都用整数比较把它钉在
  `n == 25` 的实例作用域上。
- 同样地，`_recon/euler_degen.py` 的 6 个退化构型、`_recon/cap_diag.py` 的
  `c_i ∈ P` 检查、`tools/cell_bound.py` 的逐胞实测，全部是**有限实例**证据，
  证据等级为 `numeric_spot_check` / `float_instance_measurement`，不构成通用陈述。

---

## 4. 复现记录

| 项 | 值 |
|---|---|
| 命令 | `python tools/cell_bound.py`（历史引擎，**未修改**） |
| 退出码 | **0** |
| 环境 | Windows 11；Anaconda Python 3.13.5；numpy 2.1.3；sympy 1.13.3 |
| 日志（UTF-8 无 BOM，27 71 字节） | `runtime/n100_cell_bound_repro_2026-10-12.txt` |
| 命令 | `python verify/lowerbound_n100.py` |
| 退出码 | **0**（19 个 error 级检查全 PASS，1 个 warn 级 L13 PASS；损坏证书自检 8/8 rejected） |
| 证书 | `verify/out/lowerbound_n100.json`（UTF-8 无 BOM） |
| payload sha256 | 见证书 `integrity.payload_sha256`（随 `generated_utc` 与输入哈希变动；设 `SOURCE_DATE_EPOCH` 可固定） |

**审计输入哈希**（证书 `inputs`，sha256 前 16 位；完整值见 JSON）：

| 输入 | 用途 | sha256(前16) |
|---|---|---|
| `docs/notes-euler-clipped.md` | 引理1/2/3、cap 恒等式与 §8 未闭合义务的正本 | `5b9148f5c42027f2` |
| `docs/notes-lowerbound-n100.md` | 历史 0.110914 的记录与放弃论证 | `ca93f9a61ba2b794` |
| `tools/cell_bound.py` | 逐胞引擎（浮点发现层） | `926ad269440a1c28` |
| `verify/euler_clipped_n25.py` | n = 25 实例精确证书脚本 | `7e1a00a5d014e0b8` |
| `verify/out/euler_clipped_n25.json` | n = 25 实例证书（仅实例） | `b65537e0030c7612` |
| `_recon/euler_degen.py` | 退化构型的数值核查脚本 | `85c0edaaf6c08d82` |
| `_recon/cap_diag.py` | cap 项与 `c_i ∈ P` 前提的数值核查 | `997a778503a37440` |
| `runtime/STATUS-n100.md.bak-stage1-20261012` | **固定**历史状态快照（含旧强度冲突标签） | `42b0c676eef49638` |

> 为什么用 `.bak-stage1-20261012` 而不是 `runtime/STATUS-n100.md`：最终 STATUS 会被修正，
> 用它当输入会形成「证书哈希随 STATUS 更新而失效」的循环。备份快照是固定历史来源，
> 其 sha256 = `42b0c676eef4963891cfd2ac028573e9055826a1a25769515a9cd780ee5283b8`
> （与 STATUS 文件里自述的哈希一致，`runtime/STATUS-n100.md:7`）。
> `L13` 默认是 **warn** 级：输入文件变了会报 stale，但不会把统一入口的退出码打成非零；
> 需要严格模式时用 `--strict-inputs`。

---

## 5. 降级的代价（5% 判据算术）

判据 `(U − L)/U ≤ 1/20`（U = 上交构型半径，L = 已证下界，U > 0）等价于 `U ≤ 20L/19`：

- 用**本阶段已证** `L = 1/10`：阈值 `U ≤ 20·(1/10)/19 = 2/19 ≈ 0.1052634`（精确有理，`L20` PASS）。
  当前候选的认证上界153/1250高于该阈值，因此本阶段交付的区间不满足5%判据。
  历史渐近密度数值不能充当有限n=100的普适下界；不能由它断言半径不超过2/19的构型不存在。
- 用**历史（未证）** `L = 0.1109141386`：阈值 `U ≤ 554570693/4750000000 ≈ 0.1167517`，
  即构型要改进约 4.6%；`docs/notes-lowerbound-n100.md:163-175` 记录四类搜索（220k+ 次评估）
  **未找到**该构型。

因此本阶段对 5% 判据的诚实结论是：**在已证强度下不达标**，且历史记录的达标路径
（加强界 + 构型改进）两侧都没有闭合证据。

---

## 6. 证书、schema 与接口

### 6.1 schema（`dsh.adb.n100.lowerbound.certificate/v1`）

```
schema, kind = "universal_lower_bound_area_only", generated_utc, stage
problem{n, domain, disks, objective, refs}
claim{lower_bound="1/10", strength, certified=true, scope, meaning}
strengthened_chain{status="not_certified", certified=false, historical_value,
                   historical_value_exact, historical_sources[], route, engine,
                   blocking_obligations[], reason, delta_vs_certified}
analytic_argument{statement, steps[S1..S7], no_symmetry_or_genericity_used,
                  rational_core_check}
arithmetic{ring, pi_certificate{method, pi_lower, pi_upper, used_for}, key_identities[]}
five_percent_criterion{definition, equivalent, with_certified_L, with_historical_L, comment}
inputs[{path, role, sha256}]            # 审计输入 + 哈希
input_schema{...}                       # 上述 inputs 元素的 schema
chain_items[20]{id, title, status, grade, refs[], note}
not_claimed[], out_of_scope[]
exact_checks[18]{id, title, pass, severity, detail?, numbers?}
integrity{payload_sha256, canonicalization}
self_test{corruption_cases[8]{case, expected_fail_check, rejected, failed_checks[]},
          all_rejected}
```

- **canonical 哈希**：`payload = 证书字段去掉 integrity 与 self_test`；
  `json.dumps(payload, sort_keys=True, separators=(',',':'), ensure_ascii=False).encode('utf-8')`
  的 sha256。
- **严格性自检**：`L18` 扫描 claim / exact_checks / chain_items / strengthened_chain / problem，
  只要出现任何 JSON 浮点就判 FAIL —— 保证「所有严格判定只整数/有理」。

### 6.2 `check_certificate` 接口

```python
import sys; sys.path.insert(0, "verify")
import lowerbound_n100 as LB
cert = json.load(open("verify/out/lowerbound_n100.json", encoding="utf-8"))
ok, report = LB.check_certificate(cert, base_dir=".", strict_inputs=False)
# report: {"ok", "all_pass", "checks": [...], "errors": [...]}
```

行为：用证书**自身的** `problem.n` / `claim.lower_bound` **独立重算** L01–L20（不读模块常量），
再 `L16` 与证书记录的 `exact_checks` 逐项比对（error 级比 pass，warn 级只比 id 集合），
最后 `L17` 校验 canonical 哈希。

### 6.3 CLI 与退出码

| 命令 | 行为 | 退出码 |
|---|---|---|
| `python verify/lowerbound_n100.py` | 生成 + 自检 + 损坏自检 + 写 `verify/out/lowerbound_n100.json` | 0（自检失败 1） |
| `python verify/lowerbound_n100.py --out DIR` | 写到干净目录 `DIR/lowerbound_n100.json`（不存在则创建） | 0 |
| `python verify/lowerbound_n100.py --check PATH` | 只校验外部证书 | 0 有效 / **2** 坏证书 |
| `python verify/lowerbound_n100.py --emit-markdown` | 打印 §3.2 的义务表 | 0 |
| `--strict-inputs` | 输入哈希不一致从 warn 升为 error | — |
| `--no-corruption-test` | 跳过损坏证书自检 | — |

**覆盖前先备份 + 去重**：目标证书已存在时，先写
`<name>.bak-<YYYYmmdd-HHMMSS>-<内容键12>`（内容键 = 文件字节把 `generated_utc` 与
`payload_sha256` 置空后的 sha256 前 12 位），再覆盖；**内容相同的重复运行不会重复造备份**
（实测第二次运行只复用同一路径）。本项目 AGENTS.md 的 `<file>.bak-<timestamp>` 约定照旧满足。

**可复现构建**：证书默认带当前 UTC 时间戳；设 `SOURCE_DATE_EPOCH=<秒>` 后两次运行产出
**逐字节相同**的证书（实测两个独立输出目录的 sha256 均为
`ce1642db6eda48c76b972efa3aa8f35486482d64d140fed1228a3c52d6d338a6`），
便于统一入口做跨运行哈希比对。证书里除 `generated_utc` 与 `payload_sha256` 外，
其余字段（claim / chain_items / exact_checks / inputs / self_test）在同一输入与同一代码下
是**确定性**的（实测逐行 diff 只差这两处）。

### 6.4 损坏证书自检（拒绝案例；`self_test.corruption_cases`）

| # | 案例 | 期望被抓的检查 | 实际失败检查 | 已拒绝 |
|---|---|---|---|---|
| 1 | `claim_strengthened_to_11/100` | `L04` | `L04`、`L05`、`L16`、`L17` | True |
| 2 | `n_changed_to_99` | `L03` | `L03`、`L16`、`L17` | True |
| 3 | `payload_hash_tampered` | `L17` | `L17` | True |
| 4 | `strengthened_chain_marked_certified` | `L14` | `L14`、`L16`、`L17` | True |
| 5 | `recorded_check_flipped_to_false` | `L16` | `L16`、`L17` | True |
| 6 | `float_smuggled_into_claim` | `L18` | `L18`、`L16`、`L17` | True |
| 7 | `open_obligation_flipped_to_proved` | `L15` | `L14`、`L15`、`L16`、`L17` | True |
| 8 | `exact_check_L05_deleted` | `L16` | `L16`、`L17` | True |

外部文件级验证也实测过：把 `claim.lower_bound` 改成 `11/100` 落盘后
`--check` 报 4 项 FAIL、退出码 **2**。

### 6.5 共享依赖披露

- 证书脚本**只依赖 Python 标准库**（`fractions` / `hashlib` / `json` / `argparse` / `pathlib` / `datetime` / `platform`），
  **不 import** `tools/cell_bound.py`、`numpy`、`sympy`。因此 §2 的算术认证与历史引擎
  **无共享代码**：前者是独立重写的整数/有理检查。
- 唯一的跨文件读数：`L12` 读 `verify/out/euler_clipped_n25.json`，但只取 `n`（整数比较）
  与 `all_passed` 字段，用来**限制**其作用域，不作为 n = 100 的任何证据。
- 未连接服务器、未执行新搜索、未修改 `tools/cell_bound.py` 或任何大盘下界引擎。

---

## 7. 实际完成 / 未决项 / 下一阶段建议

### 7.1 实际完成（本文件与产物可核对）

1. 历史 0.1109141386 链逐条核账：7 条已证（P1–P7）、3 条仅实例支持（I1/I2/O1/O4/O10）、
   9 条未闭合（O2/O3/O4'/O5/O6/O7/O8/O9 与 O10 的算术升级部分），每条带证据等级与 `路径:行`。
2. 保底普适有理下界 **L = 1/10**：解析测度论证（§2.1）+ 20 项整数/有理判定
   （§2.2 表：18 项 payload 级 + L16/L17 报告级）+ π > 3 的整数定点 Machin 证书（§2.3）。
3. 可运行证书 + `check_certificate` 接口 + 输入 schema/哈希 + 8 个损坏证书拒绝案例；
   CLI 退出码实测 0 / 2；`--out` 支持干净输出目录（供统一入口使用）。
4. 历史引擎复现（`python tools/cell_bound.py`，退出码 0），并指出构型口径差异与
   「该界不依赖构型」这一事实。

### 7.2 未决项（诚实清单）

- **0.1109141386 仍不是已证普适下界**：O1–O9 未闭合 → 本阶段标 `not_certified`。
  若要把它升级回来，最小工作量是：O4/O4' 的扇形与 cap 贯通论证、O1/O2/O3 的退化分类
  （建议做「以弧数 b_arc 为准」的重新记账）、O6–O9 的退化逐类处理、O10 的不动点论证。
- **n = 25 实例证书不能补这些洞**（§3.5），别把 I1 当成 n = 100 的普适性。
- **5% 判据在已证强度下不达标**（§5），因为 L = 1/10 的阈值是 2/19。
- **`r_D(100)` 精确值 / 极小多项式 / 局部最优 / 族内最优：未触及**（不属本侧范围）。
- 需要他人（主审计/STATUS 侧）修正的历史表述（我**不改**这些文件，只列位置）：
  `docs/notes-euler-clipped.md:6-8`（「两条有效普适下界」）、
  `docs/notes-lowerbound-n100.md:183`、`:206-212`、`:229`、
  `docs/goal-n100.md:223`、`:226-229`、`handoff-n100-research-plan-2026-10-11.md:26`。

### 7.3 阶段2 / 阶段4 建议（**仅建议，未执行**）

- **阶段2（结构搜索）**：本轮不启动。若要启动，建议先把「覆盖侧的候选完整性」做完，
  因为下界侧对构型不敏感（§3.4 第 4 点），构型侧的价值只能体现在上界 U。
  停止条件建议沿用：连续 N 轮同类随机搜索无改善即停，并记录每个候选的严格认证半径。
- **阶段4（有限见证点下界）**：若要真正把 L 提上去，绕开 O1–O9 的最短路径是
  「几何模式完整性 + 组合不可行」的见证点证书（有理阈值 + SAT/对偶不可行），
  它不依赖 Voronoi/Euler 记账，因此不受上述退化义务阻塞；但需要**精确有理**的
  见证点与半径，且必须先在小 n 上用已知最优值校准。建议规模：先在 n = 8/9/10
  与 n = 25 上跑通（答案已知，可判对错），再谈 n = 100。

---

## 8. 复现命令一览

```bash
# 1) 历史加强链的浮点复现（发现层，退出码 0；日志见 runtime/n100_cell_bound_repro_2026-10-12.txt）
python tools/cell_bound.py

# 2) 保底下界证书：生成 + 自检 + 损坏自检（退出码 0）
python verify/lowerbound_n100.py

# 3) 干净输出目录（统一入口推荐用法）
python verify/lowerbound_n100.py --out <clean_dir>

# 4) 校验一份既有证书（有效 0；坏证书 2）
python verify/lowerbound_n100.py --check verify/out/lowerbound_n100.json

# 5) 打印义务表（与证书 chain_items 一致）
python verify/lowerbound_n100.py --emit-markdown
```

---

### 附：本文件的自我限定

- 本文件**不**声称 n = 100 的全局最优性，**不**声称 0.1109141386 已证，
  **不**声称覆盖侧（上界）的任何结论，**不**声称历史构型 0.1223432713 的严格性。
- 本文件**不**写 `runtime/STATUS-n100.md`、**不**写 `docs/audit-baseline-n100.md`、
  **不**改统一入口、**不**改 `tools/cell_bound.py` 与任何大盘下界引擎。
- 本文件所有「判定」均为整数/有理算术；所有浮点数字只作为历史记录或发现层数据出现，
  且在证书里以字符串保存（`L18` 强制）。

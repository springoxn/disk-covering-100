# 阶段2 pilot 目标函数与启动器独立审查（review，非交付）

审查对象（只读，未修改任何被审文件）：

- `docs/pilot-plan-n100.md`（阶段2 计划）
- `tools/rings_cover.py`（现行目标函数机具）
- `verify/coverage_n100.py`（唯一严格判定路径）
- `runtime/run_server_pilot_n100.py`（启动器，nohup+pid 版）
- 输入：`runtime/freecover_n100.json`、`runtime/n100_polar_probe.json`
- 尚未交付：`tools/pilot_n100_stage2.py`（本文件不对其内容作任何判断）

本文件的所有数字都是**浮点发现层**或**精确证书层**的实际运行结果，来源与复现命令随文给出。
审查者本机复算（Anaconda Python 3.13.5 / numpy 2.1.3 / scipy 1.15.3），**未连服务器、未装环境、
未改动仓库内任何既有文件**。

---

## 0. 结论摘要

1. **目标函数的必要条件可以写成完备的有限候选集**（§1），且它有一个关键的单向性：
   报告值 **恒 ≤ 真实覆盖半径**，所以**只会低估，不会高估**；低估在报表上看起来正是"改进"。
   因此唯一合法的判定路径是 `verify/coverage_n100.py` 的精确证书，浮点值只能用来**猜 R**。
2. **对称性扇区限制是本次审查发现的最大阻断性错误风险**（§2）：在被审计的历史构型上，
   把中心挪动 4e-3 后真实覆盖半径升到 0.1235142，而 `k=8` 扇区目标函数**仍然报 0.1223433**
   （虚假改进 0.95%）。自由点候选一律必须走 `cover_radius_points(P, k=1, ...)`。
3. **旧机具 `rings_cover.py` 的预算账要按它自己算**（§3）：6000 次求值在它的 `mode="full"`
   下需要 ~80 min（超 30 min 预算），`mode="delaunay"` 下 ~36 s，而 Delaunay→full 回退是
   **静默**的（`rings_cover.py:202-208`）。**pilot 不 import 它**（自包含）：pilot 自己的实测是
   15.3 ms/次（Delaunay + 完整边界集）→ 6000 次 ≈ 92 s；即使完全没有 scipy（全部三元组路径）
   也只要 233 ms/次 → 6000 次 ≈ 1397 s（仍在 30 min 内）。所以 pilot 的预算**可行**；
   真正的问题是量级：100 自由点 = 200 维，6000 次只有 ~15 次坐标扫描，且 `--stall 150` 会让
   每个 run 在 ~152 次求值后停（§9.3）→ 实际只用到 ~1000/6000。
4. **紧化已经正式落地**（§4）：正式锚点
   `verify/out/pilot-n100-anchor/replay.json`（`all_passed=true`）在
   `R = 1223433/10000000 = 0.1223433` 上给出 49720 叶（cov 49316 / out 404）、max_depth 26、
   未决 0、3.53 s，并由**独立实现**复核（`independent.verified=true`、
   `generator_helpers_imported=false`、整数角点判据）。认证上界从 `153/1250 = 0.1224` 收到
   `0.1223433`。**证书不是瓶颈，构型才是。** 审查者自己跑过的收紧阶梯只是未经复核的诊断
   （§10.1），不作为证据。
5. **输入格式**（§5）：`freecover_n100.json` 与精确校验器的 `/best/P`+100 中心契约完全吻合；
   `n100_polar_probe.json` 是 105 条**环族描述**（非 100 个点），全部 n=100、半径可精确复算，
   但**最好的一条 0.1231779 比自由点基线差 0.68%**，且生成这 105 条记录的历史耗时合计
   **9235 s ≈ 2.6 h**（远超 pilot 的 1800 s 全预算）。
6. **启动器**（§6、§10.3）：nohup+`setsid`+`timeout`+持久 pid+状态三态+收集哈希校验+带时间戳
   备份这一轮改动**修掉了上一版的关键缺陷**；剩下的实质问题见 §10.3（pid 归属、
   `timeout` 与 pilot 内计时的相位差、deploy 守卫报错信息）。

---

## 1. 连续覆盖半径的完备有限候选集（必要条件）

对固定构型 `C = {c_1..c_n}`（圆心允许在单位闭盘 D 外），记

```
rho(C) = max_{x in D} d(x),   d(x) = min_i |x - c_i|,   D = {|x| <= 1}
```

这是**这个构型**的覆盖半径。`rho(C)` 是 `r_D(n) = inf_C rho(C)` 的上界来源；它本身对最优性
什么都不说。完备候选集：

| 类型 | 候选点 | 为什么完备 |
|---|---|---|
| 内部极大 | 任意三元组的**外心**（限于 `|u| <= 1`） | 内部局部极大 ⇒ 至少三个心等距且是最近心（Voronoi 顶点）；取全部三元组是**超集**，安全 |
| 内部退化 | 任意二心的**中点**；**原点** O | 共线/退化顶点与"Voronoi 顶点跑到无穷"的兜底 |
| 边界极大（二等距） | 对**每一对** `(i,j)`，其垂直平分线与单位圆的**两个交点** | 边界上 `d` 的极大若发生在两个心打平的折点，该点必同时满足 `|x|=1` 与 `|x-c_i|=|x-c_j|` |
| 边界极大（单中心） | 每个 `c_i != 0` 的**反向极值** `-c_i/|c_i|` | 单心最近时 `d` 限制在圆周上的驻点只有 `±c_i/|c_i|`，其中只有反向点是极大 |

两条必须写进验收的性质：

- **单向性（安全性）**：候选集里每个点都在 D 内，所以对任意子集 `U ⊆ D` 都有
  `max_{x in U} d(x) <= rho(C)`。**候选集不完整只会低估**——不会让一个坏构型看起来合格，
  但会让一个坏构型看起来"改进了"。
- **完备性（正确性）**：开 Voronoi 边上 `d` 是严格凸的（沿边中点是极小），所以内部极大必是
  顶点而非开边上的点；边界极大只有上述两种。故上式取等当且仅当候选集含一个全局最大点。

**审查者独立复算**（`runtime/freecover_n100.json` 的 `/best/P`，全部 161700 个三元组 +
4950 对 + 99 个对跖点 + 200 万点网格）：

| 候选类型 | 数量 | `max d` |
|---|---|---|
| 内部：全部三元组外心（`|u|<=1`） | 124596 / 161700 | **0.12234327132827788** |
| 内部：Delaunay 三角形外心 | 183 三角形 | 0.12234327132827787 |
| 边界：全部对的平分线×圆 | 9900 | 0.12162188188690415 |
| 边界：Delaunay 边的平分线×圆 | 564 | 0.12162188188690409 |
| 边界：对跖点 | 99 | 0.10508133053184779 |
| 密网格（2 008 036 点） | — | 0.12230124083895828（按定义是下界） |

- 完备候选集给出 `rho = 0.12234327132827788`，与历史发现值 `0.12234327132827787` 一致到 1e-17；
  最优点在 `(0.847619, ±0.489373)`（`|x| = 0.9787`，**内部** Voronoi 顶点，不在边界上）。
  **修正（按审查纪律）**：`0.12234327132827788` 是**浮点发现**，不是严格下界——候选集在数学上
  是完备的（故"精确计算的话"取等），但它的取值没有精确/区间算术复核，按本仓库纪律
  （`verify/` 的判定只用整数与有理数）不得称证书或下界。可严谨陈述的只有：
  `rho(C) <= 153/1250`（已证，覆盖侧）以及 `rho(C) ≈ 0.1223432713282779`（浮点发现）。
  `r_D(100)` 的已证下界仍然只有 `1/10`（`docs/audit-lowerbound-n100.md:24`）。
  pilot 侧对此的处理是正确的：候选只写"float discovery"，并明确要求交给精确校验器。
- Delaunay 模式与全枚举一致到 1e-17 ⇒ `mode="delaunay"` 作为**发现**层可用（与
  `docs/notes-n100-rings.md:153-155` 的说法一致）；但它仍只是发现。
- `mode="sub"`（三元组抽稀）在**这个**构型上凑巧没漏（cap=4000/20000 都得同一值）——
  所以"冒烟测试通过"**不能**用来证明抽稀路径可用；任何判定都不得使用 `mode="sub"`。
- 退化计数必须记录：本构型 161700 个三元组里 **4288 个 `|det| <= 1e-15`** 被静默丢弃
  （`rings_cover.py:221`）；`|c_i| = 0` 的对跖点被跳过（`:261`）；共圆输入会让 Qhull 抛异常
  并触发 `:207` 的静默回退。这些都要进日志。

---

## 2. 阻断性风险：扇区（C_k）限制只在构型真的 C_k 不变时才合法

`critical_points` 把所有候选点过滤到 `[0, 2π/k]`（`rings_cover.py:273-283`），docstring 用的
是"轨道必与闭合扇区相交"的论证（`:41-43`、`docs/notes-n100-rings.md:29-30`）。该论证**依赖
构型在 C_k 下不变**。实测两种失效：

| 构型 | 真实 `rho`（k=1 全枚举） | `k=8` 扇区目标 | 低估 |
|---|---|---|---|
| 随机非对称 40 点 | 0.582177736986 | 0.375810352875 | **−35%** |
| 历史构型（六方格点，实为 C_6） | 0.122343271328 | 0.122343271328（**恰好**命中） | 0 |
| 历史构型把 `c_0=(0,0)` 挪 0.004 | **0.123514165403** | **0.122343271328** | **−0.95%（虚假改进）** |

第三行是本次审查最有价值的反例：挪动中心盘后真实半径**变大**（近原点出现 0.1235 的洞），
而 `k=8` 目标函数仍报旧值 `0.1223433`——因为新最大点落在 150°，不在 `[0°,45°]` 扇区，
而构型又不是 C_8 不变。历史构型上 `k=11` 同样"恰好"给出正确值（实际是 C_6 轨道里的 30° 落在
`[0°,32.7°]` 内），**这是运气，不是正确性**。

结论（对 pilot 的硬约束）：

- `--ring-input` 里的环族可以继续用 `cover_radius(k, rings, centre)`（那些构型在构造上就是
  C_k 不变的，`build()` 里 `m % k == 0`，`rings_cover.py:103-104`）；
- 一旦出现**自由边界层/自由点**，必须 `cover_radius_points(P, k=1, ...)`；
- 若 pilot 声称某候选的对称群是 C_k，必须有**独立的对称性检验**（例如把点集与旋转后的点集
  做精确/带容差比对）并把群记录在产物里；否则默认 k=1。

---

## 3. 预算核算：6000 次求值 / 30 min 与机具的实际代价

实测单次目标函数求值（同一历史构型，N=100）。**左半是旧机具 `rings_cover.py`，
右半是已交付的 pilot（自包含、不 import 旧机具）**：

| `rings_cover.py` 路径 | 单次 | 6000 次 | pilot 路径 | 单次 | 6000 次 |
|---|---|---|---|---|---|
| `mode="delaunay"` | 0.0060 s | ~36 s | `mode="objective"`（Delaunay + 完整 4950 对边界） | **0.0153 s** | **~92 s** |
| `mode="sub"`, `triple_cap=6000` | 0.0937 s | ~9.4 min | —（pilot 无抽稀路径） | — | — |
| `mode="full"` | 0.795 s | **~80 min** | `mode="full"`（全部 161700 三元组） | **0.233 s** | **~1397 s** |

pilot 的 `mode="objective"` 比旧机具的 Delaunay 路径慢 2.5×，因为它**每次都对全部 C(100,2)
对算边界候选**（这是 §1 要求的完备性，是正确取舍）。因此对 pilot 而言：有 scipy 时 6000 次
≈ 92 s；**即使 Delaunay 持续失败/无 scipy，改走全部三元组也只是 1397 s，仍在 30 min 内**
（我先前按旧机具算出的 "80 min" 不适用于 pilot）。真正的问题不是单次代价，而是量级与停止规则
（见 §9.3）。

三个具体问题（针对旧机具 `rings_cover.py`；pilot 不 import 它，但第 3 条对 pilot 同样适用）：

1. **静默回退会击穿预算**：`critical_points` 把 Delaunay 的任何异常吞掉并改走 `full`
   （`rings_cover.py:202-208`）。一次回退把每次求值从 6 ms 变成 0.8 s（×130）。
   pilot 必须把实际 mode/回退次数记入产物，并把预算检查放进**被包装的目标函数内部**。
2. **现有代码无法强制 6000**：`pattern_search` 返回 `nfev` 但 `_local_solve` 把它丢掉
   （`rings_cover.py:443`），而随后 Nelder-Mead 的 `maxiter=40*(2q+1)`（`:449-451`）在 scipy 默认
   `maxfev` 下可达约 2000 次评估；`optimize_rings` 每轮结束还会做一次**不计入预算**的
   `mode="full"` 全审计（`:523`、`:534`）。6000 必须由 pilot 自己的计数器兜住（见 §7 清单）。
3. **维度上不可行**：100 个自由点 = 200 维；一次坐标扫描 = 400 次求值；
   6000 次 ≈ **15 次扫描**（`h0=0.08` 时连一次完整收敛都做不到）。所以计划里的
   "自由边界层"在 6000 次预算内**只能是局部微调**，不是搜索。可动的只有低维环族
   （`2q ≈ 10–14` 维）。这一点建议写进 pilot 的显式声明，而不是让它跑完再解释。

旁证（历史代价标尺）：生成 `n100_polar_probe.json` 的 105 条环记录累计 **9235 s ≈ 2.6 h**
（记录自带 `seconds`，均值 88 s/条）；而 pilot 全部预算是 1800 s。

---

## 4. 紧化：正式锚点 `R = 0.1223433`（已复核）与审查者的未复核诊断

`verify/coverage_n100.py` 的精确四叉树在 `R > rho` 时必然终止，代价由最深的洞决定。

**正式证据（唯一可引用）**：`verify/out/pilot-n100-anchor/replay.json`，`all_passed=true`：

| 字段 | 值 |
|---|---|
| `radius` / `generator_result.R_exact` | `1223433/10000000` = 0.1223433 |
| `generator_result.n_leaves_checked` | 49720（cov 49316 / out 404，未决 0） |
| `generator_result.max_depth` | 26 |
| `elapsed_seconds` | 3.53 |
| `independent.verified` | true（`n_leaves=49720`、`n_covered=49316`、`n_outside=404`、`max_depth=26`、`prefix_free=true`、`kraft_complete=true`） |
| `independent.method` / `generator_helpers_imported` | 整数角点判据 / **false**（不共享生成器几何函数） |
| `source_sha256` | `36286ebc…a92e`（= `runtime/freecover_n100.json`） |

**审查者的诊断（⚠️ 未落盘、未经复核，仅供趋势参考，不得引用为证据）**：我用**同一个生成器**
在进程内跑过一条收紧阶梯（未写任何文件）：

| R（我跑的） | 叶数 | 深度 | 未决 | 秒 |
|---|---|---|---|---|
| 153/1250 | 22804 | 16 | 0 | 1.6 |
| 122344/1000000 | 38392 | 22 | 0 | 2.3 |
| 1223435/10000000 | 42460 | 23 | 0 | 3.8 |
| 12234328/100000000 | 53824 | 28 | 0 | 2.3 |
| 122343272/1000000000 | 62728 | 32 | 0 | 2.7 |
| 1223432715/10000000000 | 67684 | 34 | 0 | 2.9 |
| 1223432/10000000（低于 rho） | 18776 | 12 | **800** | FAIL |

**与我数字的差异已核对清楚（不是矛盾）**：我的最紧一点是 `R = 0.1223432715`（距浮点 rho
1.7e-10），而正式锚点是 `R = 0.1223433`（距 rho 2.9e-8），**两者 R 不同**。正式锚点恰好落在
我两个相邻点之间（0.1223435 → 42460 叶/深度 23；0.12234328 → 53824 叶/深度 28），
49720 叶与深度 26 与这条趋势一致；`out=404` 在我所有点和正式点上都相同（外叶与 R 无关）。
因此"67684 叶 / 深度 34"只是**更紧的 R** 下的诊断值，**不构成与正式锚点的分歧**，也不被本文件
引用为证据。

- 未复核诊断中 `R = 0.1223432`（低于 rho）给出 800 个未决叶并 FAIL ⇒ 生成器非空（fail-closed），
  与 `coverage_n100.py` 的 vacuity 对照一致。
- 结论不变：**证书粒度不是瓶颈**——0.1224 可以收到 0.1223433（已复核），pilot 的诚实门槛是
  `R_anchor = 0.1223433`（否则退回 `153/1250`），且必须在**同一个有理 R** 上出证书。

---

## 5. 候选输入格式审查

### 5.1 `runtime/freecover_n100.json`（作为 `--baseline-input`）——可用

结构 `{n, best:{seed, r, P[[x,y]×100]}, all_r, hex_init}`；`best.P` 是 100 个十进制字面量。
与精确校验器的契约完全吻合：`coverage_n100.py:100` 硬编码 `SOURCE_POINTER='/best/P'`，
`:178-179` 要求**恰好 100 个中心**，`:173-177` 用 `parse_float=str` 把十进制读成
**精确有理数**。注意两条隐含要求：

- pilot 的输出必须能变成 `{"best": {"P": [[x,y]×100]}}` 这样的文件（十进制全精度字面量），
  否则不能直接送进 `--mode gen`；
- `check_certificate` 要求**中心互异**（`coverage_n100.py:521-522`），重复中心会让证书 FAIL，
  pilot 必须去重（并记录做了什么）。
- 中心允许在 D 外（本构型 85/100 在盘内、15 个在外，证书照样成立）；若 pilot 做投影归约
  （数学上 WLOG 合法），必须作为显式步骤记录，不能悄悄改坐标。

### 5.2 `runtime/n100_polar_probe.json`（作为 `--ring-input`）——可用，但方向不对

105 条记录，键 `{k, centre, mults, rings[(m,ρ,φ)], radius, argmax, x, seconds}`，按半径升序。
审查者全量复核：

- **105/105 都是 n=100**（`centre` + `Σmults`），无脏记录；
- 前 6 条用 `rings_cover.cover_radius(k, rings, centre)` 重算，与存储的 `radius` 一致到 1e-12
  （例：k=11 → 0.123177917970 完全一致）⇒ 输入自洽；
- **但 105 条里没有一条好于 0.1224**，最好的一条（k=11 + 中心，`[11,11,22,22,33]`）
  是 **0.1231779，比自由点基线 0.1223433 差 0.68%**。
  ⇒ 只在这个环族里跑的 pilot **不可能**改善认证上界；环输入应定位为多样性/回归输入，
  真正的改进路径只有自由点侧（而 `docs/notes-lowerbound-n100.md:163-175` 记录的
  220k+ 次评估四类搜索全部无法改进 0.1223432713）。
- 记录里**没有随机种子字段**，`x` 只是优化器原始向量；计划要求的"确定种子"必须由 pilot
  自己记录。
- 该文件 103 KB，含 105 条而非单条；pilot 的 `--ring-input` 解析必须明确"取哪一条"
  （建议取 `min(radius)`，即第 0 条，并记录 index 与完整 ring 参数）。

### 5.3 未证数字的传染风险

`runtime/n100_anneal.json` 里有 `target: 0.116752`，它正是**未证**历史界 0.110914 除以 0.95
得到的 5% 判据阈值（`docs/audit-lowerbound-n100.md:332-337`）。当前启动器没有把它传给 pilot
（好），但 pilot 若自行读取任何 `target`/`0.116752`/`0.110914` 作为停止或验收条件，就等于把
未证数字引进了判定。**唯一可用的锚点是**：已证下界 `L = 1/10`、已证上界（构型）`153/1250`
（或按 §4 收紧后的 `0.1223433`）。`0.1109141386` 在 `docs/notes-lowerbound-n100.md:183,206-212,229`
仍被写成"已证"，这些位置已在 `docs/audit-lowerbound-n100.md:460-463` 列为待修正——
在修正前，pilot 侧必须自行把它当**未证**。

---

## 6. 启动器审查：`runtime/run_server_pilot_n100.py`（nohup + 持久 pid 版）

改进确认：`nohup /bin/bash -c <wrapper> </dev/null > launcher.log 2>&1 &` + `printf "$!"` 让
远程进程不再依赖本地 SSH 通道生命期；`exit_code` 改为 `collect` 阶段写入；这两点是对的。
逐条实质问题：

### 6.1 阻断级

1. **`collect` 无法区分"还在跑"与"跑完"，并且会读到陈旧退出码。**
   `:49` 无条件读 `exit-code.txt`。REMOTE 目录是**固定复用**的，`run` 阶段
   （`:34-44`）**不清理**上一次的 `exit-code.txt`。所以：(a) pilot 还在跑时 `collect` 会
   `FileNotFoundError` 直接抛栈；(b) 若目录里残留上次的 `exit-code.txt`，`collect` 会把
   **上一次的退出码**写进本次 record 并据此 `sys.exit`。
   修法：`run` 启动时删除/改名旧的 `exit-code.txt`、`launcher.log`；`collect` 先做
   `kill -0 <pid>` 与 `test -e exit-code.txt` 双重检查，区分 `running / finished / unknown`
   三种状态，绝不在 `running` 时写 `exit_code`。
2. **远程没有硬超时。** 现在唯一的 30 min 约束是 pilot 自己的 `--seconds 1800`。
   若 pilot 没实现或没兜住，进程会无限跑（且 `started.json` 已存在，无法重跑）。
   修法：wrapper 前面加 `/usr/bin/timeout -k 30 1800 ...`，并把 124/137 记为
   "timeout/budget" 而不是崩溃（这是与 pilot 内计时**互为独立**的第二道闸）。

### 6.2 高

3. **记录的 pid 不是可靠的取消句柄。** `$!` 拿到的是 `nohup` exec 出来的
   `/bin/bash -c <wrapper>` 的 PID，而 wrapper 里是多条命令（`cd && python ; rc=...; printf;
   exit`），bash 不会把 python exec 掉，python 是它的**子进程**。`kill <pid>` 只杀 wrapper，
   python 可能变成孤儿继续吃 CPU。
   修法：`setsid` 起新进程组并记录 pgid，取消时 `kill -TERM -<pgid>`；或让 pilot 自己写
   `out/pilot.pid`，并提供一个 `stop` action。启动器目前**没有** stop/取消路径。
4. **本地记录不自包含。** `record['stdout']` 在 nohup 模式下恒为空，真正的证据
   （`run.log`、`launcher.log`）留在服务器上；`collect` 只在 `pull_dir` 成功时才有内容，
   传输失败就什么都不剩。修法：`collect` 时把 `tail -n 200 run.log`、`sha256sum run.log`、
   `wc -c run.log`、以及远程 `date -u` 起止时间写进 record 再落盘。
5. **运行记录缺 provenance。** `server-run-n100-stage2.json` 里没有代码哈希、没有解释器与
   numpy/scipy 版本、没有与 `server-deployment-n100-stage2.json` 清单的关联；计划要求每次
   运行记录"代码哈希"。修法：run/collect 时把 manifest 哈希（或运行前重算的远端哈希）+
   `python -c "import sys,numpy,scipy"` 版本并入 record，并要求 pilot 在自己的产物里自嵌
   `code_sha256`。

### 6.3 中/低

6. **`int(pid)` 解析脆弱**（`:42-43`）：任何多余 stdout（banner/警告）都会 ValueError，
   而这时**任务已经启动**，record 却没写。修法：先落盘原始 stdout，再容错解析，
   失败时回退到远端 `run.pid`。
7. **`collect` 覆盖 `runtime/n100-stage2-server/` 无备份、无哈希校验**（`:47-49`），
   与仓库 `<file>.bak-<timestamp>` 约定不符；`record_path.with_suffix('.json.bak-before-collect')`
   （`:54`）的备份名固定，第二次 `collect` 会覆盖第一次的证据。修法：带时间戳、且当
   record 已有非空 `exit_code` 时拒绝重复 collect。
8. **没有启动即失败检测**：`python` 路径错会得到 exit 127，但只有到 `collect` 才知道。
   建议 launch 后 `sleep 3; kill -0 <pid>` 做一次存活探测并写入 record。
9. **`deploy` 的两个老问题**（`:22-32`）：`test ! -e started.json` 失败时抛出的信息是
   `remote exit 1: ...`，读起来像传输坏了，其实是"已经跑过"的守卫；多文件推送中途失败会留下
   半成品目录且不写 manifest（可重跑覆盖，风险低但应说明）。
10. **接口契约未验证**：`--max-evals 6000 --seconds 1800 --baseline-input --ring-input --out-dir`
    必须与 pilot 的 argparse 逐个对齐，否则远端 exit 2。脚本未交付前这项只能是待验项。

---

## 7. 交给 pilot 的验收清单（因为脚本未交付，这是可执行的最小要求）

1. **预算**：包装目标函数计数**每一次**调用（含审计与 Nelder-Mead polish），加
   `time.monotonic()` 截止；超限抛专用 `BudgetStop`，产物流水账记录
   `stopped_by: evals|seconds|plateau` 与未处理账本；**不得**把中断写成完整。
2. **模式与退化**：记录实际 mode、Delaunay 回退次数、`|det|<=1e-15` 三元组数、
   对跖点跳过数、重复中心处理；`mode="sub"` 禁止出现在任何判定路径。
3. **对称性**：自由点一律 `k=1`；若声明 C_k，附独立对称性检验与记录。
4. **候选产物**：全精度十进制 100 心、**互异**，形状可直接被 `/best/P` 读取；
   记录每个入选候选的 `R_cert`、精确生成器的退出码/叶数/未决数。
5. **深洞与接触图**：在**明确写出的有理 R** 上算接触图（本构型在 `R=153/1250` 与 `rho` 上
   完全相同：261 边、1 个连通块、度分布 `{2:3,3:12,4:9,5:12,6:64}`，所以"接触图相同"
   在 `[rho, 153/1250]` 上**不敏感**，不能单独当停止条件）；应保存**洞的三元组结构**
   （定义每个 argmax 的三个心）与规范哈希。
6. **不许声称改进**：只有精确生成器在 `R < R_anchor`（`0.1223433` 或 `153/1250`）上 PASS
   才算改善；浮点值、`0.110914`、`0.116752` 一律只能作为发现层记录。

---

## 8. 复现命令（本机，全部只读；工作目录 `E:\study\ADB`）

```bash
# 完备候选集 / Delaunay 对比 / 网格 / 子抽稀 / 接触图 / 目标函数计时
python C:\Users\lenovo\AppData\Local\Temp\rev_n100\calib.py

# 精确证书收紧阶梯（进程内调用 verify/coverage_n100.py 生成器，不落盘）
python C:\Users\lenovo\AppData\Local\Temp\rev_n100\tighten.py
python C:\Users\lenovo\AppData\Local\Temp\rev_n100\tighten2.py

# 环输入自洽性与质量复核
python -c "import json,sys;sys.path.insert(0,r'tools');import rings_cover as RC;d=json.load(open(r'runtime/n100_polar_probe.json',encoding='utf-8'));print(all(RC.disk_count(int(x['k']),x['rings'],x['centre'])==100 for x in d),min(x['radius'] for x in d),sum(x['seconds'] for x in d))"
```

```bash
# pilot 自检（已交付后重跑；写入临时目录，不污染仓库）
python tools/pilot_n100_stage2.py --selftest --out-dir <TEMP>/n100-pilot-selftest

# 只读探针：不编辑 pilot，import 后直接跑它自己的加载器/求值器/预算器
python C:\Users\lenovo\AppData\Local\Temp\rev_n100\probe_pilot.py <TEMP>
```

审查者本机实测环境：Python 3.13.5 (Anaconda)、numpy 2.1.3、scipy 1.15.3；**未**在服务器上
执行任何命令，**未**修改 `tools/rings_cover.py`、`verify/coverage_n100.py`、
`runtime/run_server_pilot_n100.py`、`tools/pilot_n100_stage2.py` 或任何证书。

---

## 9. `tools/pilot_n100_stage2.py` 审查（已交付；审查快照见 §9.0）

审查方式：读代码 + **在本机临时目录实跑**（`--selftest` 与 `--max-evals 600` 的完整 6-run 流程）
+ 一个**只读探针**（`probe_pilot.py`：import 该模块，不编辑它，直接调用 `load_baseline_centers`
/ `load_ring_records` / `CoverEvaluator.evaluate` / `search_run` / `main`）。

### 9.0 审查快照与一次重要的时序事实

该文件在我审查期间**被改过至少两次**（行数 1862 → 1865 → 1866 → **1881**）。我实跑到的
**第一个**快照（`--selftest` 与 `--max-evals 600` 两次运行）**exit 1，且是自检自身失败**：
`negative control: wrong count (99 centres)` 被判为 **未拒绝**，于是
`calibration FAILED; refusing to start the pilot` ⇒ **pilot 在任何搜索开始前就退出 1**。
根因是自检把 `validate_centers(arr, name)` 用在 99 中心的负对照上，而没有传
`n_expected`，而 `validate_centers` 只在 `n_expected is not None` 时校验数量
（真正的搜索路径不受影响，因为 `evaluate` 传了 `n_expected=N_CENTERS`）。

**当前快照（sha256 `ff1180a254c896bb…2d60`，1881 行）已修掉这一处**：
`:1372` 现在是 `validate_centers(arr, name, n_expected=N_CENTERS)`，我重跑 `--selftest`
得 **22 cases / 0 failed / PASS**。给部署方的要求：**部署前把 hash 写进 manifest 并确认
selftest PASS**——这个文件仍在变动，我下列结论只对 `ff1180a2…` 这一版负责。

### 9.1 阻断级（当前快照下仍存在或需确认）

1. **两个"预算"相位不一致，会把干净的预算停止变成 SIGTERM。**
   启动器现在是 `/usr/bin/timeout -k 10 1800 <python pilot --seconds 1800>`：`timeout` 从
   **进程启动**算 1800 s，而 pilot 的 `Clock` 在 `:1744` 创建——**在校准之后**（`:1716`）。
   校准本身要跑 n≤20 的一批 case + `_grid_refine_max`（601² 网格）+ 4096 点密集边界扫描。
   于是 pilot 计划跑到的墙钟时刻是 `t_calib + 1800 - reserve`（reserve = max(20, 54) = 54 s），
   只要 `t_calib > 54 s`，**外层 timeout 会先到**：进程被 SIGTERM（10 s 后 SIGKILL），
   `n100_stage2_result.json` 不写、候选 JSON 不写，只剩 `checkpoint.json`，退出码 124/137 也
   与"预算正常停止"混在同一个字段里。
   修法（任一）：pilot 在 `main` 开头就建 `Clock`（把校准计入 `--seconds`，这也符合计划里
   "本地累计30分钟"的口径）；或启动器传 `--seconds $((1800 - 校准预留))` 并把
   `timeout` 放大到 1800+校准；或校准只跑一次并把 `selftest.json` 复用。
   **请先在本机量一次 `--selftest` 的墙钟**（我这边 selftest 明显不是秒级），再定这两个数。
2. **残留的"best 丢失"路径：全局配额先到时仍然会丢候选。**
   当前快照在循环顶部加了保护（`:970-974`：`run_evals >= per_run_evals - 2` 就停，
   给最后那次 all-triple 交叉检查留额度），我实测 `per_run_evals=5` 时
   `stop_reason=run_quota_reserve_for_final_check`、`has_best=True`、`has_diagnostics=True`
   ——**这条已修好**。但该保护只检查**per-run** 计数：若 `--per-run-evals` 被显式设成
   `len(plan)*per_run > max_evals`，则会由**全局**配额在 `ev.evaluate` 里抛
   `BudgetExhausted("global_evals_reached")`，随后 `:1027` 的强制 `mode="full"` 交叉检查
   再次 charge 并抛出 ⇒ 整个 `best` / `diagnostics` / 候选 JSON 块被跳过（与 9.0 的机制同源）。
   启动器当前的调用（`--max-evals 6000`、6 runs、per-run 自动 = 1000）**不触发**它，
   属潜在缺陷。修法：保护条件同时看全局（`global_evals >= max_evals - 2`），
   或给最终交叉检查/诊断一个**不计入配额**的独立通道。

### 9.2 几何与初值：结论是好的（附实测）

- **数学核心与 §1 的完备候选集一致**：`(I)` 内部 = 全部 Delaunay 单形外心（无 scipy 时全部
  C(n,3)）；`(B1)` **全部 C(n,2) 对**的平分线×单位圆交点；`(B2)` 全部对跖点；`(B3)` 四个坐标轴
  安全点。`mode="objective"` 用在搜索里，`mode="full"`（全部三元组）用于校准**以及每个 run
  结束时的强制交叉检查**；`:1031` 在 `full - objective > 1e-6` 时抛 `DiagnosticError`，
  并且记录半径取 `max(objective, full)`（`:1036-1041`，宁大不小，方向正确）。
- **退化与异常纪律正确**：`validate_centers` 显式拒绝 NaN/Inf、形状错、数量错（传了
  `n_expected`）、间距 <1e-9 的近重合；共线三元组被跳过**并计数**；`|c_i| = 0` 的对跖点跳过并计数；
  `evaluate` 只 `charge` 后即放行，**不吞异常**；`search_run` **只**捕获 `BudgetExhausted`，
  其它异常一律冒泡到 `main` 写 `failed_run.json` + exit 1。校准里还有
  "注入目标函数异常必须原样抛出"的负对照（`:1368-1385`）与 `_fatal_run_probe`（`:1445`）——
  这两条正是历史上的 1e3 事故的解药。
- **对称性风险不存在**：pilot 全程以**自由点集**工作，没有任何扇区/C_k 过滤，也不 import
  `rings_cover.py`（自包含）；`--ring-input` 只被用来**物化成点集**（`ring_points`），
  之后按自由点处理。§2 的 0.95% 虚假改进风险因此不适用于本脚本。
- **真实输入实测**（探针，非证书）：`Delaunay` 在 100 点六方格点补丁上**成功**
  （`source="scipy.spatial.Delaunay (all simplices)"`，`delaunay_failures=0`），
  `mode="objective"` 与 `mode="full"` **完全一致**（差 0.0）：
  **0.12234327132827873**（历史浮点值 0.12234327132827787，差 5e-16）；
  `argmax_kind="interior"`，边界极大 0.12162188188690420；最深洞的活跃三元组已记录
  （如 `[64,67,96]`、`[52,64,77]`、`[40,69,70]`）——这正是"洞的接触三元组"，符合计划要求。
- **输入加载实测**：`freecover_n100.json` → 100 心、sha16 `36286ebc48041a2a`；
  `n100_polar_probe.json` → 105 条记录、**105 条可用、0 条被拒**，按记录半径升序，
  前三条 0.123177917970 / 0.123685466401 / 0.124529753341 ⇒ 环族最好的三条确实被选进出初值。
- **候选产物格式实测可用**：`candidates/<label>.json` 的 `best.P` 是 100 个 raw float 字面量，
  指针 `best.P` == `verify/coverage_n100.py` 的 `SOURCE_POINTER='/best/P'`；写完后有
  canonical 哈希回读校验（`:1647-1651`），并且 `validate_centers` 保证互异 ⇒ 可直接喂给
  `python verify/coverage_n100.py --mode gen --input <candidate> --R <p/q>`。

### 9.3 预算与验收口径（中）

- **实测单次代价**：`mode="objective"` 0.0153 s/次（首次 0.037 s），`mode="full"` 0.233 s/次。
  ⇒ 6000 次 objective ≈ **92 s**；6 个 run 的诊断扫描（8192 边界点 + 361² 网格 + 120000 随机点）
  约 0.5–1 s/run。所以**时间不是瓶颈**。
- **但预算大概率用不完**：`--stall 150`（`:1445`/默认 150）意味着一个 run 在连续 150 次无改进
  后停止；从历史基线出发（已知局部最优，220k+ 次评估无法改进）预期每个 run 约 152–200 次求值
  ⇒ 6 个 run 合计 **~1000/6000**，全局 `stopped_globally` 会是 `planned_runs_completed`，
  **既不是计划列的三条停止条件（预算用尽 / 目标函数或输入异常 / 全部入选结果重复同一接触图
  且无认证上界改善），也没有把"接触图重复"当作停止规则**（只在 `cross_run` 里报告）。
  建议：把计划的三条条件显式落成 `stop_reason`（例如新增
  `duplicate_contact_graph_no_improvement`），并在结果里显式印 `budget_used_fraction`；
  或者把 `--stall` 提到能让 6000 次预算真正被消耗的量级（否则"6000 次预算"名不副实）。
- **`--seconds` 不含校准**（见 9.1.1）：结果 JSON 的 `ledger.elapsed_seconds` 与启动器记录的
  墙钟会系统性差一个校准时长，对账时要注意。
- **`safe_rational_suggestions` 的 "tight_1e6" 可能不够安全**：它是 `ceil(r*1e6)/1e6`，
  余量落在 `[0, 1e-6)`；而 `:1031` 允许 `full - objective` 大到 **1e-6**。若某候选的交叉检查
  差值正好接近 1e-6，则 `tight_1e6` 可能低于该构型真实半径 ⇒ 精确生成器按 vacuity 失败
  （fail-closed，不会误报改进，但白跑一趟）。建议印 `safe_1e4`（+2e-5）作为默认建议命令，
  或改成 `ceil((r + 1e-6)/1e6)`。
- **`--no-calibrate` 现在只跳过搜索前的自检并打 WARNING**（`:1721-1722`），
  `--selftest` 仍强制校准（`:1715`，不会再 NoneType）。但"用 `--no-calibrate` 跑搜索"等于
  绕过唯一的自检闸门；建议在结果 JSON 里显式写 `calibration_skipped: true`，或干脆禁止该组合。

### 9.4 CLI 与启动器契约（实测）

- pilot 的 argparse 有 `--out-dir --baseline-input --ring-input --max-evals --seconds`
  （外加 `--per-run-evals --seeds --families --stall --checkpoint-every --diagnostic-grid
  --random-points --no-scipy --no-calibrate --selftest --verbose --baseline-pointer`）；
  与启动器 `:36` 传的 5 个参数**名称与类型全部对齐**（`--seconds` 是 float）⇒ 无 exit 2 风险。
- 启动器**不部署** `verify/coverage_n100.py`（manifest 只有 pilot + 两个输入）。
  这是**独立性上的优点**（判定路径与被审代码不共享），但也意味着
  "candidate 已可被阶段1校验器读取"这一步只能在本地做：collect 之后需要在本机跑
  `verify/coverage_n100.py --mode gen`。建议把它固化成一条本地命令（或启动器加一个
  `verify` 动作，明确在**本机**执行），否则计划里"每个入选候选交给阶段1严格验证器"没有闭环。
- pilot 打印的复核命令引用 `runtime/replay_pilot_candidate_n100.py`（存在 ✔，已在本仓库）。

---

## 10. 与正式锚点的对账、以及启动器最新版（`setsid` 版）

### 10.1 锚点对账（结论：我的数字与正式锚点不矛盾）

正式锚点 `verify/out/pilot-n100-anchor/replay.json`：`R = 1223433/10000000`、
49720 叶（cov 49316 / out 404）、深度 26、未决 0、3.53 s、`independent.verified=true`。
我的未复核诊断跑到的最紧一点是 `R = 1223432715/10000000000`（67684 叶 / 深度 34）——
**R 不同**（1.7e-10 vs 2.9e-8 的余量），且我的两个相邻点 0.1223435（42460 叶 / 深度 23）与
0.12234328（53824 叶 / 深度 28）把正式锚点夹在中间 ⇒ 趋势一致，`out=404` 在两边也相同。
**本文件只引用正式锚点；我的阶梯标注为未复核诊断，不作为证据。**

### 10.2 锚点的意义

- 认证区间从 `[1/10, 153/1250]` 收紧为 `[1/10, 0.1223433]`（下界仍是已证的面积界 `1/10`；
  `0.1109141386` 依旧 `not_certified`）。
- 这给 pilot 一个**硬门槛**：候选只有在某个有理 `R < 0.1223433` 上通过精确生成器，才算改善；
  建议起步就用 `1223432/10000000`（若 >rho 则证书通过，否则按 vacuity 失败并逐档上调）。

### 10.3 启动器最新版（61 行，已修掉上一版的关键缺陷）

**已修好**（我逐条确认）：远程硬超时 `/usr/bin/timeout -k 10 1800`（`:36`）；
`setsid` 新会话（`:38`）；`started-utc.txt` / `finished-utc.txt` 远程时钟（`:37`）；
启动守卫同时拒绝已存在的 `started.json` **和** `exit-code.txt`（`:35`，杜绝陈旧退出码）；
`status` 三态 `finished|running|unknown` + `tail run.log`（`:44-47`）；
`collect` 拒绝重复收集（`exit_code is not None`，`:49`）与拒绝覆盖已有 `dst`（`:51`）；
收集后**逐文件校验 sha256**（`:52-56`）；`save()` 带时间戳备份（`:10-12`）；
run 记录嵌入 deployment manifest（`:41`）。

**仍存的问题**：

1. **pid 归属依赖 `setsid` 是否 fork。** `:38` 用 `p=$!` 记录 `/usr/bin/setsid` 的 PID。
   `setsid(1)` 在调用者已是进程组组长时会 **fork**，此时 `$!` 指向一个立即退出的
   `setsid` 进程，而真正的 wrapper bash 换到了新会话（pgid = 它自己的 pid）⇒
   `run.pid` 失效、`status` 退化成 `unknown`、`kill -TERM -<pgid>` 打不到目标。
   更稳的写法：在 wrapper 里第一句就 `printf '%s\n' $$ > run.pid`（bash 自己就是会话/进程组
   首进程），不要依赖 `$!`。**建议部署前先 `status` 一次确认不是 `unknown`。**
2. **`timeout 1800` 与 pilot `--seconds 1800` 的相位差**：见 §9.1.1，这是当前最可能把
   "预算停止"变成"被杀且丢产物"的一条。
3. `deploy` 的守卫仍以 `remote exit 1: ...` 报错（`:20`），而它实际含义是"这个目录已经跑过"；
   手工排障时易误判为传输故障。改成先探测再给出明确信息即可。
4. `execute()` 仍是"先读 stdout 再读 stderr"（`:18`）：对当前这些小命令没问题，
   若将来把 `find -exec sha256sum`（`:52`，输出随文件数增长）接到大目录上，参数化命令的输出量
   会让这个顺序读取成为 paramiko 的经典死锁点；建议改用 `ChannelFile` 并发读或把大输出落到远程
   文件再分块取。
5. `status` 不报"已跑多久 / 距 1800 s 还有多少"，建议把 `started-utc.txt` 与剩余量一起打印。

### 10.4 给部署方的三条最小动作

1. 部署前：记录 `tools/pilot_n100_stage2.py` 的 sha256 并确认 `--selftest` PASS
   （该文件在我审查期间改过，见 §9.0）；manifest 里已有哈希，补充"selftest 结果"字段。
2. 定标：在本机量一次 `--selftest` 墙钟，据此定 `timeout` 与 `--seconds` 的相位
   （或让 pilot 把 Clock 提到校准之前）。
3. 闭环：collect 之后在本机跑
   `python verify/coverage_n100.py --mode gen --input <candidate> --R 1223432/10000000 --out <dir>`
   （必要时逐档上调 R），只有它 PASS 才允许说"上界改善"。

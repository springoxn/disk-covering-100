# n100 协同候选与下界前置：当前已验证进展

最优半径极小多项式目标仍未完成；持续goal保持active。

## 最新严格区间

`11323/100000 < r_D(100) ≤ 1154469548855829/10^16`，即 `0.11323 < r_D(100) ≤ 0.1154469548855829`。

来源固定为外部提交67ebf1c，已实际完整重放、独立上界与本项目四叉树交叉验证，见[吸收报告](result-external-disk100-absorption.md)。[完整区间证据](../verify/out/external-disk100-bounds-67ebf1c.json)退出0，六个下界分支重新计算PASS；连续几何仍由解析证明承担。局部932变量孤立KKT根和严格局部极小性也实际重放通过，[证据](../verify/out/external-disk100-strict-local-67ebf1c.json)保留freshroot/whole-disk与8/8破坏测试拒绝。后续代数化主路线使用这个已隔离根，而不再优先使用欠平衡旧polish小数。

以下为吸收前的历史前置，旧基线 `0.11148 ≤ r_D(100) ≤ 0.119877` 已被新区间支配。

新上界R=0.119877。`verify/out/n100-cooperative-polish-tight/replay.json`实际退出0，`all_passed=true`、`independent.verified=true`，35584叶、最大深度23、未解析0。输入为只读冻结 `runtime/n100-cooperative-polish/best.json`。其十进制坐标字面量被视作精确有理数，不替换成所谓格点或拟合代数坐标。

## 三阶段收紧轨迹

| 阶段 | 浮点发现半径（不作判定） | 正式有理上界 | 证据 |
|---|---|---|---|
| 原精确格点 | 0.1221694443563052 | 1/sqrt67（代数） | verify/out/n100-algebraic-bounds-bundle.json |
| 协同首轮 | 0.1200703574813639 | 18761/156250=0.1200704 | verify/out/n100-cooperative-anchor-tight/replay.json |
| refine | 0.1198908685151380 | 119891/1000000=0.119891 | verify/out/n100-cooperative-refine-tight/replay.json |
| polish | 0.1198764764337424 | 119877/1000000=0.119877 | verify/out/n100-cooperative-polish-tight/replay.json |

各阶段输出只读冻结，完整100中心、搜索预算、源码与输入哈希、失败范围均保存。第一轮中间评估器单位bug失败快照未原样保留（session-log重建）；后续refine第一次失败快照已备份，并在不同产物中修复后重放。

## 代数化诊断

每阶段仍只有1个tight孔（阈值1e-9），同时多个near-tight孔参与有限band模型。polish在4×30轮cap处仍115次strict改善，末端下降未停；局部系统没有KKT/邻域最优证书。所谓LP t只是有限固定见证线性模型，不是真全局或KKT残差。当前不可用其小数猜极小多项式。

接触平衡/SQP单元已经实际退出0，但状态 `NO_IMPROVEMENT`：60秒内发现只降约1.25e-9，低于验收门槛，不保存新候选、不更新上界。自由辅助外心SQP和smooth max方向的真实半径大多上升，被真评估器拒绝；有限失败不证明局部最优。驻点系统诊断已实际退出0（1.3秒），产物 `runtime/n100-stationarity-system/result.json`。1e-6近活跃带有123个接触，但1e-7只剩2个、1e-9只剩1个；114条内点梯度行浮点秩114，列零空间维86。所测非负KKT乘子LP在各容差下均未找到平衡，且边界三接触的等权fallback不尊重旋转规范。以上是有限浮点诊断，既不证明没有别的平衡分支，也不证明候选‘不可代数化’的普适结论；说明当前提取系统不足以作为可验收的代数KKT根。下一步需完整边界分支与真正多接触平衡延拓。所有浮点只发现，入选候选才通过有理覆盖认证更新U。

## 新普适下界前置

新长弦二次亏损的普适解析引理经过三轮独立审查修订，最终几何稿SHA256 `658863d2a36118be915fda66f10596f05073aadd51738da55bcf35f967d8cf73`。主/独立有理算术由新入口 `python verify/run_longchord_n100.py --out <fresh-path>` 完整重放；正式事实源 `verify/out/n100-longchord-bundle-frozen.json`，实际统一退出0、子退出码 `[0,0]`、`all_passed=true`、`universal_lower_bound_accepted=true`，566个B全正余量、worst_B42、6/6负对照拒绝。因此接受普适下界 `2787/25000=0.11148`。几何是解析证明加审查，`machine_verified_geometry=false`；不得称形式化证明或最优性。修订中发现的正弦二阶导区间错误、有理端点笔误、边界集合包含错误都已修；独立checker负对照无限递归也已修，失败运行已终止，最终绑定为修复后实际重放。

另一逐胞等弧/边数5,6采样族模型发现0.1118772，但对手族未证完备，不能当普适下界。径向壳LP的约92.56值也不是连续覆盖数认证上界：细网格复查样本解不可行；报告已按独立质疑纠正。因此有限见证路线没有被证明“不可能”，只是所测松弛未显足够收益。

## 完整最优端点公式

`proofs/n100-real-algebraic-optimal-endpoint.md`给中心投影、紧致可达与全量词Feas/Opt；实闭域QE定理保证r_D100是代数数。独立审查认可数学，小n1/2/3校准最终入口 `verify/out/real_algebraic_endpoint_n100_audited.json`退出0。但没有执行n100 QE，没有取得最优多项式全部系数或次数。

## 最优多项式仍缺的证据

稳定代数配置、局部竞争分支处理、覆盖等号、无对称限制的全局排除、上下界闭合同一代数数、不可约性和唯一根隔离。当前上下界仍不同，不能把任何候选多项式提交为r_D100答案。

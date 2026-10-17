# n100 历史数值0.1109141386的普适加强下界：完成报告

现已通过新的整数边数路线证明精确命题：

`r_D(100) ≥ 554570693/5000000000 = 0.1109141386`。

结合既有连续覆盖上界，当前严格区间为

`554570693/5000000000 ≤ r_D(100) ≤ 1223433/10000000`。

[完整验收证据](../verify/out/strengthened_lowerbound_n100.json) `all_passed=true`、`universal_lower_bound_accepted=true`；实际执行 `python verify/run_strengthened_lowerbound_n100.py` 退出0。[正式证明](../proofs/n100-strengthened-lowerbound-combined.md) SHA256 `7d3bc950832342070a94fc4c0075a0d38ae3933c662c887fad321ee7a775ff1e` 与[独立解析审查](../verify/out/strengthened_geometry_review_n100.json)的最终审查哈希匹配。

## 为什么旧问题被修复

原[阶段1审计](audit-lowerbound-n100.md)仍是对旧连续Jensen、逐胞扇形和浮点不动点链的正确历史记录，不改写成“旧证明本来就成立”。新证明替换该链：

1. 盘外中心投影到D不增加D中任何点的距离；投影后去重，N≤100且所有裁剪Voronoi胞正面积。覆盖保证胞V_i含于各自半径r盘。
2. 每条圆周弧角≤2asin r。目标区间r≤L内用精确有理平方得到asin r<14/125，故弧数B≥29。B按弧数计，不假设每胞一段弧。
3. 每段弧的凸包圆缺属于所属凸胞；用内向弦半平面的交定义统一内接P。其它胞的弦约束在V_i上冗余，因此Q_i=V_i∩P只有自己的弦新增，名义边数e_i≤m_i+a_i。退化点/线段项面积0。
4. 无一般位置的平面图记账以实际图顶点细分，边界切换点至少三度；允许K≥1连通分量，Euler和度计数给Σe_i≤6N−6−B≤565。共圆、共线、边界多活跃中心不需要微扰。
5. 任意凸k边多边形含于半径r盘，面积≤r²f(k)。从最小包围圆圆心扇形分解，免去原中心必须属于P的前提。
6. f在[3,∞)凹增，经过5、6的割线在所有整数边数上方（5与6之间没有整数）；正截距吸收e≤2的零面积。故面积P≤r²(65f6+35f5)<253L²。
7. 弧长粗下界给面积P> (157/50)(1−(2/3)(14/125)²)。它与上述上界矛盾，因为精确正余量为

`101163967314311009/75000000000000000000 > 0`。

该余量同时覆盖全部r∈(0,L]，不靠有限半径采样、不靠400步浮点迭代、不遗留分段断点。r=0不可能由有限点覆盖D。逐构型覆盖半径>L只用于推出inf≥L，不声称inf严格大于L。

## 机器验证与解析审查的区别

- [主算术证书](../verify/out/strengthened_arithmetic_n100.json)：18项精确重算，10种损坏输入拒绝；仍标记`conditional_geometry=true`，因为该脚本单独不证明几何。
- [独立有理证书](../verify/out/independent_strengthened_arithmetic_n100.json)：15项Fraction检查，π使用更粗下界3.14，收口分数一致；不导入主算术函数。
- 完整验收还比较全部主证书负载与重新生成结果，并拒绝3种重新计算哈希后的篡改案例，避免单靠文件哈希检查算术。
- [独立解析审查](review-strengthened-geometry-n100.md)逐条认可最终正式稿的14项命题，关闭3处缺句并记录6项撤回。审查记录绑定正式稿哈希，未把数值DP或随机构型当普适证据。
- [几何支持检查](../proofs/out/n100_geometry_check.json)7项实际退出0，其中4项是发现层浮点，余下仅有限对象精确检查；它不是普适几何证明。

完整验收报告明确 `machine_verified_geometry=false`。普适性来自正式稿的解析推理和独立对抗审查；整数/有理运算认证有限常数和统一矛盾。没有Lean/Coq形式化，也没有把解析审查JSON当作自动证明内核。

## 历史浮点数的舍入

[发现材料](../runtime/lowerbound-constant-discovery-n100.json)显示历史连续路线根约 `0.11091413859240942829`，比目标小约7.59×10⁻¹²。这是高精度发现，不是有理根隔离证书，不能单独据此断言精确舍入定理。新路线不依赖该根：整数边数带来的余量直接支持原样精确目标，没有悄悄下调目标。

历史“每胞单弧”有精确三中心反例；旧`P=D\union int(cap)`集合公式也为假（保留圆周弧），新证明完全改用闭半平面。具体反例与修订在[详细几何说明](proof-lowerbound-n100-geometry.md)及独立审查中保留。

## 复现

在项目根执行，新的输出文件必须尚不存在：

```text
python verify/run_strengthened_lowerbound_n100.py --out verify/out/strengthened-lowerbound-replay-new.json
```

期望退出0，输出 `PASS reviewed analytic proof + two exact arithmetic implementations; geometry is analytic, not machine-certified`。报告绑定正式证明、独立审查及两套算术代码/证书的SHA256。若证明文件被改动，审查哈希不匹配会拒绝，须重新审查。

## 范围

本阶段只完成指定加强下界。不证明r_D(100)精确值、历史构型最优性、最优半径极小多项式或任何更强小数下界。旧面积法证书和旧审计保留，新的下界证据在独立产物中。上界仍来自阶段2已验证的历史构型覆盖证书。当前相对缺口按 `(U-L)/U` 约9.35%，仍未达到5%指标。

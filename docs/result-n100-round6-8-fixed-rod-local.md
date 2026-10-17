# 第6—8轮执行收口：固定杆不等式域的显式局部球

本阶段完成固定候选杆域的局部定量推导、标量预算、独立审查与有理盒包含。没有完成覆盖拓扑对应、候选图全域排除或百盘全局最优性。

| 执行 | 实际结果 | 回执 |
|---|---|---|
| python verify/n100_fixed_rod_local_budget.py | exit0，全部有理标量要求通过，2个过大半径负控制拒绝 | [预算](../verify/out/n100-fixed-rod-local-budget.json) |
| python verify/n100_local_midpoint_box_containment.py | exit0，493坐标半宽10^-42有理中点盒位于精确根10^-40欧氏球 | [盒包含](../verify/out/n100-local-midpoint-box-containment.json) |
| python verify/n100_local_augmented_audit.py | 父会话exit0，21项精确检查通过；模型恒等式/Young平方/矩阵界/域符号关系审查通过 | [独立审查](../verify/out/n100-local-augmented-audit.json) |

结论：精确KKT根x*处乘子固定，半径ε=10^-40。若493变量点x满足同一406条杆f≤0、32个单位圆等式和1个仿射规范，且0<||x-x*||₂≤ε，则`t(x)-t*≥||x-x*||₂²/(4×10^12)>0`。

依赖已验收SOSC回执的枢轴逆、核基和Cholesky变换精确界，未在本阶段重复大矩阵验证。独立审查是有理算术和解析论证审查，不是形式化内核证明。中点乘子不满足精确驻定，故不得用中点替代本定理的精确根乘子。

完整[推导](n100-fixed-rod-local-exclusion.md)，[审查说明](n100-local-augmented-audit.md)，[依赖图](../proof_graph/n100-exact-value-dependencies.md)。

下一单元：覆盖孔分支的隐函数定量构造、边界分支与最近中心严格余量、覆盖局部极大库存的稳定性，以及中心空间邻域到493变量杆域的明确距离转换。没有这些对应，固定杆球不能自动接受任何真实覆盖树叶。其他拓扑、m<100、退化和全局下界闭合仍须继续；候选根多项式不能升级为r_D(100)的极小多项式。

当前区间不变：`11323/100000 < r_D(100) ≤ 1154469548855829/10^16`。持续目标未完成。

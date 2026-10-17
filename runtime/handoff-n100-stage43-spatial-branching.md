# n=100 阶段43交接

主verify/n100_spatial_branch_trees.py与独立verify/n100_spatial_branch_independent.py均实际退出0，pwsh-6/pwsh-7输出已收集，无后台作业。

证据verify/out/n100-spatial-branch-trees.json及verify/out/n100-spatial-branch-independent.json；报告docs/result-n100-stage43-spatial-branching.md。

从阶段42已验证根盒构建两棵深度6完整覆盖二分树，方案[0,6,12,18]和真实[30,6,14,22]各127节点(63 split+64 unresolved)，无排除叶，两根均未排除。合计958930次收缩。独立Floyd/独立承包器重放全部节点、父子盒、最终盒和计数；重复子节点/非内部切分控制拒绝。

本轮是将连续分支结构接通，不是新的局部排除或全局下界。4776根域、87计数族与半径区间不变。真实候选根未排除不等同精确构型已定位到某叶。

下一步需要更强耦合（共享顶点、盘交等）或评估有针对性的分支；浅层分支没有排除不能称深分支无效，也不宜无估计地加深至爆炸。全核心枚举、全局最优性、极小多项式仍未完成，目标active。

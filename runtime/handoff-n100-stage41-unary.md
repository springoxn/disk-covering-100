# n=100 阶段41交接

两最终命令退出0，无后台作业：
python verify/n100_axis_unary_feasibility.py
python verify/n100_axis_unary_independent.py

证据verify/out/n100-axis-unary-feasibility.json与verify/out/n100-axis-unary-independent.json；报告docs/result-n100-stage41-unary-feasibility.md。

实证：4776方案*100内面=477600逐面圆心域，4365不同四轴最短距离向量。所有域(|c|<=1且|c-a_i|<=(2d_i+1)U)都有分母64有理点。独立Floyd重算次数/全域，纯整数逐点检查，4损坏控制拒绝。新增排除0。

重要路线结论：仅优化阶段40五个逐面盘约束的分离权重不可能增加排除，因为交集已精确证实非空。下一步必须加跨面耦合/共享顶点几何/更紧距离界。当前有理点不是覆盖配置，也不保证彼此满足邻接圆心距离。

全核心枚举、保留方案完整连续域排除、全局最优性和极小多项式均未完成；区间和87计数族不变，目标active。

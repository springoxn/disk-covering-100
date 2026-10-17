# n=100 阶段33交接

实际完成：
- `python verify/n100_one_interior_models_independent.py --out verify/out/n100-one-interior-axis-pair-sos.json`：退出0。
- 16个内部顶点轨道模型所有多项式独立重建，有理赋值通过。
- 固定轴点两点SOS恒等式用Fraction逐系数验证；16轨道最大下界均t>=1，于U²处全部排除。
- 真正602半边百盘候选没有同面固定轴点对，下界0，正确保留。

证据verify/out/n100-one-interior-axis-pair-sos.json；报告docs/result-n100-stage33-axis-pair-sos.md。

初版接口审计证据n100-one-interior-models-independent.json保留，不覆盖；SOS版输出用新路径。曾一次默认输出拒绝覆盖，未覆盖旧证书；最终指定新路径成功。

当前严格区间与87计数族不变。新增排除只针对16个小地图模型，不是n100候选或n100族排除。

后续：小规模校准已足够，下一阶段应推进真实n100图域的坐标盒/模式剪枝或定量局部叶连接；不要以更多小族校准代替全局进展。下一轮首先核查通用模型的充分性与外边界弧覆盖依赖，确认全局枚举究竟需要哪些约束与退化闭包。

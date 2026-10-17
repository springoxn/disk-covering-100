# 阶段40交接

两次最终运行退出0，背景作业pwsh-1/pwsh-2已收集。

主verify/n100_axis_multianchor_pruning.py输出verify/out/n100-axis-multianchor-pruning.json：对阶段39保留4776方案，逐100内面检查4个三轴和1个四轴子集，权重1/R_i²，R_i=(2d_i+1)U；无新增排除，4776全部保留，真实候选保留。

独立verify/n100_axis_multianchor_independent.py输出verify/out/n100-axis-multianchor-independent.json：独立Floyd与未中心化矩判据，4365距离向量、21825子集测试，分区相同；符号正负控制通过。

报告docs/result-n100-stage40-multianchor.md说明首跑接口失败及数学实现修正；失败版未出接受证书。当前主脚本有未调用两点辅助函数和过宽历史头注释，实际接受循环采用正确同面(2d+1)U方差；后续重构若改脚本需新证书绑定。

本轮无新排除，严格半径区间及87计数族不变，不要重复同一权重扫描。下一步若走多轴应优化分离权重/圆交判定，或切到坐标域分支。全核心生成、全局最优性、极小多项式仍缺。

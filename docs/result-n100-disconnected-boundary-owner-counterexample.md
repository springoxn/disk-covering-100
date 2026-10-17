# 边界所有权连通性剪枝不成立

[主反例检查器](../verify/n100_disconnected_boundary_owner_counterexample.py)与[独立整数检查器](../verify/n100_disconnected_boundary_owner_independent.py)均实际退出0，见[主回执](../verify/out/n100-disconnected-boundary-owner-counterexample.json)、[独立回执](../verify/out/n100-disconnected-boundary-owner-independent.json)。

圆心A=(99/100,0),B=(1,0)，圆周点P±=(323/325,±36/325),M=(1,0)。三个点严格在单位圆周，A在两端严格最近，B在中间严格最近。平分线x=199/200，两端x<199/200而中间x>199/200。A本身在当前U下覆盖整条P−到P+短弧，证明服务集连通不能推出分配所有权连通。凸胞腔D∩{x≤199/200}的圆周交集同样不连通。

反例仅为局部几何，不是两盘在当前U下覆盖整个单位盘。它否定拟采用的推理依据；没有据此证明某个完整百盘地图一定可行。抽象覆盖地图亦未要求所有权等同最近中心。因此不得单凭同一面出现非相邻边界弧排除模型。此规则没有加入任何枚举器。

当前候选与六小地图的外环所有者序列已保存于主回执，只用于审计。无新半径界或全局最优性结果。

# n=100 阶段45：边界圆周环带必要条件

对拥有外边界半边的内面，若其圆心c覆盖某个单位圆点，则必有 `|c| >= 1-U`。因此若固定点坐标盒整体落在半径1-U以内，可以认证空盒。

本轮只对外边界拥有面施加该条件；首跑错误地对所有内面施加，错误在证书前被发现，没有采用。修正版 `verify/n100_boundary_annulus_boxes.py` 实际退出0，证书 `verify/out/n100-boundary-annulus-boxes-v2.json`。

首个保留轴方案和真实候选均无环带空盒。独立 `verify/n100_boundary_annulus_independent.py` 实际退出0，证书 `verify/out/n100-boundary-annulus-independent.json`，独立重算外边界拥有面集合和整数环带判据；原点盒算术负控制通过。

这是边界圆周信息的廉价必要松弛，不是完整圆周等式或弧端点约束。无新增排除，非空仍不代表几何可行。当前阶段只检查两个固定方案，未扫描4776全部方案。

严格半径区间、87族、全局最优性和极小多项式不变，machine_verified_geometry=false。

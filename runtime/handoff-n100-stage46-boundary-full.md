# n=100 阶段46交接

主/独立扫描均实际退出0：
python verify/n100_boundary_annulus_full.py
python verify/n100_boundary_annulus_full_independent.py

证据verify/out/n100-boundary-annulus-full.json与verify/out/n100-boundary-annulus-full-independent.json；报告docs/result-n100-stage46-boundary-full.md。

固定真实核心阶段42保留域4776项全部通过外边界圆心环带必要条件，新增排除0。边界拥有面集合独立重算一致，候选保留。廉价环带已证明对该固定点域无增益，后续不要重复扫描；需要角度弧端点/圆周等式、共享顶点圆周耦合或其他核心完备枚举。

全局目标active，半径区间与87计数族不变；完整地图枚举、全局最优性、极小多项式缺失。

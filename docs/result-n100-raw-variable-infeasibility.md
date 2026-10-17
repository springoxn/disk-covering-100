# 原变量不可行证书：校正与独立重建

[生成器](../verify/n100_face_axis_raw_variable_certificates.py)和[独立验算器](../verify/n100_face_axis_raw_independent.py)实际退出0。正式证据仅采用[v2回执](../verify/out/n100-face-axis-raw-variable-certificates-v2.json)和[独立回执](../verify/out/n100-face-axis-raw-independent.json)。

初版回执n100-face-axis-raw-variable-certificates.json不验收：初版商公式没有删去全部被除变量、没有累加同项，也没有核对商重建；所谓错误常数拒绝只检查记录不同。初版执行PASS不足以支持原变量证书。保留初版产物与脚本备份以供审计，不能用其verified字段判定本阶段。

修正后每一步精确检查N=N(x_i=a_i)+(x_i-a_i)q_i，最后余式为−δ。因而原变量下N−Σ(x_i−a_i)q_i=−δ，其中N是两条距离约束的1/2倍、两个平方和T−t。除以正δ即可得−1。等式乘子允许符号自由，所有不等式与平方乘子严格正。

独立实现不导入生成器，直接读取原模型距离多项式，重建平方、上界与正δ，并累加保存的商乘原轴等式；最终全部原变量系数精确为0。实际核对每个轴等式确实存在于模型。六个小地图全部通过，错误轴常数、错误商、缺商、错误距离引用四项控制全部拒绝。

v2生成器末尾stdout沿用初版的corruption rejected字样，但v2自身未做篡改测试；真正拒绝证据在独立回执，不能仅凭该stdout宣称负控制通过。

证明范围仍限六个已校准小地图及双轴同面结构。没有新百盘全域排除，没有全局最优性或真实极小多项式；严格区间保持11323/100000<r_D(100)≤1154469548855829/10^16。

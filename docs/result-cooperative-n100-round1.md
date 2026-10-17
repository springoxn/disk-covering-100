# n100 持续目标：协同构型首轮结果

用户目标仍是取得r_D(100)本身的极小多项式，**未完成**。本阶段取得可独立复现的新严格上界及端点代数性前置。

## 当前已认证区间

`1111720153/10^10 ≤ r_D(100) ≤ 18761/156250=0.1200704`。

上界事实源：[更紧独立重放](../verify/out/n100-cooperative-anchor-tight/replay.json)，实际命令退出0，`all_passed=true`、独立 `verified=true`，19540叶、最大深度25、未解析0。输入固定为 [冻结配置](../runtime/n100-cooperative/anchor-certified-012008.json)，源SHA256 `413af66fccfc2988aae9f52ca666de3cf5c25f3eaf01d98559d0402db3edc722`，100中心有理十进制字面量，坐标canonical hash `70905174d03611c7cbbac03c16d2e3136d6af23284d7bb38f39e26e075c0d53b`。

命令：

```text
python runtime/replay_pilot_candidate_n100.py --input runtime/n100-cooperative/anchor-certified-012008.json --R 18761/156250 --out-dir verify/out/cooperative-replay-fresh --depth-cap 28
```

输出目录须新建；不覆盖证据。

## 发现与有限线性前置

[协同搜索](../tools/cooperative_minimax_n100.py)总预算实际66.9秒、退出0。初始97+3精确格点半径1/sqrt67，父agent枚举168活跃孔（156内部、12边界），构造协同LP；[有理方向证书](../verify/out/n100-contact-direction.json)认证168条固定有限线性不等式严格为负。它不证明非线性覆盖下降。有限位移通过完整连续关键点浮点评估，再做若干协同迭代，发现半径约0.12007035748136387。

[首轮结果](../runtime/n100-cooperative/result.json)最终 `status=OK`，全三元组与独立旧评估器交叉一致。中间有单位换算错误导致CROSSCHECK_FAILED，之后修复；原失败快照在父agent备份指示到达前已被覆盖，当前 [运行说明](../runtime/n100-cooperative/NOTES-run.md)记录的是session-log重建，不能称原快照已保存。最初exact报告源metadata随后被脚本最终落盘更改使字节哈希失效，因此改用冻结anchor重新认证；正式事实源以上更紧冻结输入重放为准。

本轮数值发现的改进已被独立精确覆盖证书确认；这不证明局部最优、更不证明全局最优。85中心在D内，15中心在D外是输入事实，不影响覆盖认证；普适最优量词可以投影后限制中心于D。

## 极小多项式存在性前置

[代数端点证明](../proofs/n100-real-algebraic-optimal-endpoint.md)：投影+紧致给最优可达，连续覆盖写完整存在中心/全称域点公式；实闭域量词消去给Q-半代数可行集，其最小端点为代数数，故r_D(100)确有极小多项式。独立审查认可解析推理，但未执行n100量词消去、未得到系数。

[审查后小n校准](../verify/out/real_algebraic_endpoint_n100_audited.json)退出0，使用真多项式卷积和端点评值；n1/2半径1，n3半径sqrt3/2的多项式与隔离。初版检查包含硬编码相等式，审查指出后已修，旧报告不作为最终校准入口。

## 下界与仍未完成

长边界弦面积损失的[发现探针](../runtime/n100-long-chord-model-discovery.json)给模型阈值约0.11148782537064933（B=42），较当前L有潜在增益。多弧/退化胞、长弦角阈值及Jensen未全部认证，**不是已接受普适下界**。仍需独立解析闭合与整数有理常数认证。

全局闭合差距仍很大；当前候选不是稳定代数KKT解，不能从其小数拟合最优半径多项式。下一执行单元是冻结候选的活跃接触分析与有界继续优化，同时精确闭合真正普适下界新约束。长周期goal保持active。

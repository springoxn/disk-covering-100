# n=100 证据台账

本文把公开仓库中的主要数字断言与证据文件一一绑定。`PASS`是脚本范围内的机器检查状态，不等于所有上游几何命题已经形式化。

| 断言 | 状态 | 证据 | 备注 |
|---|---|---|---|
| 存在100圆盘构型，半径不超过`0.1154469548855829` | 已重放 | `verify/out/external-disk100-bounds-67ebf1c.json` | 构型上界；不是最优性 |
| 三角晶格候选满足`alpha²=1/67` | 独立复核 | `verify/out/independent_lattice97_upperbound_n100.json` | 另一个明确的构型上界材料 |
| B31排除 | PASS | `verify/out/n100-B31-at-11324.json` | 在更大半径候选上验证，可向较小半径继承 |
| B32排除 | PASS | `verify/out/n100-B32-complete-149.json` | 含M25和高M分区 |
| B33排除 | PASS | `verify/out/n100-B33-complete-167-v2.json` | 低M/高M和邻居分裂 |
| B34排除 | PASS | `verify/out/n100-B34-complete-180.json` | 23无弦+47单弦模型 |
| B35排除 | PASS | `verify/out/n100-B35-complete-203.json` | 低M、M25、M26、高M |
| B>=36在`R=0.113235`排除 | PASS | `verify/out/n100-tail-candidate-224.json` | 完整pair域有理箱重放 |
| 候选总预算守恒 | PASS | `verify/out/n100-candidate-budget-222.json` | 总余量和每B增益严格为正 |
| 六分支在`R=0.113235`闭合 | PASS | `verify/out/n100-candidate-complete-225.json` | 独立组合器；不是单点诊断 |
| `0.11324`已证明 | 未证明 | `verify/out/n100-tail-support-obstruction-206.json` | B36旧松弛有精确障碍，不应写成PASS |
| `0.113236`或`0.113237`已证明 | 未证明 | `docs/result-n100-stage229-current-best.md` | 尝试过但未得到完整退出0证书 |

## 证据等级

- **A：结构化机器产物**：JSON证书、状态、计数、哈希和退出码。
- **B：独立重放**：不同脚本或不同阶段对同一子断言复核。
- **C：发现性材料**：浮点搜索、候选排序和失败实验，只能指导下一步。
- **D：继承性推理**：例如“较大半径排除可继承到较小半径”，必须在组合器中显式记录。

## 不应做的推断

不能把一个通过的局部盒子、一个未阻塞的障碍点、一个存在的构型，分别写成全局下界、完整覆盖证明或最优性证明。公开README和本台账刻意保留失败、未决和依赖边界。

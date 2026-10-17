# n100 阶段4有限见证点校准交接

## 本轮目标与结论

本轮完成阶段4首个独立校准 goal：建立有限有理见证点的连续中心模式归约、独立精确复核、负对照和强度报告。目标已验收；没有改善 n100 当前下界，也没有声称 n100 全局最优性。

## 实际验证

1. 原加强下界基线重放：
   `python verify/run_strengthened_lowerbound_n100.py --out verify/out/strengthened-lowerbound-stage4-baseline-replay.json`
   退出0，`all_passed=true`。
2. 首例见证生成：
   `python verify/witness_calibration_n100.py`
   退出0；21个闭单位盘内有理点，半径 `7/25`，53个非空可行子集，32个极大模式，506个生成事件，总权重 `21/2`。
3. 独立 checker：
   `python verify/independent_witness_calibration_n100.py`
   退出0；`verified=true`、`all_passed=true`、74项检查、0 failures、11个负对照全部拒绝；不导入生成器，判定使用整数/Fraction，`machine_verified_geometry=false`。
4. 统一重放：
   `python verify/run_witness_calibration_n100.py --out verify/out/witness_calibration_bundle_n100.json`
   退出0；两个子命令退出码 `[0,0]`，bundle `all_passed=true`，证明/输入/checker哈希均绑定。
5. 额外三点公式交叉检查：420个有理三点/半径组合全部通过。

## 数学范围

解析完整性依赖平面 Helly 定理或有限集最小包围圆支撑不超过3点，未作 Lean/Coq 形式化。独立复核重新枚举全部可行子集和候选圆极大族，结果一致：21个单点和32条相邻网格边，没有可行三点组。`w=1/2` 给总权重 `21/2>10`，所以半径 `7/25` 下排除 n=8、9、10；严格半径表述由面积界补足，避免从逐构型排除误推下确界严格性。

这只是工程校准：`7/25 < 1/sqrt(n)` 对 n=8、9、10 均成立。独立报告还证实该网格在该半径的对偶最优值恰为12，且 r≥3/10 时8个盘覆盖全部见证点，因此本见证集不能超越面积界，也不能迁移为 n100 改进。

## 下一步

另立强度校准 goal，优先 n=8，挑战高于面积界的阈值，例如 `9/25`；再考虑 n=9 的 `17/50` 与 n=10 的 `33/100`。这些阈值目前只是计划。新见证集必须包含真正的三点/更大模式并取得独立可重放的不可行证书；若枚举达到100000事件或30分钟，应保存未完成账本且不得称完整。只有新路线在小n通过强度校准后，才评估 n100 的点数、模式规模和对偶目标是否可能超过100。服务器重算不在本轮授权内。

关键文件：`runtime/goal-plan-n100-stage4-witness-calibration.md`、`proofs/n100-witness-calibration.md`、`docs/result-witness-calibration-n100.md`、`verify/out/witness_calibration_bundle_n100.json`。

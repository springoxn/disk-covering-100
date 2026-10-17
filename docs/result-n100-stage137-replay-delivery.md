# 阶段137：完整复现结果与交付接续

本说明更新[综合总报告](result-n100-stage136-integrated-study.md)第7/8节的待运行状态。总报告保留其生成时的口径；最终实证以[交付回执](../verify/out/n100-study-delivery-receipt.json)为准。

## 本次端到端结果

[全量快照封装](../verify/run_n100_full_revalidation.py)在新目录实际退出0：[快照清单](../runtime/full-revalidation-136/snapshot-replay-manifest.json)及[新4776结果](../runtime/full-revalidation-136/verify/out/n100-boundary-circle-full-revalidation.json)。所有4776配置的主、独立及历史完整输出相等，新旧全量重验证据的results逐项相同。564个排除、4188个fixed、24个capped。fixed只表示传播达到固定点，capped表示达到轮次上限；两者均不证明真实覆盖。

[四研究隔离重放入口](../verify/run_n100_timing_studies_replay.py)实际退出0，[汇总](../runtime/timing-studies-replay-136/replay.json)记录独立计时、组合/规模、共享支持、分布接口四项全部通过，旧verify/out最终证书未被改写，源快照未变。它补齐原计时入口固定输出不能直接复跑的问题。

```powershell
python verify/run_n100_timing_studies_replay.py --run-dir runtime/new-isolated-study --kind all
```

也可用--kind timing / composition / shared / distribution选择一项。输出路径必须不存在。worker运行原脚本，只有父进程最终证书的Path.open/exists被重定向；这不是完整虚拟文件系统。新时间数据在有并发全量任务时获得，只用于验证执行路径和精确判定一致，不替换首批正式校准或作硬件性能比较。

[回执核验器](../verify/n100_study_delivery_receipt.py)实际退出0，核对完整快照文件、新旧全量results、四研究退出与旧证书不变、16入口源绑定、875/665正式热检查记录，生成当前[最终回执](../verify/out/n100-study-delivery-receipt.json)。goal_completion_claim明确为false。

## 研究交付与目标剩余项

当前可复现研究材料已交付：m99边界线路；16组执行入口；20家族及344路径范围清单；174旧源的逐源条件契约；独立操作模型；固定规模和位长/目标数留出测量；同域重叠、顺序、缓存及共享准备研究；快速封印和完整/隔离重放。

整个目标尚未宣告完成。174个条件旧main尚缺源特定几何/域/输出桥和独立重放，无法把它们每一项的独立时间当作已测。gate拒绝和复杂度模板是缺口管理，不是这些变体的数学验证。没有具体外部阻塞，故不把目标标为blocked；仍为active。

完整n100原题也未解决，包括最优半径极小多项式和完整全局最优性。它本来不属于本阶段完成标准，但不能与上述旧源接口缺口混淆。内部地图枚举仍未覆盖，当前边界代表不是内部地图列表。

建议接续按[交接指针](../runtime/handoff-n100-stage136-study.md)逐规则补实际桥，优先反向平方距离、强平移目标前沿、正确所有者的图路径锚点，而不是继续生成名称清单。

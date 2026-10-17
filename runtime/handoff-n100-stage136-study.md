# n100接口与组合研究接续指针（阶段136后）

## 本轮目标及完成口径

当前目标是边界线路收尾、剪枝清点/可组合接口、独立复杂度/时间与组合研究；不以解决完整n100最优性为完成标准。综合说明见[研究总报告](../docs/result-n100-stage136-integrated-study.md)。

目标尚未完整达成，不能仅因20轮自动继续用尽而标记complete。具体未达成项是174个旧变体仍缺源特定几何/域/输出桥及独立重放，逐main的独立时间也未获得。清点、条件契约和明确拒绝门已经交付，不等于这些main已完成验证。原完整n100数学问题仍未解。

## 已落地事实源

- 当前m99边界线路3601->327的主/独立重放：[边界报告](../docs/result-n100-stage118-line-closure.md)与[隔离结果](boundary-line-replay-118/replay.json)。内部地图、m100全部边界代表及完整家族未覆盖。
- 已登记16组接口：[最终登记表](../verify/out/n100-final-proof-interface-registry.json)。292顶层源是该表生成时的快照；随后增加的封装/回执源不在这个数内。
- 递归范围：[344源/320内容清单](../verify/out/n100-pruning-recursive-inventory-v3.json)与[6控制](../verify/out/n100-pruning-recursive-inventory-controls.json)。源名字/AST标签不是数学审查。
- 174旧变体逐源缺口：[条件契约](../verify/out/n100-legacy-rule-disposition.json)。全部gate实际返回PRECONDITION_MISSING，16个涉及旧源的规则家族。
- 九批已激活接口输出逐字节一致：[运行依赖账本](../verify/out/n100-interface-runtime-dependencies.json)。读过旧证书不代表上游引理重算。
- 首批875热调用：[校准证书](../verify/out/n100-interface-timing-calibration.json)。规模/位长及组合665热调用：[组合证书](../verify/out/n100-composition-scaling.json)。共享准备：[共享会话证据](../verify/out/n100-shared-support-session.json)。补充分布70热调用：[分布契约](../verify/out/n100-center-distribution-interface-contracts.json)。
- 快速统一核验两次通过467文件封印：[项目回执](../verify/out/n100-delivery-audit-135.json)。其范围不包含后来总报告和最终表，最终回执另绑定。

## 当前长任务与接续核对

全4776新目录快照封装的目标目录是[完整重放目录](full-revalidation-136/snapshot-replay-manifest.json)；四项计时隔离封装的目标汇总是[四项隔离结果](timing-studies-replay-136/replay.json)。本指针写入时两项任务尚在运行，链接目标可能尚未生成，不能仅凭本说明认定通过。当前会话后台job为pwsh-22、pwsh-25。应先收集最终exit及日志，再运行[最终回执核验器](../verify/n100_study_delivery_receipt.py)。

```powershell
python verify/n100_study_delivery_receipt.py
```

该脚本要求全4776主/独立/历史完整输出等同且新旧results逐行相等，核验快照内容；要求四研究全部退出0且原始保存证书未变；输出到[最终交付回执](../verify/out/n100-study-delivery-receipt.json)。若文件已存在，拒绝覆盖，先读取现有证据。

四项计时的[隔离入口](../verify/run_n100_timing_studies_replay.py)是新增加的复现封装；原始研究脚本有固定verify/out最终目标，直接重复会因不可覆盖而停止。封装只重定向父进程最终Path.open/exists，worker仍运行原脚本；新遥测不替换原正式校准，特别是并发全量重放时CPU负载不同。

## 数学/组合纪律

m/B/k含义、半径/平方半径单位、同图/坐标/父域绑定都不能省略。连续端点是闭实区间，分割不可cut+1。耳打包与实际面积替换不能重复预算；多个目标面积和容量亏损默认不相加。LOCAL仅指定盒，有限支持不是连续覆盖，单图SOS不是所有图。

现有支持会话每次哈希核对证书及已加载本地源，但不是完整形式核验器；解析规范化/短弧/面积次可加性桥继承，环境稳定性仍是前提。一个历史代码哈希不匹配已以全4776算术等值桥处理，原错误哈希未被改写；不能泛化为所有历史依赖均已独立数学证明。

## 建议的下一具体工作

从条件清单中逐个或逐规则补桥，而不是再生成一轮名字定位清单。优先项：

1. reverse squared-distance旧变体：两符号平方逆像保守包络，显式原模型约束域，独立二分根重放；作为现有连续5原语的增补，而非直接信任旧main。
2. 强平移目标最低覆盖数：新接口只有面积数，旧方向脚本用递归更强前沿。为目标盘缩放建立半径域包含桥、独立最低数证据，再在声明连续盒调用。
3. 固定核轴规则：正确paired-dart所有者、图路径长度到(2d+1)U锚点半径桥，方差内核已可精确复核，但不能跳过核/标签域提升。
4. 旧边界/耳枚举：写源特定输入域转换和完整枚举receipt；冻结副本/独立checker候选不作为独立剪枝重复计数。
5. 凡未激活方法，时间先标NOT_ESTIMATED；不从当前代表内核把整main的搜索难度和扫描域假设成已知。

## 运行纪律

本地工作，不需服务器。服务器数据重算仍要用户明确确认。子代理路由仅用户指定OpenCode Go DeepSeek V4.1 Flash，未恢复时不换路由。当前文件策略danger-full-access且审批禁用，调用不应设置sandbox_permissions。所有旧证书和已封印源不改写，修正另存新版本。总目标保持active，最终收尾报告如有新增结果，应以新证据为准。

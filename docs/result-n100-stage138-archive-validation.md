# 阶段138：归档解压运行与当前最终交付状态

本说明补充[综合研究报告](result-n100-stage136-integrated-study.md)和[完整复现收尾](result-n100-stage137-replay-delivery.md)。

## 归档实证

[研究归档](../runtime/n100-interface-study-137.zip)包含1339个成员，压缩体积21704627字节。构建器对全部归档成员逐项校验SHA256，并通过ZIP CRC检查。证据见[归档回执](../verify/out/n100-study-archive.json)。归档内STUDY-ARCHIVE-MANIFEST.json给出所有成员哈希和范围，保留撤回证据为历史数据，不自动接受其结论。

实际解压到新目录后，在解压包中执行：

```powershell
python verify/run_n100_delivery_audit.py --run-dir runtime/unpacked-fast-audit --manifest runtime/delivery-audit-135/manifest.json
```

退出0；核对467个已封印文件，重放6个精确叶结果、2个分布结果、4个共享支持输入和174个条件门。随后[解包回执核验器](../verify/n100_study_archive_unpacked_receipt.py)实际退出0，证据见[解包运行回执](../verify/out/n100-study-archive-unpacked-audit.json)。此解包测试没有再次跑全4776，不能把快速测试称为包内全量复算；完整4776在前一步快照工作区已通过。

归档在阶段137报告后构建，因此本说明及解包回执核验器不在该归档中，作为外部补充交付。归档本身已含所需快速核验器、正式接口、旧条件契约、原始计时、全量快照、总报告及阶段137说明。

## 已验证的收尾结果

- 4776新目录快照重放退出0，全部主/独立/历史结果一致，564排除、4188传播固定、24达到轮次上限。
- 四项研究隔离重放退出0，原证书不变。新的受负载影响时间不替代正式875热检查和665组合检查的校准。
- [研究交付回执](../verify/out/n100-study-delivery-receipt.json)已实际生成，绑定16接口组、总代价与组合研究证据、全量/隔离复现和总报告。
- 快速核验在原工作区两次、归档解压目录一次通过；本项目当前研究材料的运行可复现性已获这些范围内的实证。

## 未完成项

目标仍active。174个条件旧main尚缺逐源几何/域/输出桥、独立重放和逐main时间。它们的PRECONDITION_MISSING与全量规则清单是显式缺口管理，不能用来声称所有旧剪枝已经可执行。完整n100极小多项式及全局最优性也未解，内部地图全域未覆盖。

没有证据表明遇到不可消除的外部阻塞，因此不把目标标为blocked。下一项具体工作从[交接指针](../runtime/handoff-n100-stage136-study.md)列出的数学桥开始，现有材料无需重复清点或重跑所有已通过计时。

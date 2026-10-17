# 阶段142：M25 hinge修复与费用行探索

目标半径仍为0.11324；本阶段尚未关闭完整B32。

[斜率同步重调入口](../verify/n100_B32_M25_hinge_retuned.py)已运行退出0，[回执](../verify/out/n100-B32-M25-hinge-retuned-142.json)记录三组斜率0.05945、0.0594、0.0593，全部通过原先失败的完整1000区间hinge支持，推进到M25最终面积行。所有斜率调整均同步修改hinge SETTINGS、核验器的斜率断言及FAN费用；没有保留更高旧支付。

## 真正的下一瓶颈

首个失败profile为e=0，两高点度数[7,7]，标记数(0,0)，star_pattern=2。精确面积余量位于

[-21247294773713886889/10^24, -21247294676535946539/10^24]。

两端均严格负，约-0.0000212473。该profile不使用FAN，降低hinge斜率不能补足它。原斜率0.0595的零点真实标量余量本身为正；之前近零区间失败属于当前区间包络不足以证明整个区间，不能误写成点值反例。三组更保守斜率给出了可核验全域支持。

## 新相干费用行探索

[初版发现](../tools/n100_B32_M25_coherent_discover.py)只改变面积比例/周长权重，使用了不准确耳部近似常数1.332634，其[候选](../runtime/B32-M25-coherent-discovery-142/proposal.json)和[回执](../runtime/B32-M25-coherent-discovery-142/receipt.json)明确保留为未接受的发现数据。实际耳部上界约1.42016417919847，不能把初版近似当证书。

[第二版发现](../tools/n100_B32_M25_coherent_discover_v2.py)用实际同半径耳部上界并同时优化高点势、边界势、面积比例和周长权重。[候选](../runtime/B32-M25-coherent-discovery-v2-142/proposal.json)和[发现回执](../runtime/B32-M25-coherent-discovery-v2-142/receipt.json)仍为发现用途，浮点最坏余量未转正。

[精确验收入口](../verify/n100_B32_M25_coherent.py)实际运行退出0，但[数学回执](../verify/out/n100-B32-M25-coherent-142.json)是NOT_CLOSED。全部局部支持已推进到同一最终profile，首个严格不足量约0.0000186055993。未通过81profile全部断言，不能称M25完成。

本阶段确认：适当降斜率能够修复hinge验证，但M25相干面积行仍需加强。为获得实际全局推进，另开启隔离副本内更小增量的统一六分支重放；其结果及证明组合审查另行交付。

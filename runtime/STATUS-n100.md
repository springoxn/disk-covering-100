# n=100 状态层：阶段1严格基线审计

## 阶段48纠错：边界拥有者与对称性

阶段45、46的环带证书使用错误的内面筛选，得到空待检集合，相关“全域无增益”验收作废。标签outer属于外面半边，须由其alpha配对半边定位内面。修正版实际核查32个边界拥有面、4776方案、152832次精确环带比较，仍新增排除0，见[纠错主证书](../verify/out/n100-boundary-owner-correction.json)和[独立证书](../verify/out/n100-boundary-owner-correction-independent.json)。独立检查用边两侧关联和四角最大范数，避免重用错误筛选。此前独立脚本复制了同一错误，exit0不足以保证数学覆盖域正确。

穷尽594个根半边像，核心保持方向及外面的自同构群仅恒等元；不能由此将4776个保留方案去重。反射及整体轴标签旋转未纳入该结论。完整地图生成与保留连续域排除尚未完成，区间与全局未完成状态不变。

## 阶段67更新：固定核心剩余域与有理弧筛选

阶段50完整4776方案圆周传播排除564，阶段51对24个capped深化新增排除12。合并后576严格排除、4200非空保留，真实候选[30,6,14,22]保留；见[完整剩余域](../verify/out/n100-boundary-circle-survivor-domain.json)及[独立分割](../verify/out/n100-boundary-circle-survivor-domain-independent.json)。该数字只适用于一个固定核心，非空不代表可行。

阶段62至65的等距/反向平方/次序承包器在33个测试盒上无额外缩盒。阶段64的64叶消融表明，观察到的进一步收缩与无等距对照最终盒完全相同，不能归功于等距式。阶段66开始采用完整圆周的精确有理弧段外包支持筛选。

阶段67以每象限256段扫描完整间隙类(7,7,7,11)的32案，实际exit0，32 fixed、0 excluded、0 capped，32案均缩盒。总额外盒宽缩减150948600个缩放单位，收敛6至9轮；[完整证书](../verify/out/n100-boundary-arc-class32.json)保存最终盒和掩码，并对全部终态掩码用独立整数端点公式重算。该复核不等于独立重放全部轨迹；输入外包性继承此前证书。见[阶段67报告](../docs/result-n100-stage67-arc-class32.md)。未扫描全部4200案，累计严格排除数不变；下一步可按弧参数分支，而非重复原宽盒。

## 当前状态

阶段207推进0.11324：**B31、B32、B33、B34、B35已完整闭合，B>=36仍未闭合**，见[六分支总账204](../verify/out/n100-11324-six-branch-ledger-204.json)。B34以独立Fraction/CAS总账关闭无弦23模型、单弦47模型，见[完整B34证书](../verify/out/n100-B34-complete-180.json)。B35正确归属全度数slack后，M25/M26剩余分别由8/3/5个环metric模型关闭；低M归约到唯一未标记度5及至少6个q4/度7核心耳，而/5不等式只允许至多1个核心耳，完整[独立B35证书](../verify/out/n100-B35-complete-203.json)实际退出0。先前阶段186的profile曾误挂到上一行，已以阶段190完整gaps纠正，阶段189草稿明确拒绝运行。尾分支旧450万箱未决的原因已定位：[精确点障碍206](../verify/out/n100-tail-support-obstruction-206.json)证明固定MU/LAM/K下capped-pair松弛在有理点高于B36面积允许的最大截距，不能仅增加箱预算或提高截距修补；这不是覆盖反例。下一步同步调整尾分支斜率/罚系数/三角支持或使用更紧相邻透镜约束。全局下界仍0.1132301，0.11324尚未接受。更新前状态保存于[阶段207前备份](STATUS-n100.md.bak-stage207)。

最新接受区间为 **`1132301/10000000 < r_D(100) ≤ 1154469548855829/10^16`**，即 **`0.1132301 < r_D(100) ≤ 0.1154469548855829`**。阶段143沿移植包完整六分支骨架，在隔离副本统一推进半径，固定费用/支持系数不变，两次完整重放退出0；[新下界最终证书](../verify/out/n100-new-lower-bound-143.json)记录全支闭合、精确正余量、CAS全中心规范化恒等式及单次预算组合审查，[依赖追踪](../verify/out/n100-radius-dependency-audit-143.json)记录20进程且没有核验入口半径错配。[阶段143报告](../docs/result-n100-stage143-new-lower-bound.md)给出完整范围与重放入口。下界比原0.11323提高恰1/10000000；更大探测目标0.11324仍有未闭合分支。精确最优及极小多项式未完成，解析几何仍非形式化内核验证。

上界及原0.11323基线来源为外部公开仓库固定提交 `67ebf1c5776f72a7b7786a8655eed5463429ae55`，本地原字节完整重放：[区间证据](../verify/out/external-disk100-bounds-67ebf1c.json)实际退出0、六下界分支全部PASS；[独立上界余量](../verify/out/external-disk100-margin-67ebf1c.json)退出0；[本项目四叉树交叉复核](../verify/out/external-disk100-local-quadtree/replay.json)在稍宽R=.115447下主/独立PASS、未解析0。见[吸收报告](../docs/result-external-disk100-absorption.md)保留的解析几何依赖与审查边界。原移植包未修改，更新前状态备份为[阶段143前状态](STATUS-n100.md.bak-stage143)。

932变量孤立代数KKT根与旋转商严格局部极小性也已在独立副本实际重放；[局部证据](../verify/out/external-disk100-strict-local-67ebf1c.json)包含fresh root/coverage与8/8破坏测试拒绝。它不证明全局最优，真实极小多项式仍未取得。后续主代数路线从该根出发，旧polish候选降为历史。

## VonEquinox方法吸收与新增组合前端

[成果吸收报告](../docs/result-vonequinox-n100-absorption.md)固定DiskCoveringSolve提交0895849；DiskCover链接本次404。19盘双链完整重放已经exit0，24,127轨道、24,126非候选域全排除、未决0，见[新凭证](../verify/out/vonequinox-windows-replay-0895849-20261013-120226/RECEIPT.json)。20盘规范重放最终接受状态也由该凭证更新，19盘通过不自动接受20盘或11..18。固定n证书不当百盘证明。[应力迁移](../docs/n100-vonequinox-stress-transfer.md)完成：406根箱正距离乘子、246节点连通、32锚点接地块PD。第2轮[真实角能量独立区间证书](../verify/out/n100-angular-energy-independent.json)实际exit0，二次型上界<-1/100000；[有理旋转反例](../verify/out/n100-harmonic-energy-relaxation-counterexample.json)实际exit0，允许角域内能量下降>10^-12。当前固定应力的全域凸能量路线不可用，应转逐杆力/约束分支与定量隔离；这不是更优覆盖，不否定54维SOSC，尚未完成候选图全域排除。[独立对抗审计](../verify/out/n100-angular-energy-obstruction-audit.json)进一步确认公式与范围。[通用理论审查](../docs/audit-vonequinox-theory-n100.md)已有[20/20精确断言证据](vonequinox-theory-audit.json)，小n1/2/3模型合法性、覆盖压缩与平方松弛通过；完整退化归约/复杂度引文尚未独立重导，仓库无通用求解器。

本项目新增[全局必要计数组合域](../verify/out/n100-vonequinox-count-domain-bound.json)实际exit0，整数/有理区间，joint常数与凹性恒等式重新核验，未决0。条件于已接受的规范化同图面积几何，在当前U下仅剩m=96..100的87组(m,B)：96:B32..35，97:B29..42，98:B28..46，99:B28..50，100:B28..54。第12轮[LOCAL叶检查](../verify/out/n100-local-leaf-check.json)实际exit0，[局部总账](../verify/out/n100-local-chain-ledger.json)实际exit0、49条哈希链通过；它只接受一个无规范中心盒半宽10^-38的局部排除叶，并明确拒绝由局部证据升级全局。完整图枚举、m<100、其他图、退化、普适下界闭合、不可约性和有理根隔离仍未完成。见[第12轮报告](../docs/result-n100-round12-local-ledger.md)。

## 阶段26：盒内共同圆心与有限模式剪枝

新增[报告](../docs/result-n100-stage26-box-aware-pruning.md)，[独立重放证书](../verify/out/n100-stage26-independent-replay.json)本轮实际退出0：32个由真实候选活跃孔支撑向外扰动生成的中心盒，16排除、16未决，两个继承子盒独立排除；不覆盖完整候选图域，不新排除计数族。主/独立实现采用平均平方距离的盒内下界和有限模式并集动态规划，[模式证据](../verify/out/n100-box-aware-capacity.json)记录两个旧全池容量界未能排除的案例；[候选域证据](../verify/out/n100-candidate-pattern-pruning.json)包含所有域和真实候选负控制。[接口反例证书](../verify/out/n100-boundary-interface-controls.json)纠正子代理审查：分段norm-cap归约不全局单射，不能推断有效中心数不变；服务圆周盘不一定拥有边界弧，不能令k=B。子代理弧长—面积帽改进仍只属未认证数值发现。全局区间不变，最优性及极小多项式未完成。

## 阶段27至32：服务盘前沿与地图模型校准

[任意圆心弧帽引理](../proofs/n100-arbitrary-center-arc-cap.md)在固定上端U给出至少46个非服务盘，主/独立有理支持、CAS恒等式证据见[任意圆心证书](../verify/out/n100-arc-cap-arbitrary-center.json)和[独立前沿](../verify/out/n100-arc-cap-mk-independent.json)；解析几何仍非形式化。87计数族全部保留，不令k=B。阶段27还确认8个父中心盒实际包含已认证连续覆盖，不能继续排除全部候选邻域。

[阶段32模型证书](../verify/out/n100-expanded-map-models.json)实际退出0：45个有限地图轨道编译，2370条多项式独立系数重建与t=1有理赋值通过。[一个内部顶点枚举证书](../verify/out/n100-one-interior-map-enumeration.json)实际退出0：V5/E7/B4、内部度>=3，3628800置换、768合法标记地图、16轨道，与允许重复端点的独立辐条构造一致。首次仅用不同端点构造漏掉平行辐条/二边形，失败后补齐；不得删除该退化分支。见[阶段32报告](../docs/result-n100-stage32-map-models.md)。这些有限族不构成完整百盘枚举，连续域排除数为0，严格区间与全局未完成范围不变。

## 历史：本项目长弦与polish基线

当时严格区间为 **`2787/25000 ≤ r_D(100) ≤ 119877/1000000`**，即 **`0.11148 ≤ r_D(100) ≤ 0.119877`**。新下界事实源：[长弦组合证书](../verify/out/n100-longchord-bundle-frozen.json)，统一重放实际退出0、子退出码 `[0,0]`、`all_passed=true`、`universal_lower_bound_accepted=true`；566个弧数全部枚举、6/6负对照被拒，并绑定最终几何稿SHA256 `658863d2a36118be915fda66f10596f05073aadd51738da55bcf35f967d8cf73`。验证标准为解析几何加独立精确有理算术，`machine_verified_geometry=false`。此前下界 `1111720153/10000000000` 已被提高。最新事实源：[polish独立重放](../verify/out/n100-cooperative-polish-tight/replay.json)，实际退出0，21checks/独立verified，35584叶、最大深度23、未解析0，输入[冻结polish候选](n100-cooperative-polish/best.json)。此前refine严格上界为 `119891/1000000`，已被此值支配。新事实源：[refine独立重放](../verify/out/n100-cooperative-refine-tight/replay.json)，实际退出0，21checks/独立verified，28063叶、最大深度24、未解析0，输入[冻结refine候选](n100-cooperative-refine/best.json)源SHA256 `060163ee5757f79f42a9f8a355618efc9c8af9f7070347c44f057f0aaad4e529`。上一轮[0.1200704证书](../verify/out/n100-cooperative-anchor-tight/replay.json)保留。

协同搜索的新100中心候选已冻结，源哈希 `413af66fccfc2988aae9f52ca666de3cf5c25f3eaf01d98559d0402db3edc722`。独立四叉树重放对 `R=1501/12500` 与更紧 `R=18761/156250=0.1200704` 均退出0；更紧证书见 `verify/out/n100-cooperative-anchor-tight/replay.json`，`all_passed=true`、`independent.verified=true`、`n_unresolved=0`。此前首轮严格区间为 `1111720153/10000000000 ≤ r_D(100) ≤ 18761/156250`，已被上述refine上界进一步收紧。候选半径来自浮点发现后有理覆盖认证，不是最优值或最优半径极小多项式。

先前版本备份为 [原状态](STATUS-n100.md.bak-stage1-20261012)，SHA256 `42b0c676eef4963891cfd2ac028573e9055826a1a25769515a9cd780ee5283b8`。该版本含互相冲突的旧强度标签，不能作为新认证依据。

## 当前事实源

| 内容 | 文件与证据 | 强度 |
|---|---|---|
| 阶段1范围和验收 | [goal计划](goal-plan-n100-stage1.md) | 计划，非数学结论 |
| 历史输入清单 | [输入证据](../verify/out/input_inventory_n100.json)，`sources[0/1].exact_input_valid=true` | 已精确检查两份文件各含100个互异有理中心；不认证覆盖 |
| 输入审计入口 | [审计脚本](../verify/audit_inputs_n100.py)，`python verify/audit_inputs_n100.py` 退出0 | 整数/Fraction输入判定 |
| 证明强度冲突 | [基线审计](../docs/audit-baseline-n100.md) | 已审计并明确降级历史加强界 |
| 统一验收 | [汇总证书](../verify/out/baseline_n100.json)，`all_passed=true`、7个步骤退出0 | `python verify/run_n100.py`实际退出0，约6.13秒 |
| 连续覆盖 | [覆盖证书](../verify/out/coverage_n100.json)，全部21项checks通过 | R=153/1250，22804叶、深度16、未决0 |
| 独立覆盖复核 | [独立证书](../verify/out/independent_coverage_n100.json)，`verified=true` | 整数角点判据，不共享生成器几何函数；3损坏案例拒绝 |
| 覆盖对照 | [对照证据](../verify/out/coverage_controls_n100.json)，`all_controls_passed=true` | 12/12正负对照符合预期 |
| 加强下界 | [完成报告](../docs/result-strengthened-lowerbound-n100.md)、[完整验收](../verify/out/strengthened_lowerbound_n100.json)、[正式证明](../proofs/n100-strengthened-lowerbound-combined.md) | `554570693/5000000000`，解析几何 + 独立审查 + 精确有理算术；无形式化几何内核 |
| 后续试跑规模 | [阶段2/4建议](../docs/pilot-plan-n100.md)，[阶段2报告](../docs/pilot-report-n100-stage2.md) | 阶段2已验收；阶段4未执行 |

历史自由点和退火结果的精确十进制中心列表具有相同规范化哈希，保存的是同一构型；85个中心在单位闭盘内，15个盘外。题面允许盘外中心。

## 历史记录与审计边界

- 约 `0.12234327132827787` 仍是历史发现值；阶段1严格认证 `153/1250=0.1224`，阶段2收紧到 `1223433/10000000=0.1223433`（[证据](../verify/out/pilot_n100_stage2_summary.json)），均不是历史半径的精确等号。充分性证明见[覆盖说明](../docs/coverage-method-n100.md)。
- 历史连续Jensen/不动点链仍保持[原审计](../docs/audit-lowerbound-n100.md)的未证标签，旧面积证书`strengthened_chain.certified=false`保留。新整数边数路线已独立证明精确目标 `0.1109141386`，见[完整验收](../verify/out/strengthened_lowerbound_n100.json)；不把历史发现根和新证明混为一条。
- 面积法给出普适下界 `1/10`：覆盖使 `π ≤ 100πr²`，故 `r ≥ 1/10`；解析证明与精确检查分开说明，并已通过统一入口严格哈希重放。
- 小n实例证书仅认证其实例，不能证明所有n100构型的普适引理。
- 有限随机或局部移动无改进不证明局部最优，有限环族探索不证明族内最优。

## 阶段4：有限见证点校准（已验收）

新的独立阶段goal见 [校准计划](goal-plan-n100-stage4-witness-calibration.md)。本轮已实际重放原加强下界，`python verify/run_strengthened_lowerbound_n100.py --out verify/out/strengthened-lowerbound-stage4-baseline-replay.json` 退出0，见[新重放证书](../verify/out/strengthened-lowerbound-stage4-baseline-replay.json)：`all_passed=true`，原proof/review哈希匹配。原正式证明和审查均不修改。

本地首例生成器 `python verify/witness_calibration_n100.py` 已退出0，见[见证点证书](../verify/out/witness_calibration_n100.json)：21个有理点、32个极大模式、53个可行非空子集、506枚举事件，总权重21/2，在r=7/25排除n=8、9、10。独立checker实际退出0，74项检查、0 failures；统一重放 `python verify/run_witness_calibration_n100.py --out verify/out/witness_calibration_bundle_n100.json` 实际退出0，两步子命令退出码 `[0,0]`，见[统一bundle](../verify/out/witness_calibration_bundle_n100.json)：`all_passed=true`、`verified=true`、证明/输入/checker哈希绑定，`machine_verified_geometry=false`。

解析完整性依赖平面Helly/MEC支撑≤3，未形式化；有限判定只用整数/Fraction。该半径弱于n=8,9,10面积界，不改善n100当前区间。见[校准结果](../docs/result-witness-calibration-n100.md)：本网格r=7/25的对偶最优值精确为12，r≥3/10时8盘即可覆盖见证集，故本构造不能成为超越面积界或迁移到n100的路线。

## 执行边界

用户已授权沿用pilot计划在服务器执行阶段2，范围见[阶段2执行计划](goal-plan-n100-stage2-server.md)。服务器现有crystalx环境导入检查退出0，无环境安装。正式服务器搜索已完成并验收，见[运行记录](server-run-n100-stage2.json)和[精确汇总](../verify/out/pilot_n100_stage2_summary.json)：远程exit0，6轮共916次目标评估/15.746秒，各因连续150次无改进停止；25文件回收SHA256通过。6候选生成器21项检查及独立整数复核均通过、未决0。未发现新构型改善，当前更紧上界来自原构型认证收紧。[阶段报告](../docs/pilot-report-n100-stage2.md)说明平台及扰动拒绝的局限；不追加同类随机重启。子代理显式采用 CommandCode 的 DeepSeek-V4.1-Flash：`deepseek-official / deepseek/deepseek-v4.1-flash`。阶段2goal以预算内试跑、候选严格复核和交接为验收，不以全局最优性为验收。

# n100 阶段2服务器试跑准备交接

用户已要求沿用试跑计划并在服务器计算，本轮goal范围见 [执行计划](goal-plan-n100-stage2-server.md)。目标为两类初值各3种子，搜索总6000次评估或1800秒，先到即停。

## 已有实证

- Paramiko 跳板通路已连接目标 `zhengyj@10.10.2.161`，无需服务器安装。
- `/home/zhengyj/miniconda3/envs/crystalx/bin/python` 导入NumPy/SciPy检查退出0；Python3.12.15、NumPy1.26.4、SciPy1.17.1，见 [环境记录](server-environments-pilot-n100.json)。默认系统Python损坏，aimath缺scipy，不使用。
- [远程入口](run_server_pilot_n100.py) 已编译通过，提供deploy/run/collect，上传SHA256复核、nohup运行、只启动一次的marker、remote exit-code落盘。服务器目录 `/home/zhengyj/adb-n100-stage2-pilot-20261012`，尚未部署/启动。
- [精确重放入口](replay_pilot_candidate_n100.py) 对已有baseline实测退出0，生成器21项检查通过，独立整数角点checker通过；[校准证据](../verify/out/pilot-n100-calibration/replay.json)。

## 正在进行

两个子代理固定 `deepseek-official/deepseek/deepseek-v4.1-flash/high`。

- `7ead89a2-0baf-4b56-9ab4-eeec392f42a5` 实现 `tools/pilot_n100_stage2.py`，截至本文尚未落盘；已要求直接全部Delaunay triangles+所有pair圆边界交点、反向极值，避免KNN漏洞。接口与远程入口一致。
- `6e24613c-6c0e-4204-a3ba-dc77a6a2bef1` 独立审查数学临界点与launcher，报告尚未交付。

## 下一步

脚本交付后读源码及review，小实例自测通过再deploy→run。服务器输出拉回 `runtime/n100-stage2-server/`；必须收集远程真实exit-code，不将本地传输退出0误当计算完成。对入选候选选择安全有理半径，精确重放产物放 `verify/out/`。预算用尽停止，不自动追加随机重启。更新状态、阶段报告、最终handoff后再完成goal。

目前无新的发现候选、无新的认证上界。已证区间仍为 `1/10 ≤ r_D(100) ≤ 153/1250`。

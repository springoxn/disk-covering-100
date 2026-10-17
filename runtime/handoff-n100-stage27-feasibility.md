# n=100 阶段27交接

阶段27实际完成：
- `python verify/n100_expanded_hole_pool.py`：修正池大小限制后退出0；8/16/24/32孔池对16个未决父盒均找到16个显式有限见证覆盖。
- `python verify/n100_stage27_feasibility_audit.py`：退出0；独立重算16个有限覆盖案例，重新运行固定67ebf1c上界覆盖检查器，并确认8个父盒实际包含已认证100盘全盘覆盖配置，索引[3,7,11,15,19,23,27,31]。
- `python verify/n100_stage26_scope_audit.py`：退出0；阶段26的32盒统计16排除/16未决及有限范围通过审计。

证据：`verify/out/n100-expanded-hole-pool.json`、`verify/out/n100-stage27-feasibility-audit.json`、`verify/out/n100-stage26-scope-audit.json`。报告：`docs/result-n100-stage27-feasibility-audit.md`。

当前严格区间不变：`11323/100000 < r_D(100) <= 1154469548855829/10^16`。全局最优性、完整地图枚举和极小多项式均未完成。

关键判断：继续扩大同一批候选活跃孔见证，不能排除包含已认证覆盖配置的父盒。下一轮应研究低于U的新下界、不同组合地图/活跃图，或新的可行候选，而不是继续排除全部当前上界邻域。

重放脚本默认不覆盖既有证据；无后台作业待收集。

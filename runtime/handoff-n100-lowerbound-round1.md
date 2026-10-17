# 下界证明 round 1 交接

目标保持 active：`goal-6f986fd0-2f61-4588-b91e-358a714145df`。精确目标 `554570693/5000000000`；目前没有发布普适下界完成结论，下界事实仍1/10。

## 实際進展

1. 主条件算术脚本[入口](../verify/strengthened_arithmetic_n100.py)实际 `--check verify/out/strengthened_arithmetic_n100.json` 退出0，18项重算通过。
2. [独立Fraction入口](../verify/independent_strengthened_arithmetic_n100.py)实际退出0，15项通过，产物[独立证书](../verify/out/independent_strengthened_arithmetic_n100.json)明确`geometry_certified=false`。未相互导入，主π下界3.14159、独立π下界3.14，正余量严格有理。
3. 发现整数边数路线绕开历史浮点根；历史连续路线根略小于target，约7.59e-12，但根还只是高精度发现，没有exactintervalisolation。
4. [几何文稿](../docs/proof-lowerbound-n100-geometry.md)已落盘、正在作者修订；核心是逐弧cap凸包属于所属凸胞，弦替换产生P的剖分，盘内多边形面积定理免中心归属，平面图对多弧按Barc计数。
5. [首轮读稿修正清单](review-strengthened-first-round-n100.md)保留明确漏洞/措辞错误，已送作者修。

## 继续任务

- 几何作者a1cc0f01-0833-4aff-8d99-64777c55eff8正在修文：cap-only集合减操作、图边细分、孤立tie、边界degree≥3、不连通Kcomponents Euler、最小包围圆有限顶点gap、导数h'=xsinx。
- 算术作者df2f9fb9-e282-40f8-bcc8-32b73a32d993正在修文/脚本doc和重发hashcert：concavef5-6割线仅integerupper，不能连续域supportingline；勿宣称几何“仓库任何地方都没有证明”。保存主check及9负对照证据。
- 独立审查9dc4228c-0a5b-4d3c-a4c1-4168f95ac1f7正在审真实几何文稿；等待明确结论，不凭作者自称闭合发布。

下轮读取修訂稿及独立review、收取实际几何check退出码；必要时完善普适证明而不是追加实例。若全部闭合，构建独立端到端验收汇总（解析lemma单列、算术机器证书单列）、审查清单，更新义务图和STATUS，最后get_goal/update complete。尚未闭合不得完成goal。

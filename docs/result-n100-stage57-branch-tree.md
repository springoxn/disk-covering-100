# 阶段57：最大剩余间隙类代表的空间分支

阶段56选定最大survivor类`(7,7,7,11)`的代表`[0,7,14,21]`。本轮从阶段42根盒重新执行边界圆周/象限/面心—顶点距离传播，然后对最宽内面心坐标作深度5闭区间二分。

主分支树实际退出0，证书verify/out/n100-boundary-circle-branch-tree.json：

- 31个split节点；
- 32个未决叶；
- 0个排除叶；
- 根未排除。

每个split将[lo,hi]拆为[lo,mid]和[mid,hi]，两闭区间并集准确覆盖父区间，共享mid不丢失父域。非空叶保留，不解释为可行配置。

独立结构审计实际退出0，证书verify/out/n100-boundary-circle-branch-tree-independent.json，核查63节点可达、深度、切分严格内部、所有子节点无孤儿，以及32个叶全部未决。它独立核查分支覆盖结构，但传播数值绑定主树证书，未另行重算每个传播节点。

首次运行因优先级证书路径写错而退出1，树生成已完成但未写证书；修正verify/out路径后正式证书通过，首跑不作依据。



## 独立全量传播复核

独立入口verify/n100_boundary_circle_branch_tree_independent_full.py实际退出0，证书verify/out/n100-boundary-circle-branch-tree-independent-full.json。它独立重建面/顶点循环、边界象限、圆周整数承包器和距离承包器，逐节点重放63个节点，核对每个最终盒、状态、失败字段、父区间和两个子盒。此前仅结构审计的限制已解除。

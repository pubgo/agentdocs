## 概述

`mergerfs` 是一个面向 Linux/FUSE 的 union filesystem：把多个独立目录/文件系统聚合为单一挂载视图，目标是降低 RAID 式聚合的复杂度与运维成本。（来源：https://trapexit.github.io/mergerfs/latest）

它的文档结构清晰地分成：快速上手、安装分发、策略配置、运行时接口、FAQ 与已知问题，适合按“部署→调优→排障”路径使用。（来源：https://trapexit.github.io/mergerfs/latest/quickstart/ ，https://trapexit.github.io/mergerfs/latest/setup/installation/ ，https://trapexit.github.io/mergerfs/latest/known_issues_bugs/）

## 核心功能

1. **统一视图聚合**：将多个分支目录整合成一个挂载点，应用侧按普通文件系统使用。（来源：https://trapexit.github.io/mergerfs/latest）
2. **策略驱动行为**：针对不同 POSIX 操作（create/search/action 等）应用不同策略，决定“去哪读/写/创建”。（来源：https://trapexit.github.io/mergerfs/latest/config/functions_categories_policies/）
3. **运行时可观测与可调**：通过 `.mergerfs` pseudo file / xattrs / CLI tooling 在运行中查询与调整行为。（来源：https://trapexit.github.io/mergerfs/latest/runtime_interface/）

## 技术原理

1. **函数分类 + 策略映射**：核心机制不是单一全局策略，而是“函数类别→策略”映射，因此同一挂载点下不同操作可能呈现不同分支选择结果。（来源：https://trapexit.github.io/mergerfs/latest/config/functions_categories_policies/）
2. **ENOSPC 语义是多因素**：空间不足不仅由 data block 决定，也可能由 inode、quota 或底层约束触发。（来源：https://trapexit.github.io/mergerfs/latest/config/moveonenospc/）
3. **跨设备语义约束**：rename/link 在跨分支（底层不同 mount/fs）时可能返回 `EXDEV`，属于文件系统语义边界而非单纯 bug。（来源：https://trapexit.github.io/mergerfs/latest/config/rename_and_link/）

## 配置与实践

1. **先用默认与 Quick Start 模式**：文档明确多数配置项改变的是行为而非“纯性能开关”，初期应先用推荐配置再针对目标场景微调。（来源：https://trapexit.github.io/mergerfs/latest/quickstart/）
2. **安装优先官方较新包/预编译**：在非滚动发行版上，系统仓库版本可能偏旧，需留意版本来源。（来源：https://trapexit.github.io/mergerfs/latest/setup/installation/）
3. **问题定位优先查 FAQ + 已知问题**：对“配置不生效、文件集中到单盘、空间异常、重命名失败”等常见故障，先按 FAQ/known issues 对照排查。（来源：https://trapexit.github.io/mergerfs/latest/faq/why_isnt_it_working/ ，https://trapexit.github.io/mergerfs/latest/known_issues_bugs/）

## 限制与风险

1. **兼容性风险**：部分第三方软件与特定平台（如 FreeBSD、mmap 相关软件、NFS 客户端、部分备份/同步工具）存在已知兼容问题。（来源：https://trapexit.github.io/mergerfs/latest/known_issues_bugs/）
2. **行为边界风险**：hard link/reflink、空间显示差异、cache.files 写入性能波动、阻塞分支等都属于需要显式评估的技术边界。（来源：https://trapexit.github.io/mergerfs/latest/faq/technical_behavior_and_limitations/）
3. **策略误配风险**：若未理解 create/search/action 的策略差异，容易出现“落盘不均衡”或“策略看似无效”的误判。（来源：https://trapexit.github.io/mergerfs/latest/config/functions_categories_policies/ ，https://trapexit.github.io/mergerfs/latest/faq/why_isnt_it_working/）

## 结论与建议

`mergerfs` 适合“多盘聚合 + 保持独立文件系统”的场景，优势在于策略灵活与部署轻量；但稳定落地依赖对策略语义和边界条件的正确理解。（来源：https://trapexit.github.io/mergerfs/latest ，https://trapexit.github.io/mergerfs/latest/config/functions_categories_policies/）

建议按以下顺序实施：**Quick Start 基线配置 → 按函数类别调策略 → 用 runtime interface 观测验证 → 以 FAQ/Known Issues 做故障分流**，可显著降低误配与排障成本。（来源：https://trapexit.github.io/mergerfs/latest/quickstart/ ，https://trapexit.github.io/mergerfs/latest/runtime_interface/ ，https://trapexit.github.io/mergerfs/latest/faq/why_isnt_it_working/ ，https://trapexit.github.io/mergerfs/latest/known_issues_bugs/）

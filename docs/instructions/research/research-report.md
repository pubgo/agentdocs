# mergerfs 研究报告

## 概述
mergerfs 是一个基于 FUSE 的用户态联合文件系统（union filesystem），用于将多个目录/文件系统聚合到单一挂载点，并通过可配置策略决定文件创建、查找和操作落在哪个分支。其定位偏向“灵活聚合与可运营配置”，而非 RAID 式冗余方案。

## 核心功能

### 1. 多分支聚合挂载
- **描述**：将多个底层路径统一呈现为一个逻辑目录树，支持保留底层分支可直接访问。  
- **用例**：家庭媒体库多盘合并、不同类型存储（本地盘/网络盘）统一入口。

### 2. 策略化路由（Policies）
- **描述**：将核心操作分为 `action/create/search` 三类，并为函数或类别绑定策略（如 `pfrd`、`mfs`、`ff`、`epmfs` 等）。  
- **用例**：控制新文件如何分布（按可用空间、随机、首个命中、仅现有路径等）。

### 3. 路径保持（Path Preservation）
- **描述**：`ep*` 系列策略只在“相对路径已存在”的分支上操作；`msp*` 支持向父目录回退查找。  
- **用例**：希望目录结构在多盘间保持一致，避免跨路径散落。

### 4. 多方式部署与运行
- **描述**：支持命令行、`/etc/fstab`、外置 config 文件、systemd 服务化部署。  
- **用例**：生产环境开机自启、集中配置管理、动态扩展分支。

### 5. 高级行为控制
- **描述**：提供缓存、线程、inode 计算、跨设备重命名处理、xattr、NFS 导出相关控制项。  
- **用例**：针对特定应用（下载器、媒体服务、备份系统）做兼容性与性能平衡。

## 技术架构
mergerfs 采用 **FUSE 用户态架构**：内核将文件请求转发到用户态进程，mergerfs 根据配置策略选择分支并执行操作。

架构要点：
- **策略与执行分离**：策略层负责“选分支”，执行层负责实际文件系统调用。
- **过滤机制**：create 类策略会基于只读状态、分支模式（RO/NC/RW）、`minfreespace` 等过滤候选分支。
- **默认策略体系**：常见默认为 `action=epall`、`create=pfrd`、`search=ff`。
- **空间计算语义**：策略计算使用可用块（`f_bavail`），与 `df` 观测可能不完全一致。

## 配置与使用

### 关键配置项
- `category.create=pfrd`：创建时按可用空间比例随机分配。  
- `func.getattr=newest`：目录属性偏向最新 mtime。  
- `minfreespace=SIZE`：创建候选分支最低剩余空间门槛。  
- `moveonenospc`：写入遇 `ENOSPC/EDQUOT` 时迁移并重试。  
- `inodecalc`：inode 生成策略（影响某些备份/32bit 软件兼容性）。  
- `cache.files`：`off|partial|full|auto-full|per-process`，决定页缓存模式。  
- `xattr` / `security-capability`：影响写路径性能与功能可用性。  
- `kernel-permissions-check`、`allow-idmap`：权限与容器映射相关核心选项。

### 常用配置示例（文档推荐常见组合）
```ini
cache.files=off
category.create=pfrd
func.getattr=newest
dropcacheonclose=false
```

### 典型场景
- **媒体池**：多块 HDD 聚合到 `/media`，上层应用统一访问。  
- **容器环境**：需注意 bind mount 与 `EXDEV` 关系，建议挂载更高层路径避免跨设备 rename/link 失败。  
- **NFS/远程文件系统**：可用但需重点关注 ESTALE/EIO 与客户端兼容行为。

## 优势与局限

### 优势
- 配置灵活，策略体系完整，可精细控制创建与查找行为。  
- 非破坏性接入，便于逐步迁移和运维。  
- 用户态实现带来较快迭代与较强跨平台适配能力。  
- 支持多种部署方式，适合从个人到团队环境。

### 局限
- 受 FUSE 边界影响：相较内核态方案有额外延迟/开销。  
- 跨设备语义不可规避：`link/rename` 遇 `EXDEV` 是系统语义限制。  
- 不支持 reflink/FICLONE（受 FUSE 能力限制）。  
- 某些缓存配置会引发明显写性能波动（尤其结合 xattr 查询时）。  
- 底层分支阻塞会传导到 mergerfs 线程，缺乏“超时隔离”手段。

## 总结与建议
mergerfs 适合“**多存储聚合 + 策略化路由 + 可运维配置**”场景，尤其是媒体与归档类工作负载。其核心价值在于灵活与可控，而非冗余与强一致抽象。

建议：
1. 默认从 Quick Start 推荐参数起步，再按应用特性逐步调优。  
2. 涉及下载器/媒体管理器时优先验证 `mmap` 与缓存策略兼容性。  
3. 容器/NFS/SMB 场景优先做 `EXDEV`、ESTALE、权限链路专项验证。  
4. 不将 mergerfs 视作 RAID 替代；需要冗余时与专门方案组合使用。

# ~/.copilot 目录结构分析

本文基于本机路径 `/Users/barry/.copilot` 的实际扫描结果，整理 Copilot 本地目录结构与用途推测，供后续排障和系统提示词工程化时参考。

---

## 1) 顶层结构

`~/.copilot` 当前包含：

- `.DS_Store`（系统文件）
- `command-history-state.json`（命令历史状态）
- `config.json`（Copilot CLI 配置）
- `ide/`（IDE 相关状态目录，当前为空）
- `installed-plugins/`（已安装插件）
- `jb/`（JetBrains 相关状态目录）
- `logs/`（运行日志）
- `session-state/`（会话状态与中间产物）

---

## 2) 关键目录解读

## `session-state/`

- 数量：`86`（扫描时）
- 命名模式：
  - `uuid-like`：`65`
  - `workflow-*`：`20`
  - `other`：`1`（`.DS_Store`）

常见子项（抽样）：

- `research/`
- `workspace.yaml`
- `checkpoints/`
- `files/`
- `vscode.metadata.json`
- `events.jsonl`

说明（推测）：

- `uuid-like` 目录通常对应普通会话
- `workflow-*` 目录通常对应工作流型会话（多阶段/编排模式）
- `events.jsonl` 用于记录会话事件流
- `checkpoints/` 与 `files/` 用于阶段快照与会话工件

### `session-state` 详细结构（重点）

按当前机器样本，典型会话目录结构如下：

```text
session-state/<session-id>/
├─ workspace.yaml
├─ checkpoints/
│  └─ index.md
├─ files/
├─ research/
├─ vscode.metadata.json        # 部分会话存在
├─ events.jsonl                # 部分会话存在
└─ rewind-snapshots/           # 极少数会话存在
```

#### 字段/目录逐项说明

- `workspace.yaml`
  - 几乎所有会话都有（本机样本 81/85）
  - 作用：记录会话关联的工作区上下文（路径、会话工作配置）

- `checkpoints/`
  - 几乎所有会话都有（本机样本 81/85）
  - 常见文件 `index.md`
  - 作用：会话阶段快照索引，便于恢复和回溯

- `files/`
  - 几乎所有会话都有（本机样本 81/85）
  - 作用：会话中间工件目录（非仓库正式文件）

- `research/`
  - 几乎所有会话都有（本机样本 81/85）
  - 作用：检索/分析类中间产物缓存目录

- `vscode.metadata.json`
  - 部分会话有（本机样本 52/85）
  - 作用：IDE 侧元数据（如会话与编辑器上下文关联）

- `events.jsonl`
  - 部分会话有（本机样本 32/85）
  - 作用：事件流日志（按行 JSON），用于精细回放执行过程

- `rewind-snapshots/`
  - 少量会话存在（本机样本 2/85）
  - 作用：回滚/重放相关快照目录

#### 两类 session-id 的差异

- `uuid-like`（例如 `2bbc5bea-e2bb-...`）
  - 常见于普通会话
  - 更容易出现 `events.jsonl` 与 `rewind-snapshots`

- `workflow-*`（例如 `workflow-caadb300`）
  - 常见于工作流编排会话
  - 结构更“流程化”，通常以 `workspace/checkpoints/files/research` 为核心

#### 可以怎么用

- 定位“某次会话做了什么”：
  1. 先看对应目录下 `events.jsonl`（如果存在）
  2. 再看 `checkpoints/index.md` 的阶段索引
  3. 最后结合 `files/` 与 `research/` 看中间产物

- 排查“会话恢复异常”：
  - 优先检查 `workspace.yaml`、`checkpoints/` 是否完整
  - 再对照 `logs/process-*.log` 看运行时错误

## `logs/`

- 数量：`178`（扫描时）
- 文件形态：`process-<timestamp>-<id>.log`

说明（推测）：

- 每次进程或子进程执行会生成独立日志文件
- 用于排查 CLI 运行时异常、插件加载问题、会话中断等

## `installed-plugins/`

- 当前可见插件目录：`awesome-copilot`

说明（推测）：

- 存放通过插件机制安装的扩展内容
- 可用于确认插件是否安装成功与版本变更影响

## `jb/`

- 含一个 UUID 子目录（以及 `.DS_Store`）

说明（推测）：

- 可能是 JetBrains 集成路径对应的会话或状态缓存

---

## 3) 与项目文档的关系

建议将以下两个文档配套阅读：

- `reference/copilot-discovery-order.md`：发现顺序（查找路径优先级）
- `reference/copilot-directory-structure.md`（本文）：本地状态落盘结构

二者区别：

- Discovery Order 解决“去哪里找配置”
- Directory Structure 解决“运行后写到了哪里”

---

## 4) 实操建议

- 排障优先看 `~/.copilot/logs/`
- 会话追踪优先看 `~/.copilot/session-state/<session-id>/events.jsonl`
- 自动化脚本若要做清理，建议只清理旧会话目录，不要直接删根目录
- 涉及行为回溯时，先保留 `session-state` 与 `logs` 再做清理

---

## 5) 注意事项

- 本文是基于当前机器快照，不同版本或不同运行方式下目录结构可能变化。
- 文件语义有部分为工程推测，建议结合具体日志内容做二次确认。


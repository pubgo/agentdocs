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


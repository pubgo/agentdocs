---
description: "编辑 Go 后端代码时使用：API handler、Copilot SDK 集成、会话管理、Registry CRUD、并发模式。"
applyTo: "internal/**/*.go,cmd/**/*.go"
---
# Go 后端约定

## Handler 模式

每个 handler 是一个闭包工厂函数，返回 `http.HandlerFunc`：

```go
func handleXxx(mgr *copilot.Manager) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // 1. jsonDecode 解析请求体（POST/PUT）
        // 2. 参数校验 + 默认值
        // 3. 调用 Manager 或 Registry
        // 4. jsonOK / jsonError 响应
    }
}
```

- 路由注册使用 Go 1.22+ ServeMux 语法：`mux.HandleFunc("METHOD /api/path/{id}", handleXxx(dep))`
- 路径参数取值：`r.PathValue("id")`
- 请求体结构体定义在 `router.go` 中，非导出，JSON tag 作为 API 合同
- 响应统一用 `jsonOK(w, data)` 和 `jsonError(w, code, msg)`

## Copilot SDK 交互规则

- Manager 是唯一持有 `*sdk.Client` 的组件，不要在其他地方直接构造 SDK 对象
- 创建/恢复会话**必须**设置 `OnPermissionRequest: sdk.PermissionHandler.ApproveAll`
- 不要对 protobuf message 做值拷贝（含 `sync.Mutex`），需要快照用 `proto.Clone`
- API 模型默认回退：请求中模型字段为空时设为 `gpt-5.3-codex`

## 并发安全

- Manager 和 Registry 内部状态用 `sync.RWMutex` 保护
- 读操作用 `RLock/RUnlock`，写操作用 `Lock/Unlock`
- 新增方法必须遵循相同的锁模式

## Registry CRUD 模式

```go
func (r *Registry) AddXxx(x *XxxType) {
    r.mu.Lock()
    defer r.mu.Unlock()
    if x.ID == "" {
        x.ID = uuid.New().String()
    }
    r.xxxMap[x.ID] = x
}
```

- 新增对象无 ID 时自动分配 UUID
- Get 返回 `(*T, bool)`，Delete 返回 `bool`

## 错误处理规范

- 错误包装统一使用 `fmt.Errorf("上下文: %w", err)`
- handler 层直接 `jsonError(w, statusCode, err.Error())`；不要在 Manager/Registry 层写 HTTP 响应

## TeamOrchestrator 模式

- `TeamOrchestrator` 是内存态的团队编排器，挂在 `Manager.Orchestrator` 上
- 阶段状态机：`team-plan` → `prd` → `exec` → `verify` → `fix` → `complete`、`failed`、`cancelled`
- 转换通过 `TransitionPhase(id, phase)` 执行，内部校验有效性（`IsValidTransition`）
- 每个阶段映射到 prompt 角色（`PhasePromptRole`）和指令（`PhaseInstructions`）
- fix 阶段有 `MaxFixAttempts` 限制，超过则自动转 failed
- handler 返回 run 状态时附带 `phase_role` 和 `phase_instructions` 辅助字段

## 任务模板 模式

- `MissionTemplate` 通过 `builtinMissionTemplates()` 种子数据注入，`Builtin: true`
- 从模板创建 Mission：读取模板字段 → 填充 Mission 结构 → `eventStore.SaveMission()`
- `RouteTaskToRole(desc)` 是纯关键词匹配，不调用 LLM，返回 `[]RoleRouterResult`（有分数排序）

## WorkflowEngine 模式

- `WorkflowEngine` 挂在 `Manager.WorkflowEngine` 上，由 `NewWorkflowEngine(mgr, reg)` 构造
- Workflow 定义通过 Registry CRUD 管理，持久化到 `~/.coagent/workflow_defs.json`
- 内置定义由 `builtinWorkflowDefs()` 注入（例如 `wf-team-pipeline`、`wf-codereview-business`、`wf-tdd-cycle`），`Builtin: true` 的定义不可删除
- `wf-codereview-business` 支持变量 `disable_coverage_gate`（默认 `false`，即开启覆盖门禁）
- `StartWorkflow(ctx, defID, vars)` 创建 `workflow-{runID[:8]}` 前缀的独立 session，后台 goroutine 执行
- 系统提示词由 `buildSystemPrompt(def, vars)` 组合三部分：base 框架 + `<instructions>` 用户自定义 + `<workflow>` 步骤流程描述
- 步骤执行 `executeStep` 注入 `<role>` prompt 内容 + 渲染 input template，通过 SSE 收集输出
- 条件评估使用 `expr-lang/expr`，变量有 `output`、`output_length`、`step_retries`、`round`、`total_steps`、`vars`
- Run 状态：pending → running → completed / failed / cancelled
- `RestartWorkflow` 重用 session，round++ 从 entry step 重新执行

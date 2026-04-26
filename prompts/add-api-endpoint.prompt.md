---
description: "为 coagent 添加新的 REST API 端点：生成 Go handler、路由注册、前端 API 函数和 UI 绑定。"
agent: "agent"
---
为 coagent 添加一个新的 API 端点，涉及以下四层改动：

## 1. 配置结构体 (`internal/copilot/config.go`)

如果需要新的数据模型，在 `config.go` 中定义结构体，JSON tag 作为 API 合同：

```go
type XxxInfo struct {
    ID   string `json:"id"`
    Name string `json:"name"`
    // ...
}
```

## 2. Manager 或 Registry 方法 (`internal/copilot/`)

- 如果是会话/消息相关 → 在 `manager.go` 添加方法
- 如果是资源配置 CRUD → 在 `registry.go` 添加方法
- 遵循 `sync.RWMutex` 并发保护模式
- 新增对象无 ID 时分配 `uuid.New().String()`

## 3. API Handler（`internal/api/router.go`）

在 `router.go` 中完成以下步骤：

1. 定义非导出请求体结构体（如需要）
2. 实现 handler 闭包工厂函数：`func handleXxx(dep) http.HandlerFunc`
3. 在 `Router()` 函数中注册路由：`mux.HandleFunc("METHOD /api/path", handleXxx(dep))`
4. 使用 `jsonDecode` 解析请求，`jsonOK`/`jsonError` 生成响应
5. 路径参数通过 `r.PathValue("id")` 获取

## 4. 前端适配（`web/`）

1. **api.js** — 添加对应的 API 调用函数，路径参数用 `encodeURIComponent` 编码
2. **main.js** — 在 `coagentApp()` 中添加状态变量和调用方法
3. **index.html** — 用 Alpine.js 指令绑定 UI（`x-model`、`@click`、`x-show` 等）

## 验证步骤

```bash
go vet ./...
go build ./cmd/coagent
```

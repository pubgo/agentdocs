# 项目协作 Skills 速览

记录团队常用的开发风格与约定，便于快速对齐。

## 服务与路由
- **Service 构造**：统一 `func New(p Params) Rsp`，`Params` 注入依赖，`Rsp` 仅暴露 proto 中的 `XxxServiceServer` 字段；内部 `server` 结构体嵌入 `Unimplemented*` 与 `Params`。
- **Router 构造**：`func New(p Params, srv servicesv1.XxxServiceServer) lava.GrpcRouter`；中间件（Auth/Audit 等）只在 Router 层绑定，Service 保持纯业务。
- **生成代码**：`pkg/gen/` 禁止手改；改 `proto/` 或 `schemas/` 后 `task gen`，并执行 `task db:schema:create` 更新 DB。

## 编码习惯
- **ID/类型转换**：Ent ID 用 `string`，Proto 用 `uint64`，显式 `strconv.ParseUint/FormatUint`；失败返回 0 或错误。
- **错误与日志**：用 `pubgo/funk` 包装错误；日志使用 `log.Logger`，避免库层 `panic`。
- **格式与检查**：`gofmt` 或 `task fmt`，`task lint`，`task test`；保持 import/变量无未使用。
- **配置/密钥**：配置由 `pubgo/funk` 读取；缺失的敏感项用占位符写入 `.env`/`configs` 并提醒补全。

## 前端习惯
- 技术栈：React 18 + Vite + TypeScript + shadcn/ui。
- 状态：Zustand；API Client：`frontend/src/gen`（protobuf-ts）。
- 依赖：优先 `pnpm`（或 `task frontend:install`）；检查类型 `task frontend:lint`。

## 常用 Task 命令
- Backend: `task build` / `task run` / `task dev` / `task test` / `task lint` / `task fmt` / `task gen`
- Frontend: `task frontend:dev` / `task frontend:build` / `task frontend:lint` / `task frontend:install`
- DB/Ent: `task db:ent:new -- <SchemaName>` / `task db:ent:gen` / `task db:schema:create`

> 如有新增约定，请同步更新本文件和 `.github/copilot-instructions.md`。

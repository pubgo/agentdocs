# Skill: 调试与排错

## 描述
调试 welogin 项目的常见问题。

## 触发词
- "调试"
- "排错"
- "问题排查"
- "报错"

## 后端调试

### 1. 启动调试模式
```bash
# 使用 delve 调试
dlv debug ./cmd/welogin -- grpc --config=./configs/welogin.yaml

# VS Code launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug welogin",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}/cmd/welogin",
      "args": ["grpc", "--config=./configs/welogin.yaml"]
    }
  ]
}
```

### 2. 日志调试
```go
import "log/slog"

slog.Info("调试信息", "key", value)
slog.Debug("详细调试", "request", req)
slog.Error("错误", "error", err)
```

### 3. 常见问题

#### 数据库连接失败
```bash
# 检查数据库配置
cat configs/components/db.yaml

# 测试数据库连接
task db:schema:diff
```

#### Proto 生成代码过期
```bash
task proto:gen
task proto:gen:ts
```

#### Ent 代码过期
```bash
task db:ent:gen
```

#### 依赖问题
```bash
task tidy
go mod download
```

## 前端调试

### 1. 开发者工具
```bash
cd frontend
pnpm dev  # 启动开发服务器，支持 HMR
```

### 2. gRPC-Web 调试
检查网络请求：
- 打开浏览器开发者工具 > Network
- 筛选 `grpc-web` 或 `application/grpc`
- 查看请求/响应内容

### 3. 常见问题

#### CORS 错误
确保后端配置了正确的 CORS：
```yaml
# configs/welogin.yaml
server:
  cors:
    allowed_origins: ["http://localhost:5173"]
```

#### Proto 类型不匹配
```bash
# 重新生成前端 proto 代码
cd frontend && pnpm run gen:proto
```

#### 依赖问题
```bash
cd frontend
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## 数据库调试

### 查看 SQL 日志
在 Ent 客户端启用调试：
```go
client.Debug()
```

### 直接查询数据库
```bash
# PostgreSQL
psql -h localhost -U user -d welogin

# SQLite
sqlite3 .local/welogin.db
```

### 重置数据库
```bash
# 删除并重建
task db:schema:create
```

## 性能分析

### pprof
```go
import _ "net/http/pprof"

go func() {
    http.ListenAndServe(":6060", nil)
}()
```

```bash
go tool pprof http://localhost:6060/debug/pprof/profile
```

### 追踪
```bash
curl http://localhost:6060/debug/pprof/trace?seconds=5 > trace.out
go tool trace trace.out
```

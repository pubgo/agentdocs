---
description: "编辑 Go 测试文件时使用：table-driven 测试模式、httptest 用法、并发安全测试、mock 约定、覆盖率要求。"
applyTo: "**/*_test.go"
---
# Go 测试约定

## 测试结构

所有测试采用 table-driven 模式：

```go
func TestXxx(t *testing.T) {
    tests := []struct {
        name     string
        // 输入字段
        // 期望输出字段
        wantErr  bool
    }{
        {name: "正常路径", ...},
        {name: "空输入", ...},
        {name: "错误场景", ...},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // 准备 → 执行 → 断言
        })
    }
}
```

## API Handler 测试

使用 `httptest` 包测试 handler：

```go
req := httptest.NewRequest(http.MethodGet, "/api/xxx", nil)
w := httptest.NewRecorder()
handler := handleXxx(dep)
handler.ServeHTTP(w, req)
// 检查 w.Code 和 w.Body
```

- 路径参数需通过 `req.SetPathValue("id", "xxx")` 设置
- POST/PUT 请求体用 `strings.NewReader` 或 `bytes.NewBufferString` 构造

## Registry 测试

Registry 是纯内存 CRUD，直接测试：

```go
reg := copilot.NewRegistry()
// 测试 Add → Get → List → Update → Delete 完整生命周期
```

- 验证无 ID 时自动分配 UUID
- 验证 Get 不存在的 ID 返回 `false`

## 并发安全测试

```go
func TestXxx_Concurrent(t *testing.T) {
    var wg sync.WaitGroup
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            // 并发读写操作
        }()
    }
    wg.Wait()
}
```

- 使用 `go test -race ./...` 检测竞态条件
- Manager 和 Registry 的所有公开方法都应有并发测试

## 命名规范

- 测试函数：`TestXxx`（对应被测函数名）
- 子测试名：简洁的中文或英文描述，如 `"正常创建"`、`"ID为空"`
- 测试文件：与源文件同目录，`xxx_test.go`

## 注意事项

- Manager 依赖 SDK Client，集成测试用 `t.Skip("需要 Copilot SDK 连接")` 标记
- 运行前确保工作目录在仓库根目录
- 测试中不要引入新的外部依赖

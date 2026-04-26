# Skill: 编写测试

## 描述
为 welogin 项目编写单元测试和集成测试。

## 触发词
- "编写测试"
- "添加单元测试"
- "测试用例"

## Go 测试

### 目录结构
测试文件与源文件放在同一目录，以 `_test.go` 结尾：

```
internal/welogin/services/serviceauth/
├── service.go
└── service_test.go
```

### 基础测试模板

```go
package serviceauth_test

import (
    "context"
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/pubgo/welogin/internal/welogin/services/serviceauth"
)

func TestService_Login(t *testing.T) {
    // Arrange
    ctx := context.Background()
    service := setupTestService(t)
    
    // Act
    resp, err := service.Login(ctx, &weloginv1.LoginRequest{
        Email:    "test@example.com",
        Password: "password123",
    })

    // Assert
    require.NoError(t, err)
    assert.NotEmpty(t, resp.AccessToken)
}

func setupTestService(t *testing.T) *serviceauth.Service {
    // 设置测试依赖
    t.Helper()
    // ...
    return &serviceauth.Service{}
}
```

### 表驱动测试

```go
func TestService_Validate(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        wantErr bool
    }{
        {
            name:    "valid email",
            input:   "test@example.com",
            wantErr: false,
        },
        {
            name:    "invalid email",
            input:   "invalid",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := validate(tt.input)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

### 数据库测试 (Ent)

```go
func TestDB_CreateAccount(t *testing.T) {
    // 使用 SQLite 内存数据库测试
    client := enttest.Open(t, "sqlite3", "file:ent?mode=memory&_fk=1")
    defer client.Close()

    ctx := context.Background()
    
    // 创建测试数据
    account, err := client.Account.Create().
        SetEmail("test@example.com").
        SetUsername("testuser").
        Save(ctx)
    
    require.NoError(t, err)
    assert.Equal(t, "test@example.com", account.Email)
}
```

## 运行测试

```bash
# 运行所有测试
task test

# 运行特定包测试
go test -v ./internal/welogin/services/serviceauth/...

# 运行特定测试
go test -v -run TestService_Login ./internal/welogin/services/serviceauth/

# 生成覆盖率报告
task test:cover
```

## 测试工具

### Mock 生成
使用 `mockgen` 生成 mock：

```bash
mockgen -source=interface.go -destination=mock_interface.go
```

### 断言库
项目使用 `testify`：

```go
import (
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/mock"
)

// assert: 断言失败继续执行
assert.Equal(t, expected, actual)
assert.NoError(t, err)

// require: 断言失败立即停止
require.NoError(t, err)
require.NotNil(t, result)
```

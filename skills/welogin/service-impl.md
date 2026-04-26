# Skill: 实现业务服务

## 描述
为 welogin 项目实现 gRPC 业务服务。

## 触发词
- "实现服务"
- "创建 service"
- "业务逻辑"

## 步骤

### 1. 创建服务目录
在 `internal/welogin/services/` 下创建新目录：

```
internal/welogin/services/serviceyour/
├── service.go      # 服务实现
└── helpers.go      # 辅助函数 (可选)
```

### 2. 实现服务接口

```go
package serviceyour

import (
    "context"

    "github.com/pubgo/dix/v2"
    "github.com/pubgo/funk/v2/errors"
    weloginv1 "github.com/pubgo/welogin/pkg/gen/proto/welogin/v1"
    "github.com/pubgo/welogin/pkg/gen/db/welogindb"
)

var _ weloginv1.YourServiceServer = (*Service)(nil)

type Service struct {
    weloginv1.UnimplementedYourServiceServer

    db *welogindb.Client `dix:""`
}

func init() {
    dix.Register(func() weloginv1.YourServiceServer {
        return &Service{}
    })
}

func (s *Service) YourMethod(ctx context.Context, req *weloginv1.YourRequest) (*weloginv1.YourResponse, error) {
    // 1. 参数校验 (protobuf validate 已处理基础校验)
    
    // 2. 业务逻辑
    result, err := s.db.YourEntity.
        Query().
        Where(yourentity.NameEQ(req.Name)).
        First(ctx)
    if err != nil {
        return nil, errors.Wrap(err, "查询失败")
    }

    // 3. 返回响应
    return &weloginv1.YourResponse{
        Id:   result.ID,
        Name: result.Name,
    }, nil
}
```

### 3. 创建路由

在 `internal/welogin/routers/` 创建：

```go
package routers

import (
    "github.com/pubgo/dix/v2"
    "github.com/pubgo/lava/v2/lava"
    "google.golang.org/grpc"
    weloginv1 "github.com/pubgo/welogin/pkg/gen/proto/welogin/v1"
    "github.com/pubgo/welogin/internal/welogin/middlewares"
)

var _ lava.GrpcRouter = (*YourRouter)(nil)

type YourRouter struct {
    service weloginv1.YourServiceServer `dix:""`
    auth    *middlewares.Auth           `dix:""`
}

func init() {
    dix.Register(func() lava.GrpcRouter {
        return &YourRouter{}
    })
}

func (r *YourRouter) ServiceDesc() *grpc.ServiceDesc {
    return &weloginv1.YourService_ServiceDesc
}

func (r *YourRouter) Middlewares() []lava.Middleware {
    return []lava.Middleware{
        r.auth.RequireAuth(),  // 需要登录
    }
}

func (r *YourRouter) RegisterService(s grpc.ServiceRegistrar) {
    weloginv1.RegisterYourServiceServer(s, r.service)
}
```

### 4. 注册到 Bootstrap

在 `bootstrap/boot.go` 中导入包以触发 `init()` 注册：

```go
import (
    _ "github.com/pubgo/welogin/internal/welogin/services/serviceyour"
)
```

## 常用模式

### 事务操作
```go
tx, err := s.db.Tx(ctx)
if err != nil {
    return nil, err
}
defer tx.Rollback()

// 执行操作...

if err := tx.Commit(); err != nil {
    return nil, err
}
```

### 从 Context 获取用户信息
```go
accountID := middlewares.GetAccountID(ctx)
sessionID := middlewares.GetSessionID(ctx)
```

### 错误处理
```go
import "github.com/pubgo/funk/v2/errors"

return nil, errors.Wrap(err, "描述")
return nil, errors.New("错误信息")
```

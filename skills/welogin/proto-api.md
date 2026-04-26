# Skill: 创建 Protobuf API

## 描述
为 welogin 项目创建新的 gRPC API 定义。

## 触发词
- "创建 API"
- "添加 protobuf"
- "新建 proto"
- "定义接口"

## 步骤

### 1. 创建 Proto 文件
在 `proto/welogin/v1/` 目录下创建 `.proto` 文件：

```protobuf
syntax = "proto3";

package welogin.v1;

option go_package = "github.com/pubgo/welogin/pkg/gen/proto/welogin/v1;weloginv1";

import "google/api/annotations.proto";
import "validate/validate.proto";

service YourService {
  rpc YourMethod(YourRequest) returns (YourResponse) {
    option (google.api.http) = {
      post: "/api/v1/your/method"
      body: "*"
    };
  }
}

message YourRequest {
  string field = 1 [(validate.rules).string.min_len = 1];
}

message YourResponse {
  // 响应字段
}
```

### 2. 生成代码
```bash
task proto:gen      # 生成 Go 代码
task proto:gen:ts   # 生成 TypeScript 代码
```

### 3. 实现服务
在 `internal/welogin/services/` 创建服务实现：

```go
package serviceyour

import (
    "context"
    weloginv1 "github.com/pubgo/welogin/pkg/gen/proto/welogin/v1"
)

type Service struct {
    weloginv1.UnimplementedYourServiceServer
    // 依赖注入
}

func (s *Service) YourMethod(ctx context.Context, req *weloginv1.YourRequest) (*weloginv1.YourResponse, error) {
    // 实现逻辑
    return &weloginv1.YourResponse{}, nil
}
```

### 4. 注册路由
在 `internal/welogin/routers/` 注册服务：

```go
package routers

import (
    "github.com/pubgo/lava/v2/lava"
    "google.golang.org/grpc"
    weloginv1 "github.com/pubgo/welogin/pkg/gen/proto/welogin/v1"
)

type YourRouter struct {
    service weloginv1.YourServiceServer
}

func (r *YourRouter) ServiceDesc() *grpc.ServiceDesc {
    return &weloginv1.YourService_ServiceDesc
}

func (r *YourRouter) Middlewares() []lava.Middleware {
    return nil
}

func (r *YourRouter) RegisterService(s grpc.ServiceRegistrar) {
    weloginv1.RegisterYourServiceServer(s, r.service)
}
```

## 验证命令
```bash
task proto:lint     # 检查 proto 文件
task build          # 确保编译通过
```

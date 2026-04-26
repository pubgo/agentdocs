---
description: "审查 Go 代码的并发安全、锁模式、错误处理和 coagent 项目中的常见陷阱。"
agent: "agent"
---
审查提供的 Go 代码，重点检查以下方面：

## 并发安全

- `sync.RWMutex` 使用是否正确：读操作用 `RLock/RUnlock`，写操作用 `Lock/Unlock`
- 是否存在未加锁的共享状态访问
- `defer Unlock()` 是否紧跟 `Lock()` 调用
- 是否有锁内执行耗时操作（网络调用、阻塞 IO）的情况

## SDK 交互检查

- 是否对 protobuf message 做了值拷贝（应使用 `proto.Clone`）
- 创建/恢复会话是否设置了 `OnPermissionRequest`
- 是否正确使用 `context.Context` 传播取消信号

## 错误处理检查

- 错误是否用 `fmt.Errorf("上下文: %w", err)` 包装
- handler 层是否正确映射到 HTTP 状态码
- 是否有被忽略的 error 返回值

## API 约定检查

- JSON tag 是否与现有 API 合同一致
- 新增 handler 是否遵循闭包工厂模式
- 路由注册是否使用 `"METHOD /path"` 语法

## 输出格式

按严重程度分类（严重 / 警告 / 信息），给出文件名、行号、问题描述和修复建议。

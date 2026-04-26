# [挂钩 (.json)](https://code.visualstudio.com/docs/copilot/customization/hooks)

代理会话的确定性生命周期自动化。使用钩子来强制执行策略、自动验证并注入运行时上下文。

## 地点

|路径|范围 |
|------|--------|
| `.github/hooks/*.json` |工作空间（团队共享）|
| `.claude/settings.local.json` |本地工作区（未提交）|
| `.claude/settings.json` |工作空间 |
| `~/.claude/settings.json` |用户简介 |

来自所有配置位置的钩子被收集并执行；工作空间和用户挂钩不会相互覆盖。

## 挂钩事件

|活动 |触发|
|------|--------|
| `会话开始` |新代理会话的首次提示 |
| `用户提示提交` |用户提交提示 |
| `PreToolUse` |工具调用之前 |
| `PostToolUse` |工具调用成功后 |
| `预压缩` |上下文压缩之前 |
| `子代理启动` |子代理启动 |
| `SubagentStop` |子代理结束 |
| `停止` |代理会话结束 |

## 配置格式

@@代码块0@@

每个钩子命令支持：
- `type`（必须是`command`）
- `命令`（默认）
- `windows`、`linux`、`osx` （平台覆盖）
- `cwd`、`env`、`超时`

## 输入/输出合约

Hooks 在 stdin 上接收 JSON，并可以在 stdout 上返回 JSON。

- 常见输出：`continue`、`stopReason`、`systemMessage`
- `PreToolUse` 权限从 `hookSpecificOutput.permissionDecision` 读取 (`allow` | `ask` | `deny`)
- `PostToolUse` 输出可以使用 `decision: block` 阻止进一步处理

`PreToolUse` 示例输出：

@@代码块1@@

退出代码：
- ‘0’成功
- `2` 阻塞错误
- 其他值产生非阻塞警告

## Hooks 与其他自定义

|原始|行为 |
|------|--------|
|说明/提示/技能/代理|指导（非确定性）|
|挂钩|运行时执行和确定性自动化 |

当必须保证行为时使用钩子（例如：阻止危险命令、强制验证、自动注入上下文）。

## 核心原则

1. 保持 hook 小且可审计
2. 验证和清理钩子输入
3. 避免在脚本中硬编码秘密
4. 更喜欢工作空间挂钩用于团队策略，用户挂钩用于个人自动化

## 反模式

- 运行长钩会阻碍正常流动
- 在简单说明就足够的情况下使用钩子
- 让代理编辑挂钩脚本而无需审批控制
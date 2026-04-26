---
description: "根据 git 暂存区的改动生成 Conventional Commits 格式的提交信息。"
agent: "agent"
tools: [execute]
---
根据当前 git 暂存区（staged）的改动，生成一条符合 Conventional Commits 规范的提交信息。

## 执行步骤

1. 运行 `git diff --staged --stat` 查看改动文件概览
2. 运行 `git diff --staged` 查看具体改动内容
3. 分析改动意图，生成提交信息

## 提交信息格式

```
<类型>(<范围>): <简短描述>

<正文：解释做了什么以及为什么>
```

### 类型选择

| 类型 | 适用场景 |
|------|----------|
| `feat` | 新功能 |
| `fix` | 修复缺陷 |
| `refactor` | 重构（不改变行为） |
| `test` | 添加或修改测试 |
| `docs` | 文档变更 |
| `style` | 格式调整（不影响逻辑） |
| `chore` | 构建、依赖等杂务 |

### 范围参考

| 范围 | 对应目录 |
|------|----------|
| `api` | `internal/api/` |
| `copilot` | `internal/copilot/` |
| `web` | `web/` |
| `cmd` | `cmd/` |

## 输出要求

- 简短描述不超过 50 个字符
- 用中文撰写正文
- 如果改动涉及多个不相关的变更，建议拆分为多条提交

---
name: event-visualizer
description: "分析 Copilot 会话事件，生成 turn/subagent/tool-call 树的 Mermaid 图。用于：可视化会话流程、调试 agent 行为、理解工具调用层级。"
argument-hint: "会话 ID 或 'current' 表示当前活跃会话"
---
# 事件可视化器

分析 Copilot 会话的事件流，生成结构化的 Mermaid 流程图。

## 使用场景

- 调试 agent 行为：查看 turn、subagent、tool call 的层级关系
- 分析会话流程：可视化一次对话的完整执行路径
- 排查问题：定位失败的 tool call 或异常的 subagent 嵌套

## 执行流程

1. **获取事件数据**

   通过 coagent API 拉取会话事件：
   ```bash
   curl -s http://localhost:8080/api/sessions/{SESSION_ID}/messages
   ```

2. **运行分析脚本**

   使用 [analyze.py](./scripts/analyze.py) 解析事件 JSON，提取树结构：
   ```bash
   curl -s http://localhost:8080/api/sessions/{SESSION_ID}/messages | python3 .github/skills/event-visualizer/scripts/analyze.py
   ```

3. **解读输出**

   脚本输出包含：
   - **摘要统计**：turn 数、tool call 数、subagent 数、总事件数
   - **Mermaid 图**：可直接粘贴到 Markdown 渲染

## 事件类型参考

| 类型 | 含义 |
|------|------|
| `assistant.turn_start/end` | Agent 回合开始/结束 |
| `subagent.started/completed/failed` | 子 Agent 生命周期 |
| `tool.execution_start/complete` | 工具调用开始/完成 |
| `user.message` | 用户输入 |
| `assistant.message_delta` | 增量消息（通常过滤） |

## 输出格式

返回 Mermaid 代码块和摘要统计，可直接在 Markdown 中渲染。

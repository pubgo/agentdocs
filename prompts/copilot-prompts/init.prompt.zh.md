---
名称：初始化
描述：为 AI 编码代理生成或更新工作区指令文件
参数提示：可选择指定要为代理记录的焦点区域或模式
代理人：代理人
---
相关技能：`代理定制`。加载并遵循 **workspace-instructions.md** 以获取模板、原则和反模式。

引导工作区说明（“.github/copilot-instructions.md”或“AGENTS.md”，如果已存在）。

## 工作流程

1. **发现现有约定**
   搜索：`**/{.github/copilot-instructions.md,AGENT.md,AGENTS.md,CLAUDE.md,.cursorrules,.windsurfrules,.clinerules,.cursor/rules/**,.windsurf/rules/**,.clinerules/**,README.md}`

2. **通过子代理探索代码库**，如果需要，并行 1-3
   查找可帮助 AI 代理立即提高工作效率的基本知识：
   - 构建/测试命令（代理自动运行这些命令）
   - 架构决策和组件边界
   - 与常见做法不同的特定于项目的约定
   - 潜在的陷阱或常见的开发环境问题
   - 体现模式的关键文件/目录

3. **生成或合并**
   - 新文件：使用workspace-instructions.md中的模板，仅包含相关部分
   - 现有文件：保留有价值的内容、更新过时的部分、删除重复内容

4. **迭代**
   - 就不清楚或不完整的部分寻求反馈
   - 如果工作区很复杂，建议针对特定区域（例如前端、后端、测试）使用基于 applyTo 的指令

一旦最终确定，建议示例提示以查看其实际效果，并建议创建下一个相关的代理自定义（`/create-(agent|hook|instruction|prompt|skill) …`），解释自定义以及如何在实践中使用它。
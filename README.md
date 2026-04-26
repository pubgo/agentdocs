# agentdocs

统一存放 Agent 相关文档、提示词、技能、模板和流程配置。

## 目录说明

- `agents/`: Agent 定义（`*.agent.md`、`*.agent.yaml` 等）
- `prompts/`: 各类提示词文档（`*.prompt.md`、角色提示词等）
- `skills/`: Skill 目录与实现说明（通常包含 `SKILL.md`）
- `instructions/`: 规范与流程说明（开发、测试、发布、评审等）
- `reference/`: 外部参考资料索引与收藏
- `hooks/`: 本地或协作流程使用的钩子配置
- `workflows/`: CI/CD 或自动化流程定义
- `templates/`: 模板类文档（如系统提示词模板）
- `tools/`: 工具清单与工具使用说明
- `missions/`: 任务包或实验任务集合
- `memory-tool/`: 记忆模式与相关文档
- `.version/`: 版本号与 changelog

## 当前整理规则

- 以“内容可复用”为目标，优先放在根目录对应分类下。
- 历史来源目录（例如某些仓库内的 `.github`、`docs`）内容已迁移到根目录分类目录。
- 迁移策略默认是：
  - 合并（merge）
  - 不覆盖已有文件（no overwrite）
  - 若后续遇到同名冲突，保留两个版本（通过改名区分来源）

## 使用建议

- 新增 Agent 时优先放到 `agents/`
- 新增提示词时优先放到 `prompts/`
- 新增技能说明时优先放到 `skills/`
- 新增规范文档时优先放到 `instructions/`

建议保持目录命名稳定，避免后续自动迁移或脚本同步时出现重复目录。

## 参考文档

- `reference/awesome.md`: Awesome Skills 参考入口
- `reference/templates-analysis.md`: templates 三文件深度分析
- `reference/template-modules-glossary.md`: 模板标签模块详解字典
- `reference/template-modules-dependency.md`: 模板模块依赖关系图与组装顺序
- `reference/prompt-system-v1-generator.md`: 可填空 Prompt System v1 生成器
- `reference/copilot-discovery-order.md`: Copilot 文件发现目录与顺序
- `reference/copilot-directory-structure.md`: `~/.copilot` 本地目录结构分析
- `reference/multi-agent-architecture-mermaid.md`: 多 Agent 协作架构图与流程图（Mermaid）

## 系统提示词模板

- `templates/system.core.md`: 系统提示词核心层（身份、边界、优先级、DoD）
- `templates/system.runtime.md`: 运行时执行层（工具策略、改动纪律、验证门）
- `templates/orchestration.md`: 编排层（模式选择、委派协议、工作流闭环）

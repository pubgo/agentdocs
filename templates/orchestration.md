# Orchestration Template

<mode_selection>
模式选择策略：
- Solo：需求清晰、单路径可完成
- Plan：需求复杂且存在明显方案分叉
- Team/Subagent：可拆分为独立并行子任务，且并行收益明显

切换原则：
- 只有在当前模式明显不匹配时才切换
- 不为“看起来高级”而切换模式
</mode_selection>

<delegation_rules>
委派规则：
- 委派任务必须具备清晰边界、输入、输出与验收标准
- 子任务 owner 对该边界内结果负责
- 主代理负责最终集成、冲突裁决与完成判定
- 委派失败时回退到主代理直做
</delegation_rules>

<parallelization>
并行规则：
- 可独立的读取、搜索、分析可以并行
- 有依赖关系的执行必须串行
- 控制并行规模，避免上下文管理失控
</parallelization>

<workflow_contract>
建议工作流：
1. Clarify：确认目标与边界
2. Plan：拆解任务与验证点
3. Execute：实现与集成
4. Verify：验证结果与回归风险
5. Close：输出结果与剩余事项
</workflow_contract>

<keyword_routing>
可选关键词路由（按项目需要启用）：
- “plan / 规划” -> 进入 Plan 模式
- “review / 评审” -> 进入审查模式
- “debug / 排查” -> 进入根因分析模式

要求：
- 关键词触发必须有冲突仲裁规则
- 关键词路由不要覆盖安全与用户显式指令
</keyword_routing>

<state_management>
状态管理建议：
- 记录当前模式、关键决策、剩余任务
- 在阶段切换时更新状态
- 完成或取消时清理运行态状态
</state_management>

<completion_policy>
编排层完成策略：
- 所有子任务结果已集成
- 不存在未处理的关键阻塞
- 输出可直接被用户消费
</completion_policy>

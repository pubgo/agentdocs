# 当前主流多 Agent 组合模式调研（2026）

本文聚焦“当前比较好用、可落地”的多 Agent 协作模式与设计模式，目标是帮助你做架构选型，而不是只看概念。

---

## 1. 结论先行（TL;DR）

当前最实用的模式组合是：

1. **Planner + Executor（计划执行分离）** 作为基础骨架  
2. **Supervisor（中心路由）** 作为默认编排模式（2~5 个 agent 时最稳）  
3. **Critic/Verifier（评审门）** 作为质量与安全门禁  
4. 视需求叠加：
   - **Concurrent 并行分工**（独立任务加速）
   - **Handoff/Swarm 去中心化交接**（低延迟优先场景）
   - **Loop 迭代改进**（质量打磨或自修复）

一句话：  
**先“中心化稳态”再“去中心化提速”，并始终保留验证闭环。**

---

## 2. 主流模式清单（按工程常用度）

## 2.1 Planner + Executor（计划-执行分离）

定义：

- Planner 只负责拆解目标、生成结构化计划，不直接调工具
- Executor 只负责按步骤执行工具调用与结果归一化

优点：

- 可观测性强（计划可存档、可 diff、可回放）
- 失败定位清晰（是计划错还是执行错）
- 适合团队分工（策略与工具适配可并行迭代）

风险：

- 计划与执行契约不清时会扯皮
- 计划过细会增加 token 成本

适用：

- 中高复杂度任务、可审计流程、工具调用较多场景

---

## 2.2 Supervisor（中心调度，层级编排）

定义：

- 一个中心协调者根据上下文把任务路由给不同 specialist agent
- worker 完成后回到 supervisor 再决策下一步

优点：

- 路由逻辑集中，易治理
- 适合 2~5 个角色清晰的 agent 团队
- 人类介入点好放（审批、停机、升级）

风险：

- 多一跳路由，带来额外延迟与成本
- supervisor 质量决定上限

适用：

- 企业内多角色协作、质量优先、可控优先的系统

---

## 2.3 Concurrent 并行模式

定义：

- 多 agent 同时处理同一输入或并行子任务，再聚合结果

优点：

- 吞吐与时延表现好
- 可做多视角评估（research/security/correctness）

风险：

- 结果聚合复杂（冲突、重复、排序）
- 并行分支状态隔离问题

适用：

- 任务天然可并行（独立分析、多专家并审）

---

## 2.4 Handoff / Swarm（去中心化交接）

定义：

- agent 之间直接 handoff，不一定经过中心 supervisor

优点：

- 少一次中心路由，延迟更低
- 对话连续性强（当前活跃 agent 可持续处理）

风险：

- 全局可观测性弱于中心化
- 容易出现路由漂移和边界不清

适用：

- 实时交互、低延迟要求高、角色边界非常明确的场景

---

## 2.5 Maker-Checker / Committee Review（实现者-评审团）

定义：

- Implementer 负责产出
- Reviewer panel 按维度并行评审（正确性/安全/测试）
- Orchestrator 聚合 verdict，失败则回流修复

优点：

- 降低“自评盲区”
- 适合高风险变更（代码、安全、合规）

风险：

- 成本与时延增加
- reviewer 标准不一致会循环拉扯

适用：

- PR 评审、关键变更、上线前质量门

---

## 2.6 Critic-before-Execution（执行前评审）

定义：

- 在“计划阶段”插入 critic，先批计划再放行执行

优点：

- 错误在最便宜阶段被拦截（未触发外部动作前）
- 对多步骤依赖链任务价值高

风险：

- 简单任务会显得过重

适用：

- 多步骤、代价高、不可逆风险高的任务

---

## 2.7 Sequential / Loop（顺序流水线与迭代环）

定义：

- Sequential：固定顺序执行
- Loop：Critic/Refiner 循环直到达标或到达上限

优点：

- 结构清晰、可预测
- 非常适合标准化流程（写-评-改）

风险：

- 过度刚性
- Loop 需要严格终止条件，防死循环

适用：

- 稳定 SOP、迭代精修、质量收敛流程

---

## 3. 选型建议（实战）

## 3.1 默认起手式（推荐）

- **Supervisor + Planner/Executor + Verifier**

这是“稳定优先”的默认组合，适合大多数生产系统。

## 3.2 什么时候加并行

满足以下两个条件再加 Concurrent：

1. 子任务之间无强依赖
2. 聚合规则可定义（去重、冲突优先级、失败处理）

## 3.3 什么时候用 Swarm/Handoff

仅在以下场景优先：

- 低延迟强诉求
- agent 职责边界非常清晰
- 你已具备较强监控与追踪能力

## 3.4 什么时候加 Critic/Committee

- 安全风险高
- 业务影响大
- 人工回滚代价高

建议使用“2~3 轮上限 + 超限升级人工”。

---

## 4. 推荐组合蓝图（给你可直接用）

## 4.1 开发协作（代码生产）

- Planner -> Executor(s) -> Reviewer Panel -> Verifier -> Merge Gate

## 4.2 文档/方案生成

- Planner -> Writer -> Critic -> Refiner(loop<=N) -> Verifier

## 4.3 实时对话系统（速度优先）

- Supervisor 起手 -> 稳定后按域切换到 Handoff/Swarm -> 保留最终 Verifier

---

## 5. 设计模式层面的“硬规则”

1. **职责单一**：planner 不执行，executor 不重规划  
2. **路由可解释**：每次分派都可追溯原因  
3. **结果结构化**：评审结果必须结构化（JSON/schema）  
4. **终止条件明确**：loop 必须有 max-iterations 或硬停止信号  
5. **质量门独立**：不要让 implementer 自己决定“是否通过”  
6. **先稳后快**：先中心化稳定，再去中心化提速

---

## 6. 对你当前仓库的落地建议

基于你已整理的模板体系（core/runtime/orchestration）：

- 在 `templates/orchestration.md` 明确 3 条默认策略：
  - 默认 Supervisor
  - 高风险任务自动启用 Critic gate
  - Loop 轮次上限 + 升级人工
- 在 `templates/system.runtime.md` 增加结构化评审输出约束
- 在 `workflows/`（或后续 workflow 定义）中实现：
  - 并行评审（correctness/security/test）
  - 聚合器（去重、分级、回流）

---

## 7. 参考来源

- [Microsoft Agent Framework - Workflow Orchestrations](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/)
- [Microsoft Agent Framework - Concurrent](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/concurrent)
- [Microsoft Agent Framework - Handoff](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/handoff)
- [Microsoft Agent Framework - Magentic](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic)
- [Google ADK - Workflow Agents 概述](https://google.github.io/adk-docs/agents/workflow-agents/)
- [Google ADK - Sequential Agents](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
- [Google ADK - Parallel Agents](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
- [Google ADK - Loop Agents](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
- [Planner + Executor Pattern（工程实践文）](https://blogs.utilia.dev/planner-executor-pattern-architecting-reliable-agents)
- [AgentPatterns - Committee Review Pattern](https://agentpatterns.ai/code-review/committee-review-pattern/)
- [AgentPatterns - Critic Agent Pattern](http://agentpatterns.ai/agent-design/critic-agent-plan-review/)
- [LangGraph Swarm Handoff 实现](https://github.com/langchain-ai/langgraph-swarm-py/blob/main/langgraph_swarm/handoff.py)

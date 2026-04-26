# 多 Agent 协作开发架构图与流程图（仓库映射版）

本文基于当前仓库结构（`agents/`、`instructions/`、`skills/`、`tools/`、`workflows/`、`templates/`）给出可直接使用的 Mermaid 图。

---

## 1) 系统架构图（目录映射版）

```mermaid
graph TD
    U[用户需求] --> O[Orchestrator 主控代理]

    subgraph TemplateLayer[模板与策略层]
        T1[templates/system.core.md]
        T2[templates/system.runtime.md]
        T3[templates/orchestration.md]
        T4[templates/AGENTS.md]
    end

    subgraph CapabilityLayer[能力层]
        A[agents/ 角色代理定义]
        I[instructions/ 执行规范]
        S[skills/ 领域技能]
        TO[tools/ 工具能力清单]
    end

    subgraph KnowledgeLayer[知识与参考层]
        R1[reference/templates-analysis.md]
        R2[reference/template-modules-glossary.md]
        R3[reference/template-modules-dependency.md]
        R4[reference/prompt-system-v1-generator.md]
    end

    subgraph DeliveryLayer[交付层]
        W[workflows/ 自动化流程]
        G[Git/CI/CD]
        D[交付输出 PR/Release/文档]
    end

    O --> T1
    O --> T2
    O --> T3
    O --> T4

    O --> A
    O --> I
    O --> S
    O --> TO

    O --> R1
    O --> R2
    O --> R3
    O --> R4

    O --> W
    W --> G
    G --> D
```

---

## 2) 协作流程图（需求到交付）

```mermaid
sequenceDiagram
    participant U as 用户
    participant O as Orchestrator
    participant P as Planner Agent
    participant E as Executor Agents
    participant R as Reviewer Agent
    participant V as Verifier
    participant W as Workflows/CI

    U->>O: 提交需求（功能/修复/重构）
    O->>P: 生成任务分解与依赖
    P-->>O: 任务图（优先级+并行建议）

    O->>E: 分派执行（按 agents/roles）
    E->>E: 按 instructions/ + skills/ 实施改动
    E-->>O: 回传变更结果与说明

    O->>R: 发起代码评审
    R-->>O: 问题清单（阻塞/建议）

    alt 存在阻塞问题
        O->>E: 回流修复任务
        E-->>O: 修复完成
    else 无阻塞问题
        O->>V: 触发验证门
        V->>W: 运行 workflows / tests / checks
        W-->>V: 验证结果
        V-->>O: 通过/失败
    end

    alt 验证通过
        O-->>U: 交付完成（可合并/发布）
    else 验证失败
        O-->>U: 返回失败原因与下一轮计划
    end
```

---

## 3) 模块装配流程图（你后续搭系统提示词可用）

```mermaid
flowchart TD
    S0[确定目标与边界] --> S1[配置 templates/system.core.md]
    S1 --> S2[配置 templates/system.runtime.md]
    S2 --> S3[配置 templates/orchestration.md]
    S3 --> S4[接入 agents + instructions + skills]
    S4 --> S5[定义 workflows 与验证门]
    S5 --> S6[运行冒烟测试]
    S6 --> S7[进入迭代优化]
```

---

## 4) 使用建议

- 架构图用于说明“模块关系”，适合设计评审
- 协作流程图用于说明“执行路径”，适合团队协作
- 模块装配图用于说明“落地顺序”，适合搭建新项目

如果后续你要区分 Go/Frontend/Docs 三条 lane，我可以再给你一版带“并行泳道”的时序图。

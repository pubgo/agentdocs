# VS Code Copilot & Agent 技术分享

---

## 开场

今天分享的主题是：**如何通过配置驱动的方法，将 AI Agent 从"能用"推进到"可落地"**。

一个背景信息：我们团队使用 Copilot 主要集中在代码补全和简单问答。现在，PR 评审、测试生成、CI 修复等环节都有 Agent 参与。关键变化不在于技术能力的提升，而在于建立了一套**配置驱动的 Agent 治理体系**。

今天的内容分四个板块：

| 板块              | 主题        | 核心目标                      |
| ----------------- | ----------- | ----------------------------- |
| **A. 规则体系**   | 1~5         | 通过配置文件约束 Agent 行为   |
| **B. 认知工具**   | 6~8         | 资源导航、行为约束、问题诊断  |
| **C. 集成与协议** | 9~11        | 从 IDE 扩展到终端、平台、产品 |
| **D. 工程闭环**   | 12~14 + RLM | 从"偶发成功"到"稳定交付"      |
| **E. 跨项目协作** | 专题        | 多项目联合开发的 Agent 方案   |

---

# A. 规则体系：通过配置约束 Agent 行为

> 这一组解决的核心问题：**Agent 缺乏项目上下文。** 不提供规则，它只能依赖通用知识推测——推测的准确率不可控。

## 主题 1：`/init`

类比来说，`/init` 相当于给 Agent 提供一份项目级的"入职文档"。

执行 `/init` 会一键生成 `copilot-instructions.md`、`AGENTS.md`、`CLAUDE.md` 等规则文件，分别面向不同的 AI Agent，内容结构一致。

其中 `copilot-instructions.md` 是**全局生效**的——每次与 Copilot 对话时都会自动加载，相当于 Agent 的持久化上下文。

`/init` 执行时会参考 `vscode-copilot/create-skill.prompt.md` 中定义的模板，因此生成内容是结构化的，而非随机的。生成后需要补充以下信息：

```
1. 必跑命令（build、test、lint）
2. 禁止操作（不可删除 migration、不可修改 proto 文件）
3. 目录约定（标注生成代码目录，避免手动修改）
```

三个关键特性：
- **幂等**：可反复执行，不会覆盖已有规则，仅补齐缺失部分
- **项目隔离**：每个仓库需要独立执行，因为每个项目的规则不同
- **模板驱动**：生成逻辑来自 prompt 模板，团队可统一定制

> **🎬 现场演示：** 在空仓库中执行 `/init`，查看生成的文件结构；再执行一次，验证幂等性；打开一次 Copilot 对话，确认 `copilot-instructions.md` 已自动加载。

实践效果：我们团队引入 `/init` 后，Agent 首次任务成功率从不到 50% 提升到 80% 以上。

---

## 主题 2：`/create-instructions`

`/init` 提供的是项目级规则，粒度较粗。`/create-instructions` 解决的是更细粒度的问题——**为特定功能或特定目录定义专属规则**。

它有两种典型用法：

**用法一：为特定功能定义规则。** 比如 ORM 模型怎么定义、API 路由怎么注册、Protobuf 文件怎么编写——每种功能都有自己的规范，需要将功能的目录路径与对应规则绑定。

**用法二：为特定目录下的文件定义规则。** 比如 `tests/` 下的测试用例需要遵循哪些约定，`docs/**/*.md` 文档需要满足什么格式要求。

示例——为 API 路由定义规则（`instructions/api-routes.instructions.md`）：

```markdown
## 适用范围
api/routes/**/*.go

## 必须
- 所有 handler 必须接收 context 参数
- 错误返回必须使用 status code，不允许 200 + error body
- 路由注册必须使用 group 分组

## 禁止
- 禁止在 handler 中直接编写 SQL
- 禁止在路由层做业务逻辑判断
```

示例——为文档目录定义规则（`instructions/docs.instructions.md`）：

```markdown
## 适用范围
docs/**/*.md

## 必须
- 每篇文档必须包含标题、概述、使用方式三个部分
- 代码示例必须可运行
```

核心价值：规则与目录/功能精确匹配，Agent 在处理不同模块时自动加载对应规范。规则可版本化、可 Code Review、可跨团队复用。

---

## 主题 3：`/create-agent` — 角色拆分与单一职责

当一个 Agent 同时承担安全评审、测试生成、代码修复等多种职责时，每项任务的完成质量都会下降。`/create-agent` 解决的是 **Agent 角色分工**问题。

定义 Agent 时遵循三个原则：**单一职责 + 最小权限 + 固定输出格式**。

以我们的 `pr-review` Agent 为例，它只承担三项职责：
1. 检查是否存在未覆盖的测试路径
2. 检查是否存在安全风险
3. 输出结构化评审意见

> 参考实际定义：`agents/pr-review-orchestrator.agent.md`

这些 Agent 定义本身就是团队的**知识资产**——角色职责明确、可复用、新成员可直接使用。

---

## 主题 4：`/create-skill`

`/create-skill` 用于将知识和流程封装为 LLM 可理解、可执行的标准化技能。它有两类核心用途：

**用途一：封装第三方类库和框架的使用方法。**

LLM 对通用知识有较好的覆盖，但对特定版本的框架 API、团队封装的内部库、或非主流工具的用法，往往不够准确。`/create-skill` 可以将这些使用方法以 LLM 可理解的方式描述出来，使 Agent 按照正确的方式调用。

```
Skill: 使用内部 ORM 框架
描述: 基于 internal/orm 封装的数据访问层
使用方式:
  1. 模型定义放在 models/ 目录，继承 BaseModel
  2. 查询使用 orm.Query[T]() 泛型接口，不使用原生 SQL
  3. 迁移文件通过 orm migrate generate 自动生成
注意事项:
  - 不支持跨库 join，需要使用 service 层聚合
  - 软删除默认开启，硬删除需要显式调用 HardDelete()
```

**用途二：封装团队常用的工具和流程。**

将团队日常重复执行的操作流程标准化，使 Agent 可以按照既定步骤自动完成。

```
Skill: 修复 Bug
输入: issue 链接 / 错误日志
步骤:
  1. 复现（找到最小复现路径）
  2. 定位（缩小到具体函数）
  3. 修复（改动最小化）
  4. 回归（跑相关 test suite）
完成标准: CI 绿 + 原 issue 场景不再复现
```

核心价值：一方面将第三方库和框架的使用知识转化为 Agent 可消费的上下文，弥补 LLM 对特定技术栈的知识盲区；另一方面将团队的工具链和工作流程标准化，降低对个人经验的依赖。

---

## 主题 5：`/create-prompt`

`/create-prompt` 用于创建 Prompt 模板，它是**触发调用 Agent 的入口**。

每个 Prompt 模板可以指定使用通用 Agent 或自定义 Agent 来执行。也就是说，前面通过 `/create-agent` 定义的角色、通过 `/create-skill` 封装的流程，最终都通过 Prompt 模板来触发调用。

```markdown
---
mode: agent               # 使用通用 Agent
# mode: pr-review         # 或指定自定义 Agent
---

请对当前 PR 进行评审，输出结构化评审意见。
重点关注：未覆盖的测试路径、安全风险、API 兼容性。
```

典型应用场景：PR 总结、API 评审、Changelog 生成、Bug 修复触发等。一次定义模板，后续每次调用都保持一致的输入结构和执行流程。

核心定位：Prompt 模板是整个 Agent 治理体系的**调用层**——rules 定义约束，agent 定义角色，skill 定义方法，prompt 定义入口。

---

> **板块 A 小结：** `/init` 定义项目规则，`/create-instructions` 细化模块规范，`/create-agent` 划分角色职责，`/create-skill` 封装方法流程，`/create-prompt` 固定高频模板。五个命令构成一套完整的 **Agent 治理体系**。

---

# B. 认知工具：资源导航、行为约束、问题诊断

> 规则定义完成后，还需要三类配套能力。

## 主题 6 & 14：Awesome 资源站与开源社区工具

这两个主题的核心观点一致：**善用已有生态，避免重复建设**。

Copilot 生态已有完善的资源导航（Awesome）和开源工具链。建议的使用路径：先通过 Learning Hub 建立整体认知，再按实际场景选取 1~2 个工具试用。

工具选型可按三层筛选：
- **协议基础设施**：MCP SDK、ACP 参考实现
- **协作编排**：Agent 框架、A2A 网关
- **模板与资产**：现成的 Instructions / Skills / Prompts 仓库

---

## 主题 7：System 提示词——深入解析

前面讲的 instructions 和 skills 作用于特定任务或领域。System 提示词则位于最高层级——它定义了 Agent **是谁、能做什么、不能做什么、怎么做**。每次对话开始时，VS Code 会把 System 提示词注入到上下文最前端，所有后续交互都在这个框架内进行。

理解 System 提示词的分层结构，对我们编写自定义指令、调试 Agent 行为都非常关键。

### 7.1 整体分层架构

System 提示词并不是一段平铺的文本，而是由多个 **XML 标签块**组成的分层结构。可以参考 `templates/system.md`（约 535 行），其整体层次如下：

```
System 提示词
├── 基础身份定义（7 行）
│   ├── 角色声明："You are an expert AI programming assistant"
│   ├── 身份约束：被问名字必须回答 "GitHub Copilot"
│   └── 内容策略：Microsoft 内容政策、版权保护、有害内容拒绝
│
├── <instructions>  核心行为规则
├── <securityRequirements>  安全要求
├── <operationalSafety>  操作安全
├── <implementationDiscipline>  实现纪律
├── <parallelizationStrategy>  并行策略
├── <taskTracking>  任务跟踪
├── <toolUseInstructions>  工具使用
│   └── <toolSearchInstructions>  延迟工具发现
├── <communicationStyle>  沟通风格
├── <notebookInstructions>  Notebook 处理
├── <outputFormatting>  输出格式
│   └── <fileLinkification>  文件链接规则
├── <memoryInstructions>  记忆系统
│   └── <memoryScopes>  三级记忆范围
│
└── 动态注入区（项目相关内容）
    ├── copilot-instructions.md 附件
    ├── <instructions> 列表（per-directory .instructions.md）
    ├── <skills> 列表
    └── <agents> 列表
```

### 7.2 各层详解

**基础身份（第 1-7 行）**

最顶层的 7 行定义了 Agent 的角色、名称和红线。这部分是硬编码的，用户无法覆盖。例如即使你在 instructions 里写"你叫小助手"，Agent 被问名字时仍会回答"GitHub Copilot"。内容策略也在此设定：遇到有害内容请求，直接拒绝，不走后续流程。

**`<instructions>` — 核心行为规则**

这是最关键的一层，定义了 Agent 的基本工作模式：

- **默认实现，而非建议**："implement changes rather than only suggesting them"——Agent 会直接编辑文件，而不是告诉你"你可以这样改"。
- **持续执行到完成**：不会中途停下来问"要继续吗？"，而是一直执行直到任务完成。
- **主动收集上下文**：遇到信息不足时，Agent 会通过工具调用主动搜索补全，而非猜测。
- **不暴力重试**：如果一种方法不行，会寻找替代方案，不会反复执行同一个失败操作。

这解释了为什么 Copilot Agent 模式下，你提一个需求它会直接动手改文件——这是 System 提示词里写死的行为。

**`<securityRequirements>` — 安全要求**

内置了 OWASP Top 10 安全清单，要求 Agent 生成的代码必须规避以下漏洞：

- 注入攻击（SQL、XSS、命令注入）
- 权限控制缺陷
- 密码学误用
- SSRF

同时要求 Agent 对工具返回的数据保持警惕，检测潜在的 prompt 注入。不得生成恶意软件、DoS 工具，不得猜测 URL。

**`<operationalSafety>` — 操作安全**

区分了 **可逆操作** 和 **不可逆操作**：

| 操作类型      | 行为     | 示例                                   |
| ------------- | -------- | -------------------------------------- |
| 可逆/本地     | 直接执行 | 编辑文件、运行测试                     |
| 不可逆/破坏性 | 必须确认 | `rm -rf`、`git push --force`、删除分支 |
| 对外可见      | 必须确认 | Push 代码、评论 PR、发消息             |

这就是为什么 Agent 改本地文件很果断，但你让它 push 代码时会问你要不要继续。

**`<implementationDiscipline>` — 实现纪律**

这一层防止 Agent 过度工程化。四条核心约束：

1. **范围**：不要超出请求范围。修一个 bug 不需要顺便重构周围代码。
2. **文档**：不要给没改过的代码加注释和 docstring。
3. **防御编码**：不要为不可能发生的场景写异常处理。
4. **抽象**：不要为一次性操作创建工具函数。

这层规则控制了 Agent 的"克制度"——如果你发现 Agent 只改了一行而不是顺便美化了半个文件，就是这个模块在起作用。

**`<parallelizationStrategy>` — 并行策略**

指导 Agent 如何并行调用工具：把独立的只读操作（比如同时搜索多个文件）批量执行，减少交互轮次。

**`<taskTracking>` — 任务跟踪**

指导 Agent 使用 todo list 管理复杂任务。你在对话中看到 Agent 创建待办清单、逐项标记完成，就是这个模块驱动的行为。

**`<toolUseInstructions>` — 工具使用规则**

这是最长的一个模块（约 100 行），核心规则包括：

- 改代码前必须先读代码，不得对没看过的代码提建议
- 优先编辑已有文件，而非创建新文件
- 不要把工具名称暴露给用户（说"我来运行命令"而不是"我来用 run_in_terminal"）
- 独立的工具调用尽量并行执行
- 读文件时一次多读，而非反复小量读取

其中嵌套的 `<toolSearchInstructions>` 管理**延迟加载工具**——并非所有工具一开始就可用，Agent 需要先通过正则搜索"发现"工具，才能调用。这是一种动态能力发现机制。

**`<communicationStyle>` — 沟通风格**

定义了 Agent 的表达风格：

- 简洁直接，不说废话
- 简单问题 1-3 句话回答
- 不加无意义的开场白（"好的，我来帮你……"）
- 执行完操作后简短确认，而非复述做了什么

甚至给出了示例对话："what's the square root of 144?" → "12"。

**`<outputFormatting>` — 输出格式**

规定了 Markdown 格式要求，其中最重要的是 `<fileLinkification>` 子模块——要求 Agent 提到文件时必须生成可点击的链接而非纯文本。这就是为什么 Agent 回复中的文件名是可点击跳转的。

**`<memoryInstructions>` — 记忆系统**

定义了三级记忆架构：

| 范围   | 路径                 | 持久性         | 用途                     |
| ------ | -------------------- | -------------- | ------------------------ |
| 用户级 | `/memories/`         | 跨项目、跨对话 | 偏好、常用命令、经验教训 |
| 会话级 | `/memories/session/` | 当前对话       | 任务上下文、进度笔记     |
| 仓库级 | `/memories/repo/`    | 当前仓库       | 代码约定、构建命令       |

用户级记忆自动加载到上下文中（前 200 行），这是 Agent 能"记住"你之前说过什么的基础。

### 7.3 动态注入——项目级内容的加载

System 提示词的后半段是**动态的**，根据你打开的项目自动填充。这也是 System 提示词最具实际价值的部分，它把前面讲的 instructions / skills / agents 全部串联起来：

**① `copilot-instructions.md` 作为附件加载**

项目根目录的 `.github/copilot-instructions.md` 会被完整注入到 System 提示词中——不是引用，是全文粘贴。所以这个文件里写的一切对 Agent 来说等同于系统级指令。

**② `.instructions.md` 按 `applyTo` 模式匹配**

每条 instruction 声明了适用的文件类型。只有当对话涉及匹配文件时，对应的指令才会被加载：

```xml
<instruction>
  <description>编辑 Go 后端代码时使用</description>
  <file>.github/instructions/go-backend.instructions.md</file>
  <applyTo>internal/**/*.go,cmd/**/*.go</applyTo>
</instruction>
```

这意味着你在聊前端问题时，Go 的指令不会被加载——减少了上下文占用，也避免了指令冲突。

**③ Skills 按需发现**

每个 skill 注册一个名称和描述，Agent 在遇到相关任务时决定是否读取 skill 文件：

```xml
<skill>
  <name>event-visualizer</name>
  <description>分析 Copilot 会话事件，生成 Mermaid 图</description>
  <file>.github/skills/event-visualizer/SKILL.md</file>
</skill>
```

Skill 文件本身不会被预加载，只有 Agent 判断需要时才主动读取。

**④ Agents 注册可用子代理**

列出当前项目中可用的 Agent 及其能力描述，Agent 在需要委派子任务时从中选择：

```xml
<agent>
  <name>test-writer</name>
  <description>编写 Go 单元测试</description>
</agent>
```

### 7.4 分层的实际意义

为什么要理解这些分层？因为调试 Agent 行为时，你需要知道**哪一层在起作用**：

- Agent 总是直接改文件而不问你？→ `<instructions>` 里写了"默认实现"
- Agent 拒绝帮你写某段代码？→ 可能触发了 `<securityRequirements>` 的安全红线
- Agent 改代码很克制，不顺便重构？→ `<implementationDiscipline>` 在约束
- Agent 提到文件时生成了链接？→ `<outputFormatting>` 的 fileLinkification 规则
- Agent 记住了你上次说的偏好？→ `<memoryInstructions>` 的用户级记忆

同时，我们编写自定义 instructions 时也应该参考这个分层思路。推荐的编写结构：

```
1. 目标：需要完成什么
2. 约束：哪些操作禁止
3. 流程：执行顺序
4. 验证：完成的判定标准（可检验的，而非主观判断）
5. 输出格式：返回的数据结构
```

这样 Agent 的输出具有确定性边界，降低随机性。

---

## 主题 8：调试视图

> **🎬 这个主题直接演示。**

使用 Agent 时最常见的问题是：**结果不符合预期，但无法定位原因。**

调试视图提供了完整的运行时可观测性，重点关注三项信息：

1. **上下文输入**：Agent 实际接收到了哪些文件和信息
2. **工具调用链**：调用了哪些工具、每次调用的返回值
3. **失败节点**：任务在哪一步中断

这是将 Agent 使用从"试错"转变为"工程化排查"的关键能力。

---

> **板块 B 小结：** 资源导航依赖 Awesome 和开源社区，行为约束依赖 System 提示词，问题诊断依赖调试视图。三者构成日常使用 Agent 的基础设施。

---

# C. 集成与协议：从 IDE 扩展到终端、平台、产品

> 前面的内容集中在 VS Code 内部。但 Agent 的价值不应局限在编辑器中。

## 主题 9：Copilot CLI

> **🎬 直接演示。**

```bash
# 交互式——在终端中直接与 Agent 对话
copilot

# 程序化——传入 prompt，获取结果，可嵌入自动化脚本
copilot -p "分析这个错误日志并给出修复建议" < error.log
```

两种模式分别适用于：交互式用于日常终端调试；程序化用于 CI/CD 自动化流程。此外可结合 `/mcp`、`/agent` 和权限参数进行精确控制。

核心转变：Agent 从对话工具升级为**可脚本化的执行节点**，能够嵌入任意自动化链路。

---

## 主题 10：MCP / ACP / A2A

这三个协议解决的是三类不同的集成场景。通过具体例子说明：

- "需要让 Agent 查询内部数据库" → **MCP**（Agent 与工具之间的协议）
- "需要在运维平台中嵌入 Agent 对话能力" → **ACP**（客户端与 Agent 之间的协议）
- "安全评审 Agent 发现问题后，自动通知修复 Agent 处理" → **A2A**（Agent 与 Agent 之间的协议）

| 场景            | 协议    | 定位           |
| --------------- | ------- | -------------- |
| 扩展工具能力    | **MCP** | Agent ↔ 工具   |
| 提供 Agent 接入 | **ACP** | 客户端 ↔ Agent |
| 多 Agent 协作   | **A2A** | Agent ↔ Agent  |

选型原则：**MCP 管工具，ACP 管接入，A2A 管协作。** 各管一件事，保持架构边界清晰。

> **🎬 现场演示：** 接入一个 MCP Server，为 Agent 扩展新的工具能力。

---

## 主题 11：Copilot SDK

前面讲的是**使用** Agent，SDK 解决的是另一个层面的问题：在自有产品中**提供** Agent 能力。

适用场景：在内部平台集成 Agent 对话、在产品中嵌入 AI 工作流等。

最小闭环四步：

```
Create Session → Send Prompt → Handle Tool Call → Return Result
```

注意事项：新版 SDK 要求显式设置 `OnPermissionRequest`，未设置会导致运行时失败。

SDK 实现的是从"个人工具"到"平台能力"的跨越。

---

> **板块 C 小结：** CLI 解决终端集成，三个协议解决架构选型，SDK 解决产品化。Agent 的边界从 IDE 扩展到整个研发基础设施。

---

# D. 工程闭环：从"偶发成功"到"稳定交付"

> 这是最关键的板块。前面所有能力如果不形成闭环，就无法离开 demo 阶段。

## 主题 12：Workflow

缺少 Workflow 的 Agent 缺乏稳定性保障——本次任务成功，不代表下次也能成功。Workflow 提供的是**流程级的确定性**：**Plan → Execute → Verify**。

三个必须配置的要素：

1. **可写范围**：限制 Agent 可以修改的文件和目录
2. **强制验证**：每步完成后必须通过的检查项
3. **失败回退**：出错时的回滚策略，而非继续执行

在 production 相关的流程中使用 Agent，Workflow 是前提条件。

---

## 主题 13：AI Agent 与自动化测试

测试领域中 Agent 的价值不在于生成测试代码，而在于：**测试点发现、失败分析、回归报告**。

我们采用三层策略：

- **风险分层**：高风险路径人工确认覆盖，低风险路径由 Agent 自动补充
- **双轨验证**：静态分析 + 动态执行，不依赖单一验证手段
- **失败归因**：Agent 需要输出"失败原因 + 建议修复方案"，而非仅报告 failed 状态

目标是提升测试效率的同时，不降低质量门槛。

---

## 实战专题：`.local/coagent` 的 RLM

> 这是今天最技术性的话题，来自我们团队的实际工程实践。

以一个场景说明：Agent 需要分析一份日志文件。

**普通模式**：Agent 一次性生成完整的分析脚本并执行。如果对日志格式的假设有误，结果就不可用。

**RLM 模式**（Recursive Language Model）：Agent 先读取日志格式，根据格式选择解析策略，解析后再决定下一步分析路径。每一步的执行结果实时影响后续决策。

$$
\text{LLM 推理} \rightarrow \text{生成表达式/脚本} \rightarrow \text{执行结果回流} \rightarrow \text{LLM 再推理}
$$

在 `workflow.go` 中通过 `EnableRLM` 开启：

```go
// 开启 RLM
cfg.EnableRLM = true

// 注入受控工具集，非全量开放
cfg.Tools = e.rlmTools(run, false)

// 显式排除高风险工具
cfg.ExcludedTools = rlmExcludedTools
```

关键设计决策——RLM 在严格的安全边界内运行：

- **不注入 `sh()`**：禁止 Agent 执行任意 shell 命令
- **工具白名单制**：仅提供必要工具
- **表达式复杂度限制**：防止生成过于复杂的脚本
- **输出体积限制**：防止内存溢出

> **🎬 现场演示：** 查看 `rlm.go` 中的工具注入和安全约束代码，运行一个 `EnableRLM + eval_expr` 实际场景。

核心定位：**可控的动态能力**——在安全边界内赋予 Agent 运行时动态决策能力。

---

# E. 跨项目联合开发

> 实际工程中，多数功能不是在单一仓库内闭环的。一个需求可能同时涉及 API 服务、SDK 库、文档仓库甚至基础设施配置。Agent 默认只看到当前项目，如何让它具备跨项目的上下文？

## 问题

Agent 在单一项目中表现良好，但遇到跨项目场景时会出现以下问题：

- 修改 API 定义后，Agent 不知道还需要同步更新 SDK 的调用方
- 修改 Protobuf 后，Agent 看不到依赖该 proto 的其他服务
- 文档仓库与代码仓库分离，Agent 无法关联变更

根本原因：**Agent 的上下文边界 = 工作区边界**。它只能看到当前工作区中的文件。

## 方案：`.local/` 符号链接 + 统一规则

我们采用的方案是通过 `.local/` 目录将关联项目符号链接到当前工作区，使 Agent 获得跨项目的完整视野。

### 第一步：建立项目链接

```bash
# 在主项目中创建 .local 目录
mkdir -p .local

# 将关联项目符号链接进来
cd .local
ln -sf ../../coagent   coagent    # API 服务
ln -sf ../../redant    redant     # 前端项目
ln -sf ../../docs-site docs-site  # 文档站点
```

链接后的目录结构：

```
my-project/
├── .local/
│   ├── coagent  → ../../coagent
│   ├── redant   → ../../redant
│   └── docs-site → ../../docs-site
├── copilot-instructions.md
├── src/
└── ...
```

Agent 打开 `my-project` 工作区后，可以同时访问 `.local/coagent/`、`.local/redant/` 等关联项目的全部代码。

### 第二步：在 `copilot-instructions.md` 中声明项目关系

```markdown
## 跨项目结构

本项目通过 .local/ 目录关联以下项目：

- `.local/coagent/`：API 服务端，Go 项目，提供后端接口
- `.local/redant/`：前端项目，TypeScript，消费 coagent 的 API
- `.local/docs-site/`：文档站点，Markdown，与 API 变更同步

## 跨项目变更规则

- 修改 API 接口定义时，必须同步检查 `.local/redant/` 中的调用方
- 修改 Protobuf 文件时，必须同步更新 `.local/coagent/` 中的生成代码
- 任何公开接口变更必须同步更新 `.local/docs-site/` 中的对应文档
```

### 第三步：为关联项目创建跨项目 instructions

```markdown
# cross-project.instructions.md

## 适用范围
.local/**/*

## 规则
- 跨项目修改时，必须在 commit message 中标注影响的项目
- 不可直接修改 .local/ 下的文件作为最终提交——修改后需回到原项目仓库提交
- 跨项目引用使用相对路径，不使用绝对路径
```

### 第四步（可选）：创建跨项目 Agent

定义一个专门处理跨项目变更的 Agent，职责包括：
- 检测当前变更是否影响关联项目
- 列出需要同步修改的文件和位置
- 生成跨项目变更清单

## 适用场景

| 场景            | 做法                                                       |
| --------------- | ---------------------------------------------------------- |
| 前后端联调      | 链接 API 服务 + 前端项目，Agent 能同时看到接口定义和调用方 |
| 微服务间依赖    | 链接上下游服务，修改 proto 后 Agent 自动检查影响面         |
| 代码 + 文档同步 | 链接文档仓库，API 变更时 Agent 提醒更新文档                |
| 共享库开发      | 链接共享库和使用方，修改库接口后 Agent 检查兼容性          |

## 注意事项

- `.local/` 应加入 `.gitignore`——链接关系是本地开发环境配置，不应提交到仓库
- 每个开发者的 `.local/` 链接路径可能不同，依赖相对路径而非绝对路径
- 跨项目的 Agent 规则写在主项目中，不要修改被链接项目的规则文件

核心价值：通过符号链接扩展 Agent 的上下文边界，使其在单一工作区内获得多项目的完整视野，同时通过 instructions 约束跨项目行为规范。

---


## 总结

今天分享的主题，核心只有一件事：

> **Agent 不是用来取代工程师的，而是用来放大工程师的能力。** 前提是通过 instructions、agents、skills、prompts、workflow 这套体系，将项目规则和团队方法论转化为 Agent 可消费的配置。

感谢大家，欢迎讨论。

---

## 参考链接

- VS Code customization：
  - https://code.visualstudio.com/docs/copilot/copilot-customization
- Copilot Chat：
  - https://code.visualstudio.com/docs/copilot/chat/copilot-chat
- GitHub Copilot 总览：
  - https://docs.github.com/en/copilot
- Copilot CLI：
  - https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview
  - https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
  - https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference
- MCP / ACP / A2A：
  - https://modelcontextprotocol.io/
  - https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/extend-copilot-chat-with-mcp
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers
  - https://docs.github.com/en/copilot/concepts/agents/cloud-agent/mcp-and-cloud-agent
  - https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server
  - https://a2a-protocol.org/latest/
- Copilot SDK：
  - https://docs.github.com/en/copilot/how-tos/copilot-sdk/use-copilot-sdk/mcp-servers
  - https://docs.github.com/en/copilot/how-tos/copilot-sdk/troubleshooting/debug-mcp-servers
- Workflow / Agent Framework：
  - https://learn.microsoft.com/zh-cn/agent-framework/overview/
  - https://learn.microsoft.com/zh-cn/agent-framework/workflows/index
  - https://learn.microsoft.com/zh-cn/agent-framework/integrations/a2a
- 生态资源：
  - https://awesome-copilot.github.com/
  - https://awesome-copilot.github.com/learning-hub
  - https://awesome-copilot.github.com/tools

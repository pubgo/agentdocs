# VS Code Copilot & Agent 分享

> 每个主题按 **这是什么 → 有什么用 → 怎么使用 → 有什么价值** 展开，穿插现场演示和讨论。

---

## 开场（5 min）

大家好，今天聊一个我觉得很值得投入的方向：**怎么把 AI Agent 从"能用"变成"能落地"**。

先说一个我们团队真实的变化——三个月前，大家用 Copilot 基本就是补全代码、问问问题。现在，我们的 PR 评审、测试生成、甚至 CI 修复，都有 Agent 在参与。不是因为我们技术多强，而是因为掌握了一套**配置驱动**的方法。

今天 14 个主题 + 1 个实战专题，分四个板块：

| 板块 | 主题 | 关键词 |
|------|------|--------|
| **A. 规则体系** | 1~5 | 让 Agent 按你的规矩办事 |
| **B. 认知工具** | 6~8 | 知道有什么、怎么约束、出了问题怎么查 |
| **C. 集成与协议** | 9~11 | 从 IDE 走向终端、平台、产品 |
| **D. 工程闭环** | 12~14 + RLM | 从"偶发成功"到"稳定交付" |

---

# A. 规则体系：让 Agent 按你的规矩办事

> 这一组解决的核心问题是：**Agent 不知道你的项目怎么跑。** 你不告诉它，它就猜——猜错了你还得花时间纠正。

## 主题 1：`/init` — 给项目写一份"入职手册"

### 这是什么

`/init` 是项目级初始化命令，一键生成 `.github/copilot-instructions.md`——相当于给 Agent 写了一份入职手册。

### 有什么用

大家想一下：新人入职第一天，你会告诉他什么？项目怎么跑、哪些东西别碰、测试怎么跑。Agent 也需要这些信息。没有它，Agent 每次都在"盲猜"。

### 怎么使用

```
在仓库根目录执行 /init → 生成模板 → 补充三件事：
1. 必跑命令（build、test、lint）
2. 禁止操作（别删 migration、别改 proto）
3. 目录约定（哪些是生成代码，别手动改）
```

> **🎬 现场演示：** 打开一个空仓库，执行 `/init`，看生成结果，然后手动补几条规则。

### 有什么价值

从"Agent 猜你想要什么"变成"Agent 按你说的做"。我们团队实测，加了 `/init` 后，Agent 首次任务成功率从不到 50% 提升到 80% 以上。

---

## 主题 2：`/create-instructions` — 把口头规范变成可执行规则

### 这是什么

创建 `.instructions.md` 规则文件的命令。和 `/init` 不同——`/init` 是项目级的"入职手册"，`/create-instructions` 是更细粒度的"岗位手册"。

### 有什么用

我们团队经常遇到一个问题：代码规范写在 wiki 上，但 Agent 不去看 wiki。`/create-instructions` 就是让规范**直接生效**，不是"建议"而是"指令"。

### 怎么使用

按目录拆分——前端一份、后端一份、测试一份。每份用"必须 / 应该 / 禁止"三级结构：

```markdown
## 必须
- 所有 API handler 必须有 context 参数
- 错误返回必须用 status code，不能 200 + error body

## 禁止
- 禁止在 handler 里直接写 SQL
- 禁止修改 pkg/gen/ 下的生成代码
```

### 有什么价值

规则可版本化、可 Code Review、可跨团队复用。不再是"老王说的"，而是仓库里白纸黑字写着的。

---

## 主题 3：`/create-agent` — 给团队造"虚拟专家"

### 这是什么

创建特定角色 Agent 的命令——比如专门做安全评审的、专门写测试的、专门看 API 设计的。

### 有什么用

打个比方：你不会让一个全科医生同时做手术、看门诊、写处方。Agent 也一样，什么都做就什么都不精。`/create-agent` 让你按角色拆分。

### 怎么使用

三个原则：**单一职责 + 最小权限 + 固定输出格式**。

举个例子，我们的 `pr-review` Agent 只做三件事：
1. 检查是否有未覆盖的测试路径
2. 检查是否有安全风险
3. 输出结构化评审意见（而不是一大段自由文字）

> 打开 `agents/pr-review-orchestrator.agent.md` 看实际定义。

### 有什么价值

任务质量更稳定。更重要的是——这些 Agent 定义就是团队的**知识资产**，新人来了不用重新教，直接用。

---

## 主题 4：`/create-skill` — 把经验封装成标准流程

### 这是什么

创建可复用工作流技能（SKILL）的命令。如果说 Agent 是"人"，Skill 就是这个人掌握的"方法论"。

### 有什么用

我们团队修 bug 的老手和新手差距在哪？不是代码能力，是**方法**——老手会先复现、再定位、缩小范围、修完跑回归。`/create-skill` 就是把这个方法固化下来。

### 怎么使用

定义清晰的：输入条件 → 执行步骤 → 分支判断 → 完成标准。

```
Skill: 修复 Bug
输入: issue 链接 / 错误日志
步骤:
  1. 复现（找到最小复现路径）
  2. 定位（缩小到具体函数）
  3. 修复（改动最小化）
  4. 回归（跑相关 test suite）
完成标准: CI 绿 + 原 issue 场景复现失败
```

### 有什么价值

新人按流程走也能做对，减少对"老师傅"的依赖。团队的方法论不再只存在于某个人的脑子里。

---

## 主题 5：`/create-prompt` — 高频任务的"一键启动器"

### 这是什么

创建可复用 Prompt 模板的命令。

### 有什么用

大家肯定有这个经历——每次让 Agent 写 PR 总结，都要重新描述一遍"给我包含哪些内容、什么格式"。用 Prompt 模板，一次定义，反复使用。

### 怎么使用

把固定结构抽成模板。我们常用的几个：

- **PR 总结**：自动提取变更范围 + 影响面 + 需要 reviewer 关注的点
- **API 评审**：检查命名一致性 + 向后兼容 + 错误码规范
- **Changelog 生成**：按 conventional commit 分类汇总

### 有什么价值

输出一致、执行快、知识可传承。团队不再依赖"谁的 prompt 写得好"。

---

> **小结——板块 A 讲完了。** 回顾一下：`/init` 定项目规矩，`/create-instructions` 定细分规范，`/create-agent` 定角色分工，`/create-skill` 定方法流程，`/create-prompt` 定高频模板。这五个命令组合起来，就是一套完整的 **Agent 治理体系**。
>
> 有问题可以现在问，或者我们继续。

---

# B. 认知工具：知道有什么、怎么约束、出了问题怎么查

> 规则定好了，接下来需要三样东西：**资源导航、行为约束、问题诊断。**

## 主题 6：GitHub Copilot Awesome — 不要重复造轮子

### 这是什么

Copilot 生态的资源导航站，汇集了学习路径、工具合集和社区实践。

### 有什么用

一句话：**别自己从零摸索。** 你想做的事情，大概率已经有人做过了，而且做得比你好。

### 怎么使用

我的建议路径：先看 Learning Hub 建立认知 → 再按 Tools 选 1~2 个和你场景强相关的工具试用 → 最后看社区案例找灵感。

### 有什么价值

节省选型时间，避免重复造轮子。

---

## 主题 7：System 提示词 — Agent 的"宪法"

### 这是什么

系统级指令，定义 Agent 的行为边界和优先级。如果前面的 instructions 是"岗位手册"，System 提示词就是"宪法"——优先级最高，不可违反。

### 有什么用

它回答的是三个关键问题：**能做什么、不能做什么、怎么证明做完了。**

### 怎么使用

我建议固定五段结构：

```
1. 目标：你要完成什么
2. 约束：哪些事情绝对不能做
3. 流程：按什么顺序执行
4. 验证：怎么判断完成（不是"看起来对"，而是可检验的标准）
5. 输出格式：返回什么结构
```

### 有什么价值

减少随机性。Agent 生成的结果不再靠运气，而是有确定性边界。

---

## 主题 8：调试视图 — 出了问题别猜，要查

### 这是什么

VS Code 中观察 Agent 运行过程的调试入口。

### 有什么用

用 Agent 最常见的困境是什么？**"它给的结果不对，但我不知道哪儿出了问题。"** 是上下文给错了？是规则没生效？还是工具调用失败了？调试视图告诉你答案。

### 怎么使用

重点看三项：

1. **上下文输入**：Agent 到底"看到"了什么？
2. **工具调用链**：调了哪些工具、返回了什么？
3. **失败节点**：在哪一步断了？

> 这个能力很重要——它把 Agent 使用从"玄学"变成"工程"。

### 有什么价值

把"感觉有问题"变成"可定位、可修复"的工程问题。不用再靠"换个 prompt 试试"来碰运气。

---

> **板块 B 小结：** 知道去哪找资源（Awesome）、知道怎么约束行为（System 提示词）、知道出了问题怎么查（调试视图）。这三个是日常使用 Agent 的基础设施。

---

# C. 集成与协议：从 IDE 走向终端、平台、产品

> 前面讲的都在 VS Code 里面。但 Agent 的价值不应该局限在编辑器——它应该能接入终端、接入平台、接入产品。

## 主题 9：Copilot CLI — 把 Agent 带进终端

### 这是什么

终端里的 Copilot Agent 入口，支持交互式和程序化两种模式。

### 有什么用

两个典型场景：
- **交互式**：你在终端调试问题，直接问 Agent，不用切回编辑器
- **程序化**：在 CI/CD 脚本里调用，比如自动生成 changelog、自动分析测试失败

### 怎么使用

```bash
# 交互式
copilot

# 程序化——传 prompt，拿结果
copilot -p "分析这个错误日志并给出修复建议" < error.log
```

还可以结合 `/mcp`、`/agent` 和权限参数精确控制行为。

> **🎬 现场演示：** 用 `copilot -p` 做一次程序化调用，感受 Agent 从"对话工具"到"可脚本化节点"的升级。

### 有什么价值

Agent 能力不再被锁在 IDE 里，可以嵌入任何终端工作流和自动化链路。

---

## 主题 10：MCP / ACP / A2A — 三个协议，各管一件事

### 这是什么

三个协议解决三类不同的集成问题：

| 协议 | 连接的是 | 类比 |
|------|----------|------|
| **MCP** | Agent ↔ 工具 | USB 接口——接外设 |
| **ACP** | 客户端 ↔ Agent | HTTP API——接入口 |
| **A2A** | Agent ↔ Agent | 内部通信协议——做协作 |

### 有什么用

大家经常问：**"我要接一个数据库查询工具，用哪个协议？"** 答案是 MCP。**"我要在我们的平台上嵌入 Agent？"** ACP。**"两个 Agent 需要配合完成任务？"** A2A。

### 怎么使用

按场景选型，不要混用：

- 扩展 Agent 能力（接工具）→ MCP
- 为平台/产品提供 Agent 接入 → ACP
- 多 Agent 编排协作 → A2A

> **🎬 现场演示：** 接入一个 MCP Server，让 Agent 获得新工具能力。

### 有什么价值

架构边界清晰。最怕的是"什么都用一个协议"，最后能力耦合、维护困难。三个协议各管一件事，扩展路径明确。

---

## 主题 11：Copilot SDK — 从"用 Agent"到"造 Agent 产品"

### 这是什么

将 Copilot 能力嵌入你自己的产品或平台的开发 SDK。

### 有什么用

前面讲的都是**用** Agent。但如果你想在自己的产品里**提供** Agent 能力——比如在你的内部平台上让用户和 Agent 对话——就需要 SDK。

### 怎么使用

最小闭环四步：

```
Create Session → Send Prompt → Handle Tool Call → Return Result
```

重点注意：新版 SDK 要求显式设置 `OnPermissionRequest`，不设会直接失败。

### 有什么价值

AI 能力可产品化、可规模化。从"个人工具"升级到"平台能力"。

---

> **板块 C 小结：** CLI 解决终端集成、三个协议解决架构选型、SDK 解决产品化。Agent 的边界从 IDE 扩展到了整个研发基础设施。

---

# D. 工程闭环：从"偶发成功"到"稳定交付"

> 最后一个板块是最关键的。前面所有能力如果不形成闭环，就永远停在"demo 阶段"。

## 主题 12：Workflow — 让 Agent 按流程干活

### 这是什么

把 Agent 的任务执行固化为可重复流程：**Plan → Execute → Verify**。

### 有什么用

没有 Workflow 的 Agent 是什么样？今天能成功，明天换个输入就挂了。Workflow 就是给它装上"流程保障"。

### 怎么使用

三个关键设置：

1. **可写范围**：Agent 只能改哪些文件/目录
2. **强制验证**：每步完成后必须跑什么检查
3. **失败回退**：出错了怎么回滚，而不是继续往下走

### 有什么价值

把"偶发成功"变成"稳定交付"。你敢在 production 相关的流程中使用 Agent，前提就是有 Workflow 保障。

---

## 主题 13：AI Agent 与自动化测试

### 这是什么

AI 参与测试全流程——不仅仅是"帮我生成测试代码"，而是覆盖测试点发现、失败分析、回归报告整个链路。

### 有什么用

测试最痛的不是写代码，而是：**该测什么？测失败了为什么？回归了哪些用例？** Agent 恰好擅长这些分析型工作。

### 怎么使用

三层策略：

1. **风险分层**：高风险路径优先覆盖，低风险 Agent 自动补
2. **双轨验证**：静态分析 + 动态执行，不只靠一种
3. **失败归因**：Agent 不只是报"failed"，而是给出"为什么 failed + 建议修复"

### 有什么价值

测试效率上去了，但质量门槛没有下来。这是 AI 在测试领域真正有价值的用法。

---

## 主题 14：开源社区工具

### 这是什么

围绕 Copilot/Agent 的开源工具生态。

### 有什么用

自己从零做太慢。社区已经有成熟的协议实现、调试工具、编排框架和模板库。

### 怎么使用

按三层筛选：

| 层级 | 典型工具 | 用途 |
|------|----------|------|
| 协议基础设施 | MCP SDK、ACP 参考实现 | 接入协议 |
| 协作编排 | Agent 框架、A2A 网关 | 多 Agent 调度 |
| 模板与资产 | Instructions/Skills/Prompts 仓库 | 快速启动 |

### 有什么价值

站在社区肩膀上，减少重复开发，加速团队落地。

---

## 实战专题：`.local/coagent` 的 RLM — 让 Agent "边跑边想"

> 这是我们团队自己的实践，也是今天最技术性的一个话题。

### 这是什么

RLM = Recursive Language Model，一个推理-执行闭环：

$$
\text{LLM 推理} \rightarrow \text{生成表达式/脚本} \rightarrow \text{执行结果回流} \rightarrow \text{LLM 再推理}
$$

普通 Agent 是"想好了再做"。RLM 是"边做边想"——每一步执行的结果会实时影响下一步的决策。

### 有什么用

举个例子：Agent 需要分析一份日志文件。普通模式下，它会一次性写一个分析脚本；RLM 模式下，它可以先看一眼日志格式，根据格式决定解析策略，解析出来再决定下一步分析什么——就像一个有经验的工程师实际操作时的思路。

### 怎么使用

在 `workflow.go` 中通过 `EnableRLM` 开启：

```go
// 开启 RLM
cfg.EnableRLM = true

// 注入受控工具集（不是所有工具都给）
cfg.Tools = e.rlmTools(run, false)

// 显式排除高风险工具
cfg.ExcludedTools = rlmExcludedTools
```

关键安全边界：
- **不注入 `sh()`**：Agent 不能随意执行 shell 命令
- **工具白名单制**：只给必要的工具，不是全部开放
- **表达式复杂度限制**：防止生成过于复杂的脚本
- **输出体积限制**：防止内存爆炸

> **🎬 现场演示：** 打开 `rlm.go`，看工具注入和安全约束的代码，然后跑一个 `EnableRLM + eval_expr` 的实际场景。

### 有什么价值

一句话总结：**可控的动态能力**。它不是"让 Agent 随便跑"，而是在严格的安全边界内，赋予 Agent 根据运行时上下文做动态决策的能力。

---

# 收尾

## 常见问题

> 这几个问题几乎每次分享都有人问，我直接给结论。

**Q：Agent 会不会改坏代码？**

会。所以才需要前面讲的 Workflow（可写范围 + 强制验证 + 回滚策略）。不是"信任 Agent 不犯错"，而是"犯了错能兜住"。

**Q：提示词会不会失效？**

会。模型升级、上下文变化都可能导致失效。所以不要靠"一条神奇 prompt"，要靠**规则体系 + 调试闭环**。Prompt 失效了，你能从调试视图定位到哪里变了。

**Q：协议太多没法选？**

记住一句话：**MCP 管工具，ACP 管接入，A2A 管协作。** 按你要解决的问题选，不要混。

---

## 30 天落地路线

给大家一个实操建议——不要想着一步到位，按周推进：

| 周 | 目标 | 交付物 |
|----|------|--------|
| 第 1 周 | 基础就绪 | `/init` + 基础 instructions + 1 个试点项目跑通 |
| 第 2 周 | 工具接入 | MCP 最小工具集 + 权限白名单 |
| 第 3 周 | 知识沉淀 | 高频 prompts/skills 沉淀 + 流程化 |
| 第 4 周 | 度量闭环 | 接入 CI + 跟踪 Lead Time / 返工率 / 缺陷率 |

---

## 最后一句话

今天讲了 14 个主题，但核心只有一件事：

> **Agent 不是用来取代你的，而是用来放大你的。** 前提是你得告诉它怎么做——这就是 instructions、agents、skills、prompts、workflow 这套体系存在的原因。

谢谢大家。有什么问题我们可以现场讨论。

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

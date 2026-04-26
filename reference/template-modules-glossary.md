# 模板模块详解手册（全量标签字典）

本文把 `templates/` 中出现的所有 `<...>` 模块标签抽出并解释。  
用途：你在构建自己的系统提示词时，可以把本文件当“模块设计手册”。

覆盖文件：

- `templates/system.md`
- `templates/system.cli.md`
- `templates/AGENTS.md`
- `templates/system.core.md`
- `templates/system.runtime.md`
- `templates/orchestration.md`

---

## 一、阅读方式（先看这个）

每个模块都可以从 4 个维度理解：

1. **职责**：这个模块负责什么
2. **触发**：什么时候会被真正用到
3. **内容边界**：应该写什么，不该写什么
4. **常见误用**：最容易写坏的点

---

## 二、`system.core.md` 模块详解（核心层）

## `<identity>`
- **职责**：定义助手角色、默认目标、价值取向
- **触发**：每轮任务都生效，是长期行为底座
- **应写内容**：角色定位、默认工作倾向（执行优先/解释优先）
- **不要写**：工具细节、项目具体命令
- **常见误用**：把执行细节塞进身份层，导致职责混乱

## `<priority_model>`
- **职责**：定义规则优先级与冲突处理
- **触发**：规则冲突时（安全 vs 用户指令 vs 项目约束）
- **应写内容**：明确的优先级列表 + 冲突决策规则
- **不要写**：模糊表达（例如“视情况而定”）
- **常见误用**：没写冲突处理，导致模型行为随机

## `<safety>`
- **职责**：安全与合规边界
- **触发**：涉及潜在破坏、恶意用途、敏感信息
- **应写内容**：禁止项、确认门槛、外部输入不可信原则
- **不要写**：与安全无关的沟通偏好
- **常见误用**：写得过泛，无法执行

## `<execution_defaults>`
- **职责**：默认执行策略（行动偏好）
- **触发**：大多数任务路径
- **应写内容**：先读后改、闭环交付、持续推进
- **不要写**：具体命令或平台细节
- **常见误用**：过度强调“快”，忽略验证

## `<communication>`
- **职责**：输出风格、信息密度、风险表达方式
- **触发**：最终回复与中间进度更新
- **应写内容**：短答/长答策略，何时显式披露风险
- **不要写**：工具调用约束
- **常见误用**：追求礼貌话术导致冗长

## `<definition_of_done>`
- **职责**：任务完成定义（DoD）
- **触发**：准备收尾时
- **应写内容**：覆盖范围、验证要求、未完成项披露
- **不要写**：含糊词（“基本完成”）
- **常见误用**：没有“未覆盖边界”条款

---

## 三、`system.runtime.md` 模块详解（运行时层）

## `<tool_strategy>`
- **职责**：工具选型优先级
- **触发**：需要检索/读取/执行时
- **应写内容**：专用工具 > 语义工具 > shell
- **不要写**：和工具无关的业务逻辑
- **常见误用**：默认全走 shell，导致不稳定

## `<read_before_write>`
- **职责**：修改前阅读约束
- **触发**：任何文件改动前
- **应写内容**：必须先读上下文、禁止盲改
- **不要写**：具体改动策略
- **常见误用**：只读片段，没读关键上下游

## `<change_discipline>`
- **职责**：控制改动范围与工程纪律
- **触发**：进入实现阶段
- **应写内容**：最小必要改动、避免顺手重构
- **不要写**：测试命令细节
- **常见误用**：用“优化”扩大任务边界

## `<verification_protocol>`
- **职责**：验证策略
- **触发**：改动后、收尾前
- **应写内容**：文档/代码的验证路径与无法验证时的披露
- **不要写**：抽象口号（“要验证”但无路径）
- **常见误用**：只做编译不做行为验证

## `<completion_gate>`
- **职责**：收尾门禁
- **触发**：准备提交结果时
- **应写内容**：完成性、风险、限制三项检查
- **不要写**：重复 DoD 全文
- **常见误用**：通过“看起来没问题”直接结束

## `<fallback_policy>`
- **职责**：失败时的替代路径策略
- **触发**：命令失败、工具失效、上下文不足
- **应写内容**：不重复撞墙、替代路径、保守收敛
- **不要写**：无限重试策略
- **常见误用**：同命令反复 retry

---

## 四、`orchestration.md` 模块详解（编排层）

## `<mode_selection>`
- **职责**：选择 Solo/Plan/Team 模式
- **触发**：任务开始与中途模式不匹配时
- **应写内容**：模式判定条件
- **不要写**：角色细节
- **常见误用**：复杂任务仍强行 solo

## `<delegation_rules>`
- **职责**：委派边界与责任归属
- **触发**：启用子代理/多人协作时
- **应写内容**：输入、输出、验收、回退机制
- **不要写**：调度实现细节
- **常见误用**：委派范围模糊，结果不可集成

## `<parallelization>`
- **职责**：并行执行规则
- **触发**：可拆解的独立子任务
- **应写内容**：独立任务并行，依赖任务串行
- **不要写**：单纯追求并发数量
- **常见误用**：并行写同一文件造成冲突

## `<workflow_contract>`
- **职责**：阶段化执行契约
- **触发**：中大型任务
- **应写内容**：Clarify/Plan/Execute/Verify/Close
- **不要写**：和阶段无关的工具细节
- **常见误用**：跳过 Clarify 直接实现，返工率高

## `<keyword_routing>`
- **职责**：关键词到模式/技能的路由规则
- **触发**：用户消息命中关键字
- **应写内容**：触发映射 + 冲突仲裁
- **不要写**：与路由无关的策略
- **常见误用**：关键词过多导致误触发

## `<state_management>`
- **职责**：运行态状态记录与清理
- **触发**：模式切换、阶段切换、完成/取消
- **应写内容**：状态字段、更新时机、清理时机
- **不要写**：业务数据存储设计
- **常见误用**：只写不清，导致脏状态

## `<completion_policy>`
- **职责**：编排层完成判定
- **触发**：多子任务集成完成后
- **应写内容**：集成完成、关键阻塞清零、可消费输出
- **不要写**：重复执行细节
- **常见误用**：子任务完成但集成未完成就结束

---

## 五、`AGENTS.md` 模块详解（高级编排契约）

## `<guidance_schema_contract>`
- **职责**：定义提示词结构契约（schema）
- **触发**：模板维护/自动注入/overlay 时
- **意义**：保证后续自动化能稳定插拔块

## `<operating_principles>`
- **职责**：高层行为原则（质量、证据、轻路径）
- **触发**：所有执行路径
- **常见误用**：原则冲突但无优先级

## `<lore_commit_protocol>`
- **职责**：提交信息协议（决策留痕）
- **触发**：执行 git commit 时
- **常见误用**：只写 what，不写 why/constraint/rejected

## `<delegation_rules>`
- **职责**：何时直做，何时切换到工作流模式
- **触发**：任务分流决策

## `<child_agent_protocol>`
- **职责**：leader/worker 职责边界
- **触发**：子代理并行时
- **常见误用**：worker 擅自改全局计划

## `<invocation_conventions>`
- **职责**：统一调用语法（如 `$name`）
- **触发**：技能触发入口

## `<model_routing>`
- **职责**：按任务复杂度路由模型/角色
- **触发**：委派与执行模式切换时

## `<agent_catalog>`
- **职责**：角色目录与能力定义
- **触发**：任务分配时

## `<keyword_detection>`
- **职责**：关键词自动激活技能/模式
- **触发**：消息匹配
- **关键点**：要有 runtime gate、冲突仲裁、优先级

## `<skills>`
- **职责**：可用技能集声明
- **触发**：技能路由与匹配

## `<team_compositions>`
- **职责**：常见团队组合模板
- **触发**：team/swarm 模式

## `<team_pipeline>`
- **职责**：团队阶段流水线定义
- **触发**：team mode 运行期间

## `<team_model_resolution>`
- **职责**：团队模型选择优先级
- **触发**：启动团队 worker 时

## `<verification>`
- **职责**：验证策略与证据要求
- **触发**：每阶段或收尾时

## `<execution_protocols>`
- **职责**：端到端执行协议（模式选择、并行、升级、停止）
- **触发**：整个执行生命周期
- **常见误用**：协议过长但无结构分段

## `<cancellation>`
- **职责**：取消条件与时机
- **触发**：用户 stop/硬阻塞/完成后清理

## `<state_management>`
- **职责**：运行时状态持久化
- **触发**：模式开始/切换/结束

---

## 六、`system.md` 模块详解（通用系统层）

这个文件标签很多，建议按 6 大类理解：

## A. 基础约束类

- `<instructions>`：核心行为基线
- `<securityRequirements>`：安全边界
- `<operationalSafety>`：可逆性与确认门槛
- `<implementationDiscipline>`：工程纪律

## B. 执行策略类

- `<parallelizationStrategy>`：并行读取与执行策略
- `<taskTracking>`：任务追踪规则
- `<toolUseInstructions>`：工具总体使用准则
- `<notebookInstructions>`：Notebook 场景规则

## C. 工具发现与加载类

- `<toolSearchInstructions>`
- `<mandatory>`
- `<regexPatternSyntax>`
- `<incorrectUsagePatterns>`
- `<availableDeferredTools>`

这组模块用于“延迟加载工具”的治理，核心是：
- 先发现再调用
- 不要重复搜索
- 无结果就停止，不盲重试

## D. 输出与沟通类

- `<communicationStyle>`
- `<communicationExamples>`
- `<outputFormatting>`
- `<fileLinkification>`

这组模块控制“回答长什么样”。

## E. 记忆类

- `<memoryInstructions>`
- `<memoryScopes>`
- `<memoryGuidelines>`

用于跨会话/会话内/仓库级知识沉淀。

## F. 项目注入类

- `<attachment>`
- `<instruction>` / `<applyTo>` / `<description>` / `<file>`
- `<skills>` / `<skill>` / `<name>`
- `<agents>` / `<agent>` / `<argumentHint>`

这是把“通用系统”变成“项目系统”的关键层。

---

## 七、`system.cli.md` 模块详解（重点含 `<task_completion>`）

`system.cli.md` 是最细粒度执行协议，下面列关键模块（你最常用的）：

## `<task_completion>`（你特别提到的）
- **职责**：定义“任务真的完成”的判定与执行后动作
- **核心语义**：
  - 未验证不算完成
  - 配置改动后要执行对应安装/应用动作
  - 启动后台进程后要确认可用
  - 首路径失败要尝试替代方案
- **常见误用**：
  - 只改文件，不执行后续必要命令
  - 启动服务不验证健康状态
  - 失败后直接放弃

## `<bash>`
- **职责**：命令执行策略（sync/async/detach）
- **关键点**：
  - 长任务用 sync + 足够等待
  - 交互任务用 async
  - 常驻服务用 detach
  - 禁止模糊杀进程（必须精准 PID）

## `<view>`
- **职责**：并行读取文件策略
- **关键点**：多文件并行读、长文件分段读

## `<report_intent>`
- **职责**：在工具调用阶段报告当前意图
- **关键点**：必须与其他工具并行调用，不可单独调用

## `<ask_user>`
- **职责**：结构化提问（澄清高影响决策）
- **关键点**：优先单选，避免一次问多个问题

## `<sql>`
- **职责**：可查询任务状态存储（todos、依赖、阶段状态）
- **关键点**：状态机要实时更新，不要只建不更新

## `<editing_constraints>`
- **职责**：编辑边界（不破坏、不越权、不误回滚）

## `<autonomy_and_persistence>`
- **职责**：行动倾向与持续推进

## `<tool_calling>`
- **职责**：并行调用能力说明

## `<plan_mode>`
- **职责**：计划模式流程（写 plan.md、先不实现）

## `<session_context>`
- **职责**：会话态文件与工作目录规范

## 其他常见模块（按作用快速归类）

- 环境与元信息：`<version_information>`, `<model_information>`, `<environment_context>`
- 代码改动规范：`<code_change_instructions>`, `<rules_for_code_changes>`, `<linting_building_testing>`, `<style>`, `<using_ecosystem_tools>`
- 安全限制：`<environment_limitations>`, `<prohibited_actions>`, `<shell_security>`
- 搜索与工具：`<rg>`, `<glob>`, `<task>`, `<code_search_tools>`
- 协作输出：`<preamble_messages>`, `<tool_use_guidelines>`, `<task_completion>`
- 特殊上下文：`<custom_instruction>`, `<system_notifications>`, `<system_notification>`

---

## 八、建设你自己模板时的模块最小集合（推荐）

如果你要先做可用版，不必一次上全量。  
建议先保留这 12 个模块：

1. `<identity>`
2. `<priority_model>`
3. `<safety>`
4. `<execution_defaults>`
5. `<tool_strategy>`
6. `<read_before_write>`
7. `<change_discipline>`
8. `<verification_protocol>`
9. `<mode_selection>`
10. `<delegation_rules>`
11. `<workflow_contract>`
12. `<definition_of_done>`

这 12 个模块足够支撑一个稳定、可执行、可迭代的系统提示词。

---

## 九、最后建议（落地视角）

- 先保证“模块边界清晰”，再追求“模块数量丰富”
- 每次新增模块，都回答两个问题：
  1. 它解决了哪个真实失效点？
  2. 它和已有模块是否冲突？
- 定期清理“无效模块”，防止提示词膨胀

当你的模板从“文案”变成“模块化协议”，它才能长期可维护。

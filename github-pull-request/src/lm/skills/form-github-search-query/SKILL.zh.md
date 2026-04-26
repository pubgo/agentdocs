---
名称：表单-github-搜索-查询
描述：根据自然语言查询和搜索类型（问题或 PR）形成 GitHub 搜索查询。此技能可帮助用户创建有效的搜索查询来查找 GitHub 上的相关问题或拉取请求。
---

# 形成 GitHub 搜索查询

## 目的

GitHub 有用于搜索问题和拉取请求的特定语法。此技能获取用户的自然语言查询和他们想要执行的搜索类型（问题或 PR），并将其转换为格式正确的 GitHub 搜索查询。这使得用户可以利用 GitHub 强大的搜索功能，而无需了解具体语法。

## 用法

要使用此技能，请提供自然语言查询并指定是否要搜索问题或拉取请求。然后，该技能将分析输入并生成可用于在 GitHub 上查找相关结果的 GitHub 搜索查询。

## 将自然语言转换为 GitHub 搜索语法

### 步骤

1. 确定查询中是否提及存储库。
2. 获取存储库的标签（如果提到）。
3. 按照“形成有效搜索查询的提示”将自然语言查询转换为 GitHub 搜索语法。

### 搜索语法概述- is: { possibleValues: ['issue', 'pr', 'draft', 'public', 'private', 'locked', 'unlocked'] }
- 受让人：{ valueDescription：'GitHub 用户名或@me' }
- 作者：{ valueDescription：'GitHub 用户名或@me' }
- 提及：{ valueDescription: 'GitHub 用户名或@me' }
- team: { valueDescription: 'GitHub 用户名' }
- commenter: { valueDescription: 'GitHub 用户名或 @me' }
- 涉及：{ valueDescription: 'A GitHub 用户名或@me' }
- label: { valueDescription: 'A GitHub issues/pr label' }
- 类型：{ possibleValues：['pr'，'问题'] }
- 状态：{ possibleValues：['打开'，'关闭'，'合并'] }
- in: { possibleValues: ['标题', '正文', '评论'] }
- user: { valueDescription: 'GitHub 用户名或 @me' }
- org: { valueDescription: 'A GitHub org, without the repo name' }
- repo: { valueDescription: 'A GitHub repo, without the org name' }
- 链接：{ possibleValues：['pr'，'问题'] }
- 里程碑：{ valueDescription：'GitHub 里程碑' }
- 项目：{ valueDescription：'一个 GitHub 项目' }
- 状态：{ possibleValues：['成功'，'失败'，'待定'] }
- head: { valueDescription: '一个 git commit sha 或分支名称' }
- base: { valueDescription: '一个 git commit sha 或分支名称' }
- 评论：{ valueDescription：'一个数字' }
- 交互：{ valueDescription: '一个数字' }
- 反应：{ valueDescription：'一个数字' }
- 草案：{ possibleValues：['true'，'false'] }
- 审查：{ possibleValues：['无'，'必需'，'已批准'，'changes_requested'] }
- reviewBy: { valueDescription: 'GitHub 用户名或 @me' }
- reviewRequested: { valueDescription: 'GitHub 用户名或 @me' }
- userReviewRequested: { valueDescription: 'GitHub 用户名或 @me' }
- teamReviewRequested: { valueDescription: 'GitHub 用户名' }
- 创建：{ valueDescription：'一个日期，带有可选的 < >' }
- 更新：{ valueDescription: '一个日期，带有可选的 < >' }
- close: { valueDescription: '一个日期，带有可选的 < >' }
- 否：{ possibleValues：['标签'，'里程碑'，'受让人'，'项目'] }
- sort: { possibleValues: ['updated', 'updated-asc', 'interactions', 'interactions-asc', 'author-date', 'author-date-asc', 'committer-date', 'committer-date-asc', 'reactions', 'reactions-asc', 'reactions-(+1, -1, smile, tada,心）'] }### 查询示例

- repo:microsoft/vscode is:问题状态:开放排序:updated-asc
- 提及：@me 组织：微软是：问题状态：开放排序：已更新
- 受让人：@me 里程碑：“2024 年 10 月”是：开放是：问题排序：反应
- 评论：>5 组织：contoso 是：问题状态：已关闭提及：@me 标签：bug
- 交互：>5 存储库：contoso/cli 是：问题状态：开放
- repo:microsoft/vscode-python is:问题排序:更新 -assignee:@me
- 存储库：contoso/cli 是：问题排序：更新编号：里程碑

### 形成有效搜索查询的技巧

- 始终尝试在您的回复中包含“repo:”或“org:”。
- “repo”通常被格式化为“所有者/名称”。
- 如果用户指定一个存储库，则始终获取该存储库的标签，并尝试将自然语言查询中的任何单词与标签名称相匹配，以将它们包含在搜索查询中（请参阅“向搜索查询添加标签”部分）。
- 内联代码块中的单词可能指的是标签。尝试将它们与存储库中的标签匹配并将它们包含在搜索查询中。
- 始终包含“排序：”参数。如果可以进行多种排序，请选择用户请求的一种。
- 如果查询包含“me”或“my”，则始终包含带有@me 值的属性。
- 仔细检查自然语言查询的每个单词，并尝试将其与语法组件相匹配。
- 在语法组件前面使用“-”表示它应该是“not-ed”。
- 使用“no”语法组件来指示属性应该为空。

### 向搜索查询添加标签

- 根据用户想要搜索的内容选择标签，而不是根据查询中的实际单词。
- 用户可能会包含有关他们希望如何显示搜索结果的信息。忽略所有这些。
- 标签将被 and-ed 在一起，所以不要选择一堆超级具体的标签。
- 尝试只选择一个标签。
- 仅选择您确定相关的标签。没有标签比不相关的标签更好。
- 不要选择用户明确排除的标签。
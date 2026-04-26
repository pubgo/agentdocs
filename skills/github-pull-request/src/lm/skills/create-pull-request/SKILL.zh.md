---
名称：创建拉取请求
描述：“从当前或指定分支创建 GitHub Pull 请求。使用时机：打开 PR、提交代码供审查、创建 PR 草稿、将分支发布为 Pull 请求、提议对存储库进行更改。”
参数提示：“可选择指定标题、基本分支或是否创建为草稿”
---

# 创建 GitHub 拉取请求

收集必要的信息，准备清晰的标题和描述，然后调用工具打开拉取请求。

## 何时使用

- 用户想要为其当前或指定分支打开 PR
- 用户已完成一项功能或修复并希望提交以供审核
- 用户想要创建 PR 草稿来共享正在进行的工作
- 用户要求“打开 PR”、“创建拉取请求”或“提交审核”

## 程序

### 1. 收集信息

调用工具前确定所需参数：

- **头分支**：如果用户未指定分支，则使用工作区或git上下文查找当前分支名称。不要使用“owner:branch”格式 - 仅传递分支名称（例如“my-feature”）。
- **基本分支**：如果用户未指定基本分支，则忽略它并让工具使用存储库的默认分支。
- **标题**：如果用户未提供标题，请从分支名称、最近提交或用户对其工作的描述中获取标题（请参阅下面的最佳实践）。
- **正文**：如果用户未提供说明，请准备一份关于更改内容和原因的简明摘要（请参阅下面的最佳实践）。
- **草案**：询问或推断 PR 是否应该是草案。默认为非草稿，除非用户表明该作品尚未准备好供审阅。

### 2. 检查未提交或未推送的更改

在创建 PR 之前，检查工作树状态。如果您需要运行 git 命令，请解释为什么需要运行该命令。1. **检查未提交的更改**：使用git工具或VS Code SCM上下文来确定是否存在暂存或未暂存的文件更改。如果是：
	 - 在打开 PR 之前询问用户是否要提交这些更改。
	 - 如果他们这样做，请帮助他们编写提交消息并提交更改（`git add -A && git commit -m "<message>"`）。
	 - 如果他们拒绝，则仅当分支上已经有领先于基础的提交时才继续 - 否则没有任何内容可放入 PR 中。

2. **检查未推送的提交**：确定本地分支是否有尚未推送到远程的提交（即该分支领先于其上游）。如果是：
	 - 在打开 PR 之前询问用户是否要推送，或者让他们知道该工具将在需要时尝试自动推送。
	 - 如果首选手动推送，请在调用该工具之前运行“git push”（如果尚未设置上游，则运行“git push --set-upstream origin <branch>”）。

3. **确认分支位于远程**：`create_pull_request`工具要求头分支存在于远程上。如果没有，请先推动它。

如果所有更改均已提交并推送，则直接继续下一步。

### 3. 准备公关细节

如果用户没有提供标题和描述，请写出好的标题和描述：

**标题**：使用祈使语气，将其控制在 72 个字符以内，并描述 PR 的“内容”（例如“为失败的 API 请求添加重试逻辑”）。

**正文**：包括：
- 更改内容及其原因的简短摘要
- 任何相关问题参考（例如“Fixes #123”）
- 值得注意的实施决策（如果对审阅者有用）

### 4.调用工具

使用“github-pull-request_create_pull_request”工具和收集的参数：

```
github-pull-request_create_pull_request({
	title: '<descriptive title>',
	head: '<branch-name>',        // branch name only, not owner:branch
	body: '<description>',        // optional but recommended
	base: '<base-branch>',        // optional; omit to use repo default
	draft: false,                 // set true for work-in-progress
	headOwner: '<owner>',         // optional; omit if same as repo owner
	repo: { owner: '<owner>', name: '<repo>' }  // optional
})
```

### 5. 确认结果

工具成功返回后：- 将 PR 号和 URL 作为 Markdown 链接报告给用户。该链接应该是 VS Code URI，例如 `vscode-insiders://github.vscode-pull-request-github/open-pull-request-webview?uri=https://github.com/microsoft/vscode-css-languageservice/pull/460` 或`vscode://github.vscode-pull-request-github/open-pull-request-webview?uri=https://github.com/microsoft/vscode-css-languageservice/pull/460`。
- 提及 PR 目标的基础分支。
- 如果 PR 是作为草稿创建的，请提醒用户在适当的时候将其标记为可供审核。

## 最佳实践

### 标题
- 使用祈使语气：“Fix”、“Add”、“Update”、“Remove”、“Refactor” - 而不是“Fixed”、“Adding”等。
- 具体一点：“修复用户登录流程中的空指针”胜过“修复错误”。
- 将其控制在 72 个字符以下，以便在 GitHub 和电子邮件通知中清晰显示。

### 描述
- 从一句话总结开始。
- 解释“为什么”需要进行更改，而不仅仅是“它做什么” - 审阅者受益于上下文。
- 使用“Fixes #<number>”或“Closes #<number>”引用相关问题，以在合并时自动关闭它们。
- 如果更改较大，请添加所涉及的主要文件或组件的简短列表。

### PR 草案
- 当代码尚未准备好进行正式审查时（例如正在进行的工作、等待方法反馈、CI 尚未通过），请使用“draft: true”。
- 草稿 PR 对合作者可见，但在标记为就绪之前不会显示为已请求审核。
- 当用户提到他们仍在处理或只是想要早期反馈时，建议使用草稿。
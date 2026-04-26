---
名称：项目设置信息本地
描述：'提供有关如何设置各种项目的信息。对于根据需求初始化项目和搭建项目很有用。
---

# 如何设置项目

确定用户想要创建什么类型的项目，然后据此选择要遵循的设置信息。仅当文件夹为空或者您刚刚调用该工具时才设置项目，首先调用该工具来创建工作区。

## vscode 扩展

使用 Yeoman 和 Generator-Code 创建 VS Code 扩展的模板。

运行这个命令：

@@代码块0@@
该命令具有以下参数：

- `-t, --extensionType`：指定扩展类型：ts、js、command-ts、command-js、colortheme、语言、snippets、keymap、extensionpack、localization、commandweb、notebook。默认为“ts”
- `-n, --extensionDisplayName`：设置扩展的显示名称。
- `--extensionId`: 设置扩展的唯一 ID。如果用户未请求唯一 ID，请勿选择此选项。
- `--extensionDescription`：提供扩展的描述。
- `--pkgManager`：指定包管理器：npm、yarn 或 pnpm。默认为“npm”。
- `--bundler`：使用 webpack 或 esbuild 捆绑扩展。
- `--gitInit`：初始化扩展的 Git 存储库。
- `--snippetFolder`：指定代码片段文件夹的位置。
- `--snippetLanguage`：设置片段的语言。

### 规则

1. 不要从命令中删除任何参数。仅在用户请求时添加参数。
2. 根据用户的查询调用工具`get_vscode_api`来获取相关引用。
3. get_vscode_api工具完成后，才可以开始修改项目。

## next-js

一个基于 React 的框架，用于构建服务器渲染的 Web 应用程序。

运行这个命令：

@@代码块1@@
该命令具有以下参数：- `--ts, --typescript`：初始化为 TypeScript 项目。这是默认设置。
- `--js, --javascript`：初始化为 JavaScript 项目。
- `--tailwind`：使用 Tailwind CSS 配置进行初始化。这是默认设置。
- `--eslint`：使用 ESLint 配置进行初始化。
- `--app`：初始化为 App Router 项目。
- `--src-dir`：在“src/”目录中初始化。
- `--turbopack`：默认启用 Turbopack 进行开发。
- `--import-alias <prefix/*>`：指定要使用的导入别名。（默认为“@/*”）
- `--api`：使用 App Router 初始化无头 API。
- `--empty`：初始化一个空项目。
- `--use-npm`：明确告诉 CLI 使用 npm 引导应用程序。
- `--use-pnpm`：明确告诉 CLI 使用 pnpm 引导应用程序。
- `--use-yarn`：明确告诉 CLI 使用 Yarn 引导应用程序。
- `--use-bun`：明确告诉 CLI 使用 Bun 引导应用程序。

## 投票

专注于速度和性能的 Web 应用程序前端构建工具。可与 React、Vue、Preact、Lit、Svelte、Solid 和 Qwik 一起使用。

运行这个命令：

@@代码块2@@
该命令具有以下参数：

- `-t, --template NAME`：使用特定模板。可用模板：vanilla-ts、vanilla、vue-ts、vue、react-ts、react、react-swc-ts、react-swc、preact-ts、preact、lit-ts、lit、svelte-ts、svelte、solid-ts、solid、qwik-ts、qwik

## mcp 服务器

模型上下文协议 (MCP) 服务器项目。该项目支持多种编程语言，包括 TypeScript、JavaScript、Python、C#、Java 和 Kotlin。

### 规则1. 首先，访问 https://github.com/modelcontextprotocol 查找所需语言的正确 SDK 和设置说明。如果未指定语言，则默认为 TypeScript。
2.使用`fetch_webpage`工具从https://modelcontextprotocol.io/llms-full.txt找到正确的实现指令
3. 更新 .github 目录中的 copilot-instructions.md 文件以包含对 SDK 文档的引用
4. 在项目根目录的 `.vscode` 文件夹中创建一个 `mcp.json` 文件，其中包含以下内容：`{ "servers": { "mcp-server-name": { "type": "stdio", "command": "command-to-run", "args": [list-of-args] } } }`。
   - mcp-server-name：MCP 服务器的名称。创建反映此 MCP 服务器功能的唯一名称。
   - 命令运行：运行以启动 MCP 服务器的命令。这是您用来运行刚刚创建的项目的命令。
   - list-of-args：传递给命令的参数。这是用于运行刚刚创建的项目的参数列表。
5. 根据所选语言安装任何所需的 VS Code 扩展（例如，Python 项目的 Python 扩展）。
6. 通知用户他们现在可以使用 VS Code 调试此 MCP 服务器。

## python 脚本

一个简单的 Python 脚本项目，当只想创建单个脚本时应选择该项目。

所需扩展：`ms-python.python`、`ms-python.vscode-python-envs`

### 规则

1.调用工具`copilot_runVscodeCommand`在VS Code中正确创建一个新的Python脚本项目。使用以下参数调用该命令。
   请注意，“python-script”和“true”是常量，而“New Project Name”和“/path/to/new/project”分别是项目名称和路径的占位符。
   @@代码块3@@

## python 包

一个Python包项目，可用于创建可分发包。

所需扩展：`ms-python.python`、`ms-python.vscode-python-envs`

### 规则

1. 调用工具 run_vscode_command 在 VS Code 中正确创建新的 Python 包项目。使用以下参数调用该命令。
   请注意，“python-package”和“true”是常量，而“New Package Name”和“/path/to/new/project”分别是包名称和路径的占位符。
   ```json
   {
     "name": "python-envs.createNewProjectFromTemplate",
     "commandId": "python-envs.createNewProjectFromTemplate",
     "args": ["python-package", "true", "New Package Name", "/path/to/new/project"]
   }
   ```
---
名称：安装-vscode-扩展
描述：'如何通过扩展 ID 安装 VS Code 扩展。当用户想要通过安装扩展向其 VS Code 环境添加新功能时非常有用。
---

# 安装 VS Code 扩展

1. VS Code 扩展通过其唯一的扩展 ID 进行标识，该 ID 通常遵循“publisher.extensionName”格式。例如，Microsoft 的 Python 扩展的 ID 为“ms-python.python”。
2. 要安装VS Code扩展，需要使用VS Code命令`workbench.extensions.installExtension`并传入扩展ID。 args 的格式为：
@@代码块0@@
> 注意：如果用户明确提及或者当前环境是 VS Code Insiders，请安装扩展的预发布版本。否则，安装稳定版本。
3. 通过 `copilot_runVscodeCommand` 工具运行该命令。确保将“skipCheck”参数传递为 true 以避免检查命令是否存在，正如我们所知。
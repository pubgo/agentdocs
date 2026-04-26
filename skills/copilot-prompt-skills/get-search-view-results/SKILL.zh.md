---
名称：获取搜索查看结果
描述：“从 VS Code 中的搜索视图获取当前搜索结果”
---

# 获取搜索查看结果

1. VS Code 有一个搜索视图，它可以有现有的搜索结果。
2. 要获取当前搜索结果，可以使用 VS Code 命令 `search.action.getSearchResults`。
3. 通过 `copilot_runVscodeCommand` 工具运行该命令。确保将“skipCheck”参数传递为 true 以避免检查命令是否存在，正如我们所知。
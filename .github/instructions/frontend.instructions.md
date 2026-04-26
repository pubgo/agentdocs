---
description: "编辑前端代码时使用：Alpine.js 组件、API 调用、事件可视化、CSS 样式、HTML 模板。"
applyTo: "web/**"
---
# 前端约定

## 技术栈

- **无构建工具**，所有依赖走 CDN（Alpine.js、Tailwind CSS、vis-network）
- 脚本加载顺序：`api.js`（API 封装）→ `main.js`（状态与交互）
- Alpine.js 应用通过 `x-data="coagentApp()"` 挂载，状态集中在单一对象

## api.js — API 客户端封装层

每个后端端点对应一个全局函数，命名与 REST 语义一致：

```js
const listXxx = () => apiGet("/api/xxx");
const addXxx = (body) => apiPost("/api/xxx", body);
const updateXxx = (id, body) => apiPut(`/api/xxx/${encodeURIComponent(id)}`, body);
const deleteXxxById = (id) => apiDelete(`/api/xxx/${encodeURIComponent(id)}`);
```

- 路径参数**一律** `encodeURIComponent`
- 基础函数 `apiGet/apiPost/apiPut/apiDelete` 统一处理错误和 JSON 解析
- SSE 流用 `new EventSource(...)` 构造

## main.js — 状态管理与交互逻辑

- 全局 `window.coagentApp` 函数返回 Alpine 数据对象
- `refreshAll()` 并发加载各资源列表
- 聊天使用 SSE 增量更新（`assistant.message_delta`），需防止与同步返回重复

## CSS 样式规范

- 事件可视化相关类名统一用 `ev-` 前缀（`ev-turn`、`ev-tool`、`ev-subagent` 等）
- 基础组件类：`.card`、`.btn`、`.input`、`.menu-*`
- Tailwind 工具类 + 自定义 CSS 混合使用

## 新增功能检查清单

1. `api.js` — 添加 API 调用函数
2. `app.js` — 在 `coagentApp()` 中添加状态和方法，`refreshAll()` 中加载新资源
3. `chat.js` — Chat 相关状态和交互（如 missionTemplates、showMissionTemplatePicker）
4. `partials/*.html` — 用 Alpine 指令绑定 UI（`x-model`、`@click`、`x-show`）
5. `styles.css` — 如需自定义样式，使用语义化类名

## 已有组件约定

- **任务模板选择器**：在 `chat.html` 中，通过 `showMissionTemplatePicker` 控制显隐，按类别分组显示，点击调用 `applyMissionTemplate(mt)`
- **技能分类徽章**：在 `skills.html` 中，Category 列显示彩色徽章（execution=emerald、planning=blue、shortcut=amber、utility=slate），Core 字段显示黄色徽章
- **Workflow 管理**：在 `workflows.html` 中，左栏（定义列表 + 快速启动 + 运行列表），右栏（定义详情/编辑器/运行详情）。编辑器支持动态增删步骤 + 条件表达式，Prompt/Agent 为下拉选择器。运行详情含步骤执行历史时间线，running 状态自动 3s 轮询。状态变量以 `workflow` 前缀命名。

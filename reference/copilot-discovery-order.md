# Copilot 文件发现目录与顺序

本文记录 Copilot 执行过程中，不同类型配置的发现目录与优先检查顺序。

---

## Instructions 发现顺序

1. `/Users/barry/.copilot/instructions`
2. `/Users/barry/.claude/rules`
3. `/Users/barry/Library/Application Support/Code/User/prompts`
4. `/Users/barry/git/coagent/.github/instructions`
5. `/Users/barry/git/coagent/.claude/rules`

---

## Skills 发现顺序

1. `/Users/barry/.copilot/skills`
2. `/Users/barry/.agents/skills`
3. `/Users/barry/.claude/skills`
4. `/Users/barry/git/coagent/.github/skills`
5. `/Users/barry/git/coagent/.agents/skills`
6. `/Users/barry/git/coagent/.claude/skills`

---

## Agents 发现顺序

1. `/Users/barry/.claude/agents`
2. `/Users/barry/.copilot/agents`
3. `/Users/barry/Library/Application Support/Code/User/prompts`
4. `/Users/barry/git/coagent/.github/agents`
5. `/Users/barry/git/coagent/.claude/agents`

---

## Hooks 发现顺序

1. `/Users/barry/.claude/settings.json`
2. `/Users/barry/git/coagent/.github/hooks`
3. `/Users/barry/git/coagent/.claude/settings.local.json`
4. `/Users/barry/git/coagent/.claude/settings.json`

---

## 备注

- 以上顺序用于描述“发现路径的检查次序”。
- 实际生效策略（覆盖、合并、冲突处理）取决于具体运行时实现与规则优先级。


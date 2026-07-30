---
type: idea
created: 2026-06-22T20:40
modified: 2026-06-22T20:40
tags: [idea, skill, planning]
status: seed
energy: high
effort: huge
impact: high
related: []
---

# Skill 发展规划

## The Spark
当前 `obsidian-vault-manager` 已经完成 V2 架构重构，接下来需要从结构治理向知识治理演进。同时需要建立 MATLAB 科研编程相关的 skill 体系。

## Why This Excites Me
- Obsidian vault 已经建立了规范的目录结构和审计体系，下一步是让知识真正"连接"起来
- MATLAB 是我日常科研的主要工具，但目前没有一个系统化的 skill 来管理 MATLAB 代码
- 两个方向都有清晰的演进路径

## Raw Thoughts

### 方向一：完善笔记管理 Skill
`obsidian-vault-manager` 已处于 Phase 1，后续还有三个阶段：

- **Phase 2: Knowledge Organization** — Note Organization、Inbox Processing、Template Management
- **Phase 3: Knowledge Linking** — Related Notes、Auto Wikilink、MOC Builder
- **Phase 4: Knowledge Intelligence** — Duplicate Detection、Knowledge Gap、Topic Clustering

最终目标是成为一个 **Research Knowledge Manager**，能回答"我已经有哪些相关知识"、"这篇新笔记应该连接到哪里"。

### 方向二：MATLAB Skill 库
建立 MATLAB 及相关科研编程的 skill 集合，按三步走：

1. **收集**：收集 MATLAB、Python、Research、Code Review、Codebase Analysis 相关 Skill
2. **分析**：分析设计模式（Router Pattern、Workflow Pattern、Tool Wrapper Pattern），抽取共性
3. **构建**：将可复用的模式迁移到 MATLAB 工作流中

## Next Steps
- [ ] 完善笔记管理 Skill — [[skill-evolution]]
- [ ] 建立 MATLAB Skill 库 — [[matlab-skill-library]]

## Related
- [[obsidian-vault-manager/SKILL.md]]
- [[obsidian-vault-manager/references/workflows/index.md]]

---
type: idea
created: 2026-06-22T20:40
modified: 2026-06-22T20:40
tags: [idea, matlab, skill-library]
status: seed
energy: high
effort: large
impact: high
related:
  - "[[skill-plan]]"
---

# MATLAB Skill 库建设计划

## The Spark
日常科研大量使用 MATLAB，但目前没有一个系统化的 skill 来管理 MATLAB 代码开发、项目结构、文档生成等工作流。需要先收集和分析现有优秀 Skill，再构建自己的 MATLAB Skill 体系。

## 三步路线

### Step 1：收集（Skill Reverse Engineering）
收集以下领域的 Skill：
- MATLAB（数字滤波器设计、Live Script 生成）
- Python / Data Science
- Code Review / Codebase Analysis
- Research Workflow

每发现一个优秀 Skill，记录：
```markdown
## Skill Name
**Purpose**: 
**Directory Structure**: 
**Workflow Structure**: 
**Interesting Ideas**: 
**Can Reuse?**: 
```

### Step 2：分析设计模式
建立分类体系，识别通用模式：

| Pattern | 特点 | 示例 |
|---------|------|------|
| Router Skill | SKILL.md 很短，大量引用外部文档 | obsidian-vault-manager V2 |
| Workflow Skill | 一个大工作流 | note-organization |
| Tool Wrapper | 主要调用脚本 | structure-check.sh |

### Step 3：构建 MATLAB Skill
将可复用的模式迁移到 MATLAB 工作流中：
- MATLAB Project Audit（项目结构检查）
- MATLAB Code Review（代码审查）
- MATLAB Documentation Generator（文档生成）

## Next Steps
- [ ] 建立 skill-catalog 目录，开始收集
- [ ] 分析第一个参考 Skill 的设计模式
- [ ] 设计 MATLAB Project Audit 的 workflow

## Related
- [[skill-plan]]
- [[obsidian-vault-manager/references/workflows/structure-audit.md]]

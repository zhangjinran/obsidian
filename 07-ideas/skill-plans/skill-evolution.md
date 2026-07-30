---
type: idea
created: 2026-06-22T20:40
modified: 2026-06-22T20:40
tags: [idea, obsidian, skill-evolution]
status: seed
energy: high
effort: huge
impact: high
related:
  - "[[skill-plan]]"
---

# 完善笔记管理 Skill 路线图

## The Spark
`obsidian-vault-manager` 当前处于结构治理阶段，未来需要向知识治理演进，最终成为一个能自动链接、发现知识关联的 Research Knowledge Manager。

## 四个阶段

### Phase 1: Vault Governance ✅ 已完成
- Structure Audit
- Frontmatter Audit
- Template Audit
- V2 架构重构（Router + Workflow + Schema）

### Phase 2: Knowledge Organization
- Note Organization 工作流
- Inbox Processing
- Template Management
- 标准化笔记模板使用

### Phase 3: Knowledge Linking
- Related Notes：自动发现相关笔记
- Auto Wikilink：自动建议 `[[链接]]`
- MOC Builder：自动生成 Map of Content
- 解决：东西怎么被发现、怎么形成知识网络

### Phase 4: Knowledge Intelligence
- Duplicate Detection：重复笔记检测
- Knowledge Gap Detection：知识空白发现
- Concept Extraction：自动提取核心概念
- Topic Clustering：主题聚类

### 笔记整理改进方向
- **标题层级优先**：使用 `#` 标题层级（`## 知识点` / `### 要点` / `#### 子标题`）替代 `-` 列表，结构更清晰，复习时一目了然

## Next Steps
- [ ] 完善 Phase 2 工作流
- [ ] 调研 Knowledge Linking 的实现方案
- [ ] 设计 MOC Builder 的 workflow
- [ ] 推广标题层级优先的笔记格式

## Related
- [[skill-plan]]
- [[obsidian-vault-manager/SKILL.md]]

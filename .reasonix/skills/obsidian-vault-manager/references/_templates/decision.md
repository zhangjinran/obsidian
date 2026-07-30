---
type: decision
created: {{date:YYYY-MM-DDTHH:mm}}
modified: {{date:YYYY-MM-DDTHH:mm}}
tags: [decision]
status: proposed
decision-makers: []
impact:
reversibility:
superseded-by:
related-project:
vault: {{vault}}
---

# {{title}}

## Context


## Decision


## Alternatives Considered
1.
2.
3.

## Consequences


## Review Date

---

## 使用示例

```markdown
# Switch to PostgreSQL

## Context
What's the situation? Why does a decision need to be made?

## Decision
What was decided and why.

## Alternatives Considered
1. **Stay with MySQL** — Pros: no migration cost. Cons: missing JSONB, worse full-text search.
2. **Use MongoDB** — Pros: flexible schema. Cons: team has no experience.
3. **PostgreSQL** (chosen) — Pros: JSONB, extensions, team knows SQL. Cons: migration effort.

## Consequences
What changes as a result of this decision.

## Review Date
Revisit this decision by: 2026-09-22
```

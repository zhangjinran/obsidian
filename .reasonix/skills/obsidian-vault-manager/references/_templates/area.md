---
type: area
created: {{date:YYYY-MM-DDTHH:mm}}
modified: {{date:YYYY-MM-DDTHH:mm}}
tags: [area]
description:
vault: {{vault}}
---

# {{title}}

## Description


## Active Projects


## Key Contacts


## Processes

---

## 使用示例

```markdown
# Engineering

## Description
What this area covers and why it matters.

## Active Projects
```dataview
TABLE status, priority, target-date
FROM "02-projects"
WHERE area = link("engineering") AND status = "active"
SORT priority ASC
```

## Key Contacts
- [[jane-smith]] — Tech Lead
- [[bob-jones]] — Senior Engineer

## Processes
- [[code-review-process]]
- [[deployment-runbook]]
```

# Frontmatter Schema Reference

This document defines the complete YAML frontmatter schema for every note type in the Obsidian vault system. Frontmatter appears between `---` fences at the top of every `.md` file.

## Table of Contents

1. [Universal Fields](#universal-fields)
2. [Daily Note](#daily-note)
3. [Meeting Note](#meeting-note)
4. [Project](#project)
5. [Area](#area)
6. [Resource](#resource)
7. [Person](#person)
8. [Idea / Brain Dump](#idea--brain-dump)
9. [Decision Log](#decision-log)
10. [Standup](#standup)
11. [Journal (Personal)](#journal-personal)
12. [List (Personal)](#list-personal)

---

## Universal Fields

Every note MUST include these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | enum | yes | Note type identifier. One of: `daily`, `meeting`, `project`, `area`, `resource`, `person`, `idea`, `decision`, `standup`, `journal`, `list` |
| `created` | datetime | yes | ISO 8601 timestamp of creation: `YYYY-MM-DDTHH:MM` |
| `modified` | datetime | yes | ISO 8601 timestamp of last modification |
| `tags` | list[string] | yes | Tag list. Always include the type as first tag. Use kebab-case. |
| `aliases` | list[string] | no | Alternative names for this note (helps with search and linking) |
| `vault` | enum | no | `work` or `personal`. Useful when cross-referencing. |

---

## Daily Note

The daily note is the anchor of each day. It links to everything created or referenced that day.

```yaml
---
type: daily
created: 2026-03-22T08:00
modified: 2026-03-22T18:00
tags: [daily]
aliases: ["Saturday March 22"]
energy: high          # high | medium | low — overall energy level
mood: great           # great | good | okay | rough
weather: sunny        # optional, personal vault
vault: personal
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)

---

## Meeting Note

```yaml
---
type: meeting
created: 2026-03-22T10:00
modified: 2026-03-22T10:45
tags: [meeting, sprint-planning]
aliases: ["Sprint Planning Mar 22"]
attendees:
  - "[[jane-smith]]"
  - "[[bob-jones]]"
project: "[[website-redesign]]"
status: completed     # upcoming | in-progress | completed | cancelled
recurring: true       # whether this is a recurring meeting
cadence: biweekly     # weekly | biweekly | monthly | quarterly (if recurring)
action-items:
  - task: "Review the wireframes"
    owner: "[[jane-smith]]"
    due: 2026-03-25
    done: false
  - task: "Set up staging environment"
    owner: "[[raja]]"
    due: 2026-03-24
    done: false
vault: work
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)
```

---

## Project

```yaml
---
type: project
created: 2026-01-15T09:00
modified: 2026-03-22T14:00
tags: [project, active, q1-2026]
aliases: ["Site Redesign", "New Website"]
status: active        # active | on-hold | completed | cancelled
priority: p1          # p0 (critical) | p1 (high) | p2 (medium) | p3 (low)
start-date: 2026-01-15
target-date: 2026-06-30
end-date:             # filled when completed
owner: "[[raja]]"
stakeholders:
  - "[[jane-smith]]"
  - "[[cto-team]]"
area: "[[engineering]]"
vault: work
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)

---

## Area

```yaml
---
type: area
created: 2026-01-01T00:00
modified: 2026-03-22T12:00
tags: [area]
aliases: []
description: "Ongoing area of responsibility"
vault: work
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)

---

## Resource

```yaml
---
type: resource
created: 2026-03-22T12:00
modified: 2026-03-22T12:00
tags: [resource, docker, devops]
aliases: ["Docker Setup Guide"]
source: "Docker Documentation"
url: "https://docs.docker.com/get-started/"
author: ""
category: how-to      # article | book | video | tool | how-to | recipe | bookmark | course
rating: 4             # 1-5 scale
status: read          # unread | reading | read | reference
related-projects: []
vault: work
---
```

---

## Person

```yaml
---
type: person
created: 2026-03-22T09:00
modified: 2026-03-22T09:00
tags: [person, engineering]
aliases: ["Jane", "JS"]
first-name: Jane
last-name: Smith
company: "Acme Corp"
role: "Tech Lead"
email: "jane@acme.com"
phone: ""
linkedin: ""
relationship: colleague   # colleague | manager | report | client | friend | family | acquaintance | mentor | mentee
last-contact: 2026-03-22
met-at: "Onboarding 2024"
birthday:                 # personal vault
vault: work
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)

---

## Idea / Brain Dump

```yaml
---
type: idea
created: 2026-03-22T03:00
modified: 2026-03-22T03:00
tags: [idea, ai, gardening]
aliases: ["Smart Garden"]
status: seed          # seed | exploring | developing | parked | executed
energy: high          # how excited you are about this: high | medium | low
effort: medium        # estimated effort: low | medium | high | huge
impact: high          # potential impact: low | medium | high
related:
  - "[[website-redesign]]"
  - "[[ai-research]]"
vault: personal
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)

---

## Decision Log

```yaml
---
type: decision
created: 2026-03-22T15:00
modified: 2026-03-22T15:00
tags: [decision, infrastructure]
aliases: ["Postgres Migration Decision"]
status: accepted      # proposed | accepted | deprecated | superseded
decision-makers:
  - "[[raja]]"
  - "[[jane-smith]]"
impact: high          # high | medium | low
reversibility: medium # easy | medium | hard | irreversible
superseded-by: ""     # link to newer decision if deprecated
related-project: "[[website-redesign]]"
vault: work
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)

---

## Standup

```yaml
---
type: standup
created: 2026-03-22T09:00
modified: 2026-03-22T09:05
tags: [standup]
sprint: "Sprint 12"
vault: work
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)

---

## Journal (Personal)

```yaml
---
type: journal
created: 2026-03-22T21:00
modified: 2026-03-22T21:30
tags: [journal, reflection]
mood: reflective      # any freeform mood word
prompt: ""            # optional journaling prompt
vault: personal
---
```

---

## List (Personal)

```yaml
---
type: list
created: 2026-03-22T10:00
modified: 2026-03-22T10:00
tags: [list, gifts]
category: gifts       # wishlist | gifts | restaurants | movies | books | travel | goals
vault: personal
---
```

---

## Course Review

课程/课堂复习笔记，适合按知识点分层整理。

```yaml
---
type: course-review
created: 2026-03-22T10:00
modified: 2026-03-22T10:45
tags: [course-review, 课程标签]
course: "课程名称"
instructor: "讲师"
semester: "2026春"
topic: "本节课/章主题"
status: to-review     # to-review | reviewing | reviewed
rating: 4             # 1-5
---
```

### 模板
完整模板（含使用示例）见 [templates.md](templates.md)

## 疑问
- ❓ 未理解的内容
- ❓ 需进一步查证的问题

## 关联
- [[相关笔记]]
```

---

## Validation Rules

When creating or editing notes, enforce these rules:

1. `type` must be one of the defined enums
2. `created` and `modified` must be valid ISO 8601 datetimes
3. `tags` must be a YAML list, not a comma-separated string
4. `status` values must match the enum for that type
5. `priority` (projects) must be p0–p3
6. Person links in `attendees`, `stakeholders`, etc. must use `"[[name]]"` format
7. `modified` must be >= `created`
8. File must be in the correct folder for its `type`

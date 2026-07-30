# Structure Audit Report

由 `structure-audit` 工作流或 `scripts/structure/structure-check.sh` 生成。

## 格式

```markdown
# Structure Audit Report
Date: YYYY-MM-DD HH:MM
Vault: [vault 名称]

## Summary
- Errors: N
- Warnings: N

## Details

[ERROR] 缺失目录: xxx/
[WARNING] 非法目录: yyy/
```

## 严重度

| 级别 | 含义 |
|------|------|
| ERROR | 必需修复 — 目录缺失影响功能 |
| WARNING | 建议处理 — 存在未定义目录 |

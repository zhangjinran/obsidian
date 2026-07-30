# Frontmatter Audit

检查 vault 中所有笔记的 frontmatter 完整性。

## 触发条件

用户说"检查 frontmatter"、"审计 frontmatter"、"查看笔记元数据完整性"。

## 步骤

### 1. 扫描所有笔记
递归查找所有 `.md` 文件，跳过 `_templates/`、`.obsidian/`

### 2. 逐项检查
对每个 `.md` 文件：
- 是否以 `---` 开头（是否有 frontmatter）
- 是否包含 `type` 字段
- 是否包含 `created` 字段
- 是否包含 `tags` 字段

### 3. 输出报告
列出所有 frontmatter 异常的笔记及问题类型

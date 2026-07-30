# Frontmatter Fix

自动修复或补全笔记的 frontmatter 字段。

## 触发条件

用户说"修复 frontmatter"、"补全 frontmatter"、"帮我补全笔记元数据"。

## 步骤

### 1. 运行 Frontmatter Audit
先执行 [frontmatter-audit.md](frontmatter-audit.md) 找出有问题的笔记

### 2. 逐篇修复
对每篇有问题的笔记：
- 缺失 `---` 包围的 frontmatter → 添加
- 缺失 `type` → 根据上下文推断并标注给用户确认
- 缺失 `created` → 用文件创建时间填充
- 缺失 `tags` → 添加 `[type]` 默认标签

### 3. 输出修复报告
列出每篇笔记修复了哪些字段

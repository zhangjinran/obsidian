# Inbox Processing

处理收件箱，将散落的笔记按类型归入正确目录。

## 触发条件

用户说"处理收件箱"、"清理 inbox"、"收件箱归零"。

## 步骤

### 1. 读取收件箱
扫描 `00-inbox/` 目录下的所有 `.md` 文件

### 2. 分析每篇笔记
读取 frontmatter 中的 `type` 字段，确定笔记类型

### 3. 移动笔记
根据笔记类型移动到对应目录（如 daily→01-daily/, project→02-projects/ 等）

### 4. 更新 frontmatter
在移动过程中补齐缺失的 frontmatter 字段

### 5. 输出处理报告
列出哪些笔记被移到了哪里

## 自动脚本

```bash
python scripts/process-inbox.py <vault-path> [--dry-run]
```

`--dry-run` 只预览不动文件。

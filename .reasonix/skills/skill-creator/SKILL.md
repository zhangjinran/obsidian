---
name: skill-creator
description: 创建、编辑、审查、整理、验证 SKILL.md 文件
---
# Skill Creator

创建、编辑、审查、整理或重构 SKILL.md 文件。

## 硬性规则

- 保持 `SKILL.md` 精简；Reasonix Code 本身已经有足够的能力
- 只有触发关键信息放在 frontmatter 的 `description` 中
- `description` 值用引号包裹
- Frontmatter 必须包含 `name` + `description`
- 长的示例/文档移到 `references/`；脚本移到 `scripts/`；模板/资源移到 `assets/`
- 不要在多文件 skill 内部添加额外的 README/changelog/setup 文档
- 编辑后验证 YAML frontmatter

## 结构

```
skill-name/
  SKILL.md      主文件
  scripts/      可选：确定性辅助脚本
  references/   可选：按需加载的文档
  assets/       可选：输出资源/模板
```

## 好的 SKILL.md 示例

```markdown
---
name: pdf-tools
description: "Inspect, split, merge, OCR, redact, or convert PDFs with local CLI tools."
---

# PDF tools

用于 PDF 操作。页面编辑优先使用确定性脚本。

## 工作流
1. 检查文件/页数
2. 选择具体操作
3. 输出放在输入旁边，除非用户另有要求
4. 渲染/验证修改后的页面
```

## 编辑工作流

1. 读取现有 skill 及附近的资源名称
2. 删除基础模型已经知道的通用建议
3. 保留脆弱的命令语法、认证注意事项、安全规则和验证步骤
4. 除非表格明显更清晰，否则用列表代替表格
5. **Reasonix 化** — 确保 skill 在 Reasonix 下可用
   - 依赖 `run_command` 的命令标注可执行性
   - Python 脚本检查 import（标准库可用，第三方标注需安装）
   - 路径改为相对 `.reasonix/skills/<name>/` 的引用
   - 在末尾添加 `## 脚本命令` 节（如有可调用的脚本）
   - 适配 Reasonix 工具名（`read_file` / `write_file` / `edit_file` 等）
6. 精简表述，片段式可接受
7. 验证 frontmatter

## 脚本命令

```bash
# 验证 skill 结构
python scripts/quick_validate.py <skill-dir>

# 从模板创建新 skill
python scripts/init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets] [--examples]

# 打包 skill 为 .skill 文件
python scripts/package_skill.py <skill-dir> [output-dir]
```

脚本在 `scripts/` 目录下，按需调用。

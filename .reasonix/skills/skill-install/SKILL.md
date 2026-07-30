---
name: skill-install
description: "将第三方 skill 安装到 Reasonix：从 GitHub/npx 下载，搬运到 .reasonix/skills/，改造为 Reasonix 兼容格式"
---

# Skill Install

从外部仓库安装 skill 到 Reasonix 运行环境。

## 触发方式

- **方式 A**: 用户发送 `npx skills add <repo-url> --skill <name>` 类命令 → 按指定地址下载
- **方式 B**: 用户说"找个合适的 skill 装上" → `web_search` 或检查已知仓库，推荐并确认后安装

## 工作流

### 步骤 1: 安装

**方式 A**（指定地址）:
```
web_fetch https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill-name>/SKILL.md
```
如果路径不对，先检查仓库目录结构：
```
web_fetch https://api.github.com/repos/<owner>/<repo>/contents/skills
```

**方式 B**（自动查找）:
1. 检查已知 skill 仓库列表，搜索匹配的 skill
   - https://github.com/anthropics/skills
   - https://skillhub.club/skills
   - https://skills.sh
   - 其他社区仓库
2. 列出候选，让用户选择
3. 确定后获取 SKILL.md + 附属内容

获取全部附属文件（scripts/、references/、assets/、license.txt）：
```
web_fetch https://api.github.com/repos/<owner>/<repo>/contents/skills/<skill-name>
```

**如需 `git clone`**：若 skill 依赖于完整项目仓库（如 `paper-reading-framework`），需先向用户提出申请，获得许可后再执行 `git clone`，不可擅自下载。

### 步骤 2: 移动

1. 在 `.reasonix/skills/<skill-name>/` 下重建目录结构
2. 写入 SKILL.md
3. 写入 scripts/、references/、assets/、license.txt 等文件
4. 检查：`directory_tree .reasonix/skills/<skill-name>`

### 步骤 3: Reasonix 化改装 + 检查

1. **检查 SKILL.md 中的命令** — 找到所有 `run_command` / shell 调用
   - 如果依赖 `npx` / `npm` / `pip` / 系统命令 — 确认当前环境有
   - 如果依赖特定 CLI（如 `obsidian`、`gh`）— 标注为"需要外部工具，调用前检查"
2. **检查 Python 脚本**
   - 读取 `scripts/` 下的 `.py` 文件
   - 检查 import 依赖是否常见（os/sys/pathlib/yaml/json 等标准库可用）
   - 第三方依赖标注"需先 `pip install xxx`"
3. **检查路径引用**
   - 脚本内硬编码路径改为相对路径
   - 确保 `python scripts/xxx.py` 可以从 `.reasonix/skills/<name>/` 目录下直接调用
4. **更新 SKILL.md**
   - 在末尾添加 `## 脚本命令` 节，列出可调用的脚本及用法
   - 保留原 skill 的核心逻辑，适配 Reasonix 工具名
5. **验证** — 如果有 `quick_validate.py` 就用它跑
   - `python3 .reasonix/skills/skill-creator/scripts/quick_validate.py .reasonix/skills/<name>`
   - 没有的话，手动检查 frontmatter 格式
   - 验证不通过则报错，不完成安装

## 注意事项

- 不要直接复制其他平台的配置文件（如 agents/ 目录下的 openai.yaml）
- license.txt 保留原样
- 非必要不修改原 skill 的核心工作流，只适配命令调用方式
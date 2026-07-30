---
name: pdf-paper-translate
description: >-
  Translate an English academic PDF paper into a layout-preserving Chinese PDF — keeps the
  original two-column/single-column format, figures, tables, equations (as real LaTeX/MathML),
  and references, while leaving the source PDF untouched. Use this whenever the user wants a
  research/academic paper PDF turned into Chinese, e.g. "把这篇论文翻译成中文PDF", "translate
  this paper to a Chinese PDF", "论文中文版", "arxiv 论文翻译", or even just handing over a
  paper.pdf and saying "翻译一下 / translate it". A bundled script does the deterministic heavy
  lifting (extract layout, render figures, typeset, print PDF) and Claude writes the translation,
  so no API key is required.
---

# PDF 论文翻译（英文 → 同格式中文 PDF）

把一篇英文学术论文 PDF 翻成中文、尽量保留原排版（双栏/单栏、图、表、公式、参考文献），
最终产出一个中文 PDF。**原文件全程只读、不改动。**

## 核心思路：脚本是护栏，模型是发动机

确定性的重活全部交给脚本 `scripts/translate_paper.py`；模型（也就是你，Claude）只做一件被严格
约束的事——**把抽取出的正文翻成中文 Markdown**。这样排版、取图、出 PDF 都稳定可控，翻译质量
则由你保证。不要试图自己用别的方式解析 PDF 或手画版面——交给脚本。

## 工作流（四阶段）

设论文在 `paper.pdf`，输出默认放到 `paper_zh/`，最终中文稿为 `paper_zh/paper_中文.pdf`。

### 阶段 1 · extract（脚本做）
```bash
python3 .reasonix/skills/pdf-paper-translate/scripts/translate_paper.py paper.pdf --stage extract
```
产出（在 `paper_zh/`）：
- `source.txt` —— 按栏重排后的正文（双栏论文会被正确还原成阅读顺序，并带 `===== PAGE n =====` 标记）
- `figs/figN.png` —— 以「Figure/图 N」图注为锚，渲染其上方的矢量/位图区域
- `figures.json` —— 图清单：`figN → 英文原图注`
- `meta.json` —— 页数、图数、自动判定的栏数、原文件哈希
- `PROMPT.md` —— 翻译铁律（与下文一致，供参考）

### 阶段 2 · translate（**你来做**——这是关键）
读 `paper_zh/source.txt` 和 `paper_zh/figures.json`，严格按下面【翻译铁律】把全文翻成中文，
**写入 `paper_zh/translated.md`**（一个 pandoc Markdown 文件）。

- 论文较长时，**分段翻译、逐步追加**到 `translated.md`，确保忠实、不截断、不漏译。
- 只输出 Markdown 内容本身；YAML 头里的 `title` 等若含冒号务必加引号（否则排版阶段会失败）。
- 无人值守 / 超长论文也可改用脚本内置 API 引擎：`--stage translate --engine api`
  （需 `pip install anthropic` 且设 `ANTHROPIC_API_KEY`），但默认推荐你亲自翻译，质量更高且免 key。

### 阶段 3 · build（脚本做）
```bash
python3 .reasonix/skills/pdf-paper-translate/scripts/translate_paper.py paper.pdf --stage build
```
`pandoc`（`--mathml --number-sections` + 学术 CSS）→ `index.html` → 浏览器打印 → `paper_中文.pdf`。
栏数默认按原文自动判定，可用 `--columns 1|2` 强制。脚本对非法 YAML 头有兜底（自动补引号/必要时去掉），
不必担心偶发的排版崩溃。

### 阶段 4 · verify（脚本做）
```bash
python3 .reasonix/skills/pdf-paper-translate/scripts/translate_paper.py paper.pdf --stage verify
```
校验：原文件哈希未变、译稿页数、图片已嵌入。

> 一条龙：直接 `python3 .reasonix/skills/pdf-paper-translate/scripts/translate_paper.py paper.pdf` 会跑 extract，然后停在 translate 等你
> 产出 `translated.md`，之后你再执行 `--stage build`。

## 翻译铁律（写 translated.md 时严格遵守）

1. **忠实**：不增、不删、不编造。个别看不懂处保留原文并标 `<!-- TODO 待核 -->`。
2. **公式**：行内用 `$...$`、独立用 `$$...$$`；符号（≥ ∈ mod ∑ □ → 等）一律 LaTeX 写法。
3. **保留英文原样，不翻译**：代码/算法标识符（如 `currentTerm`、`AppendEntries RPC`、`log[]`）、
   变量名、函数名；以及**参考文献条目**（作者、题名、出处、页码、DOI、URL 全部原样）。
4. **标题**用 `#/##/###`，不要自己写编号（`--number-sections` 会自动编号）。
5. **图**：源文里出现 "Figure N / Fig. N / 图 N" 处，插入对应图片
   `![译后的图注](figs/figN.png)`；图注依据 `figures.json` 里的英文原注翻译。
6. **表**：把源文里的表重建为 Markdown 表格，翻译表头与单元格；表题写在表格下一行
   `: **表 N.** 表题`。
7. **YAML 头**：文档顶部用 YAML 写 `title`、`author`、`abstract`，把摘要正文、关键词、CCS 概念
   一并放进 `abstract`。含冒号的值要加引号。
8. **参考文献**置于 `# 参考文献 {-}` 之下，逐条保留英文原文，不翻译。
9. **附录**前插入单独一行 `\appendix`，其后的 `#` 标题会自动变成 A、B…。
10. **术语**首次出现可中英并列，如：线性一致性（linearizability）。语言：简体中文，学术语体。

## 依赖

- 必需：`python3` + `pymupdf`（`pip install pymupdf`）、`pandoc`。
- 出 PDF：`playwright`（`pip install playwright && playwright install chromium`）或 `agent-browser`。
- 中文字体：系统需装中文衬线字体——macOS 自带 Songti SC；Linux 装 `fonts-noto-cjk`
  （**缺字体会让中文渲染成豆腐块**，是最常见的坑）。
- 仅 `--engine api` 需要：`pip install anthropic` 且设 `ANTHROPIC_API_KEY`。

## 排障

- **中文变方块/豆腐块** → 没装 CJK 字体，装 `fonts-noto-cjk`（Linux）或确认 macOS 有 Songti SC。
- **build 时 pandoc 退出 64 / YAML 报错** → `translated.md` 的 YAML 头非法（多半是 `title` 含未转义
   冒号）。脚本已有自动兜底；若仍失败，手动给 YAML 值加引号。
- **无显示/服务器上 chromium 起不来** → 设 `CHROMIUM_NO_SANDBOX=1` 再跑 build。
- **图裁得偏大/偏小或漏检** → 图裁剪是启发式；手动重渲 `figs/figN.png` 即可，不影响其它阶段。
- **公式/表格复杂** → 表格依赖你从正文重建，复杂跨行表可能需人工微调。

## 已知边界

只处理可提取文本的 PDF，不做 OCR（扫描版不支持）。目标是「读起来是同一篇论文」，不保证与原版
逐像素一致。

## 脚本命令

```bash
# extract: 从 PDF 提取正文和图片
python3 .reasonix/skills/pdf-paper-translate/scripts/translate_paper.py <paper.pdf> --stage extract

# build: 从 translated.md 生成中文 PDF
python3 .reasonix/skills/pdf-paper-translate/scripts/translate_paper.py <paper.pdf> --stage build

# verify: 校验完整性
python3 .reasonix/skills/pdf-paper-translate/scripts/translate_paper.py <paper.pdf> --stage verify

# 一键跑完 extract → translate（等待你写 translated.md）→ 手动 build → verify
python3 .reasonix/skills/pdf-paper-translate/scripts/translate_paper.py <paper.pdf>
```

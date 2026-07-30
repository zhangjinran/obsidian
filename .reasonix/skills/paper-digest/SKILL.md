---
name: paper-digest
description: >-
  论文阅读室:读取工作目录里新加入的论文(PDF),外语论文自动翻译成中文,
  提炼摘要、核心思想、方法、亮点,并生成中文全文,统一汇入一个带左侧菜单栏的
  精美 HTML 页面(paper-digest/index.html),每处理一篇就增量加入。
  触发场景:用户说"处理论文"、"读论文"、"总结论文"、"翻译论文"、"更新论文库"、
  "有新论文"、"paper digest"、"summarize this paper",或往目录里丢了 PDF 论文
  让你读/总结/翻译时。不适用于写论文、改论文、文献检索。
---

# 论文阅读室 Paper Digest

把论文 PDF 处理成中文阅读页:每篇论文一份「总结」+ 一份「中文全文」,
全部汇入一个带左侧导航的单页 HTML。数据与页面分离,页面由脚本重建,永不手改。

## 目录约定

以**论文所在目录**(通常是当前工作目录,用户另有指定则从其指定)为根:

```
<根目录>/
├── *.pdf                      # 用户丢进来的论文
└── paper-digest/
    ├── index.html             # 生成物,禁止手动编辑
    └── data/<slug>/
        ├── meta.json          # 元信息
        ├── summary.html       # 总结(HTML 片段)
        └── fulltext.html      # 中文全文(HTML 片段)
```

`slug`:从论文标题取 2–4 个关键词的小写 ascii kebab-case,如 `attention-is-all-you-need`。

## 工作流程

### 1. 找出新论文

- 列出根目录下所有 PDF(`ls *.pdf`,必要时也看一层子目录,但跳过 `paper-digest/`)。
- 读取已有的 `paper-digest/data/*/meta.json`,其 `source` 字段记录了已处理的文件名。
- 两者相减即待处理清单。没有新论文就直接告诉用户"没有新论文",并报告当前库里有哪些。

### 2. 逐篇处理(一篇完全做完再做下一篇)

**读取**:用 Read 工具读 PDF,每次最多 20 页,长论文分多次读(`pages: "1-20"`, `"21-40"` …),直到读完正文。参考文献列表可略读。

**判断语言**:正文是中文则无需翻译,`lang: "zh"`;否则记录原语言并翻译。

**写 `meta.json`**(所有字段必填,没有的填 `""`):

```json
{
  "slug": "attention-is-all-you-need",
  "title": "Attention Is All You Need",
  "title_zh": "注意力就是你所需要的一切",
  "authors": "Ashish Vaswani, Noam Shazeer, et al.",
  "venue": "NeurIPS",
  "year": "2017",
  "lang": "en",
  "source": "1706.03762.pdf",
  "added": "2026-07-02",
  "tags": ["Transformer", "注意力机制"]
}
```

`added` 用今天的日期。中文论文的 `title_zh` 就是原标题,`title` 可留原标题或英文题名。

**写 `summary.html`**(纯 HTML 片段,不要 `<html>/<body>` 外壳),固定结构:

```html
<h2>摘要</h2>
<p>用中文重述论文摘要,2–4 句,准确不空泛。</p>

<h2>核心思想</h2>
<p>这篇论文最本质的一个想法是什么、为什么成立。1–2 段。</p>

<h2>方法概述</h2>
<p>技术路线怎么走的,关键组件与流程。可用 <ul> 分点。</p>

<h2>亮点</h2>
<ul>
  <li><strong>一句话点题</strong>:展开说明。3–5 条,含实验结论中的硬数字。</li>
</ul>

<h2>局限与思考</h2>
<p>论文自述的局限 + 你的批判性观察。</p>
```

**写 `fulltext.html`**(中文全文,同样是 HTML 片段):

- **忠实全译,不是缩写**:逐节翻译正文(引言、相关工作、方法、实验、结论),
  只有参考文献列表可省略为一句 `<p class="note">(参考文献从略,见原文)</p>`。
- 章节标题用 `<h2>`(一级节)/`<h3>`(小节),保留原编号,如 `<h2>3 模型架构</h2>`。
- 术语首次出现时括注英文:`自注意力(self-attention)`。人名、系统名保留原文。
- 数学公式写成 LaTeX,行内 `\( ... \)`、独立 `\[ ... \]`(页面已接 MathJax)。
- 表格译成 `<table>`;图片无法提取,在原位置放
  `<blockquote class="figure">图 2:多头注意力结构示意(见原文)。图注译文…</blockquote>`。
- 中文论文不翻译,把正文整理成同样结构的 HTML 即可。
- 全文很长,**分段写入**:先 Write 写入开头几节,之后用 Bash
  `cat >> fulltext.html <<'EOF' ... EOF` 追加,每次追加 1–3 节,直到译完。
  中途不要偷懒截断;写完后用 `grep -c '<h2'` 对照原文章节数自查完整性。

### 3. 重建页面

每处理完一篇就跑一次(脚本在本 skill 的 base directory 下,即本文件所在目录):

```bash
python3 <skill目录>/scripts/build.py <根目录>/paper-digest
```

个人级安装时 `<skill目录>` 通常是 `~/.claude/skills/paper-digest`,
项目级安装时是 `<项目>/.claude/skills/paper-digest`;以会话中报告的 base directory 为准。

脚本会扫描全部 `data/*/`,按收录日期倒序生成 `index.html`。报错就修数据,不要改 index.html。

### 4. 汇报

全部处理完后告诉用户:新收录了哪几篇(中文标题 + 一句话核心思想)、
页面路径,并提示可用 `open <根目录>/paper-digest/index.html` 打开。
macOS 上可以直接帮用户 `open` 它。

## 红线

- `index.html` 只能由 build.py 生成,任何情况下都不要手工编辑它。
- 总结与翻译必须来自真实读到的 PDF 内容,读不到的部分明确说明,不得编造。
- 一次会话论文很多时,按用户关心程度排序逐篇做,做一篇报一篇进度。

## 脚本命令

```bash
# 重建 paper-digest 页面
python3 .reasonix/skills/paper-digest/scripts/build.py <paper-digest目录>
```

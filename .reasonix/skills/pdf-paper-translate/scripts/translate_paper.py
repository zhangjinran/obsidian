#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translate_paper.py — 学术论文 PDF「按原格式」翻译流水线（中文）

设计思路（harness 思路）：
  脚本负责一切确定性的重活——按栏取文、矢量图区域渲染、字体探测、
  HTML/CSS 排版、浏览器打印 PDF、完整性校验；
  模型（默认 Sonnet）只做一件被严格约束的事：把抽取出来的正文翻成中文 Markdown。
  这样即便接入较轻量的模型，也能稳定产出高质量结果。

四个阶段：
  extract   只读原 PDF → source.txt（按栏重排）+ figs/figN.png + figures.json + meta.json
  translate 把 source + 图表清单 + 严格提示词交给模型 → translated.md
              · engine=api    调 Anthropic API（需 anthropic SDK + ANTHROPIC_API_KEY）
              · engine=agent  写出 _translate_request.md，由 Claude Code 子 Agent / 你来产出 translated.md
  build     pandoc(translated.md) → index.html(内嵌学术 CSS, --mathml) → 浏览器打印 PDF
  verify    校验原文件未被改动、图已嵌入、页数

用法：
  python3 translate_paper.py paper.pdf                         # 跑 extract+translate(+build/verify)
  python3 translate_paper.py paper.pdf --engine api            # 用 API 自动翻译
  python3 translate_paper.py paper.pdf --stage extract         # 只抽取
  python3 translate_paper.py paper.pdf --stage build           # 已有 translated.md 后再排版
依赖：pymupdf(fitz)、pandoc、agent-browser（或 playwright python）；api 模式还需 anthropic。
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

# ── 翻译约束层（"协议"）：让模型即便是 Sonnet 也照着这套规则走 ──────────────
PROMPT = r"""你是学术论文翻译引擎。把给定英文论文忠实翻译成中文，产出一个 pandoc Markdown 文件。
只输出 Markdown 本身，不要任何解释、前言或代码围栏包裹。

铁律：
1. 忠实：不增、不删、不编造。个别看不懂处保留原文并标 <!-- TODO 待核 -->。
2. 数学/公式用 $...$（行内）或 $$...$$（独立）；符号（≥ ∈ mod ∑ □ → 等）一律用 LaTeX 写法。
3. 以下保持英文原样，不要翻译：代码/算法标识符（如 currentTerm、AppendEntries RPC、log[]）、
   变量名、函数名；以及参考文献条目（作者、题名、出处、页码、DOI、URL 全部原样保留）。
4. 章节标题用 #/##/###，且不要自己写编号（编号由 --number-sections 自动生成）。
5. 图：源文本中出现 "Figure N / Fig. N / 图 N" 的位置，插入对应图片
   ![译后的图注](figs/figN.png)；图注依据下方【图表清单】里的英文原注翻译。
6. 表：把源文本中的表格重建为 Markdown 表格，翻译表头与单元格；表题写在表格下一行：
   `: **表 N.** 表题`。表内若有 t mod n = s 这类式子用普通文本即可。
7. 文档顶部用 YAML 写 title、author、abstract；把摘要正文、关键词、CCS 概念一并放进 abstract。
8. 参考文献置于 `# 参考文献 {-}` 之下，逐条保留英文原文，不翻译。
9. 附录前插入一行 \appendix（单独成行），其后的 # 标题会自动变为 A、B…。
   若原文有"红色文字为 X 特有"一类说明，按义译出，并在相应条目后加"（X 特有）"。
10. 术语首次出现可中英并列，如：线性一致性（linearizability）。语言：简体中文，学术语体。"""

# ── 学术版式 CSS（双栏、宋体、跨栏标题/图/表；可用 --css 覆盖）─────────────
CSS = r"""<style>
@page { size: A4; margin: 1.5cm 1.3cm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html { font-size: 10.5pt; }
body{ font-family:"Songti SC","STSong","Noto Serif CJK SC",serif; line-height:1.5; color:#000;
  column-count:2; column-gap:1.5em; text-align:justify; margin:0; hyphens:auto; }
#title-block-header{ column-span:all; text-align:center; margin-bottom:.6em; }
h1.title{ font-size:17pt; line-height:1.35; margin:.2em 0 .3em; }
.author{ font-size:10.5pt; margin:.2em 0 .6em; }
.abstract{ column-span:all; text-align:justify; font-size:9.7pt; line-height:1.5;
  margin:.2em 2.2em 1em; padding-top:.4em; border-top:1px solid #999; }
.abstract::before{ content:"摘要　"; font-weight:bold; }
h1:not(.title){ font-size:12.5pt; margin:.9em 0 .35em; border-bottom:1px solid #bbb; padding-bottom:2px; }
h2{ font-size:11pt; margin:.7em 0 .3em; } h3{ font-size:10.5pt; margin:.6em 0 .25em; }
p{ margin:.35em 0; }
figure{ column-span:all; text-align:center; margin:1em auto; break-inside:avoid; }
figure img{ max-width:94%; height:auto; }
figcaption{ font-size:9pt; color:#222; margin-top:.4em; text-align:justify; padding:0 1em; }
table{ column-span:all; width:100%; border-collapse:collapse; font-size:9.3pt; margin:.8em 0; break-inside:avoid; }
caption{ caption-side:bottom; font-size:9pt; margin-top:.4em; text-align:left; }
th,td{ border:1px solid #333; padding:5px 7px; vertical-align:top; text-align:left; }
th{ background:#f0f0f0; }
code{ font-family:"Menlo","Consolas",monospace; font-size:.9em; background:#f4f4f4; padding:0 2px; border-radius:3px; }
ul,ol{ margin:.3em 0; padding-left:1.4em; } li{ margin:.12em 0; }
a{ color:#000; text-decoration:none; }
</style>"""

CAP_RE = re.compile(r'^\s*(Figure|Fig\.?|图)\s*\d', re.I)

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def need(tool: str) -> bool:
    return shutil.which(tool) is not None

# ── 阶段 1：抽取 ─────────────────────────────────────────────────────────
def extract(pdf: Path, outdir: Path):
    import fitz
    figs_dir = outdir / "figs"; figs_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    parts, manifest, fig_n, col_votes = [], [], 0, []
    for pno, page in enumerate(doc):
        W = page.rect.width
        blocks = [b for b in page.get_text("blocks") if b[6] == 0]
        mid = W / 2; margin = W * 0.06
        n = len(blocks)
        left_only = sum(1 for b in blocks if b[2] < mid + margin)   # 整块落在左半
        right_only = sum(1 for b in blocks if b[0] > mid - margin)  # 整块落在右半
        two_col = n >= 6 and left_only >= 0.25 * n and right_only >= 0.25 * n
        if two_col:
            col_votes.append(2)
            L = sorted([b for b in blocks if (b[0]+b[2])/2 < mid], key=lambda b: b[1])
            R = sorted([b for b in blocks if (b[0]+b[2])/2 >= mid], key=lambda b: b[1])
            ordered = L + R
        else:  # 单栏：按 y 再按 x 排，保住阅读顺序
            col_votes.append(1)
            ordered = sorted(blocks, key=lambda b: (round(b[1] / 4.0), b[0]))
        parts.append(f"\n\n===== PAGE {pno+1} =====\n")
        parts += [b[4] for b in ordered]
        # 图：以"Figure/图 N"图注为锚，取其上方的矢量/位图并集区域渲染
        caps = [b for b in blocks if CAP_RE.match(b[4])]
        graphics = [fitz.Rect(d["rect"]) for d in page.get_drawings()]
        for img in page.get_images(full=True):
            try: graphics += [fitz.Rect(r) for r in page.get_image_rects(img[0])]
            except Exception: pass
        used = []
        for cap in caps:
            cx0, cy0, cx1, cy1 = cap[:4]
            above = [g for g in graphics if g.y1 <= cy0 + 6 and g.y1 > cy0 - 420 and g.width > 12 and g.height > 8]
            if not above:
                continue
            u = above[0]
            for g in above[1:]: u |= g
            clip = fitz.Rect(min(u.x0, cx0)-6, u.y0-6, max(u.x1, cx1)+6, min(cy0, u.y1)+4) & page.rect
            # 太小：多半是横线/边框碎片，不是图
            if clip.width < 100 or clip.height < 60:
                continue
            # 文字量过大（>1200 字符）多半是带框正文/表格，不当作图片渲染
            inside = page.get_textbox(fitz.Rect(clip.x0, clip.y0, clip.x1, cy0)) or ""
            if len(inside.strip()) > 1200:
                continue
            # 与本页已渲染的图重叠则去重
            if any(abs(clip.x0-ux) < 30 and abs(clip.y0-uy) < 30 for ux, uy in used):
                continue
            used.append((clip.x0, clip.y0))
            fig_n += 1
            pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip, alpha=False)
            fname = f"figs/fig{fig_n}.png"; pix.save(outdir / fname)
            manifest.append({"id": f"fig{fig_n}", "file": fname, "page": pno+1,
                             "caption_src": re.sub(r'\s+', ' ', cap[4]).strip()[:300]})
    (outdir / "source.txt").write_text("".join(parts), encoding="utf-8")
    (outdir / "figures.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    columns = 2 if col_votes.count(2) > len(col_votes) / 2 else 1
    (outdir / "meta.json").write_text(json.dumps(
        {"source_pdf": str(pdf), "source_sha256": sha256(pdf), "pages": doc.page_count,
         "figures": len(manifest), "columns": columns}, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "PROMPT.md").write_text(PROMPT, encoding="utf-8")
    print(f"[extract] {doc.page_count} 页, {len(manifest)} 张图, 版式={columns} 栏 → {outdir}/source.txt, figs/")
    return manifest

def _request_text(outdir: Path) -> str:
    src = (outdir / "source.txt").read_text(encoding="utf-8")
    man = (outdir / "figures.json").read_text(encoding="utf-8")
    return f"{PROMPT}\n\n# 图表清单（figN → 英文原图注）\n```json\n{man}\n```\n\n# 源文本（已按栏重排）\n{src}\n"

# ── 阶段 2：翻译 ─────────────────────────────────────────────────────────
def translate(outdir: Path, engine: str, model: str):
    req = _request_text(outdir)
    if engine == "api":
        try:
            import anthropic
        except ImportError:
            sys.exit("[translate] 需要 anthropic SDK：pip install anthropic")
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("[translate] 需要环境变量 ANTHROPIC_API_KEY")
        client = anthropic.Anthropic()
        print(f"[translate] 调用 {model} 中…")
        msg = client.messages.create(
            model=model, max_tokens=32000,
            system="你是严谨的学术论文翻译引擎，只输出 Markdown。",
            messages=[{"role": "user", "content": req}])
        md = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        md = re.sub(r'^```(?:markdown)?\s*\n|\n```\s*$', '', md.strip())
        (outdir / "translated.md").write_text(md + "\n", encoding="utf-8")
        print(f"[translate] 已写出 {outdir}/translated.md（{len(md)} 字符）")
    else:  # agent / manual
        (outdir / "_translate_request.md").write_text(req, encoding="utf-8")
        print("[translate] 已写出 _translate_request.md。")
        print("  接入 Sonnet 的方式（任选其一）：")
        print("   · Claude Code 里开一个 sonnet 子 Agent，让它读 _translate_request.md，")
        print("     严格按其中规则把译文写入  " + str(outdir / "translated.md"))
        print("   · 或装好 anthropic 后改用  --engine api")

# ── 阶段 3：排版 ─────────────────────────────────────────────────────────
def build(outdir: Path, columns: str = "auto"):
    md = outdir / "translated.md"
    if not md.exists():
        sys.exit(f"[build] 缺少 {md}（请先完成 translate 阶段）")
    if not need("pandoc"):
        sys.exit("[build] 需要 pandoc")
    if columns == "auto":
        cols = json.loads((outdir / "meta.json").read_text(encoding="utf-8")).get("columns", 2) \
               if (outdir / "meta.json").exists() else 2
    else:
        cols = int(columns)
    css = CSS if cols == 2 else CSS.replace("column-count:2", "column-count:1")
    print(f"[build] 输出版式：{cols} 栏")
    (outdir / "head.html").write_text(css, encoding="utf-8")
    html = outdir / "index.html"
    # 偶发非法 YAML 头（title 含未转义冒号等）会让 pandoc 退出 64。
    # 先试"补引号修复版"，失败再退到"去掉 YAML 头"，保证一定能出版。
    md_text = md.read_text(encoding="utf-8")
    build_md = outdir / "_build.md"
    build_md.write_text(_sanitize_front_matter(md_text), encoding="utf-8")
    try:
        _run_pandoc(outdir, build_md.name)
    except subprocess.CalledProcessError:
        print("[build] YAML 头无法解析，去掉 YAML 头后重试…")
        build_md.write_text(_strip_front_matter(md_text), encoding="utf-8")
        _run_pandoc(outdir, build_md.name)
    print(f"[build] HTML → {html}")
    pdf = outdir / (Path((json.loads((outdir/'meta.json').read_text()))['source_pdf']).stem + "_中文.pdf") \
          if (outdir/'meta.json').exists() else outdir / "translated_中文.pdf"
    _render_pdf(html, pdf)
    return pdf

def _run_pandoc(outdir: Path, md_name: str):
    subprocess.run(["pandoc", md_name, "-o", "index.html", "-s", "--mathml",
                    "--number-sections", "-H", "head.html", "--metadata", "lang=zh"],
                   cwd=outdir, check=True)

def _front_matter_bounds(md: str):
    if not md.startswith("---\n"):
        return None
    end = md.find("\n---", 4)
    return (4, end) if end != -1 else None

def _sanitize_front_matter(md: str) -> str:
    """给首部 YAML 里未加引号的顶层标量值补引号，修复 title/author 含冒号等非法 YAML。"""
    bounds = _front_matter_bounds(md)
    if not bounds:
        return md
    start, end = bounds
    block, rest = md[start:end], md[end + 4:]
    fixed = []
    for line in block.split("\n"):
        m = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(\S.*)$", line)
        if m and not line[:1].isspace():
            val = m.group(2).strip()
            if val and val[0] not in "\"'|>[{":
                val = '"' + val.replace("\\", "\\\\").replace('"', '\\"') + '"'
                fixed.append(f"{m.group(1)}: {val}")
                continue
        fixed.append(line)
    return "---\n" + "\n".join(fixed) + "\n---" + rest

def _strip_front_matter(md: str) -> str:
    """彻底去掉首部 YAML，把 title 还原成一级无编号标题，保证 pandoc 一定能解析。"""
    bounds = _front_matter_bounds(md)
    if not bounds:
        return md
    start, end = bounds
    block, rest = md[start:end], md[end + 4:]
    mt = re.search(r"^title:[ \t]*(.+)$", block, re.M)
    title = mt.group(1).strip().strip("\"'") if mt else ""
    head = f"# {title} {{-}}\n\n" if title else ""
    return head + rest.lstrip("\n")

def _render_pdf(html: Path, pdf: Path):
    url = "file://" + str(html.resolve())
    if need("agent-browser"):
        try:
            subprocess.run(["agent-browser", "--allow-file-access", "open", url], check=True)
            subprocess.run(["agent-browser", "wait", "--load", "networkidle"], check=False)
            subprocess.run(["agent-browser", "pdf", str(pdf.resolve())], check=True)
            subprocess.run(["agent-browser", "close"], check=False)
            print(f"[build] PDF → {pdf}（agent-browser）"); return
        except Exception as e:
            print(f"[build] agent-browser 失败：{e}，尝试 playwright…")
    try:
        from playwright.sync_api import sync_playwright
        args = ["--no-sandbox"] if os.getenv("CHROMIUM_NO_SANDBOX") == "1" else []
        with sync_playwright() as p:
            b = p.chromium.launch(args=args); pg = b.new_page()
            pg.goto(url); pg.wait_for_load_state("networkidle")
            pg.pdf(path=str(pdf), format="A4", print_background=True,
                   margin={"top":"1.5cm","bottom":"1.5cm","left":"1.3cm","right":"1.3cm"})
            b.close()
        print(f"[build] PDF → {pdf}（playwright）")
    except Exception as e:
        print(f"[build] 自动出 PDF 失败（{e}）。HTML 已生成，可手动在浏览器里打印为 PDF：{html}")

# ── 阶段 4：校验 ─────────────────────────────────────────────────────────
def verify(pdf_src: Path, outdir: Path):
    meta = json.loads((outdir / "meta.json").read_text(encoding="utf-8"))
    ok = sha256(pdf_src) == meta["source_sha256"]
    print(f"[verify] 原文件未改动：{'是 ✅' if ok else '否 ❌（注意！）'}")
    out_pdf = list(outdir.glob("*_中文.pdf"))
    if out_pdf:
        try:
            import fitz
            d = fitz.open(out_pdf[0])
            imgs = sum(len(p.get_images()) for p in d)
            print(f"[verify] 译稿 {out_pdf[0].name}：{d.page_count} 页，嵌入图片 {imgs} 张")
        except Exception:
            print(f"[verify] 译稿：{out_pdf[0].name}")
    else:
        print("[verify] 未发现 *_中文.pdf（可能 build 未完成）")

def main():
    ap = argparse.ArgumentParser(description="学术论文 PDF 按原格式翻译流水线")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--out", type=Path, default=None, help="输出目录（默认 <pdf名>_zh/）")
    ap.add_argument("--stage", choices=["all", "extract", "translate", "build", "verify"], default="all")
    ap.add_argument("--engine", choices=["api", "agent"], default=None,
                    help="翻译引擎；默认有 ANTHROPIC_API_KEY 时用 api，否则 agent")
    ap.add_argument("--model", default="claude-sonnet-4-6", help="api 模式所用模型")
    ap.add_argument("--columns", choices=["auto", "1", "2"], default="auto",
                    help="输出版式栏数；auto=按原 PDF 自动判定")
    args = ap.parse_args()
    if not args.pdf.exists(): sys.exit(f"找不到 {args.pdf}")
    outdir = args.out or args.pdf.with_name(args.pdf.stem + "_zh")
    outdir.mkdir(parents=True, exist_ok=True)
    engine = args.engine or ("api" if os.environ.get("ANTHROPIC_API_KEY") else "agent")

    if args.stage in ("all", "extract"): extract(args.pdf, outdir)
    if args.stage in ("all", "translate"): translate(outdir, engine, args.model)
    if args.stage in ("all", "build"):
        if (outdir / "translated.md").exists(): build(outdir, args.columns)
        else: print("[build] 跳过：translated.md 尚未就绪（agent 模式下需先产出译文再 --stage build）")
    if args.stage in ("all", "verify"):
        if (outdir / "meta.json").exists(): verify(args.pdf, outdir)

if __name__ == "__main__":
    main()
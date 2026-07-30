#!/usr/bin/env python3
"""Rebuild paper-digest/index.html from data/<slug>/{meta.json,summary.html,fulltext.html}.

Usage: python3 build.py <paper-digest-dir>
"""
import html
import json
import sys
from datetime import date
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"


def esc(s):
    return html.escape(str(s or ""), quote=True)


def load_entries(data_dir):
    entries = []
    for meta_path in sorted(data_dir.glob("*/meta.json")):
        d = meta_path.parent
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            sys.exit(f"错误: {meta_path} 不是合法 JSON: {e}")
        if not meta.get("slug"):
            meta["slug"] = d.name
        if not meta.get("title_zh"):
            sys.exit(f"错误: {meta_path} 缺少 title_zh")

        def frag(name, fallback):
            p = d / name
            return p.read_text(encoding="utf-8") if p.exists() else f"<p class=\"note\">{fallback}</p>"

        entries.append((
            meta,
            frag("summary.html", "(暂无总结)"),
            frag("fulltext.html", "(暂无中文全文)"),
        ))
    entries.sort(key=lambda e: (e[0].get("added", ""), e[0].get("slug", "")), reverse=True)
    return entries


def render_nav(meta):
    sub = " · ".join(x for x in [meta.get("title"), str(meta.get("year") or "")] if x)
    return (
        f'    <a class="nav-item" href="#{esc(meta["slug"])}" data-slug="{esc(meta["slug"])}">\n'
        f'      <span class="nav-title">{esc(meta["title_zh"])}</span>\n'
        f'      <span class="nav-sub">{esc(sub)}</span>\n'
        f"    </a>"
    )


def render_section(meta, summary, fulltext):
    slug = esc(meta["slug"])
    meta_bits = " · ".join(x for x in [
        meta.get("authors"),
        " ".join(str(v) for v in [meta.get("venue"), meta.get("year")] if v),
        f"收录于 {meta['added']}" if meta.get("added") else "",
    ] if x)
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in meta.get("tags", []))
    tagrow = f'\n      <div class="tagrow">{tags}</div>' if tags else ""
    orig = f'\n      <p class="orig-title">{esc(meta["title"])}</p>' \
        if meta.get("title") and meta.get("title") != meta.get("title_zh") else ""
    return f"""  <section class="paper" id="{slug}" data-slug="{slug}" hidden>
    <header class="paper-head">
      <h1>{esc(meta["title_zh"])}</h1>{orig}
      <p class="meta-line">{esc(meta_bits)}</p>{tagrow}
      <nav class="tabs">
        <button class="tab active" data-pane="summary">总结</button>
        <button class="tab" data-pane="fulltext">中文全文</button>
      </nav>
    </header>
    <div class="pane pane-summary active"><article class="prose">
{summary}
    </article></div>
    <div class="pane pane-fulltext"><article class="prose">
{fulltext}
    </article></div>
  </section>"""


def main():
    if len(sys.argv) != 2:
        sys.exit("用法: python3 build.py <paper-digest目录>")
    root = Path(sys.argv[1]).expanduser().resolve()
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    entries = load_entries(data_dir)
    out = (
        TEMPLATE.read_text(encoding="utf-8")
        .replace("{{COUNT}}", str(len(entries)))
        .replace("{{UPDATED}}", date.today().isoformat())
        .replace("{{NAV}}", "\n".join(render_nav(m) for m, _, _ in entries))
        .replace("{{SECTIONS}}", "\n".join(render_section(*e) for e in entries))
    )
    (root / "index.html").write_text(out, encoding="utf-8")
    print(f"OK: {len(entries)} 篇论文 -> {root / 'index.html'}")


if __name__ == "__main__":
    main()
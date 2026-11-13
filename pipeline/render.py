"""套模板輸出 HTML（render_html），以及用無頭瀏覽器檢查版面（版面閘門 check_render）。"""
import copy
import json
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape

HERE = Path(__file__).resolve().parent
CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"
FIGURES = {"patterns", "ladder", "react_loop", "workflow_agent"}
LATIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.%+\-]*")
OVERFLOW_PX = 4   # 超過這麼多像素才算超出版面（旋轉的便利貼、紅圈會凸出幾 px）
SMALL_SCREENS = [(390, 844), (1024, 640)]   # 手機直立、小筆電


BLANK = {"text": "", "span": 1, "latin": False}


def to_cells(text):
    """稿紙格：中文和標點一字一格、英數連續的字兩個一格，空白略過。"""
    tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9.%+\-]*|\S", text or "")
    return [{"text": t, "span": max(1, (len(t) + 1) // 2), "latin": True} if LATIN.fullmatch(t)
            else {"text": t, "span": 1, "latin": False} for t in tokens]


def title_cells(title, row):
    """題目置中寫在一排格子裡。"""
    cells = to_cells(title)
    pad = max(0, row - sum(c["span"] for c in cells))
    return [BLANK] * (pad // 2) + cells + [BLANK] * (pad - pad // 2)


def manuscript(title, subtitle, cols=14):
    """封面：整張稿紙。題目置中寫在第二行，副標題照作文格式空兩格起寫、寫滿換行。"""
    def pad(row):
        return row + [BLANK] * (cols - sum(c["span"] for c in row))
    rows, line = [[BLANK] * cols, title_cells(title, cols), [BLANK] * cols], []
    for cell in [BLANK, BLANK] + to_cells(subtitle):
        if sum(c["span"] for c in line) + cell["span"] > cols:
            rows.append(pad(line))
            line = []
        line.append(cell)
    return rows + [pad(line), [BLANK] * cols]


def mark_refs(content, pages):
    """替每個有 cite 的欄位加上 ①② 標記；回傳（加了標記的內容, 依出現順序的 Wiki 頁）。"""
    refs = []

    def visit(node):
        if isinstance(node, list):
            for item in node:
                visit(item)
        elif isinstance(node, dict):
            if isinstance(node.get("cite"), list):
                marks = []
                for path in node["cite"]:
                    if isinstance(path, str) and path in pages:
                        if path not in refs:
                            refs.append(path)
                        marks.append(CIRCLED[min(refs.index(path), len(CIRCLED) - 1)])
                node["marks"] = "".join(dict.fromkeys(marks))
            for key, value in list(node.items()):
                if key != "cite":
                    visit(value)

    content = copy.deepcopy(content)
    visit(content)
    return content, refs


def wiki_href(path):
    repo = json.loads((HERE / "site.json").read_text(encoding="utf-8")).get("repo_url", "").rstrip("/")
    return f"{repo}/blob/main/wiki/{path}" if repo else f"../../wiki/{path}"


def view_model(slides, pages):
    deck = []
    for n, spec in enumerate(slides, 1):
        raw = spec.get("content")
        content, refs = mark_refs(raw, pages) if isinstance(raw, dict) else (None, [])
        visual = spec.get("visual") if spec["type"] in ("concept", "steps") and spec.get("visual") in FIGURES else None
        deck.append({
            "id": spec["id"], "n": n, "type": spec["type"], "title": spec["title"],
            "cells": title_cells(spec["title"], 18),
            "sheet": manuscript(spec["title"], (raw or {}).get("subtitle", "") if isinstance(raw, dict) else "")
            if spec["type"] == "cover" else None,
            "c": content, "visual": visual, "notes": (raw or {}).get("notes", "") if isinstance(raw, dict) else "",
            "refs": [{"mark": CIRCLED[min(i, len(CIRCLED) - 1)], "title": pages[p]["title"], "href": wiki_href(p)}
                     for i, p in enumerate(refs)],
        })
    return deck


def inline_code(text):
    """模型偶爾用 Markdown 反引號標函式名稱（s08 的 `quote_order`）：先跳脫 HTML，再把反引號換成 <code>。"""
    return Markup(re.sub(r"`([^`\n]+)`", r"<code>\1</code>", str(escape(text or ""))))


def render_deck(slides, pages, out_path, run_id):
    env = Environment(loader=FileSystemLoader(HERE / "templates"), autoescape=True, trim_blocks=False)
    env.filters["code"] = inline_code
    deck = view_model(slides, pages)
    html = env.get_template("deck.html.j2").render(deck=deck, deck_title=deck[0]["title"] if deck else "教學簡報",
                                                   run_id=run_id)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path


MEASURE = """() => {
  const out = {};
  document.querySelectorAll('.slide').forEach((s) => {
    const body = s.querySelector('.body'), row = s.querySelector('.title-row'), cells = s.querySelector('.cells');
    const dy = body ? body.scrollHeight - body.clientHeight : 0;
    const dx = cells && row ? cells.offsetWidth - row.clientWidth : 0;
    const dz = s.scrollHeight - s.clientHeight;
    const worst = Math.max(dy, dx, dz);
    if (worst > %d) out[s.id] = worst;
  });
  return out;
}""" % OVERFLOW_PX


def check_render(html_path, shots_dir):
    """版面閘門：每頁內容不能超出 1280×720、不能有主控台錯誤；順便替每頁截圖存證。"""
    from playwright.sync_api import sync_playwright
    shots_dir = Path(shots_dir)
    shots_dir.mkdir(parents=True, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")   # 用 Windows 內建的 Edge，不另外下載瀏覽器
        page = browser.new_page(viewport={"width": 1280, "height": 776})
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(Path(html_path).resolve().as_uri())
        page.evaluate("async () => { await document.fonts.ready; }")
        page.wait_for_timeout(800)
        overflow = page.evaluate(MEASURE)
        count = page.evaluate("window.deck.count")
        for i in range(count):
            page.evaluate(f"window.deck.go({i})")
            page.wait_for_timeout(400)
            page.locator("#stage").screenshot(path=str(shots_dir / f"{i + 1:02d}.png"))
        # 手機、小筆電：整張投影片要落在視窗裡。v3 才發現 grid 置中在比 1280px 窄的視窗會偏到右下，原本只量 1280 寬看不出來
        small_screen = {}
        for w, h in SMALL_SCREENS:
            page.set_viewport_size({"width": w, "height": h})
            page.wait_for_timeout(300)
            box = page.evaluate("(() => { const b = document.getElementById('stage').getBoundingClientRect();"
                                " return [b.left, b.top, b.right, b.bottom]; })()")
            if box[0] < -1 or box[1] < -1 or box[2] > w + 1 or box[3] > h + 1:
                small_screen[f"{w}x{h}"] = [round(v) for v in box]
        browser.close()
    return {"overflow": overflow, "console_errors": errors, "screenshots": count, "small_screen": small_screen}

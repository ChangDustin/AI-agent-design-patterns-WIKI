"""讀取 Wiki、取出教學用段落、把查詢結果回存到 Wiki（CLAUDE.md 的 Query 流程）。"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
sys.path.insert(0, str(ROOT / "tools"))
import wiki_lint  # noqa: E402  共用 frontmatter 解析與健檢

LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
# 每種頁面取哪些固定段落當教學材料（CLAUDE.md §4）；None 表示整頁
EXCERPT_SECTIONS = {
    "concept": ["一句話定義", "生活比喻", "運作步驟", "例子", "什麼時候用、什麼時候別用", "常見誤解"],
    "source": ["一段話摘要", "可用的教學素材"],
}


def split_sections(text):
    """{二級標題: 內文}，保留行內程式碼（和 wiki_lint.sections 不同）。"""
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def plain(text):
    """去掉 frontmatter，把 [文字](網址) 換成文字，省 token。"""
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    return LINK.sub(r"\1", text)


def load_pages():
    pages = {}
    for path in sorted(WIKI.rglob("*.md")):
        rel = path.relative_to(WIKI).as_posix()
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        meta = wiki_lint.frontmatter(text) or {}
        pages[rel] = {"title": meta.get("title", rel), "type": meta.get("type", ""),
                      "plain": plain(text), "sections": split_sections(text)}
    return pages


def lint():
    return wiki_lint.lint(WIKI)


def index_for_planner():
    """目錄頁轉成給規劃者看的精簡版：「標題 <路徑> — 摘要」。"""
    text = (WIKI / "index.md").read_text(encoding="utf-8")
    text = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r"\1 <\2>", text)
    return "\n".join(line for line in text.splitlines() if line.strip() and not line.startswith(">"))


def excerpt(pages, path, limit):
    """取出一頁的教學段落，超過 limit 字就在行尾截斷。"""
    page = pages[path]
    names = EXCERPT_SECTIONS.get(page["type"])
    if names:
        body = "\n".join(f"【{n}】\n{page['sections'][n]}" for n in names if page["sections"].get(n))
    else:
        body = page["plain"]
    body = re.sub(r"\n{2,}", "\n", LINK.sub(r"\1", body)).strip()
    if len(body) > limit:
        body = body[:limit].rsplit("\n", 1)[0] + "\n……（以下截斷）"
    return f"### 頁面 {path}：{page['title']}\n{body}"


def file_query_page(name, title, summary, body):
    """把查詢結果存成 wiki/queries/<name>.md，並在 index 的「查詢結果」登記（已登記就略過）。"""
    rel = f"queries/{name}.md"
    head = f"---\ntitle: {title}\ntype: query\nsources: []\nupdated: {date.today()}\n---\n\n# {title}\n\n"
    (WIKI / rel).write_text(head + body.strip() + "\n", encoding="utf-8")
    index = WIKI / "index.md"
    text = index.read_text(encoding="utf-8")
    if f"]({rel})" not in text:
        text = text.replace("## 查詢結果\n\n", f"## 查詢結果\n\n- [{title}]({rel}) — {summary}\n", 1)
        index.write_text(text, encoding="utf-8")
    return rel


def append_log(heading, lines):
    with open(WIKI / "log.md", "a", encoding="utf-8") as f:
        f.write(f"\n## [{date.today()}] {heading}\n\n" + "\n".join(f"- {line}" for line in lines) + "\n")

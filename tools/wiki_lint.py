"""Wiki 健檢（lint）：依 CLAUDE.md 的規則檢查 wiki/。

用法：
  python tools/wiki_lint.py              檢查 wiki/
  python tools/wiki_lint.py --selftest   用一個小型假 Wiki 測試這支程式

ERROR 要先修好才能 ingest 下一篇；WARN 給人複查；GAP 是標了「待補」的資料缺口。
"""
import re
import sys
import tempfile
from pathlib import Path

CONCEPT_SECTIONS = ["一句話定義", "生活比喻", "運作步驟", "例子", "什麼時候用、什麼時候別用", "常見誤解", "相關概念", "來源"]
SOURCE_SECTIONS = ["基本資訊", "一段話摘要", "重點", "對 Wiki 的影響", "可用的教學素材", "限制與存疑"]
CITED = set(CONCEPT_SECTIONS[:6])  # 概念頁這幾段的每一句都要有出處
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CITATION = re.compile(r"\]\((?:\.\./)?sources/[^)]+\)|Wiki 綜合")
SPECIAL = {"index.md", "log.md"}  # 目錄和日誌不檢查格式，它們的連結也不算「被連入」


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    meta = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if not sep or line.startswith(" "):
            continue
        value = value.split("#")[0].strip()
        meta[key.strip()] = [v.strip() for v in value.strip("[]").split(",") if v.strip()] if value.startswith("[") else value
    return meta


def prose_lines(text):
    """去掉程式碼區塊和行內程式碼後的每一行。"""
    code = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            code = not code
            continue
        if not code:
            yield re.sub(r"`[^`]*`", "", line)


def sections(text):
    """{二級標題: [內文行]}"""
    out, cur = {}, None
    for line in prose_lines(text):
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def is_claim(line):
    s = line.strip()
    return bool(s) and not s.startswith(("#", ">", "|")) and not s.endswith("：")


def lint(wiki):
    wiki = Path(wiki).resolve()
    errors, warns, gaps = [], [], []
    pages = sorted(wiki.rglob("*.md"))
    name = lambda p: p.relative_to(wiki).as_posix()
    inbound = {name(p): 0 for p in pages}
    index = (wiki / "index.md").read_text(encoding="utf-8") if (wiki / "index.md").exists() else ""
    source_ids = {p.stem for p in (wiki / "sources").glob("*.md")}

    for p in pages:
        n, text = name(p), p.read_text(encoding="utf-8").replace("\r\n", "\n")
        for line in prose_lines(text):
            for target in LINK.findall(line):
                if re.match(r"[a-z]+:", target) or target.startswith("#"):
                    continue
                dest = (p.parent / target.split("#")[0]).resolve()
                if not dest.exists():
                    errors.append(f"{n}: 斷掉的連結 → {target}")
                elif p.name not in SPECIAL and dest.is_relative_to(wiki) and dest != p:
                    inbound[name(dest)] = inbound.get(name(dest), 0) + 1
        if p.name in SPECIAL:
            continue
        meta = frontmatter(text)
        if meta is None:
            errors.append(f"{n}: 缺 frontmatter")
            continue
        for key in ("title", "type", "sources", "updated"):
            if key not in meta:
                errors.append(f"{n}: frontmatter 缺 {key}")
        for sid in meta.get("sources") or []:
            if sid not in source_ids:
                errors.append(f"{n}: frontmatter 的來源 {sid} 沒有對應的 sources/{sid}.md")
        if f"]({n})" not in index:
            errors.append(f"{n}: 沒有列在 index.md")
        kind, secs = meta.get("type"), sections(text)
        for s in {"concept": CONCEPT_SECTIONS, "source": SOURCE_SECTIONS}.get(kind, []):
            if s not in secs:
                errors.append(f"{n}: 缺固定段落「{s}」")
        for s, lines in secs.items():
            for line in lines:
                if "待補" in line:
                    gaps.append(f"{n}「{s}」{line.strip()}")
                elif kind == "concept" and s in CITED and is_claim(line) and not CITATION.search(line):
                    warns.append(f"{n}「{s}」缺出處：{line.strip()[:50]}")

    for n, count in inbound.items():
        # queries/ 是查詢結果回存，列在 index 就夠了（CLAUDE.md §5）
        if count == 0 and n not in SPECIAL and n != "overview.md" and not n.startswith("queries/"):
            warns.append(f"{n}: 孤兒頁（除了 index 之外沒有頁面連進來）")
    return errors, warns, gaps


def selftest():
    head = "---\ntitle: t\ntype: {}\nsources: [{}]\nupdated: 2026-11-12\n---\n"
    files = {
        "index.md": "- [a](concepts/a.md)\n- [x](sources/x.md)\n",
        "sources/x.md": head.format("source", "x") + "".join(f"## {s}\n內容\n" for s in SOURCE_SECTIONS),
        "concepts/a.md": head.format("concept", "x, y")
        + "## 一句話定義\n有出處（[x](../sources/x.md)）\n沒有出處的句子\n## 例子\n目前資料未提及，待補。\n[壞連結](nope.md)\n",
        "concepts/b.md": head.format("entity", ""),
    }
    with tempfile.TemporaryDirectory() as tmp:
        for rel, body in files.items():
            (Path(tmp) / rel).parent.mkdir(parents=True, exist_ok=True)
            (Path(tmp) / rel).write_text(body, encoding="utf-8")
        errors, warns, gaps = lint(tmp)
    found = "\n".join(errors + warns)
    for expected in ["斷掉的連結 → nope.md", "來源 y 沒有", "缺固定段落「生活比喻」", "concepts/b.md: 沒有列在 index.md",
                     "缺出處：沒有出處的句子", "concepts/b.md: 孤兒頁"]:
        assert expected in found, expected
    assert "缺出處：有出處" not in found and "sources/x.md:" not in found, found
    assert len(gaps) == 1 and "待補" in gaps[0], gaps
    print("selftest OK")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        return selftest()
    errors, warns, gaps = lint(Path(__file__).resolve().parent.parent / "wiki")
    for tag, items in (("ERROR", errors), ("WARN", warns), ("GAP", gaps)):
        for item in items:
            print(f"[{tag}] {item}")
    print(f"結果：{len(errors)} 個錯誤、{len(warns)} 個警告、{len(gaps)} 個待補缺口")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

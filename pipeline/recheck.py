"""人在迴圈中：人指定要重審哪幾頁，從某次執行的結果續跑，不重跑整份簡報。

從 RUN_DIR 的 final_slides.json（每頁內容）和 report.md（分數、版本、是否通過）重建狀態，寫成 RUN_DIR/resume.json：
指定的頁清掉舊分數，交給 check_slides 用目前的閘門重新檢查；其他頁照舊沿用。接著執行
  .venv/Scripts/python -m pipeline.graph --resume RUN_DIR --max-rounds 3
（rounds 從 1 開始，--max-rounds 3 讓重審的頁還有 2 輪改寫機會。）
第一次重審是手寫的 runs/20261113-002929/recheck_v3.py，之後改成這個工具。

用法（在專案根目錄）：.venv/Scripts/python -m pipeline.recheck runs/<run-id> s04 s15 --why "為什麼要重審"
"""
import argparse
import json
import re
from pathlib import Path

from . import graph, wiki

# report.md 投影片表的一列；舊版報告沒有最後的「通過閘門」欄
ROW = re.compile(r"^\| (s\d+) \| \w+ \| .*? \| ([\d.]+) \| 第 (\d+) 輪 \| [^|]* \|(?: ([✓✗]) \|)?$", re.M)


def rebuild(run, recheck):
    final = json.loads((run / "final_slides.json").read_text(encoding="utf-8"))["slides"]
    outline = [{k: v for k, v in s.items() if k != "content"} for s in final]
    slides = {s["id"]: s["content"] for s in final}
    unknown = set(recheck) - set(slides)
    if unknown:
        raise SystemExit(f"這次執行沒有這些頁：{sorted(unknown)}")
    rows = ROW.findall((run / "report.md").read_text(encoding="utf-8"))
    if len(rows) != len(final):
        raise SystemExit(f"report.md 的投影片表只讀到 {len(rows)} 列，應該是 {len(final)} 列")
    pages = wiki.load_pages()
    excerpts = {s["id"]: "\n\n".join(wiki.excerpt(pages, p, graph.EXCERPT_PER_PAGE) for p in s.get("pages", []))
                for s in outline}
    best = {sid: {"slide": slides[sid], "score": float(score), "passed": mark != "✗", "round": int(rnd)}
            for sid, score, rnd, mark in rows if sid not in recheck}
    return {"outline": outline, "excerpts": excerpts, "slides": slides, "best": best, "failing": {},
            "changed": list(recheck), "rounds": 1, "render_fix_done": False}


def main():
    parser = argparse.ArgumentParser(description="指定要重審的頁，寫出 resume.json")
    parser.add_argument("run_dir")
    parser.add_argument("slides", nargs="+", help="要重審的投影片 id，例如 s04 s15")
    parser.add_argument("--why", required=True, help="為什麼要重審（寫進 resume.json，留下紀錄）")
    args = parser.parse_args()
    run = Path(args.run_dir)
    state = rebuild(run, args.slides)
    (run / "resume.json").write_text(json.dumps({"next": "check_slides", "state": state, "note": f"pipeline.recheck：{args.why}"},
                                                ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已寫出 {run / 'resume.json'}：重審 {args.slides}，沿用 {len(state['best'])} 頁")


if __name__ == "__main__":
    main()

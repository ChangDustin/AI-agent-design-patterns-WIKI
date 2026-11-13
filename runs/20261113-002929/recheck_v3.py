"""v3 回歸檢查：用新的閘門重新檢查這次執行被標記的頁，不重跑整份簡報。

這次執行結束時標記 4 頁：s04、s13 超出版面，s05、s08 被判字數超過上限。改了三件事之後
（width() 英數字算半格、有圖的 concept 頁最多 2 點、評審看得到字數上限和圖的內容），
先不呼叫 LLM、只用新閘門和新模板重量一次：s05、s08 其實排得下（舊的 len() 誤退件），
s13 換了模板就不超出；只剩 s04 還要改。s05、s08 最後的版本從沒給評審看過，所以和 s04 一起重審。

這次執行沒有存最後的 state，從 final_slides.json 和 report.md 的投影片表重建，寫成 resume.json，
再用 `python -m pipeline.graph --resume runs/20261113-002929 --max-rounds 3` 從 check_slides 續跑
（rounds 從 1 開始，--max-rounds 3 讓這次還有 2 輪改寫機會）。

用法（在專案根目錄）：.venv/Scripts/python runs/20261113-002929/recheck_v3.py
"""
import json
import re
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import graph, wiki  # noqa: E402

RECHECK = ["s04", "s05", "s08"]
final = json.loads((RUN / "final_slides.json").read_text(encoding="utf-8"))["slides"]
outline = [{k: v for k, v in s.items() if k != "content"} for s in final]
slides = {s["id"]: s["content"] for s in final}
pages = wiki.load_pages()
excerpts = {s["id"]: "\n\n".join(wiki.excerpt(pages, p, graph.EXCERPT_PER_PAGE) for p in s.get("pages", []))
            for s in outline}

# report.md 投影片表的一列：| s13 | concept | 能簡單就簡單 | 0.9 | 第 3 輪 | ... |
rows = re.findall(r"^\| (s\d+) \| \w+ \| .*? \| ([\d.]+) \| 第 (\d+) 輪 \|", (RUN / "report.md").read_text(encoding="utf-8"), re.M)
assert len(rows) == len(final), f"report.md 只讀到 {len(rows)} 列"
# 要重審的頁不放進 best：舊分數是舊閘門給的，新的一輪重新評分
best = {sid: {"slide": slides[sid], "score": float(score), "round": int(rnd)}
        for sid, score, rnd in rows if sid not in RECHECK}

state = {"outline": outline, "excerpts": excerpts, "slides": slides, "best": best, "failing": {},
         "changed": RECHECK, "rounds": 1, "render_fix_done": False}
(RUN / "resume.json").write_text(json.dumps({"next": "check_slides", "state": state,
                                             "note": "由 recheck_v3.py 從 final_slides.json 與 report.md 重建（v3 回歸檢查）"},
                                            ensure_ascii=False, indent=2), encoding="utf-8")
print("重審：", RECHECK, "｜沿用分數：", len(best), "頁")

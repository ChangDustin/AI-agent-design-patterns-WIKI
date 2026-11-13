"""一次性修復：這次執行在 revise_slides 第 2 輪因網路斷線中止，當時 pipeline 還沒有自動存 resume.json。
從 calls/（每次 LLM 呼叫的完整回應）和 check_round0/1.json 重建斷線前的狀態，寫成 resume.json，
再用 `python -m pipeline.graph --resume runs/20261113-001206` 從 revise_slides 續跑。

用法（在專案根目錄）：.venv/Scripts/python runs/20261113-001206/recover_state.py
"""
import json
import re
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import graph, wiki  # noqa: E402

outline = json.loads((ROOT / "runs/20261113-000224/outline_reviewed.json").read_text(encoding="utf-8"))["slides"]
pages = wiki.load_pages()
excerpts = {s["id"]: "\n\n".join(wiki.excerpt(pages, p, graph.EXCERPT_PER_PAGE) for p in s.get("pages", []))
            for s in outline}

calls = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(RUN.glob("calls/*.json"))]
last_check = max(c["n"] for c in calls if c["node"] == "check_slides")   # 第 1 輪檢查的最後一次呼叫
draft, round1, round2 = {}, {}, {}
for c in calls:
    if not c["response"] or c["node"] not in ("draft_slides", "revise_slides"):
        continue
    sid = re.search(r"=== 投影片 (s\d+) ===", c["user"]).group(1)
    target = draft if c["node"] == "draft_slides" else (round2 if c["n"] > last_check else round1)
    target[sid] = json.loads(c["response"])

r0 = json.loads((RUN / "check_round0.json").read_text(encoding="utf-8"))
r1 = json.loads((RUN / "check_round1.json").read_text(encoding="utf-8"))
best, slides = {}, {}
for s in outline:
    sid = s["id"]
    v1 = round1.get(sid, draft[sid])                       # 第 1 輪檢查時的版本
    candidates = [(r0["scores"][sid], 0, draft[sid]), (r1["scores"][sid], 1, v1)]
    score, rnd, slide = max(candidates, key=lambda c: (c[0], c[1]))   # 同分取較新的版本
    best[sid] = {"slide": slide, "score": score, "round": rnd}
    slides[sid] = round2.get(sid, v1)                      # 目前最新的版本（含第 2 輪已改好的頁）

state = {"outline": outline, "excerpts": excerpts, "slides": slides, "best": best,
         "failing": {sid: v for sid, v in r1["failing"].items() if sid not in round2},
         "changed": sorted(round2), "rounds": 1, "render_fix_done": False}
(RUN / "resume.json").write_text(json.dumps({"next": "revise_slides", "state": state,
                                             "note": "由 recover_state.py 從 calls/ 與 check_round*.json 重建"},
                                            ensure_ascii=False, indent=2), encoding="utf-8")
print("第 2 輪已改好：", sorted(round2), "｜還要改：", sorted(state["failing"]))

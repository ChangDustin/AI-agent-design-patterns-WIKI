"""不需要 API key 的自我測試：程式閘門、稿紙格、引用編號、流程圖；加 --preview 會用假投影片渲染並截圖。

用法：.venv/Scripts/python -m pipeline.test_offline [--preview 輸出資料夾]
"""
import sys
from pathlib import Path

from . import checks, render, wiki

PAGES = wiki.load_pages()
R, T, P, M, W = ("concepts/reflection.md", "concepts/tool-use.md", "concepts/planning.md",
                 "concepts/multi-agent-collaboration.md", "concepts/workflow-vs-agent.md")
L, H, A, RE = ("concepts/agent-limitations.md", "concepts/human-in-the-loop.md",
               "concepts/agentic-workflow.md", "concepts/react.md")


def cite(text, *paths):
    return {"text": text, "cite": list(paths)}


FIXTURE = [
    {"id": "s01", "type": "cover", "title": "AI 代理設計模式", "goal": "封面", "pages": [], "visual": "none",
     "content": {"subtitle": "讓 AI 像人一樣：先打草稿、再修改", "notes": "今天要聊的是 AI 怎麼分多步把事情做好。"}},
    {"id": "s02", "type": "hook", "title": "同一題，誰的分數高？", "goal": "流程比換模型更重要", "pages": [A], "visual": "none",
     "content": {"stats": [{"value": "48.1%", "label": "GPT-3.5 一次寫完", "cite": [A]},
                           {"value": "67.0%", "label": "GPT-4 一次寫完", "cite": [A]},
                           {"value": "95.1%", "label": "GPT-3.5＋代理迴圈", "cite": [A]}],
                 "takeaway": cite("改流程帶來的進步，比換成更強的模型還大", A), "notes": "這是 HumanEval 程式題的答對率。"}},
    {"id": "s03", "type": "concept", "title": "反思：自己改作文", "goal": "懂反思", "pages": [R], "visual": "none",
     "content": {"definition": cite("讓 LLM 檢查自己剛產出的結果、提出具體改進建議，再依建議重寫。", R),
                 "analogy": cite("寫完作文先自己訂正一遍，或請同學幫忙挑毛病，再改出第二版。", R),
                 "points": [cite("評論要看得到原始需求，原始需求優先於評論", R),
                            cite("Self-Refine 在 7 種任務平均進步約 20%", R),
                            cite("數學推理幾乎沒進步：回饋 94% 說看起來都對", R)],
                 "notes": "反思就是多一次呼叫，讓模型當自己的評論者。"}},
    {"id": "s04", "type": "concept", "title": "四種招式一次看", "goal": "地圖", "pages": [A, R], "visual": "patterns",
     "content": {"definition": cite("代理式工作流程：不要求 LLM 一次寫完，而是分多步、多次呼叫，逐步把作品改好。", A),
                 "analogy": cite("像正常人寫作：列大綱、查資料、寫初稿、挑毛病、再修改。", A),
                 "points": [cite("反思、工具使用比較穩定", R), cite("規劃、多代理比較難預測", A)], "notes": "先給大家一張地圖。"}},
    {"id": "s05", "type": "steps", "title": "ReAct：想→做→看", "goal": "懂 ReAct", "pages": [RE], "visual": "react_loop",
     "content": {"steps": [{"label": "想法", "text": "要先知道今天會不會下雨", "cite": [RE]},
                           {"label": "動作", "text": "查天氣[台北]", "cite": [RE]},
                           {"label": "觀察", "text": "降雨機率 80%", "cite": [RE]},
                           {"label": "完成", "text": "機率很高，帶傘出門", "cite": [RE]}],
                 "notes": "這是自編的例子，觀察結果是假設的。"}},
    {"id": "s06", "type": "steps", "title": "麥茶 20 杯夠不夠？", "goal": "懂工具使用", "pages": [T], "visual": "none",
     "content": {"steps": [{"label": "轉成請求", "text": "LLM 把問題變成 JSON：麥茶、20 杯", "cite": [T]},
                           {"label": "程式執行", "text": "Python 查價格，算出 20 × 30 = 600 元", "cite": [T]},
                           {"label": "整理回答", "text": "LLM 依實際結果回答：800 元預算夠用", "cite": [T]}],
                 "notes": "模型只寫請求，真正算錢的是程式。"}},
    {"id": "s07", "type": "compare", "title": "跟團 vs. 自由行", "goal": "工作流程與代理", "pages": [W], "visual": "none",
     "content": {"left": {"heading": "工作流程", "points": [cite("照事先寫好的程式路徑走", W), cite("穩定、可預期", W)]},
                 "right": {"heading": "代理", "points": [cite("LLM 自己決定下一步", W), cite("彈性大，但成本高、錯誤會累積", W)]},
                 "notes": "能簡單就簡單。"}},
    {"id": "s08", "type": "concept", "title": "能簡單就簡單", "goal": "複雜度階梯", "pages": [W], "visual": "ladder",
     "content": {"definition": cite("先試單次呼叫，不夠才加複雜度；代理式系統是用延遲和成本換表現。", W),
                 "analogy": cite("工作流程像跟團，代理像自由行。", W), "points": [], "notes": "階梯由下往上爬。"}},
    {"id": "s09", "type": "steps", "title": "誰決定下一步", "goal": "對照", "pages": [W], "visual": "workflow_agent",
     "content": {"steps": [{"label": "單次呼叫", "text": "很多應用這樣就夠了", "cite": [W]},
                           {"label": "工作流程", "text": "任務能拆成固定步驟時", "cite": [W]},
                           {"label": "代理", "text": "步驟沒辦法事先寫死時", "cite": [W]}], "notes": "三種選擇。"}},
    {"id": "s10", "type": "quiz", "title": "小測驗", "goal": "檢查理解", "pages": [T], "visual": "none",
     "content": {"question": "工具使用時，誰真正去執行程式？", "options": ["LLM 自己", "外部的程式", "使用者", "沒有人"],
                 "answer": 1, "explanation": cite("模型只是寫出呼叫請求，真正執行的是外面的程式。", T), "notes": "先讓大家想一下再揭曉。"}},
    {"id": "s11", "type": "summary", "title": "本章重點", "goal": "總結", "pages": [A, L, H], "visual": "none",
     "content": {"points": [cite("AI 代理是讓模型分多步工作的流程設計", A), cite("能簡單就簡單，複雜度要證明有用才加", A),
                            cite("代理會出包，自評也有盲點", L), cite("AI 做事、人來把關", H)], "notes": "回顧四個重點。"}},
]


def test_checks():
    outline = {"slides": [dict(s) for s in FIXTURE] + [
        {"type": "concept", "title": f"補充{i}", "goal": "g", "pages": [p]} for i, p in enumerate([P, M, L, H], 1)]}
    outline["slides"].append(outline["slides"].pop(10))   # summary 移到最後
    assert checks.check_outline(outline, PAGES) == [], checks.check_outline(outline, PAGES)
    bad = {"slides": [{"type": "intro", "title": "這個標題真的非常非常非常非常非常長喔", "pages": ["nope.md"]}]}
    issues = "\n".join(checks.check_outline(bad, PAGES))
    for expected in ["必須是 15～20 頁", "type「intro」不合法", "標題要 1～16 字", "缺少 goal", "不存在的 Wiki 頁", "第 1 頁必須是 cover",
                     "至少要有 1 頁 quiz", "缺少引用 concepts/reflection.md"]:
        assert expected in issues, expected
    for spec in FIXTURE:
        assert checks.check_slide(spec["content"], spec, PAGES) == [], (spec["id"], checks.check_slide(spec["content"], spec, PAGES))
    concept = dict(FIXTURE[2]["content"], points=[cite("數學推理進步了 96%", R), cite("字" * 50, R), cite("看 ReAct", RE)])
    issues = "\n".join(checks.check_slide(concept, FIXTURE[2], PAGES))
    for expected in ["數字 ['96']", "超過上限 46 字", "不是這頁提供的 Wiki 段落"]:
        assert expected in issues, expected
    quiz = dict(FIXTURE[9]["content"], answer=7)
    assert any("answer" in i for i in checks.check_slide(quiz, FIXTURE[9], PAGES))
    assert checks.check_slide(None, FIXTURE[2], PAGES) == ["整頁缺失或不是 JSON 物件"]
    assert checks.ungrounded_numbers("95.1% 與 4 種模式", [PAGES[A]["plain"]]) == []
    assert checks.width("Self-Refine 提升 20%") == 10   # 英數字算半格：v2 用 len() 誤退件
    assert checks.check_slide(dict(FIXTURE[2]["content"], points=[cite("x" * 50, R)]), FIXTURE[2], PAGES) == []
    crowded = dict(FIXTURE[3]["content"], points=FIXTURE[3]["content"]["points"] + [cite("多代理比較難預測", A)])
    assert "points：要 0～2 點" in checks.check_slide(crowded, FIXTURE[3], PAGES)   # 有圖的 concept 頁最多 2 點


def test_render_helpers():
    cells = render.title_cells("ReAct：想→做→看", 18)
    assert sum(c["span"] for c in cells) == 18 and [c["text"] for c in cells if c["text"]][:2] == ["ReAct", "："]
    assert next(c for c in cells if c["text"] == "ReAct")["span"] == 3
    assert str(render.inline_code("呼叫 `quote_order` <b>")) == "呼叫 <code>quote_order</code> &lt;b&gt;"
    content, refs = render.mark_refs(FIXTURE[3]["content"], PAGES)
    assert refs == [A, R] and content["definition"]["marks"] == "①" and content["points"][0]["marks"] == "②"


def test_graph_builds():
    from . import graph
    assert "check_slides" in graph.build().get_graph().draw_mermaid()
    assert "約 1 行" in graph.overflow_feedback(38) and "約 2 行" in graph.overflow_feedback(41)
    # 平均 0.85 但沒通過評審的頁、超出版面的頁，都要算未通過（v3 以前用平均分數判斷，誤報全部通過）
    graph.CTX["args"] = type("Args", (), {"stop_after_outline": False})()
    state = {"best": {"s04": {"score": 0.85, "passed": False}, "s05": {"score": 0.9, "passed": True}},
             "render_result": {"overflow": {"s13": 9}}}
    assert "2 頁未通過檢查（s04、s13）" in graph.decide_status(state), graph.decide_status(state)
    from . import recheck
    row = "| s04 | concept | 四種招式一次看 | 0.85 | 第 2 輪 | overview.md, concepts/agentic-workflow.md | ✗ |"
    assert recheck.ROW.findall(row) == [("s04", "0.85", "2", "✗")]
    assert recheck.ROW.findall(row[:-4]) == [("s04", "0.85", "2", "")]   # 舊版報告沒有「通過閘門」欄


def preview(out_dir):
    out = render.render_deck(FIXTURE, PAGES, Path(out_dir) / "preview.html", "preview")
    result = render.check_render(out, Path(out_dir) / "shots")
    print("preview:", out, result)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    test_checks()
    test_render_helpers()
    test_graph_builds()
    print("offline tests OK")
    if "--preview" in sys.argv:
        preview(sys.argv[sys.argv.index("--preview") + 1])

"""教學簡報 pipeline（LangGraph）：LangGraph 只管節點和邊；LLM 呼叫在 llm.py，程式檢查在 checks.py。

用法（在專案根目錄）：
  .venv/Scripts/python -m pipeline.graph --graph-only                         只輸出流程圖（不需要 API key）
  .venv/Scripts/python -m pipeline.graph --stop-after-outline                 產生大綱後停下，給人審閱
  .venv/Scripts/python -m pipeline.graph --outline runs/<run-id>/outline.json 用核准的大綱產生簡報
設計依據：wiki/queries/pipeline-design.md
"""
import argparse
import json
import math
import time
from datetime import datetime
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from . import checks, prompts, render, wiki
from .llm import FormatError

ROOT = wiki.ROOT
MAX_OUTLINE_TRIES = 3   # 第一次＋重擬最多 2 次
# v2：撰稿、評審、修改都一次只處理 1 頁。v1 一次寫 3 頁時，15 頁只交回 6 頁（執行 20261113-000549）
EXCERPT_PER_PAGE = 700  # 每個 Wiki 頁最多取幾個字給 LLM
PASS_SCORE = 0.7
CTX = {}                # 不放進 State 的執行環境：args、llm、tracer、pages、run_dir


class State(TypedDict, total=False):
    draft_outline: dict
    outline: list
    outline_issues: list
    outline_tries: int
    excerpts: dict
    slides: dict
    best: dict
    failing: dict
    changed: list
    rounds: int
    render_fix_done: bool
    render_result: dict
    status: str


class Tracer:
    """記錄每個節點的執行、LLM 呼叫、格式錯誤、限流、例外，以及被哪個閘門退件。"""

    def __init__(self, run_dir):
        self.path = Path(run_dir) / "trace.jsonl"
        self.stats, self.rejections = {}, []

    def stat(self, node):
        return self.stats.setdefault(node, {"runs": 0, "seconds": 0.0, "llm_calls": 0, "tokens": 0,
                                            "format_errors": 0, "rate_limited": 0, "exceptions": 0,
                                            "rejected": 0})

    def write(self, **record):
        record["time"] = datetime.now().isoformat(timespec="seconds")
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def node(self, name, seconds, **info):
        s = self.stat(name)
        s["runs"] += 1
        s["seconds"] += seconds
        self.write(kind="node", node=name, seconds=round(seconds, 1), **info)

    def llm_call(self, node, usage, error):
        s = self.stat(node)
        s["llm_calls"] += 1
        s["tokens"] += (usage or {}).get("total_tokens") or 0

    def event(self, node, kind, **info):
        key = {"format_error": "format_errors", "rate_limited": "rate_limited"}.get(kind)
        if key:
            self.stat(node)[key] += 1
        self.write(kind=kind, node=node, **info)

    def rejected(self, producer, gate, details):
        """閘門退件：算在「產生這份內容的節點」頭上。details = {位置: [問題]}。"""
        self.stat(producer)["rejected"] += len(details)
        self.rejections.append({"gate": gate, "producer": producer, "details": details})
        self.write(kind="rejected", node=producer, gate=gate, count=len(details), details=details)


def node(name):
    def wrap(fn):
        def run(state):
            started = time.time()
            try:
                update = fn(state) or {}
            except Exception as exc:
                CTX["tracer"].stat(name)["exceptions"] += 1
                CTX["tracer"].node(name, time.time() - started, error=str(exc)[:500])
                # 存下進入這個節點前的狀態，之後用 --resume 從這裡續跑，不必從頭來（Anthropic 2025）
                save_json("resume.json", {"next": name, "state": state})
                raise
            CTX["tracer"].node(name, time.time() - started, info=update.pop("_info", None))
            return update
        run.__name__ = name
        return run
    return wrap


def save_json(name, data):
    path = CTX["run_dir"] / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def spec_view(spec):
    return {k: spec[k] for k in ("id", "type", "title", "goal", "pages", "visual") if k in spec}


def bundle(specs, excerpts, extra=None):
    """組合給撰稿／評審／修改節點的資料包：每頁的規格、Wiki 段落，以及額外資料。"""
    parts = []
    for spec in specs:
        block = f"=== 投影片 {spec['id']} ===\n【投影片規格】\n{json.dumps(spec_view(spec), ensure_ascii=False)}\n"
        if spec.get("type") in ("concept", "steps") and spec.get("visual") in prompts.FIGURE_NOTES:
            block += f"【這頁的圖】{prompts.FIGURE_NOTES[spec['visual']]}\n"
        block += f"【Wiki 段落】\n{excerpts.get(spec['id']) or '（這頁不需要 Wiki 段落）'}\n"
        for label, values in (extra or {}).items():
            block += f"【{label}】\n{values.get(spec['id'], '（無）')}\n"
        parts.append(block)
    return "\n".join(parts)


def producer_of(state):
    return "draft_slides" if state.get("rounds", 0) == 0 else "revise_slides"


@node("load_wiki")
def load_wiki(state):
    errors, warns, gaps = wiki.lint()
    CTX["pages"] = wiki.load_pages()
    info = {"lint_errors": len(errors), "lint_warnings": len(warns), "gaps": len(gaps), "pages": len(CTX["pages"])}
    if errors:
        return {"status": "Wiki 健檢有錯誤，停止生成：" + "；".join(errors[:5]), "_info": info}
    if CTX.get("resume"):
        return {**CTX["resume"]["state"], "_info": dict(info, resume_at=CTX["resume"]["next"])}
    if CTX.get("approved_outline"):
        return {"outline": CTX["approved_outline"], "_info": info}
    return {"_info": info}


@node("plan_outline")
def plan_outline(state):
    user = "【Wiki 目錄】\n" + wiki.index_for_planner()
    if state.get("outline_issues"):
        user += "\n\n【上一版大綱沒有通過檢查，請全部修正後重新輸出完整大綱】\n"
        user += "\n".join(f"- {issue}" for issue in state["outline_issues"])
    data = CTX["llm"].ask_json("plan_outline", prompts.PLANNER, user, max_tokens=3000)
    return {"draft_outline": data, "outline_tries": state.get("outline_tries", 0) + 1}


@node("check_outline")
def check_outline(state):
    draft = state.get("draft_outline")
    issues = checks.check_outline(draft, CTX["pages"])
    save_json(f"outline_try{state.get('outline_tries', 0)}.json", {"draft": draft, "issues": issues})
    if issues:
        CTX["tracer"].rejected("plan_outline", "大綱閘門", {"outline": issues})
        return {"outline_issues": issues, "_info": {"issues": len(issues)}}
    slides = [dict(s, id=f"s{i:02d}", visual=s.get("visual", "none"))
              for i, s in enumerate(draft["slides"], 1)]
    save_json("outline.json", {"slides": slides})
    return {"outline": slides, "outline_issues": [], "_info": {"slides": len(slides)}}


@node("retrieve")
def retrieve(state):
    pages = CTX["pages"]
    excerpts = {s["id"]: "\n\n".join(wiki.excerpt(pages, p, EXCERPT_PER_PAGE) for p in s.get("pages", []))
                for s in state["outline"]}
    return {"excerpts": excerpts, "_info": {"chars": sum(len(v) for v in excerpts.values())}}


def write_slide(node_name, system, spec, state, extra=None):
    """撰稿或修改一頁（strict JSON Schema）。格式仍失敗就回傳 None：記成缺頁交給閘門，不讓整條流程中止（v2）。"""
    try:
        return CTX["llm"].ask_json(node_name, system, bundle([spec], state["excerpts"], extra),
                                   schema=prompts.slide_schema(spec["type"], spec.get("pages", [])))
    except FormatError:
        CTX["tracer"].event(node_name, "slide_missing", slide=spec["id"])
        return None


@node("draft_slides")
def draft_slides(state):
    slides = {spec["id"]: write_slide("draft_slides", prompts.WRITER, spec, state) for spec in state["outline"]}
    slides = {sid: s for sid, s in slides.items() if s is not None}
    return {"slides": slides, "rounds": 0, "best": {}, "_info": {"written": len(slides)}}


def judge(sid, state, outline):
    """LLM 評審一頁：一次呼叫依評分規準打分；回傳（平均分數, 是否通過, 問題清單）。"""
    user = bundle([outline[sid]], state["excerpts"],
                  {"待審查的投影片": {sid: json.dumps(state["slides"][sid], ensure_ascii=False)}})
    try:
        review = CTX["llm"].ask_json("check_slides", prompts.JUDGE, user, max_tokens=2000, schema=prompts.JUDGE_SCHEMA)
    except FormatError:
        CTX["tracer"].event("check_slides", "judge_missing", slide=sid)
        return PASS_SCORE, True, []
    raw = review.get("scores") if isinstance(review.get("scores"), dict) else {}
    scores = [min(max(float(raw.get(k, 0) or 0), 0.0), 1.0) for k in ("faithful", "citation", "clarity", "goal")]
    ok = review.get("pass") is True and min(scores) >= PASS_SCORE
    issues = [f"{i.get('where', '?')}：{i.get('problem', '')} → 建議：{i.get('fix', '')}"
              for i in review.get("issues", []) if isinstance(i, dict)]
    return round(sum(scores) / 4, 3), ok, issues or ([] if ok else ["評審分數未達 0.7，請依規格與 Wiki 段落改寫"])


@node("check_slides")
def check_slides(state):
    pages, outline = CTX["pages"], {s["id"]: s for s in state["outline"]}
    rounds = state.get("rounds", 0)
    # 第 0 輪檢查全部；之後只重審這輪改過的頁，沒改到的頁沿用上一輪的問題（省 token）
    targets = list(outline) if rounds == 0 else [sid for sid in state.get("changed", []) if sid in outline]
    failing = {} if rounds == 0 else {sid: v for sid, v in state.get("failing", {}).items() if sid not in targets}
    best, to_judge, scores, passed = dict(state.get("best", {})), [], {}, {}
    for sid in targets:
        spec = outline[sid]
        problems = checks.check_slide(state["slides"].get(sid), spec, pages)
        if problems:
            failing[sid] = problems
            scores[sid], passed[sid] = 0.0, False
        else:
            to_judge.append(sid)
    for sid in to_judge:
        scores[sid], passed[sid], issues = judge(sid, state, outline)
        if not passed[sid]:
            failing[sid] = issues
    # 保留最好的版本（Self-Refine：可能越改越差）：先比有沒有通過閘門，再比分數。
    # v3 以前只比平均分數，s04 平均 0.85 但 goal 0.6 沒通過，仍被當成通過（執行 20261113-024148）
    for sid, score in scores.items():
        old = best.get(sid)
        if sid in state["slides"] and (old is None or (passed[sid], score) >= (old.get("passed", False), old["score"])):
            best[sid] = {"slide": state["slides"][sid], "score": score, "passed": passed[sid], "round": rounds}
    if failing:
        CTX["tracer"].rejected(producer_of(state), "投影片閘門", failing)
    save_json(f"check_round{rounds}.json", {"checked": targets, "scores": scores, "failing": failing})
    return {"failing": failing, "best": best, "changed": [],
            "_info": {"round": rounds, "checked": len(targets), "judged": len(to_judge), "failing": len(failing)}}


@node("revise_slides")
def revise_slides(state):
    outline = {s["id"]: s for s in state["outline"]}
    slides, changed = dict(state["slides"]), set(state.get("changed", []))
    for sid, issues in state["failing"].items():
        extra = {"目前的投影片": {sid: json.dumps(slides.get(sid), ensure_ascii=False)},
                 "審查意見": {sid: "\n".join(f"- {i}" for i in issues)}}
        revised = write_slide("revise_slides", prompts.REVISER, outline[sid], state, extra)
        if revised is not None:
            slides[sid] = revised
            changed.add(sid)
    return {"slides": slides, "changed": sorted(changed), "rounds": state.get("rounds", 0) + 1,
            "_info": {"revised": sorted(changed)}}


def final_slides(state):
    best = state.get("best", {})
    return [dict(spec, content=(best[spec["id"]]["slide"] if spec["id"] in best else state.get("slides", {}).get(spec["id"])))
            for spec in state["outline"]]


@node("render_html")
def render_html(state):
    slides = final_slides(state)
    save_json("final_slides.json", {"run_id": CTX["run_id"], "slides": slides})
    path = render.render_deck(slides, CTX["pages"], ROOT / "docs" / "slides" / "index.html", CTX["run_id"])
    return {"_info": {"path": str(path.relative_to(ROOT))}}


def overflow_feedback(px):
    """把「超出幾 px」換成模型做得到的刪減量（內文一行約 40px、約 25 字）。v2 只說超出幾 px，s13 改了一輪還是超出。"""
    lines = math.ceil(px / 40)
    return f"版面：內容超出投影片 {px}px（約 {lines} 行），請刪掉 1 個要點，或把文字合計縮短約 {lines * 25} 字（不要刪掉 cite）"


@node("check_render")
def check_render(state):
    result = render.check_render(ROOT / "docs" / "slides" / "index.html", CTX["run_dir"] / "shots")
    save_json(f"render_check{'_fix' if state.get('render_fix_done') else ''}.json", result)
    overflow = result.get("overflow", {})
    # 版面放不下的版本不能當「最佳版本」：分數歸零，改寫後的版本只要通過閘門就會取代它
    best = {sid: (dict(b, score=0.0, passed=False) if sid in overflow else b) for sid, b in state.get("best", {}).items()}
    if overflow and not state.get("render_fix_done"):
        failing = {sid: [overflow_feedback(px)] for sid, px in overflow.items()}
        CTX["tracer"].rejected(producer_of(state), "版面閘門", failing)
        return {"failing": failing, "best": best, "render_fix_done": True, "render_result": result,
                "_info": {"overflow": overflow}}
    return {"failing": {}, "best": best, "render_result": result,
            "_info": {"overflow": overflow, "console_errors": len(result.get("console_errors", [])),
                      "small_screen": result.get("small_screen", {})}}


@node("finalize")
def finalize(state):
    status = state.get("status") or decide_status(state)
    write_report(state, status)
    return {"status": status}


def decide_status(state):
    if state.get("outline_issues"):
        return f"大綱連續 {state.get('outline_tries')} 次沒通過大綱閘門，停止並交給人處理"
    if CTX["args"].stop_after_outline:
        return "大綱通過閘門，等待人工審閱"
    unresolved = {sid for sid, b in state.get("best", {}).items() if not b.get("passed")}
    unresolved |= set(state.get("render_result", {}).get("overflow", {}))
    small = state.get("render_result", {}).get("small_screen")
    if small:   # 模板的問題，改投影片內容修不好，交給人改模板
        return f"簡報已產生，但小螢幕版面錯位（{'、'.join(small)}），需要人工修模板"
    if unresolved:
        return f"簡報已產生，但有 {len(unresolved)} 頁未通過檢查（{'、'.join(sorted(unresolved))}），需人工處理"
    return "簡報已產生，全部頁面通過三個閘門"


def after_load(state):
    if state.get("status"):
        return "finalize"
    if CTX.get("resume"):
        return CTX["resume"]["next"]
    return "retrieve" if state.get("outline") else "plan_outline"


def after_outline(state):
    if state.get("outline_issues"):
        return "plan_outline" if state.get("outline_tries", 0) < MAX_OUTLINE_TRIES else "finalize"
    return "finalize" if CTX["args"].stop_after_outline else "retrieve"


def after_slides(state):
    return "revise_slides" if state.get("failing") and state.get("rounds", 0) < CTX["args"].max_rounds else "render_html"


def after_render(state):
    return "revise_slides" if state.get("failing") else "finalize"


def build():
    g = StateGraph(State)
    for fn in (load_wiki, plan_outline, check_outline, retrieve, draft_slides, check_slides,
               revise_slides, render_html, check_render, finalize):
        g.add_node(fn.__name__, fn)
    g.add_edge(START, "load_wiki")
    g.add_conditional_edges("load_wiki", after_load, ["plan_outline", "retrieve", "draft_slides", "check_slides",
                                                      "revise_slides", "render_html", "check_render", "finalize"])
    g.add_edge("plan_outline", "check_outline")
    g.add_conditional_edges("check_outline", after_outline, ["plan_outline", "retrieve", "finalize"])
    g.add_edge("retrieve", "draft_slides")
    g.add_edge("draft_slides", "check_slides")
    g.add_conditional_edges("check_slides", after_slides, ["revise_slides", "render_html"])
    g.add_edge("revise_slides", "check_slides")
    g.add_edge("render_html", "check_render")
    g.add_conditional_edges("check_render", after_render, ["revise_slides", "finalize"])
    g.add_edge("finalize", END)
    return g.compile()


def write_report(state, status):
    """runs/<run-id>/report.md：各節點統計、閘門退件紀錄、最終投影片；同時回存 Wiki（Query 流程）。"""
    tracer, run_id = CTX["tracer"], CTX["run_id"]
    seconds = time.time() - CTX["started"]
    lines = [f"# 執行紀錄 {run_id}", "",
             f"- 模式：{'只產生大綱（等待人工審閱）' if CTX['args'].stop_after_outline else '產生完整簡報'}"
             + (f"；從 {CTX['resume']['from']} 的 {CTX['resume']['next']} 節點續跑" if CTX.get("resume") else ""),
             f"- 結果：{status}",
             f"- 總耗時：{seconds / 60:.1f} 分鐘；LLM 呼叫 {sum(s['llm_calls'] for s in tracer.stats.values())} 次；"
             f"token 約 {sum(s['tokens'] for s in tracer.stats.values()):,}",
             "", "## 各節點統計", "",
             "| 節點 | 執行次數 | LLM 呼叫 | token | 格式錯誤 | 限流等待 | 例外 | 被閘門退件 | 耗時（秒） |",
             "|---|---|---|---|---|---|---|---|---|"]
    for name, s in tracer.stats.items():
        lines.append(f"| {name} | {s['runs']} | {s['llm_calls']} | {s['tokens']:,} | {s['format_errors']} | "
                     f"{s['rate_limited']} | {s['exceptions']} | {s['rejected']} | {s['seconds']:.0f} |")
    lines += ["", "「被閘門退件」算在產生那份內容的節點頭上（大綱 → plan_outline；投影片 → draft_slides 或 revise_slides）。",
              "", "## 閘門退件紀錄", ""]
    for i, r in enumerate(tracer.rejections, 1):
        lines.append(f"### {i}. {r['gate']}（產生者：{r['producer']}）")
        for where, issues in r["details"].items():
            lines += [f"- **{where}**"] + [f"  - {issue}" for issue in issues]
        lines.append("")
    if not tracer.rejections:
        lines.append("（沒有退件）")
    if state.get("outline"):
        lines += ["", "## 投影片", "", "| id | 類型 | 標題 | 最終分數 | 採用的版本 | 引用的 Wiki 頁 | 通過閘門 |",
                  "|---|---|---|---|---|---|---|"]
        for spec in state["outline"]:
            b = state.get("best", {}).get(spec["id"])
            lines.append(f"| {spec['id']} | {spec['type']} | {spec['title']} | {b['score'] if b else '-'} | "
                         f"{('第 %d 輪' % b['round']) if b else '-'} | {', '.join(spec.get('pages', []))} | "
                         f"{('✓' if b.get('passed') else '✗') if b else '-'} |")
    lines += ["", "## 流程圖", "", "```mermaid", build().get_graph().draw_mermaid(), "```"]
    (CTX["run_dir"] / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (CTX["run_dir"] / "stats.json").write_text(json.dumps(tracer.stats, ensure_ascii=False, indent=2), encoding="utf-8")
    log_lines = [status, f"執行紀錄：[runs/{run_id}/report.md](../runs/{run_id}/report.md)"]
    if CTX["args"].stop_after_outline and state.get("outline"):
        rows = "\n".join(f"| {s['id']} | {s['type']} | {s['title']} | {s['goal']} | {'、'.join(s.get('pages', [])) or '—'} |"
                         for s in state["outline"])
        body = (f"> 由簡報 pipeline（{run_id}）查詢 Wiki 目錄後產生，通過大綱閘門，等待作者審閱。\n\n"
                "| id | 類型 | 標題 | 這頁的目標 | 引用的 Wiki 頁 |\n|---|---|---|---|---|\n" + rows)
        rel = wiki.file_query_page("slide-outline", "查詢｜教學簡報大綱", "pipeline 產生的大綱：每頁對應哪些 Wiki 頁", body)
        log_lines.append(f"大綱回存：[{rel}]({rel})")
    wiki.append_log(f"query | 教學簡報 pipeline（{run_id}）", log_lines)


def main():
    parser = argparse.ArgumentParser(description="用 LLM Wiki 產生教學 HTML 簡報（LangGraph + Groq）")
    parser.add_argument("--stop-after-outline", action="store_true", help="大綱通過閘門後就停下，給人審閱")
    parser.add_argument("--outline", help="已核准的大綱 JSON，跳過擬大綱")
    parser.add_argument("--max-rounds", type=int, default=2, help="投影片最多改寫幾輪")
    parser.add_argument("--graph-only", action="store_true", help="只輸出 Mermaid 流程圖")
    parser.add_argument("--render-only", metavar="RUN_DIR", help="用某次執行的 final_slides.json 重新套模板並過版面閘門（不呼叫 LLM）")
    parser.add_argument("--resume", metavar="RUN_DIR", help="從某次執行失敗的節點續跑（讀 RUN_DIR/resume.json）")
    args = parser.parse_args()
    CTX["args"] = args
    if args.resume:
        CTX["resume"] = dict(json.loads((Path(args.resume) / "resume.json").read_text(encoding="utf-8")),
                             **{"from": Path(args.resume).name})
    if args.render_only:   # 換模板或連結後重新輸出；照樣過版面閘門，結果另存，不蓋掉原本的紀錄
        run = Path(args.render_only)
        saved = json.loads((run / "final_slides.json").read_text(encoding="utf-8"))
        out = render.render_deck(saved["slides"], wiki.load_pages(), ROOT / "docs" / "slides" / "index.html", saved["run_id"])
        result = render.check_render(out, run / "shots_rerender")
        (run / "render_check_rerender.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        ok = not result["overflow"] and not result["console_errors"] and not result["small_screen"]
        print(f"已重新輸出 {out.relative_to(ROOT)}；版面閘門：{'通過' if ok else result}")
        return
    if args.graph_only:
        out = ROOT / "docs" / "pipeline-graph.mmd"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build().get_graph().draw_mermaid(), encoding="utf-8")
        print(f"流程圖已寫入 {out.relative_to(ROOT)}")
        return
    from .llm import LLM  # 需要 API key，放在這裡讓 --graph-only 不需要金鑰
    CTX["run_id"] = datetime.now().strftime("%Y%m%d-%H%M%S")
    CTX["run_dir"] = ROOT / "runs" / CTX["run_id"]
    CTX["started"] = time.time()
    CTX["tracer"] = Tracer(CTX["run_dir"])
    CTX["llm"] = LLM(CTX["run_dir"], CTX["tracer"])   # 先確認金鑰，再建立 runs/<run-id>/
    if args.outline:
        CTX["approved_outline"] = json.loads(Path(args.outline).read_text(encoding="utf-8"))["slides"]
    state = {}
    try:
        for state in build().stream({}, stream_mode="values", config={"recursion_limit": 60}):
            pass
    except Exception as exc:   # 任何節點失敗：照樣寫出紀錄，停在哪裡一目瞭然
        write_report(state, f"失敗：{str(exc)[:300]}")
        raise
    print(f"\n{state.get('status')}\n執行紀錄：runs/{CTX['run_id']}/report.md")


if __name__ == "__main__":
    main()

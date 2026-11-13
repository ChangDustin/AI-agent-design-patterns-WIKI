"""程式檢查（閘門）：大綱閘門與投影片閘門裡「程式能確認的事情交給程式」的部分。"""
import re

TYPES = {"cover", "hook", "concept", "steps", "compare", "quiz", "summary"}
VISUALS = {"none", "patterns", "ladder", "react_loop", "workflow_agent"}
REQUIRED_PAGES = [
    "concepts/reflection.md", "concepts/tool-use.md", "concepts/planning.md",
    "concepts/multi-agent-collaboration.md", "concepts/workflow-vs-agent.md",
    "concepts/agent-limitations.md", "concepts/human-in-the-loop.md",
]
# 字數上限（用 width() 計算：中文 1、英數 0.5），模板版面依這些上限設計
LIMITS = {"title": 16, "subtitle": 30, "point": 46, "step_label": 10, "step": 46, "heading": 10,
          "compare_point": 40, "definition": 60, "analogy": 60, "stat_value": 8, "stat_label": 20,
          "question": 50, "option": 24, "explanation": 60, "notes": 220}
NUMBER = re.compile(r"\d+(?:\.\d+)?")
FIGURE_POINTS = 2   # 有圖的 concept 頁：便利貼擠到左欄，要點最多 2 點（v3：版面閘門在 s04、s13 量到超出後提前到這裡檢查）


def width(text):
    """版面寬度：中文字和全形標點算 1，英數字和半形符號算 0.5（字型裡半形字約佔半格）。
    v2 用 len() 把英數字也算 1，s05、s08 版面排得下卻被判超過上限（執行 20261113-002929）。"""
    return sum(0.5 if ord(ch) < 0x2E80 else 1 for ch in text)


def check_outline(outline, pages):
    """回傳問題清單；空清單代表大綱通過閘門。"""
    slides = outline.get("slides") if isinstance(outline, dict) else None
    if not isinstance(slides, list) or not slides:
        return ['大綱必須是 {"slides": [...]} 而且不能是空的']
    issues, titles, cited = [], set(), set()
    if not 15 <= len(slides) <= 20:
        issues.append(f"目前 {len(slides)} 頁，必須是 15～20 頁")
    for i, s in enumerate(slides, 1):
        tag = f"第 {i} 頁"
        if not isinstance(s, dict):
            issues.append(f"{tag} 必須是物件")
            continue
        if s.get("type") not in TYPES:
            issues.append(f"{tag} 的 type「{s.get('type')}」不合法，只能是 {sorted(TYPES)}")
        title = s.get("title")
        if not isinstance(title, str) or not 0 < len(title) <= LIMITS["title"]:
            issues.append(f"{tag} 的標題要 1～{LIMITS['title']} 字")
        elif title in titles:
            issues.append(f"{tag} 的標題「{title}」重複了")
        titles.add(title)
        if not isinstance(s.get("goal"), str) or not s["goal"].strip():
            issues.append(f"{tag} 缺少 goal")
        if s.get("visual", "none") not in VISUALS:
            issues.append(f"{tag} 的 visual 只能是 {sorted(VISUALS)}")
        refs = s.get("pages", [])
        if not isinstance(refs, list) or (s.get("type") != "cover" and not 1 <= len(refs) <= 3):
            issues.append(f"{tag} 的 pages 要列 1～3 個 Wiki 頁")
            continue
        for ref in refs:
            if ref not in pages:
                issues.append(f"{tag} 引用了不存在的 Wiki 頁「{ref}」")
            else:
                cited.add(ref)
    types = [s.get("type") for s in slides if isinstance(s, dict)]
    if types[:1] != ["cover"]:
        issues.append("第 1 頁必須是 cover")
    if types[-1:] != ["summary"]:
        issues.append("最後一頁必須是 summary")
    if "quiz" not in types:
        issues.append("至少要有 1 頁 quiz")
    issues += [f"缺少引用 {ref} 的投影片" for ref in REQUIRED_PAGES if ref not in cited]
    return issues


def ungrounded_numbers(text, page_texts):
    """回傳文字中「在被引用的 Wiki 頁裡找不到」的數字。
    shortcut: 個位數整數（序號、幾種、幾頁）不檢查，子字串比對也可能放過 45 vs 245；要更嚴再改成詞界比對。"""
    corpus = "\n".join(page_texts).replace(",", "")
    return [n for n in NUMBER.findall(text.replace(",", ""))
            if ("." in n or int(n) >= 10) and n not in corpus]


def _text_issues(where, value, limit, allowed, pages, need_cite=True):
    """檢查一個 {"text", "cite"} 欄位。"""
    if not isinstance(value, dict) or not isinstance(value.get("text"), str) or not value["text"].strip():
        return [f"{where}：缺少文字（要寫成 {{\"text\": ..., \"cite\": [...]}}）"]
    issues, text = [], value["text"]
    if width(text) > limit:
        # 模型數不準字數：給一個比上限少 2 成的明確目標，而不是只說「超過了」（Self-Refine：回饋要可行動）
        issues.append(f"{where}：{width(text):g} 字，超過上限 {limit} 字，請改寫到 {int(limit * 0.8)} 字以內"
                      "（刪掉修飾語或次要資訊，保留重點）")
    cites = value.get("cite")
    if need_cite:
        if not isinstance(cites, list) or not 1 <= len(cites) <= 2:
            return issues + [f"{where}：cite 要列 1～2 個 Wiki 頁"]
        bad = [c for c in cites if c not in allowed]
        if bad:
            issues.append(f"{where}：cite {bad} 不是這頁提供的 Wiki 段落，只能用 {sorted(allowed)}")
        texts = [pages[c]["plain"] for c in cites if c in pages and c in allowed]
        missing = ungrounded_numbers(text, texts)
        if missing:
            issues.append(f"{where}：數字 {missing} 在引用的 Wiki 頁裡找不到，請改成 Wiki 裡的數字或拿掉")
    return issues


def check_slide(slide, spec, pages):
    """回傳問題清單；空清單代表通過程式檢查（之後才送 LLM 評審）。"""
    if not isinstance(slide, dict):
        return ["整頁缺失或不是 JSON 物件"]
    allowed = set(spec.get("pages", []))
    issues = []   # 標題一律用大綱（人核准過）的標題，不檢查投影片 JSON 裡的 title
    notes = slide.get("notes")
    if not isinstance(notes, str) or not notes.strip() or len(notes) > LIMITS["notes"]:
        issues.append(f"notes：講者備註要有內容，最多 {LIMITS['notes']} 字")
    kind = spec.get("type")

    def items(field, low, high, limit, where_prefix=None):
        values = slide.get(field)
        if not isinstance(values, list) or not low <= len(values) <= high:
            return [f"{field}：要 {low}～{high} 點"]
        out = []
        for i, v in enumerate(values):
            out += _text_issues(f"{where_prefix or field}[{i}]", v, limit, allowed, pages)
        return out

    if kind == "cover":
        sub = slide.get("subtitle")
        if not isinstance(sub, str) or not 0 < width(sub) <= LIMITS["subtitle"]:
            issues.append(f"subtitle：要 1～{LIMITS['subtitle']} 字")
    elif kind == "hook":
        stats = slide.get("stats")
        if not isinstance(stats, list) or not 1 <= len(stats) <= 3:
            issues.append("stats：要 1～3 個數據")
        else:
            for i, s in enumerate(stats):
                if not isinstance(s, dict) or not isinstance(s.get("value"), str) or not isinstance(s.get("label"), str):
                    issues.append(f"stats[{i}]：要有 value 和 label")
                    continue
                if width(s["value"]) > LIMITS["stat_value"] or width(s["label"]) > LIMITS["stat_label"]:
                    issues.append(f"stats[{i}]：value 最多 {LIMITS['stat_value']} 字、label 最多 {LIMITS['stat_label']} 字")
                issues += _text_issues(f"stats[{i}]", {"text": s["value"] + " " + s["label"], "cite": s.get("cite")},
                                       LIMITS["stat_value"] + LIMITS["stat_label"] + 1, allowed, pages)
        issues += _text_issues("takeaway", slide.get("takeaway"), LIMITS["point"], allowed, pages)
    elif kind == "concept":
        issues += _text_issues("definition", slide.get("definition"), LIMITS["definition"], allowed, pages)
        issues += _text_issues("analogy", slide.get("analogy"), LIMITS["analogy"], allowed, pages)
        issues += items("points", 0, FIGURE_POINTS if spec.get("visual", "none") != "none" else 3, LIMITS["point"])
    elif kind == "steps":
        steps = slide.get("steps")
        if not isinstance(steps, list) or not 3 <= len(steps) <= 5:
            issues.append("steps：要 3～5 步")
        else:
            for i, s in enumerate(steps):
                label = s.get("label") if isinstance(s, dict) else None
                if not isinstance(label, str) or not 0 < width(label) <= LIMITS["step_label"]:
                    issues.append(f"steps[{i}].label：要 1～{LIMITS['step_label']} 字")
                issues += _text_issues(f"steps[{i}]", s, LIMITS["step"], allowed, pages)
    elif kind == "compare":
        for side in ("left", "right"):
            box = slide.get(side)
            if not isinstance(box, dict):
                issues.append(f"{side}：缺少")
                continue
            heading = box.get("heading")
            if not isinstance(heading, str) or not 0 < width(heading) <= LIMITS["heading"]:
                issues.append(f"{side}.heading：要 1～{LIMITS['heading']} 字")
            points = box.get("points")
            if not isinstance(points, list) or not 1 <= len(points) <= 3:
                issues.append(f"{side}.points：要 1～3 點")
            else:
                for i, p in enumerate(points):
                    issues += _text_issues(f"{side}.points[{i}]", p, LIMITS["compare_point"], allowed, pages)
    elif kind == "quiz":
        q, options, answer = slide.get("question"), slide.get("options"), slide.get("answer")
        if not isinstance(q, str) or not 0 < width(q) <= LIMITS["question"]:
            issues.append(f"question：要 1～{LIMITS['question']} 字")
        if not isinstance(options, list) or not 3 <= len(options) <= 4 or \
                not all(isinstance(o, str) and 0 < width(o) <= LIMITS["option"] for o in options):
            issues.append(f"options：要 3～4 個選項，每個 1～{LIMITS['option']} 字")
        elif type(answer) is not int or not 0 <= answer < len(options):
            issues.append("answer：要是正確選項的索引（從 0 開始的整數）")
        issues += _text_issues("explanation", slide.get("explanation"), LIMITS["explanation"], allowed, pages)
        quiz_text = (q or "") + " ".join(o for o in options or [] if isinstance(o, str))
        missing = ungrounded_numbers(quiz_text, [pages[p]["plain"] for p in allowed if p in pages])
        if missing:
            issues.append(f"question/options：數字 {missing} 在這頁的 Wiki 段落裡找不到")
    elif kind == "summary":
        issues += items("points", 3, 5, LIMITS["point"])
    else:
        issues.append(f"type「{kind}」不支援")
    return issues

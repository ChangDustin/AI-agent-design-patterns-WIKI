# 用 LLM Wiki 做教學簡報：AI 代理設計模式

先用 Karpathy 的 **LLM Wiki** 模式，把 7 篇資料整理成一個會持續累積的知識庫；再用一條 **LangGraph 流程**，把 Wiki 當知識來源，產生給非資工大學生看的教學 HTML 簡報。每一頁投影片都標出依據的 Wiki 頁。

**線上看（GitHub Pages）**：[繳交首頁](https://changdustin.github.io/AI-agent-design-patterns-WIKI/)、[教學簡報](https://changdustin.github.io/AI-agent-design-patterns-WIKI/slides/)

| 成果 | 位置 |
|---|---|
| **繳交首頁**（六項繳交內容整理在一頁） | [`docs/index.html`](docs/index.html)（GitHub Pages 首頁） |
| LLM Wiki | [`wiki/`](wiki/index.md)（從目錄 `index.md` 開始看） |
| 教學 HTML 簡報 | [`docs/slides/index.html`](docs/slides/index.html) |
| loop／graph 設計 | [`wiki/queries/pipeline-design.md`](wiki/queries/pipeline-design.md)、程式在 [`pipeline/`](pipeline/README.md) |
| 實際執行與檢查紀錄 | [`runs/`](runs/) |
| 「先討論、後生成」的討論紀錄 | [`discussions/`](discussions/) |

## 1. LLM Wiki

主題是 **AI 代理設計模式**：反思、工具使用、規劃、多代理協作，以及「工作流程 vs. 代理」怎麼選。

依照 Karpathy〈LLM Wiki〉（2026-04-04）的三層架構：

| 層 | 位置 | 說明 |
|---|---|---|
| 原始資料 | `raw/` | 7 篇資料，唯讀。原文有著作權，不上傳；[`raw/README.md`](raw/README.md) 記錄出處 |
| Wiki | `wiki/` | 由 LLM（Claude Code）撰寫與維護：來源頁、概念頁、人物／工具頁、總覽、目錄、日誌 |
| 規則書（schema） | [`CLAUDE.md`](CLAUDE.md) | 頁面格式、引用規則，以及 Ingest／Query／Lint 三種操作的流程 |

**先討論、後生成**：每篇資料 ingest 前，LLM 先在 `discussions/` 寫提案（重點、要新增或修改的頁、和既有內容的衝突、要問作者的問題），作者回覆後才寫入 Wiki。7 篇資料共 7 輪討論，加上一輪簡報大綱審閱。

**三種操作都實際用過**：

- **Ingest**：7 篇，依序是 Ng、Anthropic、Weng、ReAct、Self-Refine、Anthropic 多代理、課程 notebook。
- **Lint**：[`tools/wiki_lint.py`](tools/wiki_lint.py) 檢查斷鏈、孤兒頁、缺段落、缺出處；每篇 ingest 後跑一次，最後再加一次人工語意健檢。
- **Query**：「根據 Wiki，簡報 pipeline 該怎麼設計？」的答案回存成 [`wiki/queries/pipeline-design.md`](wiki/queries/pipeline-design.md)。每次 pipeline 執行也算一次 Query，會記進 [`wiki/log.md`](wiki/log.md)。

## 2. 簡報 pipeline 與執行結果

流程是「帶閘門的提示鏈＋評估者—優化者迴圈」：擬大綱 →〔大綱閘門〕→ 人審大綱 → 一次寫 1 頁 →〔投影片閘門：程式檢查 → LLM 評審〕→ 只改不合格的頁（最多 2 輪）→ 套模板 →〔版面閘門：瀏覽器實測〕→ 執行紀錄。流程圖和設計理由見 [`docs/index.html`](docs/index.html#flow) 與 [`pipeline-design.md`](wiki/queries/pipeline-design.md)。

| 執行 | 版本 | 結果 |
|---|---|---|
| [000224](runs/20261113-000224/report.md) | v1 | 大綱閘門退件 1 次後通過，停下給人審（[討論 08](discussions/08-slide-outline-review.md)） |
| [000549](runs/20261113-000549/report.md) | v1 | 失敗：一次寫 3 頁，15 頁只交回 6 頁 |
| [001206](runs/20261113-001206/report.md) | v2 | 中止：網路斷線（之前退件以字數超過為主） |
| [002929](runs/20261113-002929/report.md) | v2 | 續跑完成，4 頁被標記 |
| [024148](runs/20261113-024148/report.md) | v3 | 修好閘門後重審 3 頁；報告誤報全部通過（已附更正） |
| [024626](runs/20261113-024626/report.md) | v3 | **18 頁全部通過三個閘門**（目前的簡報） |

每次修改的原因和證據記在 [`pipeline-design.md`](wiki/queries/pipeline-design.md) 的「v1 → v2」「v2」「v2 → v3」三節，反思整理在 [`docs/index.html`](docs/index.html#reflection)。

## 3. 重現方式

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```

把 `.env.example` 複製成 `.env`，填入自己的 Groq API key，再依 [`pipeline/README.md`](pipeline/README.md) 執行。

## 4. 目錄結構

```
CLAUDE.md        Wiki 規則書（schema）
raw/             原始資料（只上傳出處清單）
wiki/            LLM Wiki：index.md、log.md、overview.md、sources/、concepts/、entities/、queries/
discussions/     每篇資料 ingest 前的討論紀錄
tools/           wiki_lint.py（Wiki 健檢）
pipeline/        LangGraph＋Groq 簡報流程
runs/            每次執行的紀錄：report.md、trace.jsonl、每次 LLM 呼叫的完整 prompt 與回應、每頁截圖
docs/            GitHub Pages：繳交首頁 index.html、簡報 slides/、流程圖
```

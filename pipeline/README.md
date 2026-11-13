# 教學簡報 pipeline（LangGraph＋Groq）

把 `wiki/` 當知識庫，產生 `docs/slides/index.html`。設計依據見 [wiki/queries/pipeline-design.md](../wiki/queries/pipeline-design.md)。

## 準備

1. 安裝套件：`python -m venv .venv`，再執行 `.venv/Scripts/python -m pip install -r requirements.txt`
2. 複製 `.env.example` 成 `.env`，在 `GROQ_API_KEY=` 後面填入自己的金鑰（`.env` 不會上傳）
3. 版面檢查用 Windows 內建的 Edge（Playwright 的 `channel="msedge"`），不必另外下載瀏覽器

## 執行（在專案根目錄）

| 指令 | 做什麼 |
|---|---|
| `.venv/Scripts/python -m pipeline.test_offline` | 離線自我測試，不需要金鑰 |
| `.venv/Scripts/python -m pipeline.graph --graph-only` | 輸出流程圖 `docs/pipeline-graph.mmd` |
| `.venv/Scripts/python -m pipeline.graph --stop-after-outline` | 擬大綱、通過大綱閘門後停下；大綱回存 `wiki/queries/slide-outline.md` 給人審閱 |
| `.venv/Scripts/python -m pipeline.graph --outline runs/<run-id>/outline.json` | 用核准的大綱產生整份簡報 |
| `.venv/Scripts/python -m pipeline.graph --render-only runs/<run-id>` | 只重新套模板並過版面閘門，不呼叫 LLM（例如改了模板或 `site.json` 的 GitHub 網址）；結果存成 `render_check_rerender.json` |
| `.venv/Scripts/python -m pipeline.graph --resume runs/<run-id>` | 從 `resume.json` 記的節點續跑（節點出錯時會自動存） |
| `.venv/Scripts/python -m pipeline.recheck runs/<run-id> s04 s15 --why "原因"` | 人指定要重審的頁：寫出 `resume.json`，再用上一行加 `--max-rounds 3` 從投影片閘門續跑 |

## 檔案

| 檔案 | 內容 |
|---|---|
| `graph.py` | LangGraph 的節點和邊、追蹤紀錄、執行報告 |
| `llm.py` | AISuite＋Groq 呼叫，沿用課程 notebook 的寫法 |
| `prompts.py` | 擬大綱、撰稿、評審、修改四個 LLM 節點的提示詞 |
| `checks.py` | 大綱閘門與投影片閘門的程式檢查（字數用版面寬度算：中文 1、英數 0.5；點數、引用、數字是否出自 Wiki） |
| `recheck.py` | 從某次執行的結果重建狀態，只重審人指定的頁 |
| `render.py`、`templates/deck.html.j2` | 「AI 的作文簿」模板，以及版面閘門（無頭瀏覽器量每頁是否超出版面） |
| `site.json` | GitHub repo 網址，用來把每頁的 Wiki 引用連到 GitHub |

每次執行的紀錄放在 `runs/<run-id>/`：`report.md`（各節點統計、閘門退件紀錄）、`trace.jsonl`、`calls/`（每次 LLM 呼叫的完整 prompt 和回應）、`shots/`（每頁截圖）。

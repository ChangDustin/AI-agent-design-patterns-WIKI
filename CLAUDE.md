# CLAUDE.md — 「AI 代理設計模式」LLM Wiki 規則書（schema）

> 這份檔案是 LLM Wiki 的第三層「schema」：告訴 LLM agent（Claude Code）這個 Wiki 怎麼組織、怎麼維護。
> 概念出處：Andrej Karpathy〈LLM Wiki〉gist（2026-04-04）。本檔由作者與 LLM 一起修訂，改了什麼要寫進 `wiki/log.md`。

## 1. 這個 Wiki 在做什麼

- **主題**：AI 代理設計模式（Agentic Design Patterns），包括反思（Reflection）、工具使用（Tool Use）、規劃（Planning）、多代理協作（Multi-agent Collaboration），以及「工作流程（workflow）vs. 代理（agent）」怎麼選。
- **下游用途**：當作知識庫，由 `pipeline/`（LangGraph + Groq）產生給**非資工大學生**看的教學 HTML 簡報。
- **語言**：繁體中文（台灣用語）。專有名詞第一次出現時附英文，例如「反思（Reflection）」。

## 2. 三層架構

| 層 | 位置 | 誰寫 | 規則 |
|---|---|---|---|
| 原始資料 | `raw/` | 作者蒐集 | 唯讀，不改內容。原文有著作權，不上傳 GitHub；`raw/README.md` 記錄出處、網址、抓取日。 |
| Wiki | `wiki/` | LLM | LLM 建立與維護所有頁面；作者負責閱讀、提問、決定重點。 |
| Schema | `CLAUDE.md` | 作者 + LLM | 就是本檔。流程有調整就更新，並在 log 記一筆。 |

## 3. 目錄

```
wiki/
  index.md      內容目錄：每頁一行「連結 — 一句話摘要」，依類別分組。每次 ingest 必更新。
  log.md        時間序紀錄，只能往後加。標題格式：## [YYYY-MM-DD] 動作 | 標題
  overview.md   主題總覽與目前的綜合理解（synthesis），每進來一篇資料都要重新檢視。
  sources/      每篇原始資料一頁摘要：<source-id>.md
  concepts/     概念頁：reflection.md、tool-use.md、planning.md …
  entities/     人物、組織、工具：andrew-ng.md、anthropic.md …
  queries/      值得留下的查詢結果（例如簡報大綱）
discussions/    每次 ingest 的「先討論」紀錄：提案 → 作者回饋 → 決定
tools/          維護 Wiki 用的小工具（wiki_lint.py）
```

## 4. 頁面格式

- **檔名**：英文小寫 kebab-case，例如 `concepts/tool-use.md`。source-id 用「作者-年份-主題」，例如 `ng-2024-agentic-patterns`。
- **連結**：只用標準相對路徑 Markdown 連結，例如 `[反思](../concepts/reflection.md)`，在 GitHub 和 Obsidian 都能點。不用 `[[wikilink]]`。
- **frontmatter**：每頁開頭都要有：

  ```yaml
  ---
  title: 反思（Reflection）
  type: concept          # source | concept | entity | overview | query
  sources: [ng-2024-agentic-patterns]
  updated: 2026-11-12
  ---
  ```

- **引用**：事實性的句子，句尾附來源頁連結，例如「……（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）」。Wiki 自己歸納出來的說法標「（Wiki 綜合）」。
- **著作權**：用自己的話改寫，不大段複製原文；非引不可時一次不超過 15 字並加引號。

### 概念頁固定段落（下游簡報從這裡取材）

1. `## 一句話定義`
2. `## 生活比喻`
3. `## 運作步驟`
4. `## 例子`
5. `## 什麼時候用、什麼時候別用`
6. `## 常見誤解`
7. `## 相關概念`
8. `## 來源`

### 來源頁固定段落

1. `## 基本資訊`（作者、日期、類型、網址、raw 路徑）
2. `## 一段話摘要`
3. `## 重點`
4. `## 對 Wiki 的影響`（新增或修改了哪些頁；和既有說法一致還是衝突）
5. `## 可用的教學素材`（比喻、例子、數字）
6. `## 限制與存疑`

## 5. 操作流程

### Ingest（先討論、後生成）：一次只處理一篇

1. 原文放進 `raw/<source-id>/`，在 `raw/README.md` 登記。
2. LLM 讀完原文，在 `discussions/NN-<source-id>.md` 寫**提案**：重點、打算新增或修改的頁、和既有內容一致或衝突的地方、要問作者的問題。
3. **作者回覆前不寫入 `wiki/`**。作者的回饋（原話）和最後決定記在同一個檔案。
4. 依決定寫入：`sources/` 摘要頁 → 新增或更新 `concepts/`、`entities/` → 修訂 `overview.md` → 更新 `index.md`。
5. 在 `log.md` 加一筆，列出這次動到的頁面。
6. 跑 `python tools/wiki_lint.py`，有錯先修好再進下一篇。

### Query

先讀 `index.md` 找相關頁 → 讀那些頁 → 回答並附引用。值得保留的答案存進 `queries/`，同時更新 index 和 log。

### Lint（健檢）

檢查頁面間的矛盾、被新資料推翻的舊說法、孤兒頁（沒有任何頁連進來；`queries/` 的頁列在 index 即可）、被提到卻沒有頁面的概念、斷掉的連結、缺來源的段落、概念頁缺固定段落。結果記進 log。

## 6. 下游：簡報 pipeline

`pipeline/`（LangGraph＋Groq）用這個 Wiki 產生教學簡報，設計依據見 `wiki/queries/pipeline-design.md`。pipeline 每次執行都算一次 Query：大綱回存 `wiki/queries/slide-outline.md`，並在 `wiki/log.md` 記一筆；執行紀錄放在 `runs/<run-id>/`。

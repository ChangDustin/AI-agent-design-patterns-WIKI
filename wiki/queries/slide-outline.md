---
title: 查詢｜教學簡報大綱
type: query
sources: []
updated: 2026-11-13
---

# 查詢｜教學簡報大綱

> 由簡報 pipeline（20261113-000224）查詢 Wiki 目錄後產生、通過大綱閘門；作者審閱後採用 Claude 的修改版（見 [討論 08](../../discussions/08-slide-outline-review.md)）。

| id | 類型 | 標題 | 這頁的目標 | 引用的 Wiki 頁 |
|---|---|---|---|---|
| s01 | cover | AI 代理設計模式 | 點出主題：讓 AI 像人一樣分多步把事情做好 | — |
| s02 | hook | 同一題，誰的分數高？ | 用 HumanEval 分數 48.1%、67.0%、95.1% 說明改流程比換更強的模型更有效 | concepts/agentic-workflow.md |
| s03 | concept | 代理式工作流程 | 不要一次寫完，而是像人寫作文一樣分多步修改（寫作文不准按倒退鍵的比喻） | concepts/agentic-workflow.md |
| s04 | concept | 四種招式一次看 | 介紹反思、工具使用、規劃、多代理協作四種模式，以及哪些比較穩定 | overview.md、concepts/agentic-workflow.md |
| s05 | concept | 反思：自己改作文 | LLM 檢查自己的產出再重寫；用 Self-Refine 的數據說明它有效，但不是萬靈丹 | concepts/reflection.md、concepts/self-refine.md |
| s06 | steps | 反思實作：心形圖貼文 | 用課程的 Python 心形圖貼文示範：需求 → 初稿 → 評論 → 第二版 | concepts/reflection.md、sources/tsai-2026-agent-notebooks.md |
| s07 | concept | 工具使用：帶計算機 | 模型只寫出呼叫請求，真正執行的是外部程式；用考試帶計算機的比喻 | concepts/tool-use.md |
| s08 | steps | 麥茶 20 杯夠不夠？ | 用課程的麥茶例子示範三階段：模型轉成請求 → 程式執行 → 依結果回答 | concepts/tool-use.md、sources/tsai-2026-agent-notebooks.md |
| s09 | concept | 規劃：出國排行程 | 規劃有兩種意思：LLM 自己決定步驟，或先寫可編輯的計畫再照著做（可頌賣完了的例子） | concepts/planning.md |
| s10 | steps | ReAct：想→做→看 | 用煮菜比喻和帶傘例子說明 想法 → 動作 → 觀察 的迴圈，它是代理最小的原型 | concepts/react.md |
| s11 | concept | 多代理：分組報告 | 多個角色分工合作；研究小組的例子，效果好 90.2% 但 token 用量約 15 倍 | concepts/multi-agent-collaboration.md |
| s12 | compare | 跟團 vs. 自由行 | 比較工作流程（程式寫死路徑）和代理（LLM 自己決定下一步） | concepts/workflow-vs-agent.md |
| s13 | concept | 能簡單就簡單 | 先試最簡單的方法，複雜度要證明有用才往上加 | concepts/workflow-vs-agent.md、concepts/agentic-workflow.md |
| s14 | quiz | 小測驗：誰在執行？ | 檢查觀眾是否懂：工具使用時真正執行的是程式，不是模型 | concepts/tool-use.md |
| s15 | concept | 代理也會出包 | 代理的限制：卡在迴圈、自評有盲點、成本高、錯誤會累積 | concepts/agent-limitations.md、concepts/llm-feedback.md |
| s16 | concept | AI 做事，人來把關 | 人在迴圈中：在關鍵處讓人檢查、修改、決定 | concepts/human-in-the-loop.md |
| s17 | quiz | 小測驗：該用代理嗎？ | 判斷什麼情況用工作流程就夠、什麼情況才需要代理 | concepts/workflow-vs-agent.md、concepts/agent-limitations.md |
| s18 | summary | 本章重點 | 回顧：分多步工作、四種模式、能簡單就簡單、AI 做事人來把關 | overview.md、concepts/workflow-vs-agent.md、concepts/human-in-the-loop.md |

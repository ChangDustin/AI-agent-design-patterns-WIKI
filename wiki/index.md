# Wiki 目錄（index）

> 主題：AI 代理設計模式。每頁一行「連結 — 一句話摘要」。LLM 每次 ingest 都會更新這頁；查詢時先讀這頁再往下找。
> 進度：已 ingest 7／7 篇（全部完成）。

## 總覽

- [AI 代理設計模式總覽](overview.md) — 三個視角（誰決定下一步、用了哪些招式、代理由什麼組成）、ReAct 這座橋、Ng 與 Anthropic 對照、待解問題

## 概念：總框架

- [工作流程 vs. 代理](concepts/workflow-vs-agent.md) — 正式用詞：程式寫死路徑（跟團）vs. LLM 自己決定（自由行）；能簡單就簡單
- [代理式工作流程](concepts/agentic-workflow.md) — Ng 的用詞：讓 LLM 分多步、多次呼叫完成工作，而不是一次寫完
- [增強型 LLM](concepts/augmented-llm.md) — 基本積木：LLM 加上檢索、工具、記憶

## 概念：代理的元件與技巧

- [記憶](concepts/memory.md) — 短期記憶＝上下文（書桌）、長期記憶＝向量資料庫＋檢索（書櫃）
- [思維鏈](concepts/chain-of-thought.md) — 叫模型一步一步想，把難題拆小；只靠內部知識容易幻覺
- [ReAct](concepts/react.md) — 想 → 做 → 看 的迴圈；工具使用＋思維鏈，代理最小的原型

## 概念：Ng 的四種模式

- [反思](concepts/reflection.md) — LLM 檢查自己的產出、提出改進、再重寫（別名：評估者—優化者）
  - [Self-Refine](concepts/self-refine.md) — 反思的單一模型版：生成 → 回饋 → 改寫；平均 +20%，但數學幾乎沒用
  - [LLM 回饋與自我評估](concepts/llm-feedback.md) — 回饋要具體可行動；LLM 自評有盲點，要搭配外部訊號
- [工具使用](concepts/tool-use.md) — LLM 寫出呼叫請求，由程式執行搜尋、計算等工具再回傳結果
- [規劃](concepts/planning.md) — 兩種意思：LLM 自主決定步驟（代理）／先寫可編輯的計畫再執行（課程的工作流程）
- [多代理協作](concepts/multi-agent-collaboration.md) — 多個角色分工、互相討論，合力完成複雜任務

## 概念：Anthropic 的工作流程模式

- [提示鏈](concepts/prompt-chaining.md) — 固定步驟依序呼叫，中間加上程式檢查的閘門
- [路由](concepts/routing.md) — 先分類，再交給專門處理那一類的流程
- [平行化](concepts/parallelization.md) — 分段同時做，或同一件事做多次再投票
- [協調者—工作者](concepts/orchestrator-workers.md) — 中央 LLM 動態拆任務、分派、整合
- 評估者—優化者 — 併入[反思](concepts/reflection.md)

## 概念：限制、評估與人的角色

- [代理的限制與風險](concepts/agent-limitations.md) — 上下文有限、規劃不穩、格式不可靠、自評有盲點、湧現行為、成本與安全風險，以及因應方式
- [如何評估代理](concepts/agent-evaluation.md) — 看結果不看固定步驟；小樣本起步；LLM 評審配評分規準；人工測試不可少
- [人在迴圈中](concepts/human-in-the-loop.md) — 在關鍵位置讓人檢查、修改、決定；AI 做事、人來把關

## 來源

- [Ng 2024〈Agentic Design Patterns〉Part 1–5](sources/ng-2024-agentic-patterns.md) — 四大模式的出處；改流程比換模型更能提升表現
- [Anthropic 2024〈Building effective AI agents〉](sources/anthropic-2024-building-effective-agents.md) — 工作流程 vs. 代理、五種工作流程、先求簡單
- [Weng 2023〈LLM Powered Autonomous Agents〉](sources/weng-2023-llm-agents.md) — 代理＝大腦＋規劃＋記憶＋工具；案例與三大挑戰
- [Yao 2022〈ReAct〉](sources/yao-2022-react.md) — 推理和行動交錯；幻覺大減但會卡迴圈；人改想法就能修正
- [Madaan 2023〈Self-Refine〉](sources/madaan-2023-self-refine.md) — 同一模型自我回饋改寫；回饋品質是瓶頸；輪數邊際效益遞減
- [Anthropic 2025〈How we built our multi-agent research system〉](sources/anthropic-2025-multi-agent-research.md) — 多代理研究系統：好 90.2%、15 倍 token；提示原則與評估方法
- [Tsai 2026 課程 notebook（Reflection／Tool Use／Planning）](sources/tsai-2026-agent-notebooks.md) — aisuite＋Groq 的逐格實作；流程寫清楚、資料不是指令、程式能確認的交給程式

## 人物、組織、工具、案例

- [Andrew Ng](entities/andrew-ng.md) — 提出四大代理設計模式的分類
- [Anthropic](entities/anthropic.md) — 提出工作流程／代理的區分與「先求簡單」原則
- [Lilian Weng](entities/lilian-weng.md) — 提出代理的元件拆解（規劃、記憶、工具）
- [蔡炎龍](entities/tsai-yen-lung.md) — 課程教材作者；Reflection、Tool Use、Planning 三份 notebook
- [LangGraph](entities/langgraph.md) — 用「圖」組裝 LLM 流程的框架；本專案的簡報 pipeline 用它，並記下框架的取捨
- [AISuite](entities/aisuite.md) — 統一呼叫多家模型的套件；課程與本專案都用它
- [Groq](entities/groq.md) — 提供 gpt-oss-120b 的服務；金鑰、額度與推理模型設定的注意事項
- [Generative Agents](entities/generative-agents.md) — AI 小鎮：25 個 LLM 角色靠記憶、反思、規劃互動
- [Claude Research](entities/claude-research.md) — Anthropic 的多代理研究系統：架構、早期出包與修正

## 查詢結果

- [查詢｜教學簡報大綱](queries/slide-outline.md) — pipeline 產生的大綱：每頁對應哪些 Wiki 頁
- [根據 Wiki，教學簡報 pipeline 該怎麼設計？](queries/pipeline-design.md) — 帶閘門的提示鏈＋評估者—優化者迴圈；15 條設計原則各自對應 Wiki 頁

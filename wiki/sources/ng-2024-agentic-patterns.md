---
title: Andrew Ng〈Agentic Design Patterns〉Part 1–5
type: source
sources: [ng-2024-agentic-patterns]
updated: 2026-11-12
---

# Andrew Ng〈Agentic Design Patterns〉Part 1–5

## 基本資訊

| 項目 | 內容 |
|---|---|
| 作者 | [Andrew Ng](../entities/andrew-ng.md) |
| 出處 | DeepLearning.AI 電子報 *The Batch* 的 Letters 專欄 |
| 日期 | Part 1：2024-03-20；Part 2：03-27；Part 3：04-03；Part 4：04-10；Part 5：04-17 |
| 類型 | 電子報專欄，5 篇短文 |
| 網址 | [Part 1 總覽](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)、[Part 2 反思](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/)、[Part 3 工具使用](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-3-tool-use/)、[Part 4 規劃](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-4-planning/)、[Part 5 多代理協作](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-5-multi-agent-collaboration/) |
| raw | `raw/ng-2024-agentic-patterns/part1.md`～`part5.md` |
| 討論紀錄 | [討論 01](../../discussions/01-ng-2024-agentic-patterns.md) |

## 一段話摘要

Ng 認為，與其等更強的模型，不如改變使用 LLM 的方式：不要讓它一次寫完，而是用「代理式工作流程」讓它分多步、反覆修改。他把常見做法歸納成四種設計模式：反思、工具使用、規劃、多代理協作。他也指出前兩種已經相當可靠，後兩種更強大，但比較難預測。

## 重點

1. 一般的 zero-shot 用法就像「寫作文不准按倒退鍵」；代理式工作流程讓 LLM 列大綱、查資料、寫初稿、挑毛病、再修改。
2. HumanEval 程式題：GPT-3.5 一次生成 48.1%、GPT-4 一次生成 67.0%；把 GPT-3.5 包進代理迴圈，最高可達 95.1%。
3. **反思**：LLM 批評自己的產出再重寫，可以重複多輪；可以加工具（單元測試、網路查證），也可以拆成產出者＋批評者兩個代理。
4. **工具使用**：LLM 輸出特定格式的呼叫請求，由外部程式執行，再把結果放回輸入；工具太多時要先挑出相關的一小組。GPT-4 在 2023 年中推出的 function calling，是讓工具使用走向通用的一大步。
5. **規劃**：LLM 自己決定步驟和順序、拆解任務，結果可能出乎開發者意料（Ng 現場 demo 時搜尋 API 被限流，代理自己改用 Wikipedia）。但很多流程步驟固定，不需要規劃。
6. **多代理協作**：同一個 LLM 用不同提示扮演不同角色。有效的原因：實驗結果好、每次呼叫能聚焦在一件事、給人一個拆解任務的思考框架。
7. **成熟度**：反思、工具使用已能穩定運作；規劃、多代理協作較不成熟，結果較難預測。

## 對 Wiki 的影響

- **新增**：[代理式工作流程](../concepts/agentic-workflow.md)、[反思](../concepts/reflection.md)、[工具使用](../concepts/tool-use.md)、[規劃](../concepts/planning.md)、[多代理協作](../concepts/multi-agent-collaboration.md)、[Andrew Ng](../entities/andrew-ng.md)、[LangGraph](../entities/langgraph.md)；首次撰寫[總覽](../overview.md)。
- **一致或衝突**：第一篇，沒有衝突。預告：Ng 把所有多步驟流程都叫 agentic workflow，之後 Anthropic 的用詞可能不同，到時要在概念頁註明。

## 可用的教學素材

- **比喻**：zero-shot＝寫作文不准按倒退鍵；代理式工作流程＝正常人寫作時的反覆修改。
- **數字（開場鉤子）**：48.1%（GPT-3.5）→ 67.0%（GPT-4）→ 95.1%（GPT-3.5＋代理迴圈）。
- **故事**：Ng 的 demo 中搜尋 API 被限流，代理自己改用 Wikipedia 完成任務（Ng 稱為「AI Agentic moment」）。
- **例子**：複利 `100 * (1+0.07)**12` 交給 Python 算，約得 225.22（Wiki 綜合，自行驗算）。
- **例子**：看男孩的照片畫一個同樣姿勢的女孩 → 拆成「偵測姿勢」＋「依姿勢生圖」兩步（HuggingGPT 的簡化例）。
- **比喻（Ng 原文）**：多代理就像公司主管決定要雇哪些角色、怎麼分工；也像寫程式時拆成多個 process／thread。
- **例子**：ChatDev，一群代理經營的虛擬軟體公司。

## 限制與存疑

- 95.1% 是 Ng 團隊彙整多篇研究後取的最佳值（原文用 up to），各方法設定不同，不是同一個實驗下的公平比較。
- 這是 2024 年初的觀點；Ng 自己也說規劃和多代理會快速進步，成熟度的判斷可能已經過時。
- 電子報短文沒有實驗細節，推薦論文要另外讀（本 Wiki 會 ingest 其中的 Self-Refine）。
- 「代理式工作流程推動的進展可能超過下一代基礎模型」是 Ng 的個人預測。

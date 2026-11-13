---
title: 工作流程 vs. 代理（Workflow vs. Agent）
type: concept
sources: [anthropic-2024-building-effective-agents, ng-2024-agentic-patterns, yao-2022-react, anthropic-2025-multi-agent-research, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# 工作流程 vs. 代理（Workflow vs. Agent）

> 本 Wiki 的正式用詞（討論 02 決定）。兩者合稱「代理式系統（agentic systems）」；Ng 的四種模式（[反思](reflection.md)、[工具使用](tool-use.md)、[規劃](planning.md)、[多代理協作](multi-agent-collaboration.md)）是組成兩者的零件。

## 一句話定義

工作流程是讓 LLM 和工具**照事先寫好的程式路徑**執行；代理則是讓 LLM **自己決定**下一步做什麼、用哪個工具（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

工作流程像跟團旅行：路線由旅行社排好，穩定、可預期；代理像自由行：邊走邊決定下一站，彈性大，但可能迷路，花費也比較高（Wiki 綜合：討論 02 選定的教學比喻）。

## 運作步驟

決定要用哪一種的步驟（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）：

1. **先試最簡單的**：單次 LLM 呼叫配上檢索和範例，很多應用這樣就夠了（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
2. **不夠才加複雜度**：任務能清楚拆成固定步驟，就選工作流程，換到穩定一致的結果（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
3. **步驟沒辦法事先寫死**：選代理，換到彈性和由模型主導的決策（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
4. **持續衡量**：只有在確實改善結果時才增加複雜度（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 例子

- **工作流程**：先寫大綱 → 用程式檢查大綱 → 依大綱寫全文（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **代理**：解 SWE-bench 程式題的代理，依任務描述自己決定要改哪些檔案（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **代理**：「電腦操作（computer use）」讓 Claude 自己操作電腦完成任務（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **代理的最小原型**：ReAct 讓 LLM 在「想法 → 動作 → 觀察」的迴圈裡，依環境回饋決定下一步，正符合 Anthropic 對代理的描述（Wiki 綜合，比較 [Yao 2022](../sources/yao-2022-react.md) 與 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **研究任務適合代理**：研究的步驟無法事先預測、路徑會隨新發現改變，寫死的線性流程處理不了（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **課程的三份 notebook**：反思、工具使用、規劃都是固定順序的幾次呼叫，教材明說不是完整的自主代理（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **本專案**：簡報 pipeline 是工作流程，不是代理：步驟和檢查都由程式寫死，LLM 只負責每一步的內容（Wiki 綜合）。

## 什麼時候用、什麼時候別用

- **工作流程**：任務定義清楚、要求結果穩定一致時（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **代理**：開放式問題，無法預測需要幾步、也寫不出固定路徑，而且你夠信任模型的判斷時（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **代理的代價**：自主代表成本更高、錯誤會一路累積，需要在沙盒中大量測試並加上防護（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **兩者都別用**：單次呼叫就能解決時；代理式系統是用延遲和成本換表現（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 常見誤解

- **「代理一定比工作流程高級」**：重點是選對系統，不是做出最精密的系統（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **「Ng 說的 agentic workflow 就是這裡的 workflow」**：Ng 的用詞涵蓋所有多步驟流程（包括 LLM 自己規劃的那種），Anthropic 的 workflow 只指預先寫好路徑的那種（Wiki 綜合，比較 [Ng 2024](../sources/ng-2024-agentic-patterns.md) 與 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **「代理的實作一定很複雜」**：代理通常只是在迴圈裡根據環境回饋使用工具的 LLM，難的是把工具設計好（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 相關概念

- [代理式工作流程](agentic-workflow.md)：Ng 的用詞，範圍較廣。
- [提示鏈](prompt-chaining.md)、[路由](routing.md)、[平行化](parallelization.md)、[協調者—工作者](orchestrator-workers.md)、[反思（評估者—優化者）](reflection.md)：Anthropic 的五種工作流程。
- [規劃](planning.md)：代理的核心能力。
- [ReAct](react.md)：代理最小的原型。
- [增強型 LLM](augmented-llm.md)：工作流程和代理共同的基本積木。

## 來源

- [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)
- [Ng 2024](../sources/ng-2024-agentic-patterns.md)（用詞對照）

---
title: LangGraph
type: entity
sources: [ng-2024-agentic-patterns, anthropic-2024-building-effective-agents]
updated: 2026-11-12
---

# LangGraph

## 在這個 Wiki 裡的角色

- Ng 把 LangGraph 和 AutoGen、Crew AI 並列，當作建構[多代理協作](../concepts/multi-agent-collaboration.md)系統的新興框架（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 在這個專案裡

- 本專案的簡報產生流程（`pipeline/`）用 LangGraph 實作：每個步驟是一個節點，「檢查不通過就退回重寫」用條件邊表示；完整設計見[查詢：pipeline 該怎麼設計](../queries/pipeline-design.md)（Wiki 綜合）。
- 這個「檢查 → 退回重寫」迴圈本身就是[反思](../concepts/reflection.md)模式；照 Anthropic 的分類，整條 pipeline 是帶閘門的[提示鏈](../concepts/prompt-chaining.md)，屬於[工作流程](../concepts/workflow-vs-agent.md)而不是代理（Wiki 綜合）。

## 框架的取捨（討論 02）

- **Anthropic 的提醒**：框架能簡化呼叫 LLM、定義工具、串接呼叫等低階工作，但抽象層可能遮住底下的 prompt 和回應、讓除錯變難，也容易誘使人加入不必要的複雜度；建議先直接用 API，用框架就要懂底層在做什麼（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **本專案的對策**：LangGraph 只負責流程控制（節點、邊、條件邊）；每個節點裡的 LLM 呼叫直接用 aisuite＋Groq、自己寫 prompt；每次呼叫的 prompt 和回應都寫進 `runs/` 的執行紀錄，讓抽象層保持透明（Wiki 綜合）。

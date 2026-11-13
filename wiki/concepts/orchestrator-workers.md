---
title: 協調者—工作者（Orchestrator-workers）
type: concept
sources: [anthropic-2024-building-effective-agents, anthropic-2025-multi-agent-research]
updated: 2026-11-12
---

# 協調者—工作者（Orchestrator-workers）

> Anthropic 的五種[工作流程](workflow-vs-agent.md)之一。

## 一句話定義

由一個中央 LLM（協調者）依照輸入動態拆解任務、分派給多個工作者 LLM，最後整合它們的結果（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

分組報告的組長：先看題目決定要分成哪幾塊、分給誰，等組員交回來再整合成一份；題目不同，分法就不同（Wiki 綜合）。

## 運作步驟

1. **看輸入、拆任務**：協調者讀取輸入，決定需要哪些子任務（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
2. **分派**：把子任務交給工作者 LLM（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。每個工作者都要拿到目標、輸出格式、該用的工具和來源、清楚的任務邊界（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
3. **整合**：協調者彙整工作者的結果（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 例子

- **寫程式的產品**：每次都要改好幾個檔案，要改哪些、怎麼改，取決於這次的任務（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **搜尋任務**：從多個來源蒐集並分析可能相關的資訊（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **[Claude Research](../entities/claude-research.md)**：主代理分析問題、擬定策略，同時派出子代理分頭搜尋，再彙整答案（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **分派不清楚的後果**：只交代「研究晶片短缺」時，一個工作者去查 2021 年車用晶片危機，另外兩個重複查 2025 年的供應鏈（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 什麼時候用、什麼時候別用

- **適合**：複雜任務、沒辦法預先知道需要哪些子任務的時候（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **依難度分配人力**：簡單查詢 1 個代理、3～10 次工具呼叫；比較型 2～4 個子代理、各 10～15 次；複雜研究 10 個以上子代理（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **別用**：子任務可以事先定好時，用[平行化](parallelization.md)或[提示鏈](prompt-chaining.md)就夠了（Wiki 綜合，依 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md) 的「先求簡單」原則）。
- **同步執行的瓶頸**：協調者要等所有工作者做完才繼續，中途沒辦法調整方向，也可能被一個慢的工作者卡住（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 常見誤解

- **「這跟平行化一樣」**：形狀很像，關鍵差別在於子任務不是事先定義的，而是協調者看過輸入才決定（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **「協調者自己會判斷該派幾個人」**：早期的主代理曾為簡單問題派出 50 個子代理，必須在提示中寫明依難度分配的規則（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 相關概念

- [規劃](planning.md)：協調者的動態拆解，就是一種規劃（Wiki 綜合）。
- [多代理協作](multi-agent-collaboration.md)：協調者和工作者可以看成不同角色的代理（Wiki 綜合）。
- [平行化](parallelization.md)

## 來源

- [Anthropic 2024：Workflow: Orchestrator-workers](../sources/anthropic-2024-building-effective-agents.md)
- [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)（真實產品案例）

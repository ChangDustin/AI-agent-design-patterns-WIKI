---
title: 平行化（Parallelization）
type: concept
sources: [anthropic-2024-building-effective-agents, yao-2022-react, anthropic-2025-multi-agent-research]
updated: 2026-11-12
---

# 平行化（Parallelization）

> Anthropic 的五種[工作流程](workflow-vs-agent.md)之一。

## 一句話定義

讓多個 LLM 呼叫同時處理任務，再用程式彙整結果。分成兩種：「分段」是把任務切成獨立的子任務一起做，「投票」是同一件事做很多次（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

分段像把考卷分給三位老師，各改一大題，同時改完再加總；投票像請三位評審各自打分，再看多數意見（Wiki 綜合）。

## 運作步驟

1. **分段**：把任務切成彼此獨立的子任務，同時交給不同的 LLM 呼叫（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
2. **投票**：把同一個任務跑很多次，得到多樣的輸出（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
3. **彙整**：用程式把各個輸出合併或計票（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 例子

- **分段（把關）**：一個模型回答使用者，另一個同時檢查有沒有不當的內容或要求；通常比讓同一次呼叫兼顧兩件事效果好（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **分段（評測）**：自動化評測時，每次呼叫只評一個面向（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **投票（抓漏洞）**：用幾個不同的提示審查同一段程式碼，任何一個發現問題就標記（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **平行的子代理與工具**：Claude Research 的主代理同時派 3～5 個子代理，子代理同時用 3 個以上工具，複雜研究的時間最多縮短 90%（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **投票（推理）**：自洽投票（CoT-SC）抽 21 條思維鏈、取多數答案，表現穩定勝過單一條思維鏈；ReAct 論文把它和 ReAct 交替使用（[Yao 2022](../sources/yao-2022-react.md)）。
- **投票（內容審查）**：判斷內容是否不當時，用多個提示、設不同的投票門檻，平衡誤判和漏判（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 什麼時候用、什麼時候別用

- **為了快**：子任務可以平行處理的時候（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **為了穩**：需要多個觀點或多次嘗試來提高信心的時候（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **為了專注**：任務有很多面向要考慮時，每個面向交給一次獨立的呼叫，模型通常表現更好（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **別用**：子任務沒辦法事先切好時，改用[協調者—工作者](orchestrator-workers.md)（Wiki 綜合，依 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md) 的比較）。

## 常見誤解

- **「平行化只是為了快」**：投票的目的是提高結果的可信度，不是速度（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 相關概念

- [協調者—工作者](orchestrator-workers.md)：形狀很像，但子任務是動態決定的。
- [多代理協作](multi-agent-collaboration.md)
- [思維鏈](chain-of-thought.md)：自洽投票是思維鏈的投票版。
- [工作流程 vs. 代理](workflow-vs-agent.md)

## 來源

- [Anthropic 2024：Workflow: Parallelization](../sources/anthropic-2024-building-effective-agents.md)
- [Yao 2022](../sources/yao-2022-react.md)（CoT-SC 的實例）
- [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)（平行工具呼叫的速度提升）

---
title: 路由（Routing）
type: concept
sources: [anthropic-2024-building-effective-agents]
updated: 2026-11-12
---

# 路由（Routing）

> Anthropic 的五種[工作流程](workflow-vs-agent.md)之一。

## 一句話定義

先把輸入分類，再交給專門處理這一類的後續流程、提示或工具（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

醫院的掛號分診：先判斷你該看哪一科，再由那一科的醫生處理（Wiki 綜合）。

## 運作步驟

1. **分類**：用 LLM 或傳統的分類模型、演算法，判斷輸入屬於哪一類（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
2. **分派**：依類別導向不同的後續流程（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
3. **專門處理**：每一類都有為它最佳化的提示和工具（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 例子

- **客服分流**：一般問題、退款申請、技術支援，分別進入不同的流程、提示和工具（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **大小模型分工**：簡單常見的問題交給小而便宜的模型，困難少見的問題交給能力較強的模型（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 什麼時候用、什麼時候別用

- **適合**：任務有明顯不同的類別、分開處理比較好，而且分類本身做得準的時候（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **好處**：關注點分離，可以寫更專門的提示；不分流的話，為某一類輸入調好的提示，可能拖累其他類輸入的表現（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **別用**：分類做不準的時候，路由的前提就不成立（Wiki 綜合，依 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md) 的適用條件反推）。

## 常見誤解

- **「路由一定要用 LLM 判斷」**：分類也可以交給傳統的分類模型或演算法（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 相關概念

- [工作流程 vs. 代理](workflow-vs-agent.md)
- [平行化](parallelization.md)：路由是「分給其中一條路」，平行化是「同時走好幾條路」（Wiki 綜合）。

## 來源

- [Anthropic 2024：Workflow: Routing](../sources/anthropic-2024-building-effective-agents.md)

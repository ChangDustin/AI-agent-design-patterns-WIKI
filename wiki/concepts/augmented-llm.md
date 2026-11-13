---
title: 增強型 LLM（Augmented LLM）
type: concept
sources: [anthropic-2024-building-effective-agents, weng-2023-llm-agents]
updated: 2026-11-12
---

# 增強型 LLM（Augmented LLM）

> 代理式系統最基本的積木。[工作流程和代理](workflow-vs-agent.md)都是用它組起來的。

## 一句話定義

在 LLM 外面加上檢索、工具、記憶等能力，讓它能自己產生搜尋查詢、挑選工具、決定要記住哪些資訊（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

一位學生（LLM）配上圖書館借書證（檢索）、計算機（工具）和筆記本（記憶）：人還是同一個人，能做的事卻多很多（Wiki 綜合）。

## 運作步驟

1. **挑能力**：依使用情境決定要加上哪些能力（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
2. **做好介面**：替這些能力提供簡單、文件清楚的介面給 LLM 使用（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
3. **接上生態系**：其中一種做法是 Model Context Protocol（MCP），能用簡單的用戶端接上第三方工具（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 例子

- **檢索**：LLM 自己產生搜尋查詢去找資料（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **工具**：LLM 依需要挑選合適的工具（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **記憶**：LLM 決定哪些資訊要保留下來（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。細節見[記憶](memory.md)。
- **Weng 的元件拆解也很像**：LLM 大腦＋規劃＋記憶＋工具；差別是 Weng 把規劃也算成元件，Anthropic 的增強型 LLM 只有檢索、工具、記憶（Wiki 綜合，比較 [Weng 2023](../sources/weng-2023-llm-agents.md) 與 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 什麼時候用、什麼時候別用

- **幾乎都會用到**：Anthropic 在介紹各種工作流程和代理時，都假設每次 LLM 呼叫都能使用這些增強能力（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **別用的時機**：目前資料未提及，待補。

## 常見誤解

- **「增強型 LLM 是另一個更強的模型」**：模型本身沒變，變的是外面接了哪些能力（Wiki 綜合）。

## 相關概念

- [工具使用](tool-use.md)：增強能力裡最常見的一種。
- [記憶](memory.md)：短期記憶在上下文，長期記憶靠外部資料庫和檢索。
- [工作流程 vs. 代理](workflow-vs-agent.md)

## 來源

- [Anthropic 2024：Building block: The augmented LLM](../sources/anthropic-2024-building-effective-agents.md)
- [Weng 2023：Agent System Overview](../sources/weng-2023-llm-agents.md)

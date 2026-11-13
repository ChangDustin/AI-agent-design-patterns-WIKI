---
title: 提示鏈（Prompt Chaining）
type: concept
sources: [anthropic-2024-building-effective-agents]
updated: 2026-11-12
---

# 提示鏈（Prompt Chaining）

> Anthropic 的五種[工作流程](workflow-vs-agent.md)之一。

## 一句話定義

把任務拆成固定順序的幾個步驟，每次 LLM 呼叫處理上一步的輸出；中間可以加程式檢查（閘門，gate），確認流程沒有走偏（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

工廠生產線：每一站只做一件簡單的事，站和站之間有品管關卡，不合格就不往下送（Wiki 綜合）。

## 運作步驟

1. **拆步驟**：把任務拆成固定的子任務序列（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
2. **依序呼叫**：每一次 LLM 呼叫都拿上一步的輸出繼續處理（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
3. **設閘門**：在任何一個中間步驟加上程式檢查，確認輸出合格（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
4. **通過才往下**：檢查通過才交給下一步，直到完成（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 例子

- **文案＋翻譯**：先寫行銷文案，再翻譯成另一種語言（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **大綱＋全文**：先寫文件大綱 → 檢查大綱是否符合條件 → 依大綱寫出全文（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **本專案**：簡報 pipeline 的「查 Wiki → 擬大綱 → 檢查 → 寫投影片 → 檢查 → 輸出 HTML」就是一條帶閘門的提示鏈（Wiki 綜合）。

## 什麼時候用、什麼時候別用

- **適合**：任務能輕易、乾淨地拆成固定子任務的時候（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **取捨**：用比較長的延遲換比較高的正確率，因為每次呼叫都變成比較容易的小任務（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **別用**：子任務沒辦法事先決定時，改用[協調者—工作者](orchestrator-workers.md)或代理（Wiki 綜合，依 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md) 的比較）。

## 常見誤解

- **「拆成多步比較慢，所以不划算」**：變慢是刻意的取捨，換的是正確率（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **「閘門也要叫 LLM 來判斷」**：閘門可以只是一段程式檢查（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 相關概念

- [工作流程 vs. 代理](workflow-vs-agent.md)
- [規劃](planning.md)：提示鏈的步驟由人事先定好，規劃的步驟由 LLM 自己決定（Wiki 綜合）。
- [反思](reflection.md)：閘門沒過就退回重寫，就形成反思迴圈（Wiki 綜合）。

## 來源

- [Anthropic 2024：Workflow: Prompt chaining](../sources/anthropic-2024-building-effective-agents.md)

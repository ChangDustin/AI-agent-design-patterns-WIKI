---
title: 代理式工作流程（Agentic Workflow）
type: concept
sources: [ng-2024-agentic-patterns, anthropic-2024-building-effective-agents]
updated: 2026-11-12
---

# 代理式工作流程（Agentic Workflow）

> 這個 Wiki 的總入口之一。四種設計模式都是「讓 LLM 分多步完成工作」的不同招式。
> **用詞注意**：這是 Ng 的用詞，泛指所有多步驟流程。本 Wiki 的正式用詞採 Anthropic 的區分，分成[工作流程和代理](workflow-vs-agent.md)兩種（討論 02 決定）。

## 一句話定義

不要求 LLM 一次生成最終答案，而是安排它分成多個步驟、多次呼叫，逐步把作品改好（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 生活比喻

一般的 zero-shot 用法就像寫作文不准按倒退鍵，從第一個字一路打到最後一個字（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
代理式工作流程則像正常人寫作：列大綱、查資料、寫初稿、自己挑毛病、再修改（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 運作步驟

以寫一篇文章為例（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）：

1. 規劃大綱（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
2. 判斷需不需要上網搜尋、要搜什麼（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
3. 寫初稿（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
4. 重讀初稿，找出站不住腳的論點或多餘的資訊（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
5. 針對找到的弱點修改，必要時重複（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 例子

- **HumanEval 程式題**：GPT-3.5 一次生成 48.1%、GPT-4 一次生成 67.0%；把 GPT-3.5 包進代理迴圈最高可達 95.1%（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **怎麼解讀**：改流程帶來的進步，比從 GPT-3.5 換成 GPT-4 還大；但 95.1% 是多篇研究的最佳值，不是同一實驗的公平比較（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 什麼時候用、什麼時候別用

- **適合**：需要高品質產出、人自己做也會反覆修改的任務，例如寫作、寫程式、做研究（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **先求最簡單**：很多應用只要把單次 LLM 呼叫配上檢索和範例調好就夠了，不一定需要代理式系統（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **代價**：代理式系統通常是用更長的延遲、更高的成本，去換更好的表現（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 常見誤解

- **「想要更好的結果只能等更強的模型」**：Ng 彙整的 HumanEval 數據顯示，好的流程能讓舊模型勝過新模型的一次生成（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **「代理式工作流程就是 AI 自己決定一切」**：很多流程的步驟是固定的，例如固定反思幾輪；只有規劃模式才讓 AI 動態決定步驟（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **「流程越複雜越好」**：只有在確實改善結果時才增加複雜度（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 相關概念

- [工作流程 vs. 代理](workflow-vs-agent.md)：本 Wiki 的正式用詞。
- [反思](reflection.md)、[工具使用](tool-use.md)、[規劃](planning.md)、[多代理協作](multi-agent-collaboration.md)：Ng 的四種設計模式。

## 來源

- [Ng 2024，Part 1](../sources/ng-2024-agentic-patterns.md)
- [Anthropic 2024：When (and when not) to use agents](../sources/anthropic-2024-building-effective-agents.md)

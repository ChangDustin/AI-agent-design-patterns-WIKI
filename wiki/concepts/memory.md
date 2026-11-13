---
title: 記憶（Memory）
type: concept
sources: [weng-2023-llm-agents, anthropic-2024-building-effective-agents, ng-2024-agentic-patterns, anthropic-2025-multi-agent-research, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# 記憶（Memory）

> 代理的三大元件之一（Weng）；也是[增強型 LLM](augmented-llm.md)的三種增強能力之一（Anthropic）。

## 一句話定義

讓代理能取得、儲存、保留並在之後找回資訊的機制，分成放在上下文裡的短期記憶，以及存在外部資料庫、需要時再檢索的長期記憶（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 生活比喻

短期記憶像書桌桌面：伸手就拿得到，但空間有限，放不下就得收走；長期記憶像書櫃：放得下很多書，但要先找出需要的那本、放上桌才能用（Wiki 綜合：討論 03 選定的教學比喻）。

## 運作步驟

1. **短期記憶**：把需要的資訊直接放進這次呼叫的上下文，模型靠 in-context learning 使用它（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
2. **長期記憶：存**：把資訊轉成 embedding（向量表示），存進向量資料庫（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
3. **長期記憶：找**：查詢時用快速的最大內積搜尋（通常是近似最近鄰演算法），找出最相關的幾筆（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
4. **放回桌上**：把找到的資訊放進上下文，交給模型使用（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 例子

- **人腦對照**：感覺記憶 ↔ 原始輸入的 embedding；短期（工作）記憶 ↔ 上下文；長期記憶 ↔ 外部向量資料庫（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **人的短期記憶**：大約只能記 7 項、維持 20–30 秒（[Weng 2023](../sources/weng-2023-llm-agents.md)，引 Miller 1956）。
- **AI 小鎮的記憶流**：用自然語言記下角色的所有經歷，再依新近程度、重要性、相關性挑出要用的記憶（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **Reflexion**：把自我反思的結果存進工作記憶（最多三則），下次嘗試時當參考（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **多代理**：每個代理可以有自己的記憶（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **課程的多階段呼叫**：每次呼叫都是新的請求，下一步需要的原始需求、初稿、評論，都要由 Python 明確放進 prompt（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **課程的 RAG**：用向量資料庫找出相關段落再交給模型回答，可以看成長期記憶的一種實作（Wiki 綜合）。
- **長任務的外部記憶**：Claude Research 的代理在上下文快滿時，把完成的階段摘要存到外部記憶，再交給新的子代理接手；需要時把研究計畫從記憶取回（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 什麼時候用、什麼時候別用

- **需要長期記憶**：資訊多到上下文放不下，或要跨很長的時間保留時（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **限制**：外部向量資料庫＋檢索能擴大知識量，但表現力不如把全部內容放進上下文直接注意（full attention）（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **別只靠一次性的靜態檢索**：傳統 RAG 一次抓出最相似的段落就生成答案；研究這類任務需要依新發現多步、動態地搜尋（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 常見誤解

- **「模型會自動記住上次的對話」**：模型不會自動記得前一次呼叫，需要的內容要在下一次 prompt 裡明確帶入（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）；要長期記住的東西，就得存到外部再檢索回來（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **「長期記憶跟上下文一樣好用」**：檢索回來的只是片段，表現力不如全部放進上下文（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 相關概念

- [增強型 LLM](augmented-llm.md)：記憶是三種增強能力之一。
- [反思](reflection.md)：Reflexion 把反思的結果存成記憶。
- [代理的限制與風險](agent-limitations.md)：上下文長度有限，是代理的主要瓶頸之一。
- [Generative Agents](../entities/generative-agents.md)：記憶流的代表案例。

## 來源

- [Weng 2023：Component Two: Memory](../sources/weng-2023-llm-agents.md)
- [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)（增強型 LLM 的記憶能力）
- [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)（靜態檢索的侷限、長任務的外部記憶）
- [Tsai 2026](../sources/tsai-2026-agent-notebooks.md)（模型不會記得上一次呼叫）

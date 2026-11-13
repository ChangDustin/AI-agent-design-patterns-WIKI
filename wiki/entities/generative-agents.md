---
title: Generative Agents（AI 小鎮）
type: entity
sources: [weng-2023-llm-agents]
updated: 2026-11-12
---

# Generative Agents（AI 小鎮）

## 是什麼

Park 等人在 2023 年做的實驗：25 個虛擬角色各由一個 LLM 代理控制，生活在受《模擬市民》（The Sims）啟發的沙盒環境裡互動（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 怎麼做到的

- **記憶流**：用自然語言記下角色的所有經歷（觀察）（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **檢索**：依新近程度、重要性、相關性挑出要用的記憶（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **反思**：把記憶彙整成更高層次的推論，指引之後的行為；和「批評自己產出」的那種反思不同（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **規劃與反應**：把反思和環境資訊轉成行動，也會考慮角色之間的關係（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 結果

- 出現自然的社交行為：消息在角色之間傳開、記得人際關係（例如延續之前聊的話題）、一起籌辦活動（例如辦派對並邀請其他人）（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 和本 Wiki 的關係

- 是[多代理協作](../concepts/multi-agent-collaboration.md)的有趣例子，也示範了[記憶](../concepts/memory.md)和另一種意思的[反思](../concepts/reflection.md)（Wiki 綜合）。

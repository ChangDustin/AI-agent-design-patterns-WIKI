---
title: Self-Refine（自我回饋改寫）
type: concept
sources: [madaan-2023-self-refine, ng-2024-agentic-patterns]
updated: 2026-11-12
---

# Self-Refine（自我回饋改寫）

> [反思](reflection.md)最具代表性的研究實作：同一個模型負責生成、回饋、改寫。是 Ng 在反思篇推薦的第一篇論文。

## 一句話定義

讓同一個 LLM 先產生初稿、再對自己的初稿給出具體回饋、接著依回饋改寫，反覆到滿足停止條件為止；不需要訓練資料、額外訓練或強化學習（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 生活比喻

寫 email 跟同事要資料：第一版寫「資料趕快寄給我」，回頭一看覺得不禮貌，改成「嗨，方便的時候可以把資料寄給我嗎？」（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 運作步驟

1. **生成**：用「生成提示」產生初稿（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
2. **回饋**：同一個模型用「回饋提示」評自己的初稿；回饋要可行動（給出具體做法）又具體（點出要改的地方）（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
3. **改寫**：同一個模型用「改寫提示」依回饋改出新版本；提示裡附上歷次的稿子和回饋，避免重犯錯誤（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
4. **停止**：做到固定輪數，或回饋表示不必再改時停止；論文的實驗上限是 4 輪（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 例子

- **具體回饋**：「這段程式用 for 迴圈暴力計算所以很慢，改用公式 n(n+1)/2 會更好」（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **整體成績**：7 種任務、三種 GPT 模型，平均絕對提升約 20%（範圍 5～40%）（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **最亮眼**：對話回應，GPT-4 的人類偏好分數從 25.4% 提升到 74.6%（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **幾乎沒用**：數學推理，GPT-4 從 92.9% 到 93.1%（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **改良網站**：從簡單的初版開始，一輪輪改良 HTML、CSS、JS，讓網站更好用、更好看（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 什麼時候用、什麼時候別用

- **適合**：目標有很多面向、或好壞難以一次說清的任務，例如對話回應、提升程式可讀性（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **適合**：要同時滿足很多條件、第一次容易漏掉的任務，例如用上 30 個指定詞造句（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **別用**：模型抓不到自己細微錯誤的任務，例如數學推理；ChatGPT 的回饋有 94% 是「看起來都對」（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **別用**：基礎模型太弱時；Vicuna-13B 連回饋格式都產不出來，給它正確回饋也不會照著改（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **輪數**：每多一輪進步越少，例如程式最佳化 22.0 → 27.0 → 27.9 → 28.8（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 常見誤解

- **「有效只是因為多生了幾份」**：它的結果勝過直接生成 4 份中的每一份，關鍵是「依回饋改寫」（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **「越改一定越好」**：多面向任務可能這裡改好、那裡改壞，所以要替各面向打分數、挑最好的版本（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **「改失敗是因為改寫能力不夠」**：失敗案例中 94% 出在回饋（33% 指錯地方、61% 建議錯改法），只有 6% 是改寫沒照做（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 相關概念

- [反思](reflection.md)：Self-Refine 是反思的「單一模型版」。
- [LLM 回饋與自我評估](llm-feedback.md)：回饋品質決定成敗。
- [代理的限制與風險](agent-limitations.md)：自評的盲點。

## 來源

- [Madaan 2023](../sources/madaan-2023-self-refine.md)
- [Ng 2024，Part 2](../sources/ng-2024-agentic-patterns.md)（推薦閱讀）

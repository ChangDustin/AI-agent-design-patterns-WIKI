---
title: LLM 回饋與自我評估
type: concept
sources: [madaan-2023-self-refine, weng-2023-llm-agents, anthropic-2024-building-effective-agents, ng-2024-agentic-patterns, anthropic-2025-multi-agent-research, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# LLM 回饋與自我評估

> 討論 05 決定新增的跨來源概念。反思、評估者—優化者，以及本專案 pipeline 的檢查節點，成敗都取決於「回饋」的品質。

## 一句話定義

讓 LLM 評估一份產出（自己的或別人的）並給出修改建議。它是反思類方法的引擎，但 LLM 的評估有盲點，常常需要外部訊號補強（Wiki 綜合，依 [Madaan 2023](../sources/madaan-2023-self-refine.md)、[Weng 2023](../sources/weng-2023-llm-agents.md)、[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

請同學幫你看報告：說「再寫好一點」沒什麼用，說「第三段的數字沒有附出處，補上來源」才有用；而且同學不是專家時，可能看不出專業上的錯（Wiki 綜合）。

## 運作步驟

1. **說清楚評估標準**：評估者—優化者最適合評估標準清楚的任務（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
2. **要求具體、可行動的回饋**：點出哪裡要改、怎麼改（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。課程的評論者分「值得保留／需要修改／仍需確認」三項回覆，沒問題可以說保留，不必硬找缺點（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
3. **必要時打分數**：多面向的任務替各面向打分，用來判斷有沒有改壞、挑出最好的版本（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。用評分規準（事實正確、引用正確、完整、來源品質）在一次呼叫裡打 0.0～1.0 分並給通過／不通過，最一致、也最接近人類判斷（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
4. **加入外部訊號**：用單元測試、上網查證、由外部告知對錯等方式，補強 LLM 的判斷（[Ng 2024](../sources/ng-2024-agentic-patterns.md)；[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 例子

- **回饋品質的影響**：情感改寫任務中，具體回饋 43.2、籠統回饋 31.2、沒有回饋 0（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **自評的盲點**：數學推理中，ChatGPT 的回饋 94% 是「看起來都對」；改由外部告知答案錯了，進步就明顯變大（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **專業領域**：ChemCrow 的 LLM 評分和化學專家的評分結論相反（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **LLM 當評審**：GPT-4 代替人評分，和人類偏好的一致率約 68～82%（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **外部訊號**：寫程式的代理可以用自動測試驗證，但人工審查仍然必要（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **人工抓到的盲點**：人工測試發現研究代理偏好 SEO 內容農場，自動評估沒抓到（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 什麼時候用、什麼時候別用

- **適合**：人給回饋時 LLM 的回答確實會變好，而且 LLM 自己也給得出這種回饋的任務（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **效果特別好**：好壞偏主觀、面向很多的任務，例如對話回應（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **別只靠它**：錯誤很細微（數學）或需要專業判斷（化學）時，LLM 自評容易說「看起來都對」，要加上程式檢查、外部查證或專家（Wiki 綜合，依 [Madaan 2023](../sources/madaan-2023-self-refine.md) 與 [Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **別用弱模型當評審**：小模型可能連回饋格式都產不出來（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **數得出來的交給程式**：字數、價格這類可以計算的東西交給 Python，不要請模型估（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 常見誤解

- **「LLM 說沒問題就是沒問題」**：一條看起來通順的推理就能騙過模型（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **「有回饋就好，內容不重要」**：籠統的回饋幫助有限，要具體到能直接動手改（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **「LLM 評審等於人類評審」**：一致率大約七、八成，好用但不完美（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **「換一個模型評論，就是獨立查核」**：換模型也不等於事實查核，外部事實仍要查可靠來源（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 相關概念

- [反思](reflection.md)、[Self-Refine](self-refine.md)：回饋是它們的引擎。
- [代理的限制與風險](agent-limitations.md)：自評有盲點。
- [如何評估代理](agent-evaluation.md)：把 LLM 評審放進整體的評估流程。
- [提示鏈](prompt-chaining.md)：閘門可以是程式檢查，不一定要叫 LLM 判斷。

## 來源

- [Madaan 2023](../sources/madaan-2023-self-refine.md)
- [Weng 2023](../sources/weng-2023-llm-agents.md)（ChemCrow）
- [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)（評估者—優化者的適用條件）
- [Ng 2024](../sources/ng-2024-agentic-patterns.md)（用工具驗證輸出）
- [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)（評分規準、人工測試）
- [Tsai 2026](../sources/tsai-2026-agent-notebooks.md)（評論者的提示設計）

---
title: 反思（Reflection）
type: concept
sources: [ng-2024-agentic-patterns, anthropic-2024-building-effective-agents, weng-2023-llm-agents, madaan-2023-self-refine, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# 反思（Reflection）

> Ng 四大模式之一，穩定度高。別名：**評估者—優化者（Evaluator-optimizer）**，是 Anthropic 的五種[工作流程](workflow-vs-agent.md)之一。
> **三種分類法**（討論 03 決定並陳）：Ng 把反思當成獨立模式；Anthropic 把它歸為一種工作流程；Weng 把它放在代理的「規劃」元件底下。三者講的是同一個機制。

## 一句話定義

讓 LLM 檢查自己剛產出的結果、提出具體改進建議，再依建議重寫（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
Anthropic 把「一個呼叫負責生成、另一個負責評估並給回饋，反覆循環」的版本稱為評估者—優化者（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

寫完作文先自己訂正一遍，或請同學幫忙挑毛病，再改出第二版（Wiki 綜合：討論 01 選定的教學比喻）。

## 運作步驟

1. **生成**：請 LLM 完成任務，例如寫一段程式（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
2. **批評**：把產出貼回給 LLM，請它從正確性、風格、效率等面向提出建設性批評（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
3. **重寫**：把「原產出＋批評」一起交給 LLM，請它依建議改寫（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
4. **重複**：在迴圈中反覆評估和修改，可能持續改進（[Ng 2024](../sources/ng-2024-agentic-patterns.md)；[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 例子

- **寫程式**：生成程式碼 → 請模型檢查正確性、風格、效率 → 依建議重寫（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **加上工具**：先跑幾個單元測試，或上網查證文字內容，再根據找到的錯誤反思（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **雙代理版**：一個代理專門產出、另一個專門給建設性批評，兩者的對話讓回答變好（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **課程實作（Python 心形圖貼文）**：需求 → 初稿 → 評論 → 第二版，是同一個模型的三次普通呼叫；評論分「值得保留／需要修改／仍需確認」（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **寫 email**：第一版「資料趕快寄給我」，回頭一看覺得不禮貌，改成「嗨，方便的時候可以把資料寄給我嗎？」（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **[Self-Refine](self-refine.md) 的成績**：同一個模型自己回饋、自己改，7 種任務平均進步約 20%；對話回應從 25.4% 提升到 74.6%（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **文學翻譯**：負責翻譯的 LLM 一開始可能抓不到細微的語感，負責評估的 LLM 可以給出有用的批評（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **複雜搜尋**：需要搜很多輪的任務，由評估者決定還要不要再搜（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **Reflexion**：每次嘗試後把反思寫進工作記憶（最多三則）當下次的參考；並用規則偵測「走太久還沒成功」或「連續重複同一個動作、得到同樣結果」（視為幻覺），就停下來重來（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 什麼時候用、什麼時候別用

- **適合**：寫程式、寫作、回答問題這類「產出可以被檢查、也有改進空間」的任務（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **適用條件**：評估標準清楚，而且反覆修改能帶來看得見、量得到的進步（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **兩個徵兆**：一是人給回饋時，LLM 的回答確實會變好；二是 LLM 自己也給得出這種回饋（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **CP 值高**：實作相對快，Ng 在一些應用中看到意外大的提升，並認為它能穩定運作（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **輪數**：Self-Refine 實驗最多 4 輪，每多一輪進步越少（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **先定標準**：沒說清楚什麼是好文章，評論者可能只是把文章拉長（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **評論者要看到原始需求**：只給初稿，它不知道讀者、限制，也不知道哪些內容是編出來的（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **別用的時機**：評估標準說不清楚、改了也量不出差別，或模型給不出有用的回饋時，反思迴圈只是白花時間和費用（Wiki 綜合，依 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md) 的適用條件反推）。
- **專業領域要小心**：ChemCrow 案例中，LLM 評審認為它和 GPT-4 差不多，化學專家卻判定它遠勝 GPT-4；缺乏專業時，LLM 看不出自己的錯（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **細微錯誤抓不到**：數學推理用 Self-Refine 幾乎沒進步，因為 ChatGPT 的回饋有 94% 是「看起來都對」（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
- **模型太弱**：Vicuna-13B 連回饋格式都產不出來，給它正確回饋也不會照改（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 常見誤解

- **「反思就是模型在腦中想一想」**：這個模式的反思是一次額外的 LLM 呼叫，產出看得見的批評，再拿批評去重寫（Wiki 綜合）。
- **「反思只能自己改自己」**：也可以接工具驗證（單元測試、搜尋），或交給另一個代理當批評者（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **「反思和評估者—優化者是兩種模式」**：兩者描述的是同一件事，Ng 叫反思，Anthropic 叫評估者—優化者（Wiki 綜合，比較 [Ng 2024](../sources/ng-2024-agentic-patterns.md) 與 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **「越改一定越好」**：多面向的任務可能這裡改好、那裡改壞，要替各面向打分數、挑出最好的版本（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。更長、更華麗，也不等於更符合任務（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「評論說什麼就改什麼」**：原始需求優先於評論；課程故意塞一條壞建議（加五個 emoji、編造教授稱讚），測試模型會不會照單全收（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「換一個模型來評論，就等於獨立查核」**：同一個模型可能重複同樣的盲點，換模型也不等於事實查核；外部事實仍要查可靠來源（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「反思只有一種意思」**：AI 小鎮（Generative Agents）的「反思」是把記憶彙整成更高層次的推論，和批評自己產出的反思不同，Weng 也特別提醒這點（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 相關概念

- [代理式工作流程](agentic-workflow.md)：反思是其中最基本的一種。
- [Self-Refine](self-refine.md)：反思的「單一模型版」研究實作。
- [LLM 回饋與自我評估](llm-feedback.md)：回饋品質決定反思的成敗。
- [記憶](memory.md)：Reflexion 把反思的結果存成記憶。
- [代理的限制與風險](agent-limitations.md)：LLM 自評有盲點。
- [工作流程 vs. 代理](workflow-vs-agent.md)：評估者—優化者屬於工作流程。
- [工具使用](tool-use.md)：用工具驗證輸出，是反思的強化版。
- [多代理協作](multi-agent-collaboration.md)：「產出者＋批評者」就是最小的多代理系統。
- [提示鏈](prompt-chaining.md)：閘門沒過就退回重寫，就形成反思迴圈。

## 來源

- [Ng 2024，Part 2](../sources/ng-2024-agentic-patterns.md)
- [Anthropic 2024：Workflow: Evaluator-optimizer](../sources/anthropic-2024-building-effective-agents.md)
- [Weng 2023：Self-Reflection](../sources/weng-2023-llm-agents.md)（Reflexion 透過這篇間接引用）
- [Madaan 2023：Self-Refine](../sources/madaan-2023-self-refine.md)
- [Tsai 2026：Agent01 Reflection](../sources/tsai-2026-agent-notebooks.md)
- 延伸閱讀（尚未 ingest）：CRITIC（Gou 等 2024）

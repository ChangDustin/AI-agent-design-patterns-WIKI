---
title: 工具使用（Tool Use）
type: concept
sources: [ng-2024-agentic-patterns, anthropic-2024-building-effective-agents, weng-2023-llm-agents, yao-2022-react, anthropic-2025-multi-agent-research, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# 工具使用（Tool Use）

> Ng 四大模式之一，穩定度高。也是[增強型 LLM](augmented-llm.md)最常見的一種能力。

## 一句話定義

給 LLM 一組可以「請求呼叫」的函式（搜尋、執行程式、寄信、查行事曆……），讓它能蒐集資訊、採取行動或處理資料，不再只靠模型本身生成文字（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 生活比喻

考試可以帶計算機、查字典：什麼時候該按計算機、要按什麼，還是你自己判斷，但算數不用再靠心算硬猜（Wiki 綜合：討論 01 選定的教學比喻）。

## 運作步驟

1. **介紹工具**：在提示裡描述每個函式做什麼、需要哪些參數（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
2. **提出請求**：LLM 判斷需要工具時，輸出一段特定格式的請求，例如 `{tool: web-search, query: "coffee maker reviews"}`（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。以 Claude 為例，打算用工具時，API 回應裡會帶一個 tool use 區塊（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
3. **程式執行**：外部程式偵測到這段請求，真的去呼叫對應的函式（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。課程的做法是只允許白名單上的工具、先檢查參數型別，不用 `eval`／`exec`（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
4. **結果回傳**：把執行結果放回 LLM 的輸入，讓它接著處理（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 例子

- **課程實作（麥茶 20 杯，預算 800 元夠嗎？）**：第一次 LLM 把問題轉成 JSON 請求（工具 `quote_order`，參數「麥茶」「20」）→ Python 檢查並執行，算出 20 × 30 = 600 元 → 第二次 LLM 依實際結果回答（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **資料一變，結果就變**：把麥茶庫存改成 8 杯，同樣的參數就得到「庫存不足」，不需要重新訓練模型（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **上網搜尋**：問「評價最好的咖啡機是哪台？」，LLM 可能決定上網搜尋、下載幾個網頁當參考（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **執行程式**：問「100 元以 7% 複利存 12 年會變多少？」，與其讓模型直接生成數字，不如讓它寫出 `100 * (1+0.07)**12` 交給 Python 執行（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。答案約 225.22 元（Wiki 綜合，自行驗算）。
- **工具很多時**：如果有上百個工具、放不進提示，就先用啟發式方法挑出這一步最相關的一小組，像 RAG 從大量文字裡挑段落（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **防呆設計**：Anthropic 的 SWE-bench 代理離開根目錄後，常把相對路徑弄錯；把工具改成一律要求絕對路徑後，模型就用得完全正確（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **測工具的代理**：給它一個有缺陷的工具，它會反覆試用、改寫工具說明；之後的代理用新說明，完成任務的時間少了 40%（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **里程碑**：GPT-4 在 2023 年中推出 function calling，讓工具使用走向通用（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **MRKL**：LLM 當路由器，把問題轉給最合適的專家模組；模組可以是神經網路，也可以是計算機、匯率換算、天氣 API 這類符號工具（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **實務例子**：ChatGPT Plugins 和 function calling；工具可以由其他開發者提供（Plugins），也可以自己定義（function calling）（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **ReAct 的陽春工具**：只給 `search[實體]`（回傳 Wikipedia 頁面前 5 句）、`lookup[字串]`（像 Ctrl+F）、`finish[答案]` 三個動作，刻意模擬人查 Wikipedia 的方式，由推理決定要搜什麼、接著搜什麼（[Yao 2022](../sources/yao-2022-react.md)）。
- **API-Bank 評測**：53 個常用 API、264 段標註對話、568 次 API 呼叫；工具使用能力分三級：會呼叫 API → 會找到要用的 API → 會規劃多次呼叫（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 什麼時候用、什麼時候別用

- **適合**：需要最新資訊（搜尋）、精確計算（執行程式），或要真的對外做事（寄信、改行事曆）的時候（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **穩定度**：Ng 認為工具使用和反思一樣，是他能穩定做出效果的模式（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **設計工具要花心思**：工具的定義和說明要像整體 prompt 一樣做提示工程；為 AI 設計的代理—電腦介面（ACI），值得投入和人機介面（HCI）一樣多的心力（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **缺資訊就追問**：使用者沒說杯數時，選 `clarify` 請他補充，不猜參數（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **別指望工具的時候**：模型不會判斷何時、怎麼用工具時。MRKL 實驗中，模型（7B 的 Jurassic1-large）連文字應用題的計算參數都抽不準；工具本身再可靠，模型不會用也沒用（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 常見誤解

- **「模型自己執行了程式、自己上了網」**：模型只是寫出呼叫請求，真正執行的是外面的程式，再把結果餵回去（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **「工具越多越好」**：工具一多就塞不進上下文，必須先挑出相關的子集（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **「工具能跑就好，說明隨便寫」**：Anthropic 做 SWE-bench 代理時，花在調工具上的時間比調整體 prompt 還多（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。說明寫不好會把代理帶到完全錯的方向，例如要找只存在 Slack 的資料卻去搜網路，一開始就注定失敗（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **「輸出格式不重要」**：同樣的內容，有些格式對模型難寫得多，例如程式碼塞進 JSON 要跳脫換行和引號、寫 diff 要先算好改幾行；格式要貼近模型在網路上常見的寫法（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **「會呼叫工具就好，不需要想」**：只做不想的版本，在問答和互動任務上都輸給邊想邊做的 ReAct（[Yao 2022](../sources/yao-2022-react.md)）。
- **「JSON 格式正確，就代表模型理解對了」**：格式正確不代表語意正確，例如預算 800 元不該被誤填成杯數（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「工具使用一定要用 API 原生的 tool calling」**：課程用 prompt 讓模型輸出 JSON，再由 Python 派送；原生介面只是把同樣的傳遞過程標準化（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「模型一定會照格式輸出」**：LLM 可能出現格式錯誤或不聽指令，很多代理程式碼都在處理、解析模型的輸出（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 相關概念

- [增強型 LLM](augmented-llm.md)：工具是增強能力的一種。
- [代理式工作流程](agentic-workflow.md)
- [反思](reflection.md)：用工具（單元測試、搜尋）驗證輸出，是反思的強化版。
- [規劃](planning.md)：規劃常常就是在安排「先用哪個工具、再用哪個」。
- [ReAct](react.md)：把推理和工具呼叫交錯成迴圈。

## 來源

- [Ng 2024，Part 3](../sources/ng-2024-agentic-patterns.md)
- [Anthropic 2024：Appendix 2 Prompt engineering your tools](../sources/anthropic-2024-building-effective-agents.md)
- [Weng 2023：Component Three: Tool Use](../sources/weng-2023-llm-agents.md)
- [Yao 2022](../sources/yao-2022-react.md)（ReAct 的動作空間）
- [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)（工具設計與測工具的代理）
- [Tsai 2026：Agent02 Tool Use](../sources/tsai-2026-agent-notebooks.md)
- 延伸閱讀（尚未 ingest）：Gorilla（Patil 等 2023）、MM-REACT（Yang 等 2023）、Chain-of-Abstraction（Gao 等 2024）

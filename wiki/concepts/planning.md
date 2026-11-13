---
title: 規劃（Planning）
type: concept
sources: [ng-2024-agentic-patterns, anthropic-2024-building-effective-agents, weng-2023-llm-agents, yao-2022-react, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# 規劃（Planning）

> Ng 四大模式之一，穩定度較難預測。在 Anthropic 的分類裡，讓 LLM 自己決定步驟的系統就是[代理](workflow-vs-agent.md)。
> **同名不同義**（討論 07 決定並陳）：(1) **自主規劃**：LLM 自己決定要做哪些步驟（Ng、Anthropic 的代理）；(2) **先計畫再執行**：固定兩步，先寫出可編輯的計畫，再照計畫完成（課程 Agent03，屬於工作流程）。

## 一句話定義

讓 LLM 自己決定要依序執行哪些步驟，把一個大任務拆成小任務來完成（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
Anthropic 把「LLM 動態主導自己的流程和工具使用」的系統稱為代理（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
課程的 Planning 則是先決定要寫什麼、怎麼安排，做成可閱讀、可修改的工作草稿，再交給下一步執行（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 生活比喻

出國前先排行程：決定要去哪些地方、順序怎麼走；遇到景點臨時關閉，就在現場改行程（Wiki 綜合：討論 01 選定的教學比喻）。

## 運作步驟

1. **給目標**：交給 LLM 一個大目標，例如「研究某個主題並寫成報告」（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
2. **拆任務**：LLM 把目標拆成子任務，例如分別查各個子題 → 整合發現 → 撰寫報告（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。拆的方法有三種：簡單提示、任務專用指令、由人提供；最基本的技巧是[思維鏈](chain-of-thought.md)（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
3. **寫計畫**：LLM 用結構化格式寫出計畫，例如依序呼叫哪些工具、每一步的輸入輸出（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
4. **照計畫執行**：程式依計畫一步步執行；過程中出狀況時，代理可以改走別條路（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
5. **看環境回饋**：每一步都從環境拿到實際結果（工具回傳、程式執行結果），用來判斷進度（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
6. **設停止條件、留檢查點**：卡關或到了檢查點就停下來問人；也要設上限（例如最多幾輪）避免失控（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 例子

- **Ng 的現場 demo**：研究代理平常都用網路搜尋，demo 時搜尋 API 卻回傳限流錯誤；代理自己改用 Wikipedia 搜尋完成任務，連 Ng 都忘了有給它這個工具（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **HuggingGPT 簡化例**：「看男孩的照片，畫一個同樣姿勢的女孩」拆成兩步：偵測男孩的姿勢 → 依這個姿勢生成女孩的圖，每一步各用一個工具（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **課程實作（可頌賣完了）**：原事件 → 回應計畫（已知事實、接住失落、兩個正向角度、選用角度和理由、小行動、寫作安排）→ 依「原事件＋計畫」寫貼文（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **HuggingGPT 的四個階段**：任務規劃（把請求拆成多個任務，標明類型、編號、相依關係、參數）→ 選擇專家模型 → 執行 → 彙整回應（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **解程式題的代理**：Anthropic 解 SWE-bench 的代理，依任務描述自己決定要改哪些檔案（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **沒有「想」會怎樣**：ALFWorld 實驗中，只做動作、不寫想法的代理，常把目標拆錯，或忘了目前的狀態；寫想法的 ReAct 會用想法拆目標、追蹤子目標、決定下一步（[Yao 2022](../sources/yao-2022-react.md)）。

## 什麼時候用、什麼時候別用

- **適合**：複雜任務、沒辦法事先把步驟寫死的時候，讓代理動態決定（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **交給代理的條件**：開放式問題、無法預測要幾步，而且你夠信任模型的判斷（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **不需要時**：很多流程其實用不到規劃，例如「固定反思幾輪」的步驟是確定的（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **代價**：規劃很強大，但結果比較難預測；Ng 認為它不如反思、工具使用成熟（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **防護**：自主代表成本更高、錯誤可能一路累積，要在沙盒裡充分測試並加上防護（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **普遍的限制**：長程規劃和任務拆解仍然困難，LLM 遇到意外錯誤時不太會調整計畫（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **先計畫再執行的好處**：中間成果可讀、可改，也能分辨問題出在「計畫不合適」還是「沒照計畫寫」（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **先計畫再執行的代價**：多一次呼叫、更多 token 和延遲；錯誤的計畫也會傳到下游（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 常見誤解

- **「所有代理都需要規劃」**：步驟能事先定好的話，固定流程更可預測（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **「規劃就是寫一份待辦清單」**：重點是 LLM 依情況動態決定步驟，連開發者都可能沒料到它會怎麼走（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **「代理開始跑之後就不用人管」**：代理可以在檢查點或卡關時停下來請人回饋，也應該設停止條件（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **「規劃就是思維鏈」**：思維鏈用中間推理步驟連接問題和結論；規劃是先決定子任務、需要的資料和順序再執行，兩者可以結合，但不是同一件事（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「有了計畫，寫作者就不需要原始資料」**：只給計畫，事實可能在摘要中遺失；下一步要同時拿到原事件和計畫，而且事實優先於計畫（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「代理遇到意外一定會隨機應變」**：Ng 的 Wikipedia 故事是一則成功軼事；Weng 指出一般而言 LLM 遇到意外錯誤很難調整計畫，軼事不代表普遍（Wiki 綜合，比較 [Ng 2024](../sources/ng-2024-agentic-patterns.md) 與 [Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 相關概念

- [工作流程 vs. 代理](workflow-vs-agent.md)：會自己規劃的系統屬於代理。
- [思維鏈](chain-of-thought.md)：拆解任務最基本的技巧。
- [ReAct](react.md)：邊想邊做，在迴圈裡隨時調整計畫。
- [代理的限制與風險](agent-limitations.md)：規劃是最容易出包的環節之一。
- [人在迴圈中](human-in-the-loop.md)：可編輯的計畫是人介入的位置。
- [工具使用](tool-use.md)：計畫裡的每一步常常就是一次工具呼叫。
- [協調者—工作者](orchestrator-workers.md)：協調者的動態拆解是一種規劃。
- [多代理協作](multi-agent-collaboration.md)：拆好的子任務可以交給不同角色。
- [代理式工作流程](agentic-workflow.md)

## 來源

- [Ng 2024，Part 4](../sources/ng-2024-agentic-patterns.md)
- [Anthropic 2024：Agents](../sources/anthropic-2024-building-effective-agents.md)
- [Weng 2023：Component One: Planning](../sources/weng-2023-llm-agents.md)
- [Yao 2022](../sources/yao-2022-react.md)（ALFWorld 的對照實驗）
- [Tsai 2026：Agent03 Planning](../sources/tsai-2026-agent-notebooks.md)
- 延伸閱讀（尚未 ingest）：Chain-of-Thought（Wei 等 2022）、HuggingGPT（Shen 等 2023）、LLM 代理規劃綜述（Huang 等 2024）

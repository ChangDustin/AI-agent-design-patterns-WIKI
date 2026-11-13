---
title: 思維鏈（Chain-of-Thought, CoT）
type: concept
sources: [weng-2023-llm-agents, ng-2024-agentic-patterns, yao-2022-react, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# 思維鏈（Chain-of-Thought, CoT）

> [規劃](planning.md)的基本技巧。[ReAct](react.md) 把它和「行動」接在一起。

## 一句話定義

在提示中要求模型「一步一步想」，讓它在推論時多花一些計算，把困難的任務拆成比較小、比較簡單的步驟（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 生活比喻

解數學應用題時把算式一行一行寫出來，而不是直接猜答案；寫出來的過程也讓老師看得懂你怎麼想的（Wiki 綜合）。

## 運作步驟

1. **下指示**：在提示裡加上「一步一步想」之類的指示（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
2. **寫出過程**：模型先寫出中間的推理步驟，再給答案（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
3. **進階版思維樹（Tree of Thoughts）**：每一步產生好幾個可能的想法，形成一棵樹，再用廣度優先或深度優先搜尋，並用提示或投票評估每個狀態（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 例子

- **簡單提示**：「XYZ 的步驟：1.」或「達成 XYZ 的子目標有哪些？」（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **任務專用指令**：寫小說時先下「寫故事大綱」（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **推薦閱讀**：Ng 把思維鏈論文（Wei 等 2022）列為規劃模式的延伸閱讀（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **自洽投票（CoT-SC）**：抽 21 條思維鏈、取多數的答案，表現穩定勝過單一條思維鏈（[Yao 2022](../sources/yao-2022-react.md)）。

## 什麼時候用、什麼時候別用

- **適合**：需要好幾個推理步驟的複雜任務（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **附帶好處**：寫出來的步驟，讓人比較能理解模型怎麼思考（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **需要查證事實時，別只靠它**：思維鏈只用模型內部的知識推理，是沒和外界接軌的「靜態黑盒子」，容易幻覺、錯誤一路傳下去；HotpotQA 上，思維鏈失敗的案例有 56% 是幻覺（[Yao 2022](../sources/yao-2022-react.md)）。

## 常見誤解

- **「思維鏈就是代理」**：思維鏈只是讓模型在一次回答裡多想幾步；代理還要和環境互動、用工具、看回饋（Wiki 綜合，依 [Weng 2023](../sources/weng-2023-llm-agents.md) 的元件拆解）。
- **「推理寫得越完整，答案越可靠」**：思維鏈的推理結構常常是對的，但裡面的事實可能是編的（[Yao 2022](../sources/yao-2022-react.md)）。
- **「思維鏈就是規劃」**：思維鏈用中間推理步驟連接問題和結論；規劃是先決定子任務和順序再執行，兩者可以結合（例如 Plan-and-Solve），但不是同一件事（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「看得到的推理步驟，就是模型真正的思考」**：對外寫出的計畫或簡短理由，不能當成模型私有推理的完整紀錄（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 相關概念

- [規劃](planning.md)：思維鏈是拆解任務最基本的方法。
- [ReAct](react.md)：把推理和工具呼叫交錯進行。
- [平行化](parallelization.md)：自洽投票就是「投票」的一種。

## 來源

- [Weng 2023：Task Decomposition](../sources/weng-2023-llm-agents.md)
- [Ng 2024，Part 4](../sources/ng-2024-agentic-patterns.md)（推薦閱讀）
- [Yao 2022](../sources/yao-2022-react.md)（思維鏈的侷限與 CoT-SC）
- [Tsai 2026：Agent03 Planning](../sources/tsai-2026-agent-notebooks.md)（CoT 與 Planning 的區分）

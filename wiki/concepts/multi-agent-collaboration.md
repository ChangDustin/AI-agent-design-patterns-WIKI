---
title: 多代理協作（Multi-agent Collaboration）
type: concept
sources: [ng-2024-agentic-patterns, anthropic-2024-building-effective-agents, weng-2023-llm-agents, anthropic-2025-multi-agent-research]
updated: 2026-11-12
---

# 多代理協作（Multi-agent Collaboration）

> Ng 四大模式之一，穩定度較難預測。

## 一句話定義

讓多個「代理」分工合作，各自處理子任務、互相討論，得到比單一代理更好的結果；這些代理通常是用不同提示讓同一個（或多個）LLM 扮演不同角色（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 生活比喻

分組報告各司其職：有人查資料、有人做投影片、有人負責檢查，最後整合成一份（Wiki 綜合：討論 01 選定的教學比喻）。
Ng 自己的比喻是公司主管：先決定要雇哪些角色，再把大專案拆給不同專長的人（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
多代理研究系統也像研究小組：組長分派題目，組員各自查資料、交回摘要（Wiki 綜合：討論 06 選定的教學比喻）。

## 運作步驟

1. **拆角色**：拆解任務，決定需要哪些角色，例如軟體工程師、產品經理、設計師、QA（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
2. **寫角色提示**：為每個角色寫提示，例如「你是擅長寫清楚、有效率程式碼的專家……」（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
3. **各做各的**：每個代理有自己的工作流程和記憶，也可以規劃、使用工具（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
4. **互相溝通**：代理之間傳遞訊息、互相求助，最後整合出成果（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
5. **避免傳話遊戲**：子代理把成果直接存成檔案，只把位置交回主代理，避免資訊在一手手轉述中失真（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 例子

- **ChatDev**：一群代理經營一間「虛擬軟體公司」的開源專案（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **[Claude Research](../entities/claude-research.md)**：主代理同時派出多個子代理分頭搜尋，在內部研究評測中比單代理好 90.2%（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **[AI 小鎮（Generative Agents）](../entities/generative-agents.md)**：25 個由 LLM 控制的角色在沙盒裡生活互動，自然出現消息傳播、記得人際關係、一起辦派對等社交行為（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **反思的雙代理版**：一個代理負責產出、另一個專門批評（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **Anthropic 的結構化版本**：[協調者—工作者](orchestrator-workers.md)（中央 LLM 動態分派）和[平行化](parallelization.md)（同時分工或投票），都可以看成多個 LLM 的協作（Wiki 綜合，依 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **常見框架**：AutoGen、Crew AI、[LangGraph](../entities/langgraph.md)（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 什麼時候用、什麼時候別用

- **理由一：實際有效**。AutoGen 論文的消融實驗顯示，多代理勝過單一代理（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **理由二：一次專注一件事**。模型就算吃得下很長的輸入，真正理解長而複雜內容的能力也參差不齊；拆成角色能讓每次呼叫聚焦（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **Anthropic 也觀察到**：任務有多個面向時，每個面向交給一次獨立的呼叫，模型通常表現更好（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **理由三：好用的思考框架**。就像寫程式時拆成多個 process／thread，多代理給開發者一個拆解任務的方法（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **理由四：花了足夠的 token**。Anthropic 發現 token 用量一項就解釋了 80% 的表現差異；多代理用各自的上下文視窗平行探索，等於加大了推理的容量（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **適合**：高度可平行、資訊量超過單一上下文、需要用很多複雜工具的高價值任務，例如研究（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **代價**：代理自由互動、又有多種工具時，輸出品質很難預測；Ng 認為它和規劃一樣不如反思、工具使用成熟（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **很燒錢**：多代理的 token 用量約為一般聊天的 15 倍（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **可靠性可以靠工程補（較新的看法）**：Ng 在 2024 年認為多代理難預測；Anthropic 在 2025 年指出，經過謹慎的工程、完整測試、仔細的提示與工具設計，多代理研究系統可以大規模可靠運作（Wiki 綜合，比較 [Ng 2024](../sources/ng-2024-agentic-patterns.md) 與 [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **不適合**：需要所有代理共享同一份上下文、或代理之間高度相依的任務，例如多數寫程式的任務；代理目前也不擅長即時協調彼此（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **用框架要小心**：框架的抽象層可能遮住底下的 prompt 和回應，讓除錯變難（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 常見誤解

- **「多代理就要用很多個不同的模型」**：多個代理可以只是同一個 LLM 的多次呼叫，換不同提示扮演不同角色（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。
- **「代理越多、互動越自由就越好」**：自由互動的多代理系統結果很難預測（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）；Anthropic 早期的研究代理還曾為一個簡單問題派出 50 個子代理（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **「多代理有效，只是因為分工比較專心」**：Anthropic 認為主要原因是能花足夠的 token、在多個獨立上下文裡平行推理；這和 Ng「一次專注一件事」的解釋不同，但不矛盾（Wiki 綜合，比較 [Ng 2024](../sources/ng-2024-agentic-patterns.md) 與 [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 相關概念

- [協調者—工作者](orchestrator-workers.md)、[平行化](parallelization.md)：Anthropic 對多個 LLM 協作的結構化分類。
- [如何評估代理](agent-evaluation.md)：多代理系統要用結果導向的方式評估。
- [反思](reflection.md)、[規劃](planning.md)、[工具使用](tool-use.md)：每個代理內部也可以用這些模式。
- [代理式工作流程](agentic-workflow.md)

## 來源

- [Ng 2024，Part 5](../sources/ng-2024-agentic-patterns.md)
- [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)
- [Weng 2023：Generative Agents Simulation](../sources/weng-2023-llm-agents.md)
- [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)（Claude Research）
- 延伸閱讀（尚未 ingest）：ChatDev（Qian 等 2023）、AutoGen（Wu 等 2023）、MetaGPT（Hong 等 2023）

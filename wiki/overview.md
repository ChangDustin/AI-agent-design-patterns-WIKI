---
title: AI 代理設計模式總覽
type: overview
sources: [ng-2024-agentic-patterns, anthropic-2024-building-effective-agents, weng-2023-llm-agents, yao-2022-react, madaan-2023-self-refine, anthropic-2025-multi-agent-research, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# AI 代理設計模式總覽

> 已 ingest 7／7 篇（全部完成）。這頁是 Wiki 對整個主題「目前的理解」，每進來一篇資料就重新檢視一次。

## 一句話

AI 代理不是一個更聰明的模型，而是讓同一個模型**分多步工作的系統設計**，而且能簡單就簡單（Wiki 綜合，依據 [Ng 2024](sources/ng-2024-agentic-patterns.md) 與 [Anthropic 2024](sources/anthropic-2024-building-effective-agents.md)）。

## 視角一：誰決定下一步？（複雜度的階梯）

```
複雜度、成本、彈性 ↑　　可預測性 ↓
│
├─ 代理（Agent）……………… LLM 在迴圈裡自己決定步驟和工具（像自由行）
├─ 工作流程（Workflow）…… 程式寫死路徑：提示鏈／路由／平行化／協調者—工作者／評估者—優化者（像跟團）
├─ 增強型 LLM ……………… 單次呼叫＋檢索、工具、記憶
└─ 單次 LLM 呼叫 …………… 先從這裡開始！
```

依 [Anthropic 2024](sources/anthropic-2024-building-effective-agents.md)：先從最下面開始，只有證明有用才往上爬。

## 視角二：用了哪些招式？（Ng 的四種模式＝零件）

```
├── 反思 Reflection ............ 自己檢查、自己改            穩定度：高
├── 工具使用 Tool Use .......... 會按計算機、會上網查        穩定度：高
├── 規劃 Planning .............. 自己拆步驟、隨機應變        穩定度：較難預測
└── 多代理協作 Multi-agent ..... 分角色合作、互相討論        穩定度：較難預測
```

穩定度依 [Ng 2024](sources/ng-2024-agentic-patterns.md) 的實務經驗判斷。

## 視角三：代理由什麼組成？（解剖圖）

```
代理 ＝ 大腦（LLM）
     ＋ 規劃：拆解子目標（思維鏈）、反思修正
     ＋ 記憶：短期＝上下文（書桌桌面）；長期＝向量資料庫（書櫃）
     ＋ 工具：呼叫外部 API（搜尋、計算、執行程式）
```

依 [Weng 2023](sources/weng-2023-llm-agents.md)。

## 從模式走到代理：ReAct 這座橋

```
想法（Thought）→ 動作（Action）→ 觀察（Observation）→ 想法 → … → 完成
   └ 思維鏈          └ 工具使用          └ 環境回饋
```

把「想」（[思維鏈](concepts/chain-of-thought.md)）和「做」（[工具使用](concepts/tool-use.md)）放進迴圈、依環境回饋決定下一步，就是 Anthropic 說的代理；[ReAct](concepts/react.md) 是它最小的原型（Wiki 綜合，依 [Yao 2022](sources/yao-2022-react.md) 與 [Anthropic 2024](sources/anthropic-2024-building-effective-agents.md)）。

## Ng 與 Anthropic 對照

| Ng 2024 的模式 | Anthropic 2024 的對應 | 備註 |
|---|---|---|
| [反思](concepts/reflection.md) | 評估者—優化者 | 同一件事，兩個名字；Weng 則把它歸在「規劃」底下 |
| [工具使用](concepts/tool-use.md) | [增強型 LLM](concepts/augmented-llm.md)的工具能力＋ACI 原則 | Anthropic 更強調工具本身的設計 |
| [規劃](concepts/planning.md) | 代理；[協調者—工作者](concepts/orchestrator-workers.md)的動態拆解 | 都是「LLM 自己決定步驟」 |
| [多代理協作](concepts/multi-agent-collaboration.md) | [協調者—工作者](concepts/orchestrator-workers.md)、[平行化](concepts/parallelization.md) | Anthropic 依結構分類，不強調角色扮演 |
| （沒有對應） | [提示鏈](concepts/prompt-chaining.md)、[路由](concepts/routing.md) | Ng 的四種模式沒有涵蓋 |

（對照表為 Wiki 綜合）

## 目前的綜合理解

1. **流程可能比模型更重要**：HumanEval 上，GPT-3.5 加代理迴圈（最高 95.1%）勝過 GPT-4 一次生成（67.0%）（[Ng 2024](sources/ng-2024-agentic-patterns.md)）。
2. **但複雜度要證明有用才加**：先用單次呼叫，不夠再用工作流程，最後才考慮代理（[Anthropic 2024](sources/anthropic-2024-building-effective-agents.md)）。
3. **熱情與節制不矛盾**：Ng 描繪代理式流程的潛力，Anthropic 提醒延遲、成本和錯誤累積；兩者一起看，才知道什麼時候該用（Wiki 綜合）。
4. **越自主越難預測**：三篇都同意規劃這類「讓 AI 自己決定」的能力最不穩；Ng 的成功軼事不代表普遍（[Ng 2024](sources/ng-2024-agentic-patterns.md)；[Anthropic 2024](sources/anthropic-2024-building-effective-agents.md)；[Weng 2023](sources/weng-2023-llm-agents.md)）。
5. **同一個機制，三種分類**：反思在 Ng 是獨立模式、在 Anthropic 是工作流程、在 Weng 是規劃的一部分；分類不同，講的是同一件事（Wiki 綜合）。
6. **代理會出包，自評也有盲點**：上下文有限、輸出格式不可靠、專業領域裡 LLM 評不出自己的錯，所以檢查不能只靠 LLM 自己（[Weng 2023](sources/weng-2023-llm-agents.md)；詳見[代理的限制與風險](concepts/agent-limitations.md)）。
7. **模式可以組合**：反思可以加工具、也可以拆成兩個代理；本專案的簡報 pipeline 就是「提示鏈＋閘門＋評估者—優化者迴圈」的組合（Wiki 綜合）。
8. **接上外界能減少瞎掰，但會帶來新問題**：只靠思維鏈時失敗案例 56% 是幻覺，ReAct 是 0%；可是 ReAct 會卡迴圈、被沒用的搜尋結果帶歪（[Yao 2022](sources/yao-2022-react.md)）。
9. **「卡迴圈」三篇互相印證**：ReAct 實測最常見的錯誤之一、Reflexion 用規則偵測重複動作、Anthropic 要求設停止條件（Wiki 綜合，依 [Yao 2022](sources/yao-2022-react.md)、[Weng 2023](sources/weng-2023-llm-agents.md)、[Anthropic 2024](sources/anthropic-2024-building-effective-agents.md)）。

10. **反思的瓶頸在回饋品質**：Self-Refine 平均進步約 20%，數學推理卻幾乎沒進步（回饋 94% 說「看起來都對」）；改失敗時 94% 是回饋的錯。這和 Anthropic 的適用條件、Weng 的 ChemCrow 互相印證：檢查要有外部訊號，不能只靠 LLM 自評（[Madaan 2023](sources/madaan-2023-self-refine.md)；詳見 [LLM 回饋與自我評估](concepts/llm-feedback.md)）。
11. **迭代有邊際效益遞減，也可能改壞**：輪數要設上限，並保留最好的版本（[Madaan 2023](sources/madaan-2023-self-refine.md)）。
12. **多代理有效，主要靠花足夠的 token**：在多個獨立上下文裡平行推理，研究評測比單代理好 90.2%；但 token 約為聊天的 15 倍，只適合高價值、可平行的任務。這和 Ng「一次專注一件事」的解釋並陳（[Anthropic 2025](sources/anthropic-2025-multi-agent-research.md)；[Ng 2024](sources/ng-2024-agentic-patterns.md)）。
13. **評估代理要看結果、及早開始**：小樣本起步、LLM 評審配評分規準（事實正確、引用正確、完整）、人工測試不可少（[Anthropic 2025](sources/anthropic-2025-multi-agent-research.md)；詳見[如何評估代理](concepts/agent-evaluation.md)）。

14. **「規劃」同名不同義**：Ng、Anthropic 的規劃是 LLM 自主決定步驟（代理）；課程的 Planning 是「先寫可編輯的計畫，再照計畫執行」的固定兩步（工作流程）。CoT 可以用來拆解任務，但 CoT 不等於規劃（[Ng 2024](sources/ng-2024-agentic-patterns.md)；[Tsai 2026](sources/tsai-2026-agent-notebooks.md)；詳見[規劃](concepts/planning.md)）。
15. **課程的實作觀點和 Anthropic 一致**：流程寫清楚、不藏進自動迴圈；資料要明確傳遞；資料不是指令；程式能確認的交給程式；最後由人把關（[Tsai 2026](sources/tsai-2026-agent-notebooks.md)；[Anthropic 2024](sources/anthropic-2024-building-effective-agents.md)；詳見[人在迴圈中](concepts/human-in-the-loop.md)）。

## 待解問題

- 7 篇資料已全部 ingest。仍缺來源支持的：增強型 LLM 的「什麼時候別用」（之後可上網找資料補）。
- 第一次正式的 Query 已完成：[根據 Wiki，教學簡報 pipeline 該怎麼設計？](queries/pipeline-design.md)。

## 頁面導覽

- 總框架：[工作流程 vs. 代理](concepts/workflow-vs-agent.md)、[代理式工作流程](concepts/agentic-workflow.md)、[增強型 LLM](concepts/augmented-llm.md)
- 代理的元件與技巧：[記憶](concepts/memory.md)、[思維鏈](concepts/chain-of-thought.md)、[ReAct](concepts/react.md)
- Ng 的四種模式：[反思](concepts/reflection.md)（研究實作：[Self-Refine](concepts/self-refine.md)；引擎：[LLM 回饋與自我評估](concepts/llm-feedback.md)）、[工具使用](concepts/tool-use.md)、[規劃](concepts/planning.md)、[多代理協作](concepts/multi-agent-collaboration.md)
- Anthropic 的工作流程：[提示鏈](concepts/prompt-chaining.md)、[路由](concepts/routing.md)、[平行化](concepts/parallelization.md)、[協調者—工作者](concepts/orchestrator-workers.md)、評估者—優化者（見[反思](concepts/reflection.md)）
- 限制、評估與人的角色：[代理的限制與風險](concepts/agent-limitations.md)、[如何評估代理](concepts/agent-evaluation.md)、[人在迴圈中](concepts/human-in-the-loop.md)
- 來源：[Ng 2024](sources/ng-2024-agentic-patterns.md)、[Anthropic 2024](sources/anthropic-2024-building-effective-agents.md)、[Weng 2023](sources/weng-2023-llm-agents.md)、[Yao 2022](sources/yao-2022-react.md)、[Madaan 2023](sources/madaan-2023-self-refine.md)、[Anthropic 2025](sources/anthropic-2025-multi-agent-research.md)、[Tsai 2026](sources/tsai-2026-agent-notebooks.md)
- 人物、組織、工具、案例：[Andrew Ng](entities/andrew-ng.md)、[Anthropic](entities/anthropic.md)、[Lilian Weng](entities/lilian-weng.md)、[蔡炎龍](entities/tsai-yen-lung.md)、[LangGraph](entities/langgraph.md)、[AISuite](entities/aisuite.md)、[Groq](entities/groq.md)、[Generative Agents](entities/generative-agents.md)、[Claude Research](entities/claude-research.md)

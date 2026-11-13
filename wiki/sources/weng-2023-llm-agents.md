---
title: Lilian Weng〈LLM Powered Autonomous Agents〉
type: source
sources: [weng-2023-llm-agents]
updated: 2026-11-12
---

# Lilian Weng〈LLM Powered Autonomous Agents〉

## 基本資訊

| 項目 | 內容 |
|---|---|
| 作者 | [Lilian Weng](../entities/lilian-weng.md) |
| 日期 | 2023-06-23 |
| 類型 | 技術部落格 Lil'Log 的綜述長文 |
| 網址 | <https://lilianweng.github.io/posts/2023-06-23-agent/> |
| raw | `raw/weng-2023-llm-agents/source.md` |
| 討論紀錄 | [討論 03](../../discussions/03-weng-2023-llm-agents.md) |

## 一段話摘要

Weng 把「以 LLM 為核心控制器的自主代理」拆成一個大腦加三個元件：規劃（拆解任務、反思修正）、記憶（短期的上下文、長期的外部向量資料庫）、工具使用（呼叫外部 API）。她逐一整理各元件的代表研究（CoT、ToT、ReAct、Reflexion、MRKL、Toolformer、HuggingGPT、API-Bank），再用 ChemCrow、科學研究代理、Generative Agents、AutoGPT、GPT-Engineer 等案例說明代理實際的樣子，最後點出三大挑戰：上下文有限、長期規劃困難、自然語言介面不可靠。

## 重點

1. 代理＝LLM 大腦＋規劃＋記憶＋工具使用。
2. **規劃**：思維鏈（CoT）讓模型一步一步想；思維樹（ToT）每一步產生多個想法，再用 BFS／DFS 搜尋；拆解可以用簡單提示、任務專用指令，或由人提供。LLM+P 則把長程規劃外包給傳統規劃器（PDDL）。
3. **反思**（Weng 把它歸在規劃底下）：ReAct 讓「想、做、看」交錯進行，比只做不想的版本好；Reflexion 把反思寫進工作記憶（最多三則），並用規則偵測「沒效率」或「幻覺」（連續重複同一個動作、得到同樣的觀察）時就重來。
4. **記憶**：感覺記憶 ↔ embedding；短期記憶 ↔ 上下文（受限於上下文視窗）；長期記憶 ↔ 外部向量資料庫，查詢時用快速的最大內積搜尋（MIPS，常用近似最近鄰演算法）。
5. **工具**：MRKL 讓 LLM 當路由器，把問題轉給專家模組；實驗中 LLM 抽不準文字應用題的算式參數，所以「何時、如何用工具」才是關鍵。Toolformer、TALM 用微調讓模型學會用 API；ChatGPT Plugins 和 function calling 是實務例子；另有 HuggingGPT 的四階段、API-Bank 的三層級評測。
6. **案例**：ChemCrow（LLM 評分和專家評分的結論相反）、科學研究代理（安全風險：合成化學武器的要求 11 次中有 4 次被接受）、Generative Agents（25 個角色的 AI 小鎮）、AutoGPT、GPT-Engineer（先問釐清問題再寫程式）。
7. **三大挑戰**：上下文長度有限；長期規劃和任務拆解很難（遇到意外錯誤時難以調整計畫）；自然語言介面不可靠（格式錯誤、偶爾不聽指令）。

## 對 Wiki 的影響

- **新增**：[記憶](../concepts/memory.md)、[思維鏈](../concepts/chain-of-thought.md)、[代理的限制與風險](../concepts/agent-limitations.md)、[Lilian Weng](../entities/lilian-weng.md)、[Generative Agents](../entities/generative-agents.md)。
- **修改**：[規劃](../concepts/planning.md)、[反思](../concepts/reflection.md)、[工具使用](../concepts/tool-use.md)（補上「別用的時機」）、[增強型 LLM](../concepts/augmented-llm.md)、[多代理協作](../concepts/multi-agent-collaboration.md)、[總覽](../overview.md)。
- **分類不同**：Weng 把反思放在規劃底下；Ng 當獨立模式；Anthropic 歸為工作流程。依討論 03 的決定，反思維持獨立頁，頁內並陳三種分類。
- **看似矛盾**：Ng 的 Wikipedia 故事（代理成功改走別條路）vs. Weng 的「LLM 遇到意外錯誤時難以調整計畫」。處理方式：軼事不代表普遍，兩篇都同意規劃不夠可靠。
- **互相印證**：ChemCrow 的發現，呼應 Anthropic 說的「LLM 要給得出有用的回饋，才適合用反思」。

## 可用的教學素材

- **比喻**：短期記憶＝書桌桌面、長期記憶＝書櫃（討論 03 選定）。
- **解剖圖**：大腦（LLM）＋規劃＋記憶＋工具。
- **故事**：AI 小鎮：25 個 AI 居民自己傳消息、記得人際關係、一起辦派對。
- **警世故事**：ChemCrow：LLM 評審說和 GPT-4 打平，化學專家說它遠勝 GPT-4。
- **數字**：人的短期記憶大約 7 項、維持 20–30 秒（Miller 1956）。
- **例子**：AutoGPT 的系統提示要求模型輸出包含想法、推理、計畫、自我批評、指令的 JSON。
- **例子**：GPT-Engineer 寫程式前先列出不清楚的地方，一次問一個釐清問題。

## 限制與存疑

- 這是 2023 年中的綜述，AutoGPT 等系統多是概念驗證，現況可能不同。
- 作者自述記憶一節請 ChatGPT 協助起草。
- 對初學者太深、只記在這裡不建概念頁的內容（討論 03 決定）：Chain of Hindsight、Algorithm Distillation（需要微調或強化學習）、MIPS 演算法（LSH、ANNOY、HNSW、FAISS、ScaNN）、LLM+P／PDDL。
- 化學武器測試的樣本很小（11 次）。

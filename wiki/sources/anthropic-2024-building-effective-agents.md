---
title: Anthropic〈Building effective AI agents〉
type: source
sources: [anthropic-2024-building-effective-agents]
updated: 2026-11-12
---

# Anthropic〈Building effective AI agents〉

## 基本資訊

| 項目 | 內容 |
|---|---|
| 作者 | [Anthropic](../entities/anthropic.md)（文末署名 Erik S.、Barry Zhang） |
| 日期 | 2024-12-19 發布；本 Wiki 依 2026-11-12 抓取的修訂版 |
| 類型 | 技術部落格（工程實務建議） |
| 網址 | <https://www.anthropic.com/engineering/building-effective-agents> |
| raw | `raw/anthropic-2024-building-effective-agents/source.md` |
| 討論紀錄 | [討論 02](../../discussions/02-anthropic-2024-building-effective-agents.md) |

## 一段話摘要

Anthropic 根據和數十個團隊合作的經驗指出：最成功的代理式系統，通常不是用複雜框架做的，而是用簡單、可組合的模式。文章先把「工作流程」（照預先寫好的路徑走）和「代理」（LLM 自己決定流程）分開，再從最基本的積木「增強型 LLM」開始，依複雜度介紹五種工作流程和自主代理，最後提出三個原則：簡單、透明、把工具介面設計好。核心建議是先用最簡單的方法，只有在證明有效時才增加複雜度。

## 重點

1. 代理式系統分兩種：**工作流程**（LLM 和工具照預先寫好的程式路徑走）和**代理**（LLM 自己決定流程和工具的使用）。
2. 先找最簡單的解法。代理式系統是用延遲和成本換表現，很多應用只要把單次 LLM 呼叫配上檢索和範例調好就夠了。
3. 框架方便上手，但抽象層會遮住底層的 prompt 和回應、讓除錯變難；建議先直接用 LLM API，真要用框架就要懂它底下做了什麼。
4. 基本積木是**增強型 LLM**：LLM 加上檢索、工具、記憶。
5. 五種工作流程：提示鏈、路由、平行化（分段、投票）、協調者—工作者、評估者—優化者。
6. **代理**＝在迴圈中根據環境回饋使用工具的 LLM。每一步要從環境拿到實際結果、可以在檢查點請人確認、要設停止條件。適合步驟數無法預測的開放問題；代價是成本高、錯誤會累積，需要在沙盒測試並加上防護。
7. 三原則：簡單、透明（把規劃步驟攤開給人看）、用心設計代理—電腦介面（ACI）。
8. 工具定義要和 prompt 一樣用心：格式貼近模型熟悉的寫法、避免格式負擔、做防呆設計。
9. 代理最有價值的兩個應用：客服、寫程式。兩者的共同點是同時需要對話和行動、成功標準清楚、有回饋迴圈、有人監督。

## 對 Wiki 的影響

- **新增**：[工作流程 vs. 代理](../concepts/workflow-vs-agent.md)、[增強型 LLM](../concepts/augmented-llm.md)、[提示鏈](../concepts/prompt-chaining.md)、[路由](../concepts/routing.md)、[平行化](../concepts/parallelization.md)、[協調者—工作者](../concepts/orchestrator-workers.md)、[Anthropic](../entities/anthropic.md)。
- **修改**：[反思](../concepts/reflection.md)（加別名「評估者—優化者」）、[代理式工作流程](../concepts/agentic-workflow.md)（加註用詞）、[工具使用](../concepts/tool-use.md)（ACI、防呆）、[規劃](../concepts/planning.md)、[多代理協作](../concepts/multi-agent-collaboration.md)、[LangGraph](../entities/langgraph.md)、[總覽](../overview.md)。
- **衝突（用詞）**：Ng 的 agentic workflow 泛指所有多步驟流程；這篇的 workflow 專指預先寫好路徑的那種。依討論 02 的決定，Wiki 以這篇的區分為正式定義，Ng 的四種模式定位成零件。
- **重點不同（語氣）**：Ng 熱情、這篇節制，兩者不矛盾，總覽頁並陳。
- **一致**：評估者—優化者就是 Ng 的反思；代理的動態決策對應 Ng 的規劃。
- **張力**：這篇提醒框架會讓 prompt 不透明，和本專案選用 LangGraph 有關；對策記在 LangGraph 頁。

## 可用的教學素材

- **比喻**：工作流程 vs. 代理＝跟團旅行 vs. 自由行（討論 02 選定）。
- **金句（改寫）**：成功不在做出最精密的系統，而在做出最適合需求的系統。
- **例子**：提示鏈：先寫大綱 → 檢查大綱是否合格 → 依大綱寫全文。
- **例子**：路由：客服問題分流；簡單的問題給小模型、困難的給大模型。
- **例子**：平行化：一個模型回答、另一個同時把關不當內容；多個提示一起找程式漏洞（投票）。
- **故事**：SWE-bench 代理常把相對路徑弄錯，改成強制用絕對路徑後就沒再出錯；團隊花在調工具的時間比調 prompt 還多。
- **概念**：防呆（poka-yoke）；代理—電腦介面（ACI）要像人機介面（HCI）一樣用心設計。

## 限制與存疑

- 網頁在 2024-12 發布後修訂過：文中提到的 Claude Haiku 4.5、Sonnet 4.5 在 2024-12 時還不存在，開頭也加註工具生態已經改變（Wiki 綜合）。框架清單與模型名稱以抓取的版本為準。
- 這是 Anthropic 根據自家客戶經驗給的建議，沒有量化數據；也可能偏好自家工具（例如 Claude Agent SDK、MCP）。
- 五種工作流程是「常見模式」，不是完整分類；作者也說可以自由組合、調整。

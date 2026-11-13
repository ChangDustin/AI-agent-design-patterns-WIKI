---
title: ReAct（推理＋行動）
type: concept
sources: [yao-2022-react, weng-2023-llm-agents, anthropic-2024-building-effective-agents]
updated: 2026-11-12
---

# ReAct（推理＋行動）

> 本 Wiki 的定位（討論 04 決定）：[工具使用](tool-use.md)＋[思維鏈](chain-of-thought.md)的結合，也是[代理](workflow-vs-agent.md)最小的原型。Weng 把它放在「自我反思」一節，分類不同。

## 一句話定義

讓 LLM 交錯寫出「想法」和「動作」，再讀回環境的「觀察」，一輪一輪往下走：推理幫忙擬定、追蹤和調整計畫，行動幫忙從外部取得資訊（[Yao 2022](../sources/yao-2022-react.md)）。

## 生活比喻

煮菜：菜切好了，心想「該燒水了」（追蹤進度）；發現沒鹽，想「改用醬油和胡椒」（處理例外）；不會做麵糰，想「上網查一下」（需要外部資訊）；為了想清楚，也會去翻食譜、打開冰箱看看（[Yao 2022](../sources/yao-2022-react.md)）。

## 運作步驟

1. **想法（Thought）**：用文字推理下一步，例如拆解目標、追蹤進度、處理例外；想法不會改變外部環境，只會加進上下文（[Yao 2022](../sources/yao-2022-react.md)）。
2. **動作（Action）**：執行一個任務動作，例如 `search[實體]`、`lookup[字串]`、`finish[答案]`（[Yao 2022](../sources/yao-2022-react.md)）。
3. **觀察（Observation）**：讀回環境的回應，例如 Wikipedia 頁面的前 5 句（[Yao 2022](../sources/yao-2022-react.md)）。
4. **重複**：反覆 1～3，直到執行 `finish` 給出答案（[Yao 2022](../sources/yao-2022-react.md)）。
5. **想多想少**：問答這類重推理的任務每一步都想；需要很多動作的任務只在關鍵處想，由模型自己決定何時想（[Yao 2022](../sources/yao-2022-react.md)）。

## 例子

- **自編教學例：出門要不要帶傘？** 想法「要先知道今天會不會下雨」→ 動作「查天氣[台北]」→ 觀察「降雨機率 80%」→ 想法「機率很高，應該帶傘」→ 動作「完成[帶傘]」（Wiki 綜合：討論 04 的自編教學例，觀察結果是假設的）。
- **幻覺大減**：HotpotQA 抽 200 條軌跡分析，只用思維鏈時，失敗案例中 56% 是幻覺；ReAct 是 0%（[Yao 2022](../sources/yao-2022-react.md)）。
- **「想」很重要**：文字家務遊戲 ALFWorld 中，ReAct 最佳成功率 71%，只做不想的版本 45%，用十萬筆示範訓練的模仿學習方法 37%（[Yao 2022](../sources/yao-2022-react.md)）。
- **購物網站 WebShop**：成功率 ReAct 40%、只做不想 30%，人類專家約 60%（[Yao 2022](../sources/yao-2022-react.md)）。
- **人在迴圈中**：人只刪掉一句幻覺的想法、補一點提示，代理的行為就大幅改變並完成任務（[Yao 2022](../sources/yao-2022-react.md)）。
- **查到最新資訊**：資料集的標準答案已經過時，只有 ReAct 上網查到最新資訊、給出合理的答案（[Yao 2022](../sources/yao-2022-react.md)）。

## 什麼時候用、什麼時候別用

- **適合**：需要外部或最新資訊、要邊做邊看結果再決定下一步的任務（[Yao 2022](../sources/yao-2022-react.md)）。
- **適合**：希望人看得懂、能檢查、能修改代理思路的時候（[Yao 2022](../sources/yao-2022-react.md)）。
- **小心卡迴圈**：固定的格式讓推理比較不靈活，ReAct 的推理錯誤比思維鏈多（47% vs. 16%），常見的是一直重複同樣的想法和動作（[Yao 2022](../sources/yao-2022-react.md)）。
- **小心被帶歪**：搜尋沒找到有用資訊時，推理很容易被帶歪、拉不回來，占 ReAct 失敗案例的 23%（[Yao 2022](../sources/yao-2022-react.md)）。
- **最好的做法**：和思維鏈合用。步數太多還沒答案就改用思維鏈投票，投票不一致就改用 ReAct（[Yao 2022](../sources/yao-2022-react.md)）。

## 常見誤解

- **「ReAct 就是反思」**：ReAct 的想法會處理例外、調整計畫，但不是「批評產出再重寫」；Weng 把它放在自我反思一節，論文本身強調的是推理和行動的結合（Wiki 綜合，比較 [Yao 2022](../sources/yao-2022-react.md) 與 [Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **「接上工具就不會出錯」**：ReAct 幾乎沒有幻覺，卻有更多推理錯誤和卡迴圈的問題（[Yao 2022](../sources/yao-2022-react.md)）。
- **「會行動就好，想不想無所謂」**：只做不想的版本在各任務都輸給 ReAct；沒有想法時，代理會拆錯子目標、忘記目前的狀態（[Yao 2022](../sources/yao-2022-react.md)）。

## 相關概念

- [思維鏈](chain-of-thought.md)：ReAct 的「想」來自思維鏈。
- [工具使用](tool-use.md)：ReAct 的「做」就是工具呼叫。
- [工作流程 vs. 代理](workflow-vs-agent.md)：Anthropic 說代理是「在迴圈中根據環境回饋使用工具的 LLM」，ReAct 正是這個樣子。
- [規劃](planning.md)：想法負責拆目標、追蹤進度。
- [代理的限制與風險](agent-limitations.md)：卡迴圈、被壞資訊帶歪。
- [人在迴圈中](human-in-the-loop.md)：人改一兩句想法就能把代理拉回正軌。

## 來源

- [Yao 2022](../sources/yao-2022-react.md)
- [Weng 2023：Self-Reflection](../sources/weng-2023-llm-agents.md)（二手介紹）
- [Anthropic 2024：Agents](../sources/anthropic-2024-building-effective-agents.md)（代理的定義）

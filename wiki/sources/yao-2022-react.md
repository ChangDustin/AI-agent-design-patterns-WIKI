---
title: Yao 等〈ReAct: Synergizing Reasoning and Acting in Language Models〉
type: source
sources: [yao-2022-react]
updated: 2026-11-12
---

# Yao 等〈ReAct: Synergizing Reasoning and Acting in Language Models〉

## 基本資訊

| 項目 | 內容 |
|---|---|
| 作者 | Shunyu Yao、Jeffrey Zhao、Dian Yu、Nan Du、Izhak Shafran、Karthik Narasimhan、Yuan Cao（Princeton、Google） |
| 日期 | arXiv 首版 2022-10-06（v3：2023-03-10）；發表於 ICLR 2023 |
| 類型 | 學術論文 |
| 網址 | <https://arxiv.org/abs/2210.03629> |
| raw | `raw/yao-2022-react/source.md`（ar5iv 全文）、`raw/yao-2022-react/abs.html` |
| 討論紀錄 | [討論 04](../../discussions/04-yao-2022-react.md) |

## 一段話摘要

ReAct 讓大型語言模型交錯產生推理文字（想法）和任務動作，並讀取環境回傳的觀察：推理幫助擬定、追蹤、調整計畫，以及處理例外；動作則從外部取得資訊來支持推理。作者在問答（HotpotQA）、事實查核（FEVER）、文字家務遊戲（ALFWorld）、購物網站（WebShop）四種任務上測試，只用 1～6 個示範例子，就勝過只推理或只行動的方法；在互動任務上，甚至勝過用大量資料訓練的模仿學習和強化學習方法。推理軌跡也讓人能檢查、甚至直接修改代理的想法。

## 重點

1. **動機**：思維鏈是沒和外界接軌的「靜態黑盒子」，容易幻覺、錯誤一路傳下去；只行動的方法則不會針對高層目標做抽象推理。
2. **方法**：把「語言」加進動作空間。想法不會改變環境，只會更新上下文；想法可以用來拆目標、注入常識、從觀察抽出重點、追蹤進度、處理例外。問答任務每一步都想（密集），決策任務只在關鍵處想（稀疏）。
3. **問答任務的動作空間**：`search[實體]`、`lookup[字串]`、`finish[答案]`，刻意做得很陽春。
4. **HotpotQA／FEVER**（PaLM-540B，只用提示）：Standard 28.7／57.1；CoT 29.4／56.3；CoT-SC 33.4／60.4；Act 25.7／58.9；ReAct 27.4／60.9；CoT-SC→ReAct 34.2／64.6；ReAct→CoT-SC 35.1／62.0；監督式最佳 67.5／89.5。
5. **錯誤分析**（HotpotQA 抽 200 條軌跡）：CoT 的失敗案例 56% 是幻覺，ReAct 是 0%；「答對但推理含幻覺」CoT 14%、ReAct 6%；ReAct 的推理錯誤 47%（包括卡在重複的迴圈裡）、CoT 16%；ReAct 的失敗有 23% 來自搜尋沒找到有用資訊。
6. **兩者合用**：ReAct 在 7 步（HotpotQA）或 5 步（FEVER）內沒答案就改用 CoT-SC；CoT-SC 的多數答案不到一半時改用 ReAct。用 3～5 個樣本，就能達到 CoT-SC 用 21 個樣本的表現。
7. **微調**：用 3,000 條正確軌跡微調後，PaLM-8B 的 ReAct 勝過所有 62B 的提示法，62B 的 ReAct 勝過所有 540B 的提示法。
8. **ALFWorld**：ReAct 最佳 71%、平均 57%；Act 最佳 45%；BUTLER（用十萬筆示範訓練的模仿學習）37%；表現最差的 ReAct 試驗（48%）也勝過其他方法的最佳成績；只用外部回饋當想法的 ReAct-IM 是 53%。
9. **WebShop**：成功率 ReAct 40.0%、Act 30.1%、模仿學習 29.1%、模仿＋強化學習 28.7%、人類專家 59.6%。
10. **換模型也有效**：用 GPT-3 做的實驗，HotpotQA 30.8、ALFWorld 78.4。
11. **可解釋、可介入**：人分得出哪些來自模型內部知識、哪些來自外部；改一兩句想法，就能修正代理的行為。
12. **限制與倫理**：動作空間大的任務需要更多示範，容易超過上下文長度；提示法仍遠低於監督式最佳。讓 LLM 對外行動有風險（查到不當或私人資訊、做出有害動作），所以實驗只限在 Wikipedia 和不會真的下單的 WebShop。

## 對 Wiki 的影響

- **新增**：[ReAct](../concepts/react.md)。
- **修改**：[思維鏈](../concepts/chain-of-thought.md)（補上「別用的時機」）、[工具使用](../concepts/tool-use.md)、[規劃](../concepts/planning.md)、[工作流程 vs. 代理](../concepts/workflow-vs-agent.md)、[平行化](../concepts/parallelization.md)、[代理的限制與風險](../concepts/agent-limitations.md)、[總覽](../overview.md)。
- **一致**：Weng 對 ReAct 的介紹（想、做、看；比只做不想好）。
- **分類不同**：Weng 把 ReAct 放在自我反思一節；論文自稱推理和行動的結合。依討論 04 的決定，Wiki 定位為「工具使用＋思維鏈的結合，也是代理的最小原型」。
- **互相印證**：ReAct 卡迴圈 ↔ Reflexion 偵測重複動作（Weng）↔ 要設停止條件（Anthropic）；人改想法修正代理 ↔ 在檢查點請人回饋（Anthropic）。

## 可用的教學素材

- **比喻**：煮菜（論文原生，討論 04 選定）。
- **自編例**：出門要不要帶傘（討論 04）。
- **數字（簡報用，討論 04 決定最多兩組）**：(a) 幻覺：CoT 失敗案例 56% vs. ReAct 0%；(b) ALFWorld 成功率：71% vs. 45%，差別只在有沒有「想」。
- **故事**：人只改一兩句想法，代理就成功完成任務。
- **故事**：資料集的答案過時了（某間飯店後來擴建），只有 ReAct 上網查到最新資訊。

## 限制與存疑

- 主要實驗用 PaLM-540B（當時沒有公開），可重現性有限；作者補上 GPT-3 實驗和完整提示。
- 提示法的分數仍遠低於監督式最佳（HotpotQA 35.1 vs. 67.5）。
- 2022 年的模型和基準，現在的模型表現可能不同。
- 錯誤分析只抽樣 200 條軌跡。

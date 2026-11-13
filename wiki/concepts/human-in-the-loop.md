---
title: 人在迴圈中（Human-in-the-loop）
type: concept
sources: [yao-2022-react, anthropic-2024-building-effective-agents, anthropic-2025-multi-agent-research, tsai-2026-agent-notebooks, weng-2023-llm-agents]
updated: 2026-11-12
---

# 人在迴圈中（Human-in-the-loop）

> 討論 07 決定新增。是簡報結尾「AI 做事、人來把關」的依據，也是本專案「先討論、後生成」的理由。

## 一句話定義

在代理或工作流程的關鍵位置安排人來檢查、修改或決定，讓錯誤能及早被發現和修正，而不是只看最後的成品（Wiki 綜合，依 [Yao 2022](../sources/yao-2022-react.md)、[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)、[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 生活比喻

實習生交報告：主管在大綱階段先看一次方向，定稿前再看一次；比等到最後才發現整份走錯方向省事得多（Wiki 綜合）。

## 運作步驟

1. **讓過程看得見**：把代理的規劃步驟、想法或中間成果攤開來（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)；[Yao 2022](../sources/yao-2022-react.md)）。
2. **設檢查點**：代理在檢查點或卡關時停下來，請人回饋（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
3. **讓人能改中間成果**：例如直接修改 ReAct 的想法，或改完計畫後只重跑寫作階段（[Yao 2022](../sources/yao-2022-react.md)；[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
4. **最後由人決定採不採用**：人對照原始需求，判斷第二版是否真的比較好（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
5. **做人工測試**：找出自動評估漏掉的問題（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 例子

- **ReAct**：人只刪掉一句幻覺的想法、補一點提示，代理就成功完成任務；人的工作從打幾十個動作，變成改幾句想法（[Yao 2022](../sources/yao-2022-react.md)）。
- **課程 Planning**：讀完計畫覺得角度不合適，就改成另一個角度，只重跑寫作（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **課程 Reflection**：介面並排顯示初稿、評論、第二版，由人判斷要不要採用（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **GPT-Engineer**：寫程式前先列出不清楚的地方，一次問使用者一個釐清問題（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **Claude Research**：人工測試發現代理偏好 SEO 內容農場（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **本專案**：每篇資料 ingest 前先和作者討論重點，作者回覆後才寫入 Wiki（Wiki 綜合，見 `CLAUDE.md` 的 Ingest 流程）。

## 什麼時候用、什麼時候別用

- **適合**：AI 自評有盲點、或錯誤代價高的任務；即使有自動測試，人工審查仍然必要（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)；[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **越早越好**：中間成果可讀、可改時，人能在錯誤擴散前介入（Wiki 綜合，依 [Tsai 2026](../sources/tsai-2026-agent-notebooks.md) 的可編輯計畫）。
- **取捨**：每多一個人工檢查點都會多花時間；代理的價值之一，是能在可信任的環境中自己跑很多步（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **別用**：字數、價格這類程式就能確認的事，交給程式，不必讓人逐一檢查（Wiki 綜合，依 [Tsai 2026](../sources/tsai-2026-agent-notebooks.md)「可由程式確認的事情交給程式」）。

## 常見誤解

- **「有人把關就不需要自動檢查」**：人工測試和自動評估要搭配使用（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **「介面把流程包好了，就不用自己判斷」**：介面幫我們包起流程，不會替我們取消判斷的責任（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **「看到 AI 的想法，就等於看到它真正的推理」**：畫面上的是外部操作紀錄或可見的計畫，不是模型內部思考的逐字稿（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 相關概念

- [ReAct](react.md)：人可以直接改代理的想法。
- [規劃](planning.md)：可編輯的計畫是人介入的位置。
- [反思](reflection.md)：最後由人判斷第二版是否比較好。
- [如何評估代理](agent-evaluation.md)：人工測試抓得到自動評估漏掉的問題。
- [代理的限制與風險](agent-limitations.md)

## 來源

- [Yao 2022](../sources/yao-2022-react.md)（改想法修正代理）
- [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)（檢查點、人工審查）
- [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)（人工測試）
- [Tsai 2026](../sources/tsai-2026-agent-notebooks.md)（可編輯的計畫、人決定採用）
- [Weng 2023](../sources/weng-2023-llm-agents.md)（GPT-Engineer 先問釐清問題）

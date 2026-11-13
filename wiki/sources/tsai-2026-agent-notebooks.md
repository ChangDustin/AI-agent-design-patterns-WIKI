---
title: 蔡炎龍〈Agent01 Reflection／Agent02 Tool Use／Agent03 Planning〉課程 notebook
type: source
sources: [tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# 蔡炎龍〈Agent01 Reflection／Agent02 Tool Use／Agent03 Planning〉課程 notebook

## 基本資訊

| 項目 | 內容 |
|---|---|
| 作者 | [蔡炎龍](../entities/tsai-yen-lung.md) |
| 日期 | 教材整理日：Agent02 為 2026-10-26；Agent01、Agent03 為 2026-10-27 |
| 類型 | 課程用 Colab notebook（繁體中文，逐格說明） |
| 網址 | Agent01、Agent02：<https://github.com/yenlung/Generative-AI>；Agent03：<https://github.com/yenlung/AI-Demo> |
| raw | `raw/tsai-2026-agent-notebooks/`（三份 .ipynb 與轉出的 .md） |
| 授權 | AI-Demo 的 README 表示非商業用途（如教學）可自由使用、修改；Generative-AI repo 沒有另外說明 |
| 討論紀錄 | [討論 07](../../discussions/07-tsai-2026-agent-notebooks.md) |

## 一段話摘要

三份逐格教學的 Colab notebook，用 AISuite 連接 Groq 的 `gpt-oss-120b`，分別示範反思（需求 → 初稿 → 評論 → 第二版）、工具使用（問題 → JSON 工具請求 → Python 檢查並執行 → 依實際結果回答）、規劃（原事件 → 可編輯的回應計畫 → 貼文）。三份有共同的理念：流程由人寫清楚，不藏在自動迴圈裡；都只是同一個模型的幾次普通呼叫，不是完整的自主代理；模型不會記得上一次呼叫，資料要明確傳遞；資料不是指令；能由程式確認的事情交給程式。

## 重點

1. **共同設計**：AISuite＋Groq `gpt-oss-120b`；「作者」「評論者」「規劃者」只是指令和資料不同，不是不同的 AI；不自動重試（避免重複消耗額度）；失敗時保留已完成的階段、標出停在哪裡；用 `safe_error` 遮蔽錯誤訊息裡的金鑰。
2. **Reflection**：固定三次呼叫就停，停止條件是人設計的。先寫清楚「好文章」的標準；評論者要同時看到原始需求和初稿，分「值得保留／需要修改／仍需確認」回覆，沒問題可以說保留；改稿時原始需求優先於評論。
3. **Reflection 的提醒**：第二版不一定比較好，「更長、更華麗，不等於更符合任務」；同一個模型可能重複同樣的盲點，換模型評論也不等於獨立的事實查核；外部事實要查可靠來源，程式和數值要用測試或工具驗證。
4. **Tool Use**：第一次 LLM 把問題轉成 JSON 工具請求（`get_menu`、`quote_order`、`clarify`）→ Python 解析、檢查、執行 → 第二次 LLM 根據「原問題＋請求＋實際結果」回答。這是用 prompt 實作的教學版工具路由，不是 API 原生的 tool calling。
5. **Tool Use 的防線**：工具就是普通 Python 函式；只允許白名單上的工具，不用 `eval`／`exec`；JSON 不合法就報錯，不猜參數；缺資訊時選 `clarify` 追問；價格與總價由 Python 計算。
6. **Planning**：先產生可閱讀、可修改的回應計畫，再依「原事件＋計畫」寫作。人可以改計畫、只重跑寫作階段。好處是能定位問題出在計畫還是寫作；代價是多一次呼叫，而且錯誤的計畫會傳到下游。
7. **Planning ≠ CoT**：CoT 是用中間推理步驟連接問題和結論；Planning 是先決定子任務、需要的資料和順序再執行。兩者可以結合，但不是同一件事；對外寫出的計畫也不是模型私有推理的完整紀錄。
8. **模型設定**：`gpt-oss-120b` 是推理模型，生成答案前可能先用掉推理 token；Agent03 用 `reasoning_effort="low"`、`max_completion_tokens=8192`，只取 `content`，不拿推理欄位當答案；回覆是空的就停止、不自動重試。

## 對 Wiki 的影響

- **新增**：[人在迴圈中](../concepts/human-in-the-loop.md)、[蔡炎龍](../entities/tsai-yen-lung.md)、[AISuite](../entities/aisuite.md)、[Groq](../entities/groq.md)。
- **修改**：[反思](../concepts/reflection.md)、[工具使用](../concepts/tool-use.md)、[規劃](../concepts/planning.md)（並陳兩種意思）、[思維鏈](../concepts/chain-of-thought.md)（CoT ≠ Planning）、[記憶](../concepts/memory.md)、[工作流程 vs. 代理](../concepts/workflow-vs-agent.md)、[LLM 回饋與自我評估](../concepts/llm-feedback.md)、[代理的限制與風險](../concepts/agent-limitations.md)、[總覽](../overview.md)。
- **同名不同義**：Ng 的「規劃」是 LLM 自主決定步驟（代理）；課程的 Planning 是固定兩步「先計畫再執行」（工作流程）。依討論 07 的決定並陳。
- **補充區分**：Weng 把 CoT 放在規劃的拆解技巧底下；課程強調 CoT 不等於 Planning。兩者不矛盾。
- **一致**：三份 notebook 都是工作流程而不是代理（呼應 Anthropic 2024）；模型不記得上一次呼叫（補上記憶頁的出處）；LLM 自評有盲點（呼應 Self-Refine、Weng）。

## 可用的教學素材

- **反思實作例**：「第一次用 Python 畫出心形圖，少打一個括號，看錯誤訊息後成功」寫成貼文：初稿 → 評論 → 第二版。
- **工具使用實作例**：「麥茶買 20 杯，預算 800 元夠嗎？」→ 模型產生 `quote_order(麥茶, 20)` → Python 算出 600 元 → 回答「夠，還剩 200 元」。
- **規劃實作例**：「特地去買可頌，到了才發現賣完了」→ 計畫 → 貼文，結尾「完全是 Lucky Vicky 呀！」。
- **課堂小實驗**：塞一條壞評論（加五個 emoji、編造教授稱讚），看模型會不會照單全收。
- **課堂小實驗**：把麥茶庫存改成 8 杯，同樣的參數得到「庫存不足」。
- **三組自我檢查問題**：評論有沒有看見原需求？參數對不對？最後回答有沒有忠於資料？

## 限制與存疑

- 教學用的虛構情境與資料；notebook 不保存執行輸出，所以沒有實測數據。
- 只用一個模型（`gpt-oss-120b`）；套件版本、模型服務與額度都可能改變。
- 用 prompt 實作的工具路由和原生 tool calling 不同，實務系統多半用原生介面。

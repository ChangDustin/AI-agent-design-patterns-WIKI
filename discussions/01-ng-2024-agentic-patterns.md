# 討論 01｜Andrew Ng〈Agentic Design Patterns〉Part 1–5

- source-id：`ng-2024-agentic-patterns`
- 原文：`raw/ng-2024-agentic-patterns/part1`～`part5`（The Batch，2024-03-20～04-17）
- 狀態：**已寫入**（2026-11-12）

## 1. LLM 的提案

### 這篇在講什麼

1. **核心主張：代理式工作流程（agentic workflow）。** 一般用 LLM 是 zero-shot，一次從頭寫到尾，Ng 比喻成「寫作文不准按倒退鍵」。代理式工作流程讓 LLM 反覆處理同一份作品：列大綱 → 判斷要不要查資料 → 寫初稿 → 自己挑毛病 → 修改。Ng 認為這股趨勢對當年 AI 進展的推動，可能比下一代基礎模型還大。
2. **吸睛數據（HumanEval 程式題）。** GPT-3.5 zero-shot 48.1%、GPT-4 zero-shot 67.0%；把 GPT-3.5 包進代理迴圈，最高可到 95.1%。換句話說，改流程帶來的進步比換更強的模型還多。⚠️ 這是 Ng 團隊彙整多篇研究後取的最佳值，不是單一實驗。
3. **四種設計模式：**
   - **反思（Reflection）**：LLM 檢查自己的產出、提出改進，再依建議重寫，可以重複多輪。也可以加工具輔助（跑單元測試、上網查證），或拆成「寫手＋評論者」兩個代理。
   - **工具使用（Tool Use）**：LLM 輸出一段特定格式的請求（例如 `{tool: web-search, query: …}`），由程式實際執行，再把結果放回對話。例如複利計算交給 Python 算，不讓模型用猜的。工具太多時要先挑出相關的一小組，做法跟 RAG 挑選段落很像。
   - **規劃（Planning）**：LLM 自己決定把大任務拆成哪些步驟。Ng 講了一段現場 demo：搜尋 API 突然被限流，代理自己改用 Wikipedia 完成任務。不過很多流程根本不需要規劃，步驟固定就好。
   - **多代理協作（Multi-agent Collaboration）**：用同一個（或多個）LLM 扮演不同角色，例如工程師、PM、QA。Ng 給了三個理由：實驗上有效；一次只專注一件事，比把長文一股腦塞進去好；給人一個拆解任務的思考框架，就像主管分工、程式拆成多個 process。
4. **成熟度差異。** 反思、工具使用比較可靠；規劃、多代理比較強大，但結果難預測。→ 這可以當簡報的「由穩到野」排序。
5. **延伸閱讀**：反思（Self-Refine、Reflexion、CRITIC）、工具（Gorilla、MM-REACT、Chain-of-Abstraction）、規劃（CoT、HuggingGPT、規劃綜述）、多代理（ChatDev、AutoGen、MetaGPT）。我們第 5 篇要讀的 Self-Refine 就在這份清單裡。

### 打算新增或修改的頁面

| 頁面 | 動作 | 內容 |
|---|---|---|
| `sources/ng-2024-agentic-patterns.md` | 新增 | 來源摘要頁 |
| `concepts/agentic-workflow.md` | 新增 | 代理式工作流程 vs. zero-shot 一次生成 |
| `concepts/reflection.md` | 新增 | 反思 |
| `concepts/tool-use.md` | 新增 | 工具使用 |
| `concepts/planning.md` | 新增 | 規劃 |
| `concepts/multi-agent-collaboration.md` | 新增 | 多代理協作 |
| `entities/andrew-ng.md` | 新增 | 人物頁 |
| `overview.md` | 首次撰寫 | 四模式地圖＋成熟度光譜 |
| `index.md`、`log.md` | 更新 | 目錄與日誌 |

### 和既有 Wiki 的關係

Wiki 目前是空的，這篇負責搭骨架。可以預見的衝突：Ng 把所有多步驟流程都叫 agentic workflow，但 Anthropic（第 2 篇）會把「工作流程」和「代理」分開定義。到時要在概念頁註明兩種用詞的差別，不能直接覆蓋。

### 想問作者的問題

1. **95.1% 的數據**：要不要當簡報開場的鉤子？寫進 Wiki 時我會註明它是多篇研究的最佳值。
2. **四個模式的生活比喻**，我的初步提案：反思＝寫完作文自己訂正（或請同學幫忙改）；工具使用＝考試可以帶計算機、查字典；規劃＝出國前先排行程；多代理＝分組報告各司其職。有想換的嗎？
3. **要不要建 `entities/langgraph.md`？** Ng 在多代理篇提到 LangGraph，我們的簡報 pipeline 也用它，可以順便連起來。

## 2. 作者回饋（原話）

> 照提案寫入

## 3. 決定

作者同意整份提案，三個問題都採用 LLM 的建議：

1. **95.1% 數據**：當簡報開場的鉤子；Wiki 裡註明它是 Ng 彙整多篇研究後的最佳值，不是單一實驗。
2. **生活比喻**：反思＝寫完作文自己訂正；工具使用＝考試帶計算機、查字典；規劃＝出國前排行程；多代理＝分組報告各司其職。
3. **建立 `entities/langgraph.md`**，連到本專案的簡報 pipeline。

寫入結果見 `wiki/log.md` 的「[2026-11-12] ingest | Andrew Ng〈Agentic Design Patterns〉Part 1–5」。

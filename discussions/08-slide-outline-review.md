# 討論 08｜簡報大綱審閱（pipeline 執行 20261113-000224）

- 對象：pipeline 產生、通過大綱閘門的大綱（`runs/20261113-000224/outline.json`，回存在 `wiki/queries/slide-outline.md`）
- 狀態：**已決定**（2026-11-13）：採用修改版

## 1. 程式閘門的紀錄

- 第 1 次擬的大綱被退件：第 8、10、17 頁標題超過 16 字；第 19 頁引用超過 3 個 Wiki 頁。
- 第 2 次擬的大綱通過（18 頁）。兩次共 2 次 LLM 呼叫，約 7,180 token。

## 2. Claude 的審閱建議（程式閘門抓不到的問題）

| # | 問題 | 依據 | 修改 |
|---|---|---|---|
| 1 | **圖示配錯**：四個模式的概念頁都放「四模式地圖」；反思步驟頁配「複雜度階梯」、工具使用步驟頁配「工作流程 vs. 代理」 | 圖要和這頁內容對應 | 地圖只放在「四種招式一次看」；階梯放在「能簡單就簡單」；想→做→看迴圈放在 ReAct |
| 2 | **缺少 ReAct** | 討論 04：ReAct 是從「模式」走到「代理」的橋 | 新增 s10「ReAct：想→做→看」 |
| 3 | **教學順序不順**：「代理 vs. 工作流程」對照頁排在兩個測驗之間 | 先講定義和選擇，再講限制 | 移到 s12，接在四種模式之後，再加 s13「能簡單就簡單」 |
| 4 | **討論定案的素材沒被指定** | 討論 01（95.1% 考卷數字）、04（煮菜、帶傘）、06（90.2% vs. 15 倍）、07（心形圖、麥茶、可頌） | 寫進各頁的 goal；步驟頁的 pages 加上課程 notebook 的來源頁 |
| 5 | **總結頁寫「未來展望」**，Wiki 沒有這部分內容，容易誘導模型亂編 | 只能用 Wiki 的事實 | 改成「本章重點」 |
| 6 | **標題太籠統**（AI 代理的崛起、反思模式、工具使用步驟……） | 標題就是這頁要記住的事 | 改成帶比喻或例子的標題（反思：自己改作文、麥茶 20 杯夠不夠？……） |

## 3. 修改版大綱（`runs/20261113-000224/outline_reviewed.json`，已通過同一個大綱閘門）

| id | 類型 | 標題 | 圖 | 引用的 Wiki 頁 |
|---|---|---|---|---|
| s01 | cover | AI 代理設計模式 | — | — |
| s02 | hook | 同一題，誰的分數高？ | — | concepts/agentic-workflow.md |
| s03 | concept | 代理式工作流程 | — | concepts/agentic-workflow.md |
| s04 | concept | 四種招式一次看 | 四模式地圖 | overview.md、concepts/agentic-workflow.md |
| s05 | concept | 反思：自己改作文 | — | concepts/reflection.md、concepts/self-refine.md |
| s06 | steps | 反思實作：心形圖貼文 | — | concepts/reflection.md、sources/tsai-2026-agent-notebooks.md |
| s07 | concept | 工具使用：帶計算機 | — | concepts/tool-use.md |
| s08 | steps | 麥茶 20 杯夠不夠？ | — | concepts/tool-use.md、sources/tsai-2026-agent-notebooks.md |
| s09 | concept | 規劃：出國排行程 | — | concepts/planning.md |
| s10 | steps | ReAct：想→做→看 | 迴圈圖 | concepts/react.md |
| s11 | concept | 多代理：分組報告 | — | concepts/multi-agent-collaboration.md |
| s12 | compare | 跟團 vs. 自由行 | — | concepts/workflow-vs-agent.md |
| s13 | concept | 能簡單就簡單 | 複雜度階梯 | concepts/workflow-vs-agent.md、concepts/agentic-workflow.md |
| s14 | quiz | 小測驗：誰在執行？ | — | concepts/tool-use.md |
| s15 | concept | 代理也會出包 | — | concepts/agent-limitations.md、concepts/llm-feedback.md |
| s16 | concept | AI 做事，人來把關 | — | concepts/human-in-the-loop.md |
| s17 | quiz | 小測驗：該用代理嗎？ | — | concepts/workflow-vs-agent.md、concepts/agent-limitations.md |
| s18 | summary | 本章重點 | — | overview.md、concepts/workflow-vs-agent.md、concepts/human-in-the-loop.md |

## 4. 作者回饋（原話）

> 用修改版

## 5. 決定

採用修改版大綱 `runs/20261113-000224/outline_reviewed.json`，以 `--outline` 參數跳過擬大綱、直接生成整份簡報；`wiki/queries/slide-outline.md` 同步換成核准版。

**這次審閱給流程設計的啟示**：程式閘門只能檢查格式（頁數、字數、引用的頁存不存在），教學順序、圖和內容對不對得上、討論定案的素材有沒有用上，都要靠人。所以大綱之後的人工審閱是必要的一關，不是多餘的步驟。

# Wiki 日誌（log）

> 只能往後加。標題格式：`## [YYYY-MM-DD] 動作 | 標題`；`grep "^## \[" wiki/log.md` 可以列出所有紀錄。

## [2026-11-12] setup | 建立 Wiki 骨架

- 和作者討論後決定：主題「AI 代理設計模式」、讀者是非資工大學生、每篇資料逐篇討論後才寫入。
- 建立 `CLAUDE.md`（schema）、`wiki/index.md`、`wiki/log.md`、`wiki/overview.md`、`raw/README.md`。
- 選定 7 篇資料並抓進 `raw/`，ingest 順序見 [raw/README.md](../raw/README.md)。
- 開始討論第 1 篇：[討論 01](../discussions/01-ng-2024-agentic-patterns.md)。

## [2026-11-12] ingest | Andrew Ng〈Agentic Design Patterns〉Part 1–5

- 討論：[討論 01](../discussions/01-ng-2024-agentic-patterns.md)。作者回覆「照提案寫入」：95.1% 當簡報開場鉤子（註明是多篇研究的最佳值）、採用四個生活比喻、建立 LangGraph 頁。
- 新增：`sources/ng-2024-agentic-patterns.md`、`concepts/agentic-workflow.md`、`concepts/reflection.md`、`concepts/tool-use.md`、`concepts/planning.md`、`concepts/multi-agent-collaboration.md`、`entities/andrew-ng.md`、`entities/langgraph.md`
- 修訂：`overview.md`（首次撰寫）、`index.md`
- 新增工具：`tools/wiki_lint.py`（自我測試通過）

## [2026-11-12] lint | ingest 01 之後

- 0 個錯誤、0 個警告、3 個待補缺口：代理式工作流程、反思、工具使用的「什麼時候別用」都還沒有來源支持。

## [2026-11-12] ingest | Anthropic〈Building effective AI agents〉

- 討論：[討論 02](../discussions/02-anthropic-2024-building-effective-agents.md)。作者回覆「照提案寫入」：採用 Anthropic 的「工作流程／代理」為正式用詞、比喻用「跟團 vs. 自由行」、四種工作流程各一頁、框架取捨寫進 LangGraph 頁。
- 新增：`sources/anthropic-2024-building-effective-agents.md`、`concepts/workflow-vs-agent.md`、`concepts/augmented-llm.md`、`concepts/prompt-chaining.md`、`concepts/routing.md`、`concepts/parallelization.md`、`concepts/orchestrator-workers.md`、`entities/anthropic.md`
- 修訂：`concepts/reflection.md`（別名評估者—優化者、補上別用時機）、`concepts/agentic-workflow.md`（用詞註記、補上別用時機）、`concepts/tool-use.md`（ACI、防呆）、`concepts/planning.md`（代理、停止條件）、`concepts/multi-agent-collaboration.md`、`entities/langgraph.md`（框架取捨）、`overview.md`（兩條軸線＋對照表）、`index.md`（概念分三組）
- 衝突處理：Ng 的 agentic workflow 與 Anthropic 的 workflow 範圍不同 → 新增概念頁說明，舊頁加註，不覆蓋。
- 更正：`raw/README.md` 的作者欄改成原文署名「Erik S.、Barry Zhang」。

## [2026-11-12] lint | ingest 02 之後

- 0 個錯誤、0 個警告、2 個待補缺口（工具使用、增強型 LLM 的「什麼時候別用」）。上一輪的 3 個缺口補上 2 個（代理式工作流程、反思）。

## [2026-11-12] ingest | Lilian Weng〈LLM Powered Autonomous Agents〉

- 討論：[討論 03](../discussions/03-weng-2023-llm-agents.md)。作者回覆「照提案寫入」：反思維持獨立頁並陳三種分類、記憶比喻用「書桌 vs. 書櫃」並連到課程 RAG、太深的內容只記在來源頁、新增「代理的限制與風險」頁。
- 新增：`sources/weng-2023-llm-agents.md`、`concepts/memory.md`、`concepts/chain-of-thought.md`、`concepts/agent-limitations.md`、`entities/lilian-weng.md`、`entities/generative-agents.md`
- 修訂：`concepts/planning.md`（拆解方法、HuggingGPT、軼事 vs. 普遍限制）、`concepts/reflection.md`（三種分類、Reflexion、兩種意思、ChemCrow）、`concepts/tool-use.md`（MRKL、API-Bank、補上別用時機）、`concepts/augmented-llm.md`、`concepts/multi-agent-collaboration.md`（AI 小鎮）、`overview.md`（第三個視角：解剖圖）、`index.md`
- 衝突處理：反思的分類三篇不同 → 並陳；Ng 的成功軼事 vs. Weng 的普遍限制 → 註明軼事不代表普遍。

## [2026-11-12] lint | ingest 03 之後

- 0 個錯誤、0 個警告、3 個待補缺口（增強型 LLM、記憶、思維鏈的「什麼時候別用」）。工具使用的缺口已由 MRKL 實驗補上。

## [2026-11-12] ingest | Yao 等〈ReAct〉

- 討論：[討論 04](../discussions/04-yao-2022-react.md)。作者回覆「照提案寫入」：用論文原生的煮菜比喻、加自編的「帶不帶傘」例子、定位為「工具使用＋思維鏈，代理最小的原型」、簡報最多用兩組數字。
- 新增：`sources/yao-2022-react.md`、`concepts/react.md`
- 修訂：`concepts/chain-of-thought.md`（補上別用時機、CoT-SC）、`concepts/tool-use.md`（ReAct 的動作空間）、`concepts/planning.md`（沒有「想」的對照實驗）、`concepts/workflow-vs-agent.md`（代理的最小原型）、`concepts/parallelization.md`（CoT-SC 投票）、`concepts/agent-limitations.md`（卡迴圈、被帶歪、示範塞不下、限制行動範圍）、`overview.md`（ReAct 這座橋、兩點新綜合）、`index.md`
- 分類差異：Weng 把 ReAct 放在自我反思一節 → ReAct 頁註明，Wiki 定位為推理＋行動。

## [2026-11-12] lint | ingest 04 之後

- 0 個錯誤、0 個警告、2 個待補缺口（增強型 LLM、記憶）。思維鏈的缺口已由 ReAct 的錯誤分析補上。

## [2026-11-12] ingest | Madaan 等〈Self-Refine〉

- 討論：[討論 05](../discussions/05-madaan-2023-self-refine.md)。作者回覆「照提案寫入」：email 例子進反思頁、新增「LLM 回饋與自我評估」頁、簡報用「平均 +20%」和「對話 vs. 數學」對比、四點 pipeline 啟示留到 7 篇完成後的第一次 Query。
- 新增：`sources/madaan-2023-self-refine.md`、`concepts/self-refine.md`、`concepts/llm-feedback.md`
- 修訂：`concepts/reflection.md`（email 例子、Self-Refine 成績、輪數、細微錯誤與弱模型的「別用」、會改壞）、`concepts/agent-limitations.md`（自評盲點數據、小模型跟不上格式）、`overview.md`（綜合理解 10、11）、`index.md`
- 更正：提案中「NeurIPS 2023」在抓到的頁面找不到依據，已從 `raw/README.md` 與討論 05 移除，改標「arXiv 預印本」。

## [2026-11-12] lint | ingest 05 之後

- 0 個錯誤、0 個警告、2 個待補缺口（增強型 LLM、記憶）。

## [2026-11-12] ingest | Anthropic〈How we built our multi-agent research system〉

- 討論：[討論 06](../discussions/06-anthropic-2025-multi-agent-research.md)。作者回覆「照提案寫入」：比喻用「研究小組」並收「傳話遊戲」、新增「如何評估代理」頁與「Claude Research」案例頁、簡報用「90.2% vs. 15 倍 token」、來源頁加偏誤註記。
- 新增：`sources/anthropic-2025-multi-agent-research.md`、`concepts/agent-evaluation.md`、`entities/claude-research.md`
- 修訂：`concepts/multi-agent-collaboration.md`（token 解釋、成本、適用與不適用、傳話遊戲）、`concepts/orchestrator-workers.md`（分派四要素、依難度分配、同步瓶頸）、`concepts/tool-use.md`（測工具的代理、說明寫壞的後果）、`concepts/llm-feedback.md`（評分規準、人工測試）、`concepts/memory.md`（補上別用時機）、`concepts/agent-limitations.md`（湧現行為、不確定性、最後一哩路、續跑與追蹤）、`concepts/workflow-vs-agent.md`、`concepts/parallelization.md`、`entities/anthropic.md`（偏誤註記）、`overview.md`、`index.md`
- 並陳：多代理為什麼有效 → Ng「專注與拆解」vs. Anthropic「花足夠的 token」。

## [2026-11-12] lint | ingest 06 之後

- 0 個錯誤、0 個警告、1 個待補缺口（增強型 LLM 的「什麼時候別用」）。記憶的缺口已補上。

## [2026-11-12] ingest | 蔡炎龍課程 notebook（Agent01 Reflection／Agent02 Tool Use／Agent03 Planning）

- 討論：[討論 07](../discussions/07-tsai-2026-agent-notebooks.md)。作者回覆「照提案寫入」：簡報用課程的三個在地化例子、規劃頁並陳兩種意思、新增「人在迴圈中」頁、pipeline 沿用課程寫法並新增 aisuite／groq 工具頁。
- 新增：`sources/tsai-2026-agent-notebooks.md`、`concepts/human-in-the-loop.md`、`entities/tsai-yen-lung.md`、`entities/aisuite.md`、`entities/groq.md`
- 修訂：`concepts/reflection.md`、`concepts/tool-use.md`、`concepts/planning.md`（同名不同義）、`concepts/chain-of-thought.md`（CoT ≠ Planning）、`concepts/memory.md`（模型不記得上次呼叫，改為有出處）、`concepts/workflow-vs-agent.md`、`concepts/llm-feedback.md`、`concepts/agent-limitations.md`、`overview.md`（7／7）、`index.md`
- **7 篇全部 ingest 完成**：7 個來源頁、19 個概念頁、9 個實體頁。

## [2026-11-12] lint | 全面健檢（7 篇完成後）

- **程式檢查**（`tools/wiki_lint.py`）：0 個錯誤、0 個警告、1 個待補缺口（增強型 LLM 的「什麼時候別用」）。
- **語意檢查**（LLM 人工逐頁）：
  - 矛盾：5 處都已在頁面中並陳或註明：反思的三種分類、ReAct 的分類、規劃的兩種意思、多代理為什麼有效、Ng 的成功軼事 vs. Weng 的普遍限制。
  - 過時說法：多代理頁只有 Ng 2024「難預測」的判斷 → 補上 Anthropic 2025「靠工程可以可靠運作」的較新看法。
  - 缺連結：`react.md`、`agent-evaluation.md` 補上連到「人在迴圈中」。
  - 被提到但沒有頁面：Reflexion（3 頁提到，只有 Weng 的二手介紹，暫不建頁）；RAG、MCP、AutoGen（各 2 頁，未達門檻）。
  - 資料缺口：增強型 LLM 的「別用時機」→ 之後可上網找資料補。

## [2026-11-12] query | 根據 Wiki，教學簡報 pipeline 該怎麼設計？

- 讀 `index.md` → 讀工作流程 vs. 代理、提示鏈、反思、Self-Refine、LLM 回饋與自我評估、如何評估代理、人在迴圈中、記憶、代理的限制與風險、LangGraph、AISuite、Groq 等頁。
- 答案回存為 [queries/pipeline-design.md](queries/pipeline-design.md)：帶閘門的提示鏈＋評估者—優化者迴圈，15 條設計原則各自對應 Wiki 頁。
- 外部查詢（非 Wiki 來源）：Groq 官方文件的速率限制（gpt-oss-120b 免費方案每分鐘 8K token），用來決定分批大小。

## [2026-11-13] query | 教學簡報 pipeline（20261113-000224）

- 大綱通過閘門，等待人工審閱
- 執行紀錄：[runs/20261113-000224/report.md](../runs/20261113-000224/report.md)
- 大綱回存：[queries/slide-outline.md](queries/slide-outline.md)

## [2026-11-13] query | 簡報大綱審閱（討論 08）

- pipeline 產生的大綱通過程式閘門，但人工審閱發現圖示配錯、缺少 ReAct、順序不順、討論定案的素材沒被指定。
- 作者回覆「用修改版」：採用 runs/20261113-000224/outline_reviewed.json（也通過大綱閘門）。
- [queries/slide-outline.md](queries/slide-outline.md) 已換成核准版；討論紀錄見 [討論 08](../discussions/08-slide-outline-review.md)。

## [2026-11-13] query | 教學簡報 pipeline（20261113-000549）

- 失敗：draft_slides：連續兩次輸出不是合法 JSON
- 執行紀錄：[runs/20261113-000549/report.md](../runs/20261113-000549/report.md)

## [2026-11-13] update | pipeline v1 第一次完整執行失敗 → 改成 v2

- v1 執行紀錄：[runs/20261113-000549/report.md](../runs/20261113-000549/report.md)。`draft_slides` 一次寫 3 頁：要求 15 頁只交回 6 頁；3 次格式錯誤（2 次括號寫錯、1 次最外層是陣列）；9 次限流等待；同一批連續兩次格式錯誤，整條流程中止。
- v2 修改：撰稿、修改、評審改用 strict JSON Schema（格式檢查往前移到生成當下，cite 只能選拿到的 Wiki 頁）；一次只寫 1 頁；格式失敗時記成缺頁交給閘門，不中止流程。
- 設計文件同步更新：[queries/pipeline-design.md](queries/pipeline-design.md)「v1 → v2」一節。smoke test：一頁 1 次呼叫、約 2,445 token、通過程式閘門。

## [2026-11-13] query | 教學簡報 pipeline（20261113-001206）

- 失敗：revise_slides：Groq 呼叫失敗
LLMError / HTTP -: An error occurred: Connection error.
APIConnectionError / HTTP -: Connection error.
ConnectError / HTTP -: [WinError 10054] 遠端主機已強制關閉一個現存的連線。
ConnectError / HTTP -: [WinError 10054] 遠端主機已強制關閉一個現存的連線。
ConnectionResetError / HTTP -: [WinError 10054] 遠端主機已強制關閉
- 執行紀錄：[runs/20261113-001206/report.md](../runs/20261113-001206/report.md)

## [2026-11-13] update | v2 執行因網路斷線中止 → 補上重試、續跑，並調整字數回饋

- v2 執行紀錄：[runs/20261113-001206/report.md](../runs/20261113-001206/report.md)。strict JSON Schema 生效：`draft_slides` 0 次格式錯誤、18 頁全部交回。投影片閘門退件：第 0 輪 8 頁（16 個問題，其中 14 個是字數超過）、第 1 輪 6 頁（5 個字數超過、2 個評審指出內容不完整）。第 2 輪改寫時網路斷線（WinError 10054），流程中止。
- 發現：最常出錯的是撰稿與改寫節點寫超過字數，而且改寫也改不太下來（例如「52 字，上限 46 字」改完還有 50 字）：模型不會精確數字數。
- 修改：字數退件意見改成具體目標（「請改寫到上限八成的字數以內」）；撰稿提示請模型比上限少寫約四分之一；steps 字數上限 40 → 46（版面實測放得下，以版面閘門為準）；網路斷線、逾時、5xx 自動重試；每日額度用完時直接停下、不空等；節點失敗時存 `resume.json`，可用 `--resume` 續跑；第 1 輪之後只重審改過的頁。
- 這次斷線時還沒有自動存檔，所以用 [recover_state.py](../runs/20261113-001206/recover_state.py) 從呼叫紀錄重建斷線前的狀態，從 `revise_slides` 續跑，省下約 10 萬 token。

## [2026-11-13] query | 教學簡報 pipeline（20261113-002929）

- 簡報已產生，但有 4 頁未通過檢查，需人工處理
- 執行紀錄：[runs/20261113-002929/report.md](../runs/20261113-002929/report.md)

## [2026-11-13] query | 教學簡報 pipeline（20261113-024148）

- 簡報已產生，全部頁面通過三個閘門
- 執行紀錄：[runs/20261113-024148/report.md](../runs/20261113-024148/report.md)

## [2026-11-13] query | 教學簡報 pipeline（20261113-024626）

- 簡報已產生，全部頁面通過三個閘門
- 執行紀錄：[runs/20261113-024626/report.md](../runs/20261113-024626/report.md)

## [2026-11-13] update | v2 → v3：閘門本身也會出錯，修好後只重審被標記的頁

- 人工檢查 20261113-002929 的截圖和退件紀錄，找到 7 個問題，例如字數用字元數算、評審不知道上限、最後狀態用平均分數判斷。細節和證據寫在 [pipeline 設計](queries/pipeline-design.md) 的「v2 → v3」一節。
- **更正**：上面「20261113-024148」那筆寫「全部頁面通過三個閘門」是誤報。s04、s15 留下的版本其實沒通過評審；該次 report.md 最後已附上更正說明。
- 修改 pipeline：`checks.width()`、有圖的 concept 頁最多 2 點、評審和修改提示加上欄位上限與「goal 和上限衝突」的規則、保留最佳版本與最後狀態改看是否通過、版面回饋換算成字數、反引號顯示成程式碼、`--render-only` 也跑版面閘門、新增 `pipeline.recheck`（人指定重審的頁）。
- 重審兩次：20261113-024148（s04、s05、s08）、20261113-024626（s04、s15），之後 18 頁全部通過三個閘門。四種模式地圖加上 overview 的穩定度後，用 `--render-only` 重新輸出，版面閘門通過。
- 動到的 Wiki 頁：queries/pipeline-design.md（新增「v2」「v2 → v3」「流程圖（v3）」三節）。
- 健檢：0 個錯誤、0 個警告、1 個待補缺口（augmented-llm「別用的時機」，原始資料沒有提到）。

## [2026-11-13] update | 版面閘門加上小螢幕檢查

- 做繳交首頁（`docs/index.html`）時，用 iframe 預覽簡報，發現比 1280px 窄的視窗裡投影片會偏到右下；390px 寬的手機上整張跑出畫面。原因是 grid 置中遇到固定 1280px 寬的投影片。版面閘門一直只在 1280×776 量，所以沒抓到。
- 修改：模板改用絕對定位置中；版面閘門另外在 390×844、1024×640 檢查投影片有沒有整張落在視窗裡。用舊模板驗證過會被擋下，新模板通過。之後用 `--render-only` 重新輸出 20261113-024626，版面閘門通過。
- 動到的 Wiki 頁：queries/pipeline-design.md（「v2 → v3」表格加第 8 點）。

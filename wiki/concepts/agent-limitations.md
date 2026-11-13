---
title: 代理的限制與風險
type: concept
sources: [weng-2023-llm-agents, anthropic-2024-building-effective-agents, ng-2024-agentic-patterns, yao-2022-react, madaan-2023-self-refine, anthropic-2025-multi-agent-research, tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# 代理的限制與風險

> 討論 03 決定新增。目的：讓觀眾知道代理會出包，也提醒本專案的檢查不能只靠 LLM 自己審自己。

## 一句話定義

代理把 LLM 放進多步驟、會採取行動的系統裡，也把 LLM 的弱點放大了：上下文有限、長程規劃不穩、輸出格式不可靠、自評有盲點，再加上成本、錯誤累積和安全風險（Wiki 綜合，依 [Weng 2023](../sources/weng-2023-llm-agents.md) 與 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。

## 生活比喻

像一位很能幹的新實習生：桌上放不下太多資料、計畫被打亂就容易慌、報告偶爾格式不對、自己檢查也看不出專業上的錯；所以要給清楚的流程、設檢查點，重要的事交給主管把關（Wiki 綜合）。

## 運作步驟

代理常見的出包路徑：

1. **上下文塞不下**：歷史紀錄、詳細指示、API 回傳一多就放不下；外部檢索能補充，但表現力不如全部放進上下文（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
2. **計畫被打亂**：長程規劃和任務拆解很難，遇到意外錯誤時 LLM 不太會調整計畫，不如人類從試誤中學習（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
3. **輸出格式出錯**：代理靠自然語言和記憶、工具溝通，但 LLM 會出現格式錯誤，偶爾也不聽指令，所以很多代理程式碼都在解析輸出（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
4. **錯誤一路累積**：代理自主跑很多步，錯誤可能層層累積，成本也比較高（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
5. **自評有盲點**：在需要專業的領域，LLM 不知道自己哪裡錯，也就評不準結果（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
6. **卡在迴圈**：代理反覆產生同樣的想法和動作、跳不出來，是 ReAct 最常見的錯誤之一（[Yao 2022](../sources/yao-2022-react.md)）。
7. **被壞資訊帶歪**：工具回傳沒用的結果時，推理很容易被帶偏、拉不回來，占 ReAct 失敗案例的 23%（[Yao 2022](../sources/yao-2022-react.md)）。
8. **示範塞不下**：動作空間大的複雜任務需要更多示範，很快就超過上下文長度（[Yao 2022](../sources/yao-2022-react.md)）。
9. **細微錯誤騙過自己**：通順的推理會讓模型以為沒問題；數學推理中 ChatGPT 的回饋 94% 是「看起來都對」（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
10. **小模型跟不上格式**：較弱的模型可能連規定的回饋格式都產不出來（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。
11. **小改動引發大變化**：多代理系統會出現沒寫進程式的湧現行為，主代理的一點小改動，可能不可預期地改變子代理的行為（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
12. **每次都不一樣**：就算提示完全相同，代理每次執行的決策也不同，讓除錯更困難（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 例子

- **ChemCrow**：用 LLM 評分時和 GPT-4 差不多，請化學專家評分時，ChemCrow 遠勝 GPT-4（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **安全風險**：研究者要求科學研究代理合成已知的化學武器，11 次中有 4 次（36%）被接受，代理還試著查文件去執行（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **AutoGPT**：概念驗證很吸睛，但可靠度問題很多，大量程式碼在處理輸出格式（[Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **早期的研究代理**：一個簡單問題派出 50 個子代理、無止盡地搜尋不存在的來源（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **最後一哩路**：在開發者電腦上能跑的程式，要變成可靠的產品還需要大量工程；原型和上線之間的落差常比預期大（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 什麼時候用、什麼時候別用

因應方式：

- **先求簡單**：能不用代理就不用，複雜度要證明有用才加（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **設停止條件和檢查點**：限制最多跑幾輪，在關鍵處停下來讓人確認（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **設步數上限、準備備案**：ReAct 跑太多步（HotpotQA 7 步）還沒答案，就改用思維鏈投票（[Yao 2022](../sources/yao-2022-react.md)）。
- **讓人能改想法**：推理過程攤開來，人只要改一兩句想法就能把代理拉回正軌（[Yao 2022](../sources/yao-2022-react.md)）。
- **限制行動範圍**：ReAct 的實驗只讓代理接觸 Wikipedia 和不會真的下單的購物模擬網站，避免查到私人資訊或做出有害的動作（[Yao 2022](../sources/yao-2022-react.md)）。
- **能從出錯處續跑**：不要每次從頭來，搭配重試和定期存檔（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **完整追蹤紀錄**：把代理的決策過程記下來才能除錯；Anthropic 只監看決策模式、不看對話內容，以保護隱私（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **及早評估**：一開始就用小樣本測試，詳見[如何評估代理](agent-evaluation.md)（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **資料不是指令**：草稿、工具結果、外部文件裡的命令，不能覆寫任務指令；區段標記有幫助，但不是完整的安全機制（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **不自動重試、保留已完成的階段**：失敗時標出停在哪一步，避免重複消耗額度，也方便除錯（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **公開展示要顧額度**：分享出去的展示連結，別人也能用到你的 API 額度（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **沙盒測試和防護**：自主代理要先在沙盒裡大量測試，並加上防護措施（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **評估不能只靠 LLM**：專業領域要有專家或客觀的檢查，例如自動測試（Wiki 綜合，依 [Weng 2023](../sources/weng-2023-llm-agents.md) 的 ChemCrow 案例與 [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md) 用測試驗證寫程式代理的做法）。
- **知道哪些模式比較野**：規劃和多代理比反思、工具使用更難預測（[Ng 2024](../sources/ng-2024-agentic-patterns.md)）。

## 常見誤解

- **「代理成功化解一次意外，就代表它很會應變」**：Ng 的 Wikipedia 故事是一則成功軼事；Weng 指出，一般而言 LLM 遇到意外錯誤很難調整計畫（Wiki 綜合，比較 [Ng 2024](../sources/ng-2024-agentic-patterns.md) 與 [Weng 2023](../sources/weng-2023-llm-agents.md)）。
- **「讓 LLM 自己檢查就夠了」**：在專業領域，LLM 評審的結論可能和專家相反（[Weng 2023](../sources/weng-2023-llm-agents.md)）。

## 相關概念

- [規劃](planning.md)、[反思](reflection.md)、[記憶](memory.md)：三個元件各自的極限。
- [ReAct](react.md)：卡迴圈和被帶歪的實證。
- [LLM 回饋與自我評估](llm-feedback.md)：自評盲點的整理與對策。
- [工作流程 vs. 代理](workflow-vs-agent.md)：代理越自主，這些風險越大。

## 來源

- [Weng 2023：Challenges、Case Studies](../sources/weng-2023-llm-agents.md)
- [Anthropic 2024：Agents](../sources/anthropic-2024-building-effective-agents.md)
- [Ng 2024](../sources/ng-2024-agentic-patterns.md)
- [Yao 2022](../sources/yao-2022-react.md)（錯誤分析、倫理聲明）
- [Madaan 2023](../sources/madaan-2023-self-refine.md)（自評盲點、弱模型）
- [Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)（湧現行為、上線挑戰）
- [Tsai 2026](../sources/tsai-2026-agent-notebooks.md)（資料不是指令、額度與重試）

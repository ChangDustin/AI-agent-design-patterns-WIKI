---
title: 如何評估代理（Agent Evaluation）
type: concept
sources: [anthropic-2025-multi-agent-research, madaan-2023-self-refine, anthropic-2024-building-effective-agents]
updated: 2026-11-12
---

# 如何評估代理（Agent Evaluation）

> 討論 06 決定新增。也是本專案簡報 pipeline「檢查節點」的設計依據。

## 一句話定義

用測試案例檢查代理有沒有達成正確的結果、過程是否合理；因為代理每次可能走出不同但都合理的路，評估的重點放在結果，而不是固定的步驟（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 生活比喻

老師改申論題：不要求每個學生的步驟都一樣，而是看結論對不對、論點有沒有根據，再拿評分標準逐項給分（Wiki 綜合）。

## 運作步驟

1. **先準備小樣本**：約 20 個代表真實使用情況的問題就能開始（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
2. **訂評分規準**：事實正確（說法和來源一致）、引用正確（引用的來源真的支持說法）、完整、來源品質、工具效率（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
3. **用 LLM 評審**：一次呼叫、一個提示，依規準打 0.0～1.0 分並給通過／不通過；這樣最一致，也最接近人類的判斷（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
4. **加入人工測試**：找出自動評估漏掉的邊角案例（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
5. **會改變狀態的代理**：看最終狀態對不對，必要時在關鍵檢查點確認，不必驗證每一步（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 例子

- **早期效果明顯**：改一句提示，成功率可能從 30% 跳到 80%，少量案例就看得出差別（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **人工測試的發現**：研究代理一直偏好 SEO 內容農場，而不選權威的學術 PDF 或個人部落格；在提示中加入來源品質的指引後改善（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **有標準答案時**：LLM 評審只要檢查答案對不對，例如是否正確列出研發預算前三大的藥廠（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **和人比對**：Self-Refine 用 GPT-4 代替人評分，和人類偏好的一致率約 68～82%（[Madaan 2023](../sources/madaan-2023-self-refine.md)）。

## 什麼時候用、什麼時候別用

- **一開始就做**：不要等到有幾百個測試案例才開始評估（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **每次改動都量**：只有在確實改善結果時才增加複雜度，所以必須量得出來（[Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)）。
- **別只靠自動評估**：人工測試能抓到幻覺、系統故障、來源偏誤這些自動評估漏掉的問題（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **別用「固定步驟」當標準**：代理可能用不同的工具、不同次數的搜尋，找到同樣的答案（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 常見誤解

- **「評估一定要很大的測試集」**：早期少量案例就看得出大的改變（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **「多找幾個評審分項打分比較準」**：Anthropic 試過，單一 LLM 呼叫、一個提示打分最一致（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **「有了 LLM 評審就不需要人」**：人工測試仍然必要（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 相關概念

- [LLM 回饋與自我評估](llm-feedback.md)：評審本身的可信度和盲點。
- [代理的限制與風險](agent-limitations.md)
- [人在迴圈中](human-in-the-loop.md)：人工測試是人把關的一種。
- [Claude Research](../entities/claude-research.md)：這些評估方法的來源案例。

## 來源

- [Anthropic 2025：Effective evaluation of agents](../sources/anthropic-2025-multi-agent-research.md)
- [Madaan 2023](../sources/madaan-2023-self-refine.md)（LLM 評審和人類的一致率）
- [Anthropic 2024](../sources/anthropic-2024-building-effective-agents.md)（衡量後才加複雜度）

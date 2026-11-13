---
title: Claude Research（多代理研究系統）
type: entity
sources: [anthropic-2025-multi-agent-research]
updated: 2026-11-12
---

# Claude Research（多代理研究系統）

## 是什麼

Anthropic 為 Claude 打造的研究功能，可以搜尋網路、Google Workspace 和各種整合工具來完成複雜的研究任務（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 架構

- **協調者—工作者**：主代理分析問題、擬定策略，同時派出多個子代理分頭搜尋；子代理像「聰明的過濾器」把結果交回，再由主代理彙整成答案（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **平行**：主代理同時派 3～5 個子代理，子代理同時用 3 個以上工具，複雜研究的時間最多縮短 90%（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 早期出包與修正

- **出包**：簡單問題派出 50 個子代理、無止盡地找不存在的來源、子代理之間過多的更新互相干擾（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **出包**：主代理只交代「研究晶片短缺」，結果一個子代理查 2021 年的車用晶片危機，另外兩個重複查 2025 年的供應鏈（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **修正**：在提示中寫明分派方式（目標、輸出格式、工具與來源、任務邊界），以及依難度分配投入的規則（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。
- **修正**：人工測試發現代理偏好 SEO 內容農場，於是在提示中加入來源品質的指引（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 成績與代價

- 在內部研究評測中比單代理 Opus 4 好 90.2%；token 用量約為一般聊天的 15 倍（[Anthropic 2025](../sources/anthropic-2025-multi-agent-research.md)）。

## 和本 Wiki 的關係

- 是[協調者—工作者](../concepts/orchestrator-workers.md)和[多代理協作](../concepts/multi-agent-collaboration.md)的真實案例，也是[如何評估代理](../concepts/agent-evaluation.md)一頁的主要來源（Wiki 綜合）。

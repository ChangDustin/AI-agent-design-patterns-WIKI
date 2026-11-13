# 原始資料（raw sources）

這一層**唯讀**：LLM 只讀不改。原文受著作權保護，完整內容不上傳 GitHub（見 `.gitignore`），這裡只登記出處；任何人都能依網址重新抓回來。

- 抓取日：2026-11-12（`curl` 取 HTML，再用 `trafilatura` 轉成同名 `.md` 方便閱讀；notebook 只取 markdown 與程式格，不含輸出）
- ingest 順序 = 表格順序：先用 Ng 的四模式搭骨架 → Anthropic 的實務分類 → Weng 的學術綜述 → 兩篇原始論文深挖 → 多代理實戰 → 課程 notebook 落地成程式

| # | source-id | 標題 | 作者／出處 | 日期 | 類型 | 為什麼選 |
|---|---|---|---|---|---|---|
| 1 | `ng-2024-agentic-patterns` | [Agentic Design Patterns Part 1](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)、[2 Reflection](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/)、[3 Tool Use](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-3-tool-use/)、[4 Planning](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-4-planning/)、[5 Multi-Agent Collaboration](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-5-multi-agent-collaboration/) | Andrew Ng／The Batch（DeepLearning.AI） | 2024-03-20～04-17 | 電子報專欄（5 篇） | 「四大設計模式」這個分類的出處，短、好懂，適合當骨架 |
| 2 | `anthropic-2024-building-effective-agents` | [Building effective AI agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic（Erik S.、Barry Zhang） | 2024-12-19 | 技術部落格 | 分清「工作流程」和「代理」，並強調先從簡單做起 |
| 3 | `weng-2023-llm-agents` | [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) | Lilian Weng | 2023-06-23 | 綜述長文 | 代理＝LLM＋規劃＋記憶＋工具，經典的元件拆解 |
| 4 | `yao-2022-react` | [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) | Yao 等（Princeton、Google） | 2022-10-06（ICLR 2023） | 論文 | 「想→做→看」迴圈，工具使用＋推理的原型 |
| 5 | `madaan-2023-self-refine` | [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) | Madaan 等（CMU 等） | 2023-03-30（arXiv 預印本） | 論文 | Ng 在反思篇推薦的論文：生成→回饋→改寫 |
| 6 | `anthropic-2025-multi-agent-research` | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Anthropic | 2025-06-13 | 技術部落格 | 多代理協作的真實產品經驗，含成本與失敗教訓 |
| 7 | `tsai-2026-agent-notebooks` | [Agent01 Reflection](https://github.com/yenlung/Generative-AI)、[Agent02 Tool Use](https://github.com/yenlung/Generative-AI)、[Agent03 Planning](https://github.com/yenlung/AI-Demo) | 蔡炎龍（政大應數）／GitHub | 2026-10-26～27 | 課程 Colab notebook | 課程同款 aisuite＋Groq 實作，把概念落地成程式 |

## 檔案

| 資料夾 | 檔案 |
|---|---|
| `ng-2024-agentic-patterns/` | `part1.html`～`part5.html`（＋同名 `.md`） |
| `anthropic-2024-building-effective-agents/` | `source.html`（＋`.md`） |
| `weng-2023-llm-agents/` | `source.html`（＋`.md`） |
| `yao-2022-react/` | `source.html`（ar5iv 全文）、`abs.html`（arXiv 摘要頁）（＋`.md`） |
| `madaan-2023-self-refine/` | `source.html`（ar5iv 全文）、`abs.html`（＋`.md`） |
| `anthropic-2025-multi-agent-research/` | `source.html`（＋`.md`） |
| `tsai-2026-agent-notebooks/` | `Agent01_Reflection_讓_AI_檢查與改進回答.ipynb`、`Agent02_Tool_Use：讓_AI_使用工具.ipynb`（yenlung/Generative-AI）、`Agent03_Planning_員瑛式思考生成器.ipynb`（yenlung/AI-Demo）（＋`.md`） |

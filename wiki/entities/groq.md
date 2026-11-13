---
title: Groq（gpt-oss-120b）
type: entity
sources: [tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# Groq（gpt-oss-120b）

## 在這個 Wiki 裡的角色

- 課程 notebook 透過 [AISuite](aisuite.md) 呼叫 Groq 服務上的 `openai/gpt-oss-120b`，一般 CPU 的 Colab 就能執行（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **金鑰與額度**：金鑰放在 Colab 密鑰或隱藏輸入，不寫進程式；每次呼叫都可能消耗額度；用 `share=True` 公開展示時，拿到連結的人也能用到你的額度（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- **推理模型的設定**：生成答案前可能先用掉推理 token；課程設定 `reasoning_effort="low"`、`max_completion_tokens=8192`，只取 `content`，不拿推理欄位當答案；回覆是空的就停止（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 在這個專案裡

- 簡報 pipeline 的 LLM 後端（開工前和作者確認的選擇）（Wiki 綜合）。

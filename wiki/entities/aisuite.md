---
title: AISuite
type: entity
sources: [tsai-2026-agent-notebooks]
updated: 2026-11-12
---

# AISuite

## 在這個 Wiki 裡的角色

- 用同一套介面呼叫多家模型的 Python 套件；課程 notebook 用它連接 [Groq](groq.md) 的 `gpt-oss-120b`，只用普通的 chat completion，不用自動的代理迴圈（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。
- 課程固定的版本是 `aisuite[groq]==0.2.0`、`groq==0.37.1`；官方專案網址是 github.com/andrewyng/aisuite（[Tsai 2026](../sources/tsai-2026-agent-notebooks.md)）。

## 在這個專案裡

- 本專案簡報 pipeline 的 LLM 節點沿用課程的寫法：AISuite＋Groq，套件版本相同（Wiki 綜合，討論 07 決定）。

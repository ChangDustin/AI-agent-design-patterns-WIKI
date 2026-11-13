"""LLM 呼叫：沿用課程 notebook（蔡炎龍 Agent01–03）的寫法。

AISuite＋Groq `openai/gpt-oss-120b`、`reasoning_effort="low"`、只取 content、錯誤訊息遮蔽金鑰。
和課程不同的一點：pipeline 是無人值守的批次工作，遇到 HTTP 429 限流會依 retry-after 等待後重試
（最多 3 次；429 代表請求沒被處理，重試不會重複消耗額度）。其他錯誤一律往上丟，由節點記錄。
"""
import json
import os
import re
import time
from pathlib import Path

import aisuite as ai

ROOT = Path(__file__).resolve().parent.parent
MODEL = "groq:openai/gpt-oss-120b"


def load_env():
    """讀專案根目錄的 .env（一行一個 KEY=VALUE），不覆蓋已經存在的環境變數。"""
    path = ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        key, sep, value = line.partition("=")
        key = key.strip()
        if sep and key and not key.startswith("#") and not os.environ.get(key):
            os.environ[key] = value.strip().strip('"').strip("'")


def safe_error(error):
    """沿著錯誤鏈列出類別、HTTP 狀態與訊息，並遮蔽金鑰（改寫自課程 notebook 的 safe_error）。"""
    lines, seen = [], set()
    key = os.environ.get("GROQ_API_KEY", "")
    while error is not None and id(error) not in seen:
        seen.add(id(error))
        detail = str(error)
        if key:
            detail = detail.replace(key, "[API key 已遮蔽]")
        detail = re.sub(r"gsk_[A-Za-z0-9_-]+", "[API key 已遮蔽]", detail)
        detail = re.sub(r"(?i)Bearer\s+\S+", "Bearer [已遮蔽]", detail)
        lines.append(f"{type(error).__name__} / HTTP {getattr(error, 'status_code', '-')}: {detail[:800]}")
        error = error.__cause__ or error.__context__
    return "\n".join(lines)


def _chain(error):
    seen = set()
    while error is not None and id(error) not in seen:
        seen.add(id(error))
        yield error
        error = error.__cause__ or error.__context__


MAX_WAIT = 90   # 429 建議等待超過這麼久（例如每日額度用完），就不空等，直接停下來留待續跑
TRANSIENT = {"APIConnectionError", "APITimeoutError", "ConnectError", "ConnectionResetError", "ReadTimeout",
             "RemoteProtocolError", "InternalServerError"}


def _retry_after(error):
    """錯誤鏈裡有 HTTP 429 時，回傳建議等待的秒數；否則回傳 None。"""
    for err in _chain(error):
        if getattr(err, "status_code", None) == 429:
            response = getattr(err, "response", None)
            header = response.headers.get("retry-after") if response is not None else None
            try:
                return float(header) if header else 20.0
            except ValueError:
                return 20.0
    return None


def _transient(error):
    """網路斷線、逾時、伺服器 5xx：短暫等待後重試通常就會好（v2 執行 20261113-001206 曾因斷線中止）。"""
    return any(type(e).__name__ in TRANSIENT or (getattr(e, "status_code", 0) or 0) >= 500 for e in _chain(error))


class FormatError(ValueError):
    """模型輸出不是合法 JSON（含 Groq JSON 模式回報的 json_validate_failed）。"""


class LLM:
    def __init__(self, run_dir, tracer):
        load_env()
        if not os.environ.get("GROQ_API_KEY", "").strip():
            raise SystemExit("找不到 GROQ_API_KEY：請把 .env.example 複製成 .env，並在 GROQ_API_KEY= 後面填入金鑰。")
        self.client = ai.Client(provider_configs={"groq": {"timeout": 120.0, "max_retries": 0}})
        self.dir = Path(run_dir) / "calls"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.tracer = tracer
        self.count = 0

    def _log(self, node, system, user, text, usage, seconds, error):
        self.count += 1
        record = {"n": self.count, "node": node, "seconds": round(seconds, 1), "error": error,
                  "usage": usage and {k: getattr(usage, k, None) for k in ("prompt_tokens", "completion_tokens", "total_tokens")},
                  "system": system, "user": user, "response": text}
        path = self.dir / f"{self.count:03d}_{node}.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        self.tracer.llm_call(node, record["usage"], error)

    def ask(self, node, system, user, max_tokens=2500, schema=None):
        """一次 chat completion，回傳文字。給 schema 時用 Groq 的 strict Structured Outputs：
        解碼時就被 JSON Schema 限制，格式錯不了（v2：把格式檢查往前移到生成的當下）。"""
        fmt = ({"type": "json_schema", "json_schema": {"name": node, "strict": True, "schema": schema}}
               if schema else {"type": "json_object"})
        for attempt in range(4):
            started = time.time()
            try:
                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                    temperature=0.3,
                    reasoning_effort="low",
                    max_completion_tokens=max_tokens,
                    response_format=fmt,
                )
            except Exception as exc:
                detail = safe_error(exc)
                self._log(node, system, user, None, None, time.time() - started, detail)
                if "json_validate_failed" in detail:
                    raise FormatError(f"{node}：Groq JSON 模式回報輸出不是合法 JSON") from None
                wait = _retry_after(exc)
                if wait is not None and wait > MAX_WAIT:
                    raise RuntimeError(f"{node}：額度用完（建議等待 {wait:.0f} 秒），停止並留待續跑\n{detail}") from None
                if wait is not None and attempt < 3:
                    self.tracer.event(node, "rate_limited", wait=wait)
                    time.sleep(wait + 1)
                    continue
                if _transient(exc) and attempt < 3:
                    self.tracer.event(node, "network_retry", attempt=attempt + 1)
                    time.sleep(5 * (attempt + 1))
                    continue
                raise RuntimeError(f"{node}：Groq 呼叫失敗\n{detail}") from None
            text = response.choices[0].message.content
            self._log(node, system, user, text, getattr(response, "usage", None), time.time() - started, None)
            if not isinstance(text, str) or not text.strip():
                raise FormatError(f"{node}：模型沒有回傳文字（content 是空的）")
            return text.strip()

    def ask_json(self, node, system, user, max_tokens=2500, schema=None):
        """要求 JSON 物件；格式錯誤時把錯誤告訴模型再試一次（記成一次格式錯誤）。"""
        note = ""
        for attempt in range(2):
            try:
                data = json.loads(self.ask(node, system, user + note, max_tokens, schema))
                if not isinstance(data, dict):
                    raise FormatError("最外層必須是 JSON 物件")
                return data
            except (FormatError, json.JSONDecodeError) as exc:
                self.tracer.event(node, "format_error", detail=str(exc)[:200])
                if attempt == 1:
                    raise FormatError(f"{node}：連續兩次輸出不是合法 JSON") from None
                note = f"\n\n【上一次的輸出無法解析成 JSON 物件（{str(exc)[:120]}），請只輸出合法的 JSON 物件。】"

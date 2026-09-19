import os
import re
import time

import litellm
from dotenv import load_dotenv

from .interface import TranslationResult
from .languages import LANGS
from .prompts import build_messages

load_dotenv()
litellm.drop_params = True


def extract_code(text: str, lang: str) -> str:
    """Pull the code block out of the LLM reply."""
    fence = re.escape(LANGS[lang]["fence"])
    blocks = re.findall(rf"```(?:{fence}|c\+\+)?[ \t]*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if blocks:
        return max(blocks, key=len).strip()
    return text.strip()


def translate(code: str, source_lang: str = "python", target_lang: str = "c",
              model: str | None = None, signature: str | None = None) -> TranslationResult:
    if target_lang not in LANGS or source_lang not in LANGS:
        raise ValueError(f"Unknown language. Choose from {list(LANGS)}")
    model = model or os.getenv("DEFAULT_MODEL", "ollama/qwen2.5-coder:7b")
    base = dict(source_lang=source_lang, target_lang=target_lang, model=model)
    start = time.time()
    try:
        resp = litellm.completion(model=model, temperature=0,
                                  messages=build_messages(code, source_lang, target_lang, signature))
    except Exception as e:
        return TranslationResult(code="", seconds=time.time() - start, error=str(e), **base)

    raw = resp.choices[0].message.content or ""
    try:
        cost = litellm.completion_cost(resp)
    except Exception:
        cost = 0.0
    usage = getattr(resp, "usage", None)
    return TranslationResult(
        code=extract_code(raw, target_lang),
        input_tokens=getattr(usage, "prompt_tokens", 0) or 0,
        output_tokens=getattr(usage, "completion_tokens", 0) or 0,
        cost_usd=cost or 0.0,
        seconds=round(time.time() - start, 2),
        raw_output=raw, **base,
    )

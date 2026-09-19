from .languages import LANGS

SYSTEM = """You are an expert {src} and {tgt} developer.
Translate the given {src} code into correct, idiomatic {tgt}.
Rules:
- Output ONE complete file inside a single ```{fence} code block. No other text.
- Keep the same function names (adapt to the target naming style if needed).
- Map types carefully and handle edge cases the same way as the original.
{rules}
"""

USER = """Translate this {src} code to {tgt}:

```{src_fence}
{code}
```"""


def build_messages(code: str, source: str, target: str,
                   signature: str | None = None) -> list[dict]:
    s, t = LANGS[source], LANGS[target]
    user = USER.format(src=s["name"], tgt=t["name"], src_fence=s["fence"], code=code)
    if signature:
        user += f"\n\nUse EXACTLY this signature:\n{signature}"
    return [
        {"role": "system", "content": SYSTEM.format(
            src=s["name"], tgt=t["name"], fence=t["fence"], rules=t.get("rules", ""))},
        {"role": "user", "content": user},
    ]

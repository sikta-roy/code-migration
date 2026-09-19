"""Shared contract between Person A (translation) and Person B (testing).
Change this file only when both agree."""
from dataclasses import dataclass, field


@dataclass
class TranslationResult:
    code: str               # clean target-language file
    source_lang: str        # "python"
    target_lang: str        # "java" | "cpp" | "c"
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    seconds: float = 0.0
    raw_output: str = ""
    error: str | None = None


@dataclass
class VerifyResult:          # Person B fills this in (Week 3+)
    compiled: bool
    static_ok: bool = False
    tests_passed: int = 0
    tests_total: int = 0
    errors: list[str] = field(default_factory=list)


# Person A: translate(code, source_lang, target_lang, model) -> TranslationResult
# Person B: verify(code, target_lang, tests) -> VerifyResult

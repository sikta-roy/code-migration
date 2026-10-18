"""Week 4: translate, check, and send failures back to the model."""
from dataclasses import dataclass, field

from .translator import translate, repair

MAX_ERROR_CHARS = 1500


@dataclass
class Attempt:
    n: int
    code: str
    ok: bool
    error: str
    seconds: float
    cost_usd: float


@dataclass
class FixResult:
    code: str
    ok: bool
    attempts: list = field(default_factory=list)

    @property
    def n_attempts(self) -> int:
        return len(self.attempts)

    @property
    def seconds(self) -> float:
        return round(sum(a.seconds for a in self.attempts), 2)

    @property
    def cost_usd(self) -> float:
        return sum(a.cost_usd for a in self.attempts)

    @property
    def fixed_on(self):
        for a in self.attempts:
            if a.ok:
                return a.n
        return None


def trim(error: str) -> str:
    if len(error) <= MAX_ERROR_CHARS:
        return error
    return error[:MAX_ERROR_CHARS] + "\n...(truncated)"


def repair_prompt(code: str, error: str, target_name: str) -> str:
    return (f"This {target_name} code does not work:\n\n"
            f"```\n{code}\n```\n\n"
            f"The compiler or test reported:\n\n"
            f"```\n{trim(error)}\n```\n\n"
            "Fix the problem. Keep the same function signatures. "
            "Output the complete corrected file in one code block, nothing else.")


def translate_with_fixes(python_code, c_test, model=None, signature=None,
                         target="c", max_attempts=3, verify=None,
                         translate_fn=None, repair_fn=None) -> FixResult:
    if verify is None:
        from .verify_c import verify_c
        verify = verify_c
    if translate_fn is None:
        translate_fn = translate
    if repair_fn is None:
        repair_fn = repair

    attempts, code = [], ""
    for n in range(1, max_attempts + 1):
        if n == 1:
            r = translate_fn(python_code, "python", target, model, signature=signature)
        else:
            r = repair_fn(code, attempts[-1].error, target, model, signature=signature)
        if r.error:
            attempts.append(Attempt(n, "", False, r.error, r.seconds, r.cost_usd))
            break
        code = r.code
        outcome = verify(code, c_test)
        attempts.append(Attempt(n, code, outcome.ok, outcome.error,
                                r.seconds, r.cost_usd))
        if outcome.ok:
            break

    return FixResult(code=code, ok=bool(attempts and attempts[-1].ok), attempts=attempts)

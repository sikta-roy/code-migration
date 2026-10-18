"""Compile + run one C translation. Used by the checkers and by the fix loop."""
import subprocess
import tempfile
from pathlib import Path

HEADERS = "#include <stdbool.h>\n#include <stddef.h>\n"
CFLAGS = ["-std=c11", "-Wall", "-Wextra", "-O0", "-fsanitize=address,undefined"]


class CheckOutcome:
    def __init__(self, compiled=False, warnings=0, passed=0, total=0, error=""):
        self.compiled = compiled
        self.warnings = warnings
        self.passed = passed
        self.total = total
        self.error = error

    @property
    def ok(self) -> bool:
        return self.compiled and self.total > 0 and self.passed == self.total


def verify_c(code: str, c_test: str, timeout: int = 60) -> CheckOutcome:
    out = CheckOutcome()
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "t.c"
        src.write_text(HEADERS + code + "\n\n" + c_test)
        exe = Path(tmp) / "t"
        c = subprocess.run(["gcc", *CFLAGS, str(src), "-o", str(exe), "-lm"],
                           capture_output=True, text=True)
        out.warnings = c.stderr.count("warning:")
        if c.returncode != 0:
            out.error = c.stderr.strip()
            return out
        out.compiled = True
        try:
            r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=timeout)
            last = (r.stdout.strip().splitlines() or ["0/0"])[-1]
            try:
                out.passed, out.total = map(int, last.split("/"))
            except ValueError:
                out.error = "test printed no passed/total line"
                return out
            if r.returncode != 0 and r.stderr:
                out.error = r.stderr.strip()
            elif out.passed < out.total:
                out.error = f"tests failed: {out.passed}/{out.total} passed"
        except subprocess.TimeoutExpired:
            out.error = f"timeout after {timeout}s (machine may be loaded)"
    return out

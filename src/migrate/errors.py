"""Week 3: put every failure into one named bucket."""
import re

RULES = [
    ("undeclared",      r"undeclared \(first use|was not declared"),
    ("implicit_decl",   r"implicit declaration of function"),
    ("redefinition",    r"redefinition of|conflicting types"),
    ("type_error",      r"incompatible|invalid conversion|makes \w+ from \w+|"
                        r"wrong type|assignment to .* from"),
    ("missing_symbol",  r"undefined reference to"),
    ("syntax_error",    r"expected .* before|error: stray|unterminated"),
    ("buffer_overflow", r"buffer-overflow|stack-overflow|heap-buffer"),
    ("use_after_free",  r"heap-use-after-free|double-free"),
    ("crash",           r"DEADLYSIGNAL|SEGV|null pointer|runtime error:"),
    ("memory_leak",     r"LeakSanitizer|detected memory leaks"),
    ("timeout",         r"^timeout$"),
    ("missing_file",    r"^missing$"),
]


def classify(error: str, compiled: bool, passed: int, total: int) -> str:
    text = error or ""
    for name, pattern in RULES:
        if re.search(pattern, text, re.I):
            return name
    if not compiled:
        return "other_compile_error"
    if total == 0:
        return "crash"
    if passed < total:
        return "wrong_output"
    return "pass"


RUNTIME_ONLY = {"buffer_overflow", "use_after_free", "crash",
                "memory_leak", "timeout", "wrong_output"}

"""Week 5: run the Python original and the C translation on the same random
inputs and compare the answers."""
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

INT, DOUBLE, STR, INT_ARR, DOUBLE_ARR, BOOL, LONG = (
    "int", "double", "str", "int[]", "double[]", "bool", "long long")


@dataclass
class Sig:
    name: str
    ret: str
    args: list
    returns_array: bool = False


def parse_signature(sig: str):
    """Return a Sig, or None if this shape is not supported."""
    sig = sig.strip().rstrip(";")
    if "typedef" in sig or "struct" in sig:
        return None
    m = re.match(r"^\s*([A-Za-z_][\w ]*?)\s*(\*?)\s*([A-Za-z_]\w*)\s*\((.*)\)\s*$", sig, re.S)
    if not m:
        return None
    ret_base, star, name, params = m.group(1).strip(), m.group(2), m.group(3), m.group(4)
    if ret_base == "void":
        return None

    parts = [p.strip() for p in params.split(",") if p.strip()]
    args, i, returns_array = [], 0, False
    while i < len(parts):
        p = parts[i]
        if "[" in p:
            return None
        if re.search(r"\bchar\s*\*", p):
            args.append(STR); i += 1
        elif re.search(r"\bint\s*\*", p) and i + 1 < len(parts) and "size_t" in parts[i + 1]:
            args.append(INT_ARR); i += 2
        elif re.search(r"\bdouble\s*\*", p) and i + 1 < len(parts) and "size_t" in parts[i + 1]:
            args.append(DOUBLE_ARR); i += 2
        elif "size_t" in p and "*" in p:
            returns_array = True; i += 1
        elif re.match(r"^(const\s+)?double\s+\w+$", p):
            args.append(DOUBLE); i += 1
        elif re.match(r"^(const\s+)?(int|long long|size_t)\s+\w+$", p):
            args.append(INT); i += 1
        elif re.match(r"^(const\s+)?bool\s+\w+$", p):
            args.append(BOOL); i += 1
        else:
            return None

    if star and "char" in ret_base:
        ret = STR
    elif star and "int" in ret_base:
        ret = INT_ARR
    elif star:
        return None
    elif ret_base in ("int", "long long", "size_t"):
        ret = LONG if ret_base == "long long" else INT
    elif ret_base == "double":
        ret = DOUBLE
    elif ret_base == "bool":
        ret = BOOL
    else:
        return None
    if ret == INT_ARR and not returns_array:
        return None
    return Sig(name=name, ret=ret, args=args, returns_array=returns_array)


_READ = {
    INT:        '    long long a{i}; if (scanf("%lld", &a{i}) != 1) return 2;',
    DOUBLE:     '    double a{i}; if (scanf("%lf", &a{i}) != 1) return 2;',
    BOOL:       '    int a{i}; if (scanf("%d", &a{i}) != 1) return 2;',
    STR:        ('    int n{i}; if (scanf("%d", &n{i}) != 1) return 2;\n'
                 '    getchar();   /* exactly one newline, so spaces survive */\n'
                 '    char *a{i} = malloc(n{i} + 1);\n'
                 '    if (n{i} > 0 && fread(a{i}, 1, n{i}, stdin) != (size_t)n{i}) return 2;\n'
                 '    a{i}[n{i}] = 0;'),
    INT_ARR:    ('    int n{i}; if (scanf("%d", &n{i}) != 1) return 2;\n'
                 '    int *a{i} = malloc((n{i} ? n{i} : 1) * sizeof(int));\n'
                 '    for (int k = 0; k < n{i}; k++) if (scanf("%d", &a{i}[k]) != 1) return 2;'),
    DOUBLE_ARR: ('    int n{i}; if (scanf("%d", &n{i}) != 1) return 2;\n'
                 '    double *a{i} = malloc((n{i} ? n{i} : 1) * sizeof(double));\n'
                 '    for (int k = 0; k < n{i}; k++) if (scanf("%lf", &a{i}[k]) != 1) return 2;'),
}

_PASS = {INT: "(int)a{i}", DOUBLE: "a{i}", BOOL: "(bool)a{i}", STR: "a{i}",
         INT_ARR: "a{i}, (size_t)n{i}", DOUBLE_ARR: "a{i}, (size_t)n{i}"}


def build_harness(sig: Sig) -> str:
    lines = ["#include <stdio.h>", "#include <stdlib.h>", "#include <string.h>", "",
             "int main(void) {"]
    for i, t in enumerate(sig.args):
        lines.append(_READ[t].format(i=i))
    call_args = ", ".join(_PASS[t].format(i=i) for i, t in enumerate(sig.args))

    if sig.ret == INT_ARR:
        lines.append("    size_t out_len = 0;")
        lines.append(f"    int *res = {sig.name}({call_args}{', ' if call_args else ''}&out_len);")
        lines.append('    printf("%zu", out_len);')
        lines.append('    for (size_t k = 0; k < out_len; k++) printf(" %d", res[k]);')
        lines.append('    printf("\\n");')
    elif sig.ret == STR:
        lines.append(f"    char *res = {sig.name}({call_args});")
        lines.append('    printf("%s\\n", res ? res : "");')
    elif sig.ret == DOUBLE:
        lines.append(f'    printf("%.12g\\n", {sig.name}({call_args}));')
    elif sig.ret == BOOL:
        lines.append(f'    printf("%d\\n", {sig.name}({call_args}) ? 1 : 0);')
    else:
        lines.append(f'    printf("%lld\\n", (long long){sig.name}({call_args}));')
    lines += ["    return 0;", "}"]
    return "\n".join(lines)


def encode_input(sig: Sig, values: list) -> str:
    out = []
    for t, v in zip(sig.args, values):
        if t == STR:
            out.append(f"{len(v)}\n{v}")
        elif t in (INT_ARR, DOUBLE_ARR):
            out.append(str(len(v)))
            out.append(" ".join(repr(x) if t == DOUBLE_ARR else str(x) for x in v))
        elif t == BOOL:
            out.append("1" if v else "0")
        else:
            out.append(repr(v) if t == DOUBLE else str(v))
    return "\n".join(out) + "\n"


def format_expected(sig: Sig, value) -> str:
    if sig.ret == INT_ARR:
        return " ".join([str(len(value))] + [str(x) for x in value])
    if sig.ret == STR:
        return str(value)
    if sig.ret == DOUBLE:
        return f"{float(value):.12g}"
    if sig.ret == BOOL:
        return "1" if value else "0"
    return str(int(value))


def same(sig: Sig, expected: str, got: str) -> bool:
    if sig.ret == DOUBLE:
        try:
            a, b = float(expected), float(got)
        except ValueError:
            return False
        return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))
    return expected.strip() == got.strip()


@dataclass
class DiffReport:
    supported: bool
    ran: int = 0
    mismatches: list = field(default_factory=list)
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.supported and not self.mismatches and not self.error


class Harness:
    """Compiled C translation that reads one input case from stdin."""

    def __init__(self, c_code: str, sig: Sig, sanitize=True):
        self.sig = sig
        self._tmp = tempfile.TemporaryDirectory()
        src = Path(self._tmp.name) / "h.c"
        src.write_text("#include <stdbool.h>\n#include <stddef.h>\n"
                       + c_code + "\n\n" + build_harness(sig))
        self.exe = Path(self._tmp.name) / "h"
        flags = ["-std=c11", "-w", "-O0"] + (["-fsanitize=address,undefined"] if sanitize else [])
        r = subprocess.run(["gcc", *flags, str(src), "-o", str(self.exe), "-lm"],
                           capture_output=True, text=True)
        self.compile_error = r.stderr.strip() if r.returncode != 0 else ""

    def run(self, payload: str, timeout=20):
        env = dict(os.environ)
        # the harness itself mallocs inputs and never frees them, so leak
        # detection here would flag our own code. check_c.py covers real leaks.
        env["ASAN_OPTIONS"] = "detect_leaks=0"
        p = subprocess.run([str(self.exe)], input=payload, capture_output=True,
                           text=True, timeout=timeout, env=env)
        if p.returncode != 0:
            return None, (p.stderr.strip()[:300] or f"exit {p.returncode}")
        return p.stdout.strip(), ""

    def close(self):
        self._tmp.cleanup()

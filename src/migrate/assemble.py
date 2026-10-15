"""Week 2: join several translated C snippets into one valid C file.

Order: includes, typedefs/structs, prototypes, then function bodies.
Duplicate function definitions are dropped (the model often re-writes a
dependency it was told to just call); the first definition wins.
"""
import re

_INCLUDE = re.compile(r"^\s*#\s*include\s*[<\"][^>\"]+[>\"]", re.M)
_FUNC_HEAD = re.compile(
    r"^((?:[A-Za-z_][\w]*\s+){1,3}\**\s*([A-Za-z_]\w*)\s*\([^;{)]*\))\s*\{", re.M)
_TYPEDEF = re.compile(r"^typedef\s+struct\s*\{[^}]*\}\s*\w+\s*;", re.M | re.S)
_KEYWORDS = ("if", "for", "while", "switch", "return", "else")


def _definitions(code: str):
    """Yield (name, head, full_text) for every top-level function definition."""
    for m in _FUNC_HEAD.finditer(code):
        head = " ".join(m.group(1).split())
        name = m.group(2)
        if head.startswith(_KEYWORDS) or name in _KEYWORDS:
            continue
        i = code.index("{", m.start())
        depth, j = 0, i
        while j < len(code):
            if code[j] == "{":
                depth += 1
            elif code[j] == "}":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        yield name, head, code[m.start():j]


def prototypes(code: str):
    return [h + ";" for _, h, _ in _definitions(code) if not h.startswith("static")]


def assemble_c(snippets):
    includes, typedefs, protos = [], [], []
    seen, bodies = set(), []

    for snip in snippets:
        for m in _INCLUDE.finditer(snip):
            inc = m.group(0).strip()
            if inc not in includes:
                includes.append(inc)
        rest = _INCLUDE.sub("", snip)

        for m in _TYPEDEF.finditer(rest):
            td = m.group(0).strip()
            if td not in typedefs:
                typedefs.append(td)
        rest = _TYPEDEF.sub("", rest)

        for name, head, text in _definitions(rest):
            if name in seen:
                continue
            seen.add(name)
            bodies.append(text.strip())
            if not head.startswith("static"):
                protos.append(head + ";")

    parts = []
    if includes:
        parts.append("\n".join(includes))
    if typedefs:
        parts.append("\n".join(typedefs))
    if protos:
        parts.append("/* prototypes */\n" + "\n".join(protos))
    parts.append("\n\n".join(bodies))
    return "\n\n".join(parts) + "\n"

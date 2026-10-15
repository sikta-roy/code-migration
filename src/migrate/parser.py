"""Week 2: split a Python file into top-level units and order them by dependency."""
from dataclasses import dataclass, field

import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY = Language(tspython.language())
_parser = Parser(PY)


@dataclass
class Unit:
    name: str
    kind: str                 # "function" or "class"
    code: str
    calls: set = field(default_factory=set)


def _text(node, src: bytes) -> str:
    return src[node.start_byte:node.end_byte].decode()


def _called_names(node, src: bytes) -> set:
    found = set()
    stack = [node]
    while stack:
        n = stack.pop()
        if n.type == "call":
            fn = n.child_by_field_name("function")
            if fn is not None:
                if fn.type == "identifier":
                    found.add(_text(fn, src))
                elif fn.type == "attribute":
                    attr = fn.child_by_field_name("attribute")
                    if attr is not None:
                        found.add(_text(attr, src))
        stack.extend(n.children)
    return found


def parse_python(code: str):
    """Return (preamble, units). Preamble holds imports and other top-level lines."""
    src = code.encode()
    tree = _parser.parse(src)
    units, preamble = [], []
    for node in tree.root_node.children:
        if node.type in ("function_definition", "class_definition"):
            name_node = node.child_by_field_name("name")
            name = _text(name_node, src) if name_node else "?"
            kind = "function" if node.type == "function_definition" else "class"
            units.append(Unit(name=name, kind=kind, code=_text(node, src),
                              calls=_called_names(node, src)))
        elif node.type not in ("comment",):
            preamble.append(_text(node, src))
    names = {u.name for u in units}
    for u in units:
        u.calls = {c for c in u.calls if c in names and c != u.name}
    return "\n".join(preamble), units


def order_units(units):
    """Dependencies first. Cycles keep their original order."""
    by_name = {u.name: u for u in units}
    done, out, visiting = set(), [], set()

    def visit(u):
        if u.name in done or u.name in visiting:
            return
        visiting.add(u.name)
        for dep in sorted(u.calls):
            if dep in by_name:
                visit(by_name[dep])
        visiting.discard(u.name)
        done.add(u.name)
        out.append(u)

    for u in units:
        visit(u)
    return out

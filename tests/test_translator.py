import sys; sys.path.insert(0, "src")
from migrate.translator import extract_code
from migrate.prompts import build_messages

def test_extract_java():
    assert extract_code("hi\n```java\nclass A {}\n```", "java") == "class A {}"

def test_extract_cpp_variant():
    assert extract_code("```c++\nint f();\n```", "cpp") == "int f();"

def test_extract_no_fence():
    assert extract_code("int f();", "c") == "int f();"

def test_prompt_has_rules():
    msgs = build_messages("def f(): pass", "python", "c")
    assert "malloc" in msgs[0]["content"] and "C11" in msgs[0]["content"]

def test_signature_in_prompt():
    msgs = build_messages("def add(a,b): return a+b", "python", "c", "int add(int a, int b);")
    assert "int add(int a, int b);" in msgs[1]["content"]


def test_parse_and_order():
    from migrate.parser import parse_python, order_units
    code = ("def b():\n    return a()\n\n"
            "def a():\n    return 1\n\n"
            "class C:\n    def go(self):\n        return b()\n")
    pre, units = parse_python(code)
    assert [u.name for u in units] == ["b", "a", "C"]
    assert units[0].calls == {"a"}
    assert [u.name for u in order_units(units)] == ["a", "b", "C"]


def test_assemble_hoists_and_declares():
    from migrate.assemble import assemble_c
    out = assemble_c(["#include <stdio.h>\nint f(int x) { return x; }",
                      "#include <stdio.h>\nint g(void) { return f(1); }"])
    assert out.count("#include <stdio.h>") == 1
    assert "int f(int x);" in out and "int g(void);" in out
    assert out.index("int g(void);") < out.index("int g(void) {")


def test_assemble_keeps_typedef_once():
    from migrate.assemble import assemble_c
    td = "typedef struct { double x, y; } Point;"
    out = assemble_c([td + "\ndouble d(Point a) { return a.x; }", td + "\nint z(void){return 0;}"])
    assert out.count("} Point;") == 1


def test_assemble_drops_duplicate_definitions():
    from migrate.assemble import assemble_c
    f = "int square(int x) { return x * x; }"
    out = assemble_c([f, f + "\nint twice(int x) { return square(x) + square(x); }"])
    assert out.count("int square(int x) {") == 1
    assert out.count("int square(int x);") == 1

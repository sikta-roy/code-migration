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


def _fake(code_out_list):
    from migrate.interface import TranslationResult
    calls = {"n": 0}

    def fn(code, src, tgt, model, signature=None, context=None):
        i = min(calls["n"], len(code_out_list) - 1)
        calls["n"] += 1
        return TranslationResult(code=code_out_list[i], source_lang=src,
                                 target_lang=tgt, model="fake", seconds=0.1)
    return fn


C_TEST = ('#include <stdio.h>\nint main(void){int p=0,t=0; t++; p+= gcd(12,18)==6; '
          'printf("%d/%d\\n",p,t); return p!=t;}')
GOOD = "#include <stdlib.h>\nint gcd(int a,int b){while(b){int t=a%b;a=b;b=t;}return abs(a);}"
WRONG = "int gcd(int a,int b){ return a; }"


def _fake_repair(code_out):
    from migrate.interface import TranslationResult

    def fn(code, error, target, model, signature=None):
        assert error, "repair must receive the error text"
        return TranslationResult(code=code_out, source_lang=target,
                                 target_lang=target, model="fake", seconds=0.1)
    return fn


def test_fixloop_repairs_on_second_attempt():
    from migrate.fixloop import translate_with_fixes
    r = translate_with_fixes("x", C_TEST, model="fake", translate_fn=_fake([WRONG]),
                             repair_fn=_fake_repair(GOOD))
    assert r.ok and r.fixed_on == 2 and r.n_attempts == 2


def test_fixloop_stops_at_max_attempts():
    from migrate.fixloop import translate_with_fixes
    r = translate_with_fixes("x", C_TEST, model="fake", translate_fn=_fake([WRONG]),
                             repair_fn=_fake_repair(WRONG))
    assert not r.ok and r.n_attempts == 3


def test_fixloop_no_retry_when_first_is_good():
    from migrate.fixloop import translate_with_fixes
    r = translate_with_fixes("x", C_TEST, model="fake", translate_fn=_fake([GOOD]),
                             repair_fn=_fake_repair(WRONG))
    assert r.ok and r.n_attempts == 1



def test_mapping_rules_are_optional():
    from migrate.prompts import build_messages
    from migrate.rules import PY_TO_C_MAPPING
    plain = build_messages("def f(): pass", "python", "c")[0]["content"]
    withr = build_messages("def f(): pass", "python", "c",
                           extra_rules=PY_TO_C_MAPPING)[0]["content"]
    assert "yield" not in plain
    assert "yield / generator" in withr
    assert len(withr) > len(plain)

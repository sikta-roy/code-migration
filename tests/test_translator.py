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

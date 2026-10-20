"""Week 8: Streamlit UI for the Python to C migration tool.

    streamlit run app.py
"""
import shutil
import sys

import streamlit as st

sys.path.insert(0, "src")
from migrate.fixloop import translate_with_fixes          # noqa: E402
from migrate.rules import PY_TO_C_MAPPING                 # noqa: E402
from migrate.translator import repair, translate          # noqa: E402
from migrate.verify_c import verify_c                     # noqa: E402

st.set_page_config(page_title="Python to C migration", layout="wide")

EXAMPLE_PY = '''def has_close_elements(numbers, threshold):
    for i, a in enumerate(numbers):
        for j, b in enumerate(numbers):
            if i != j and abs(a - b) < threshold:
                return True
    return False
'''
EXAMPLE_SIG = "bool has_close_elements(const double *numbers, size_t n, double threshold);"
EXAMPLE_TEST = '''#include <stdio.h>
int main(void){int p=0,t=0;
 double a[]={1.0,2.0,3.0}; t++; p+= has_close_elements(a,3,0.5)==false;
 double b[]={1.0,2.8,3.0}; t++; p+= has_close_elements(b,3,0.3)==true;
 printf("%d/%d\\n",p,t); return p!=t;}
'''

with st.sidebar:
    st.header("Settings")
    model = st.text_input("Model", value="ollama_chat/qwen2.5-coder:7b",
                          help="Any LiteLLM model string. Local Ollama needs the "
                               "ollama_chat/ prefix; API models need a key in .env")
    attempts = st.slider("Max repair attempts", 1, 5, 3)
    use_rules = st.checkbox("Add Python-to-C mapping rules", value=True,
                            help="Explicit mappings for exceptions, classes, "
                                 "generators, default arguments and None")
    feedback = st.radio("Error feedback", ["compile", "test"], index=0,
                        help="compile: send back compiler and sanitizer errors only. "
                             "test: also send back which test failed (the model then "
                             "sees the answer key, so report it separately)")
    st.divider()
    if shutil.which("gcc"):
        st.success("gcc found")
    else:
        st.error("gcc not found: verification will fail")
    st.caption("Verification runs gcc with -Wall -Wextra and "
               "AddressSanitizer, then executes the tests.")

st.title("LLM code migration: Python to C")
st.caption("Translate, verify, and repair. Every claim on this page comes from "
           "actually compiling and running the generated code.")

left, right = st.columns(2)

with left:
    st.subheader("Python source")
    py_code = st.text_area("Python", value=EXAMPLE_PY, height=260,
                           label_visibility="collapsed")
    sig = st.text_input("Required C signature (optional but recommended)",
                        value=EXAMPLE_SIG,
                        help="Without this the model invents its own API, which "
                             "may be correct but unusable by existing callers")
    with st.expander("C test harness (must print passed/total)"):
        c_test = st.text_area("Test", value=EXAMPLE_TEST, height=160,
                              label_visibility="collapsed")
    go = st.button("Translate and verify", type="primary", use_container_width=True)

RULES = PY_TO_C_MAPPING if use_rules else None


def tr(code, src, tgt, model_, signature=None, context=None):
    return translate(code, src, tgt, model_, signature=signature,
                     context=context, extra_rules=RULES)


def rp(code, error, target, model_, signature=None):
    return repair(code, error, target, model_, signature=signature, extra_rules=RULES)


def make_verify(test_src):
    def v(code, _=None):
        res = verify_c(code, test_src)
        if feedback == "compile" and res.compiled and not res.ok:
            sanitizer = ("AddressSanitizer" in res.error
                         or "runtime error:" in res.error
                         or "LeakSanitizer" in res.error)
            if not sanitizer:
                res.error = "the code compiles but gives wrong results"
        return res
    return v


if go:
    if not py_code.strip() or not c_test.strip():
        st.warning("Python source and a C test are both needed.")
        st.stop()
    with st.spinner(f"Translating with {model}..."):
        try:
            result = translate_with_fixes(
                py_code, c_test, model=model, signature=sig.strip() or None,
                max_attempts=attempts, verify=make_verify(c_test),
                translate_fn=tr, repair_fn=rp)
        except Exception as e:
            st.error(f"Could not run the model: {e}")
            st.stop()
    st.session_state["result"] = result

result = st.session_state.get("result")

with right:
    st.subheader("Generated C")
    if result is None:
        st.info("Run a translation to see the C output here.")
    elif not result.code:
        st.error("The model returned no code.")
        st.code((result.attempts[-1].error if result.attempts else "")[:2000])
    else:
        st.code(result.code, language="c")
        st.download_button("Download .c", result.code, file_name="translated.c")

if result is not None and result.code:
    st.divider()
    final = verify_c(result.code, c_test)
    a, b, c, d = st.columns(4)
    a.metric("Compiles", "yes" if final.compiled else "no")
    b.metric("Tests passed", f"{final.passed}/{final.total}")
    c.metric("Compiler warnings", final.warnings)
    d.metric("Attempts used", result.n_attempts)

    if result.ok:
        if result.fixed_on and result.fixed_on > 1:
            st.success(f"Passed after repair on attempt {result.fixed_on}. "
                       "The first translation was wrong and the error was fed back.")
        else:
            st.success("Passed on the first attempt.")
    else:
        st.error("Still failing after every attempt. The error is below.")

    if final.error:
        with st.expander("Verification output", expanded=not result.ok):
            st.code(final.error[:4000])

    if result.n_attempts > 1:
        st.subheader("Repair history")
        for att in result.attempts:
            label = f"Attempt {att.n} - {'passed' if att.ok else 'failed'} ({att.seconds}s)"
            with st.expander(label, expanded=False):
                if att.error:
                    st.caption("What verification reported:")
                    st.code(att.error[:1500])
                if att.code:
                    st.caption("Code produced:")
                    st.code(att.code, language="c")

    st.caption(f"Model: {model} | "
               f"total time {result.seconds}s | "
               f"mapping rules {'on' if use_rules else 'off'} | "
               f"feedback mode {feedback}")
